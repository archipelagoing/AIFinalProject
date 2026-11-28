# compass/evidence.py
#
# Ticket CMP-1112-D2-04 (Gate 1): evidence IDs - the "receipts" behind every number.
#
# WHAT THIS FILE DOES
#   1. data_version(con)        fingerprint of the transactions, part of every result_id
#   2. coverage_for(con, ...)   how much of a period the imports actually cover
#   3. save_evidence(...)       write "this result used / left out these transactions"
#                               into ticket 2's `evidence` table
#   4. resolve_evidence(...)    read them back for explain_total, or fail with
#                               evidence_not_found
#   5. run_tool / call_tool     MINIMAL reference versions of the 4 tools, so the whole
#                               path (model JSON -> validate -> compute -> evidence ->
#                               explain) can be tested now. The full finance tools are a
#                               later ticket; these only use money.py's existing rules.
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/compass/evidence.py  (new file, nothing existing is edited)
#   Uses:      compass/db.py (ticket 2)   -> the `evidence` and `import_coverage` tables and the
#                                            `transaction_merchants` view, created by connect()
#              compass/db.py (repo)       -> the `transaction_details` view (effective type/category)
#              compass/money.py (ticket 1)-> SPENDING_KINDS, Txn, spending_cents: all money rules
#              compass/contracts.py       -> validate_cents
#              compass/tool_contracts.py  -> every args/result model, make_result_id, error envelope
#   Used by:   tests/python/test_evidence_ids.py (on the synthetic DB from compass/seed_synthetic.py)
#              compass/tools.py -> wraps call_tool() as plain Python functions (Dev 1, Q3);
#              (later) Financial X-Ray UI via tools.explain_total
#   Differs from compass/analytics.py: analytics works on in-memory Transaction lists for one
#              calendar month; this file queries SQLite for any [start, end) period, but applies
#              the same rule (spending = expenses - refunds; transfers/unknown never count).
#
# EXAMPLE OF WHAT ENDS UP IN THE evidence TABLE
#   "You spent $37.00 in October" (category_summary, result res_9b0d33e1aa42):
#     owner_type    owner_id          transaction_id  role      reason
#     tool_result   res_9b0d33e1aa42  T1              included  NULL
#     tool_result   res_9b0d33e1aa42  T2              included  NULL
#     tool_result   res_9b0d33e1aa42  T3              included  NULL
#     tool_result   res_9b0d33e1aa42  T4              included  NULL
#     tool_result   res_9b0d33e1aa42  T5              excluded  transfer
#     tool_result   res_9b0d33e1aa42  T6              excluded  income

from __future__ import annotations
# Allows type hints that name classes not yet defined (and keeps hints as plain text).

import hashlib
# sha256 for data_version(). hashlib.sha256(b"x").hexdigest() -> 64 hex chars.

import re
# Regular expressions: used to check a result_id's format before writing it.

import sqlite3
# Only for the Connection / Row type hints; the connection itself comes from compass.db.connect().

from collections.abc import Iterable, Sequence
# Iterable = "anything you can loop over" (list, tuple, generator).
# Sequence = "list-like, can be indexed" (list, tuple).

from datetime import date
# DateRange holds real date objects; SQLite returns text, so we convert with date.fromisoformat.

from compass.money import SPENDING_KINDS, Txn, spending_cents
# Reused money rules from ticket 1 - no money math is re-invented here:
#   SPENDING_KINDS = ("expense", "refund")
#   Txn            = the small record money.py's functions expect
#   spending_cents = -(sum of expense + refund amounts); T1..T4 -> 3700

from compass.contracts import validate_cents
# validate_cents(176300) -> 176300; rejects floats/bools/out-of-range numbers.

from compass.tool_contracts import (
    ERROR_EVIDENCE_NOT_FOUND,
    RESULT_ID_PATTERN,
    CategorySummaryArgs,
    Coverage,
    DateRange,
    ExplainResult,
    ExplainTotalArgs,
    Exclusion,
    GetTransactionsArgs,
    MerchantSummaryArgs,
    SummaryLine,
    SummaryResult,
    ToolArgs,
    ToolError,
    ToolResult,
    TransactionRow,
    TransactionsResult,
    canonical_json,
    error_envelope,
    make_result_id,
    validate_call,
)
# Everything schema-shaped comes from tool_contracts.py; this file only fills it in.

DATA_VERSION_HEX_LEN = 16
# Length of the data fingerprint. 16 hex = 64 bits; it only needs to change when data changes.

OWNER_TYPE = "tool_result"
# The evidence table serves insights, chat messages and tool results.
# Everything this file writes is owner_type 'tool_result'.

# One query for "the transactions in a period", used by every tool.
# transaction_details (repo view)        -> effective_type / effective_category
#                                            (the user's correction if any, else the prediction)
# transaction_merchants (ticket 2 view)  -> the clean merchant name ('STARBUCKS #1234' -> 'Starbucks')
# The {filters} slot gets extra "AND ..." conditions; values are ALWAYS passed as ? parameters,
# never pasted into the SQL text, so a category like "x' OR 1=1" is just a category name.
_PERIOD_ROWS_SQL = """
SELECT d.id, d.posted_date, d.description, d.amount_cents,
       d.effective_type, d.effective_category, m.merchant
FROM transaction_details d
JOIN transaction_merchants m ON m.transaction_id = d.id
WHERE d.posted_date >= ? AND d.posted_date < ? {filters}
ORDER BY d.posted_date, d.id
"""
# posted_date >= start AND < end  = the half-open period [start, end).
# Dates are ISO text ('2026-10-03'), and ISO text sorts in date order, so text
# comparison is date comparison.


# ---------------------------------------------------------------------------
# 1. Data version
# ---------------------------------------------------------------------------

def data_version(con: sqlite3.Connection) -> str:
    """Fingerprint of everything a tool result depends on.

    Changes when a transaction is added, deleted, re-dated, re-classified by the
    user, or gets a different merchant name from an alias rule. So:
        same question + same data   -> same result_id (stable, cacheable)
        same question + edited data -> new result_id (old evidence can't be mistaken for new)

    Example: on the 7-row synthetic DB -> something like '3f9a0c...' (16 hex chars).
    """
    rows = con.execute(
        "SELECT d.id, d.posted_date, d.amount_cents, d.effective_type, d.effective_category, m.merchant "
        "FROM transaction_details d JOIN transaction_merchants m ON m.transaction_id = d.id "
        "ORDER BY d.id"
    ).fetchall()
    # ORDER BY id -> same rows always hashed in the same order.
    text = canonical_json([list(r) for r in rows])
    # sqlite3.Row -> list of plain values -> one canonical JSON string, e.g.
    # '[["T1","2026-10-03",-575,"expense","Coffee","Starbucks"],...]'
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:DATA_VERSION_HEX_LEN]


# ---------------------------------------------------------------------------
# 2. Coverage
# ---------------------------------------------------------------------------

def coverage_for(con: sqlite3.Connection, period: DateRange) -> Coverage:
    """How much of `period` the imported files cover (from ticket 2's import_coverage).

    Synthetic DB: one import covering 2026-10-01 .. 2026-11-05 (exclusive).
        October  [10-01, 11-01) -> complete=True
        November [11-01, 12-01) -> complete=False (data stops at Nov 4)
        March    [03-01, 04-01) -> covered_start=None, covered_end=None, complete=False
    """
    row = con.execute(
        "SELECT MIN(covered_start), MAX(covered_end) FROM import_coverage "
        "WHERE covered_start < ? AND covered_end > ?",
        (period.end.isoformat(), period.start.isoformat()),
    ).fetchone()
    # Two half-open ranges overlap when each starts before the other ends.
    # MIN/MAX over the overlapping imports give the outer edges of what we have.
    # With no overlapping import, both come back NULL -> None.
    lo = date.fromisoformat(row[0]) if row[0] else None
    hi = date.fromisoformat(row[1]) if row[1] else None
    # '2026-10-01' -> date(2026, 10, 1); None stays None.
    complete = lo is not None and lo <= period.start and hi >= period.end
    # Complete = the covered edges reach both ends of the requested period.
    # (DRAFT: a gap between two separate imports is not detected yet.)
    return Coverage(requested=period, covered_start=lo, covered_end=hi, complete=complete)


# ---------------------------------------------------------------------------
# 3 + 4. Save and resolve evidence
# ---------------------------------------------------------------------------

def _check_result_id(result_id: str) -> None:
    """Refuse to write evidence under a malformed ID.

        _check_result_id('res_9b0d33e1aa42') -> passes
        _check_result_id('res_XYZ')          -> ValueError
    """
    if not isinstance(result_id, str) or not re.fullmatch(RESULT_ID_PATTERN, result_id):
        raise ValueError(f"malformed result_id: {result_id!r}")


def save_evidence(
    con: sqlite3.Connection,
    result_id: str,
    included: Sequence[str],
    excluded: Iterable[Exclusion],
) -> int:
    """Write the receipts for one result. Returns how many rows were written.

        save_evidence(con, 'res_9b0d33e1aa42', ['T1','T2','T3','T4'],
                      [Exclusion(transaction_id='T5', reason='transfer'),
                       Exclusion(transaction_id='T6', reason='income')])  -> 6

    Safe to call twice for the same result_id: the old rows are replaced, not doubled.
    (Same result_id = same question on the same data, so the evidence is identical anyway.)
    The whole write is one transaction: all rows are saved, or none.
    Unknown transaction IDs fail on the table's REFERENCES rule (foreign keys are on).
    """
    _check_result_id(result_id)
    rows = [(OWNER_TYPE, result_id, tid, "included", None) for tid in included]
    # reason is NULL for included rows - nothing to explain.
    rows += [(OWNER_TYPE, result_id, ex.transaction_id, "excluded", ex.reason) for ex in excluded]
    # Excluded rows carry their reason ('transfer', 'income', 'unknown').
    with con:
        # "with con:" = commit if everything succeeds, roll back if anything raises.
        con.execute("DELETE FROM evidence WHERE owner_type = ? AND owner_id = ?", (OWNER_TYPE, result_id))
        con.executemany(
            "INSERT INTO evidence(owner_type, owner_id, transaction_id, role, reason) VALUES(?,?,?,?,?)",
            rows,
        )
        # executemany runs the INSERT once per tuple in `rows`.
    return len(rows)
    # Known DRAFT limit: a result with zero rows (an empty period) writes no evidence,
    # so explain_total on it reports evidence_not_found. Flag for Dev 1 / Dev 4.


def resolve_evidence(con: sqlite3.Connection, result_id: str) -> ExplainResult:
    """Read the receipts for a result back. Raises ToolError(evidence_not_found) if none.

        resolve_evidence(con, 'res_9b0d33e1aa42')
            -> ExplainResult(evidence_ids=('T1','T2','T3','T4'),
                             excluded=(T5 transfer, T6 income), included_sum_cents=-3700)
        resolve_evidence(con, 'res_000000000000')
            -> ToolError with envelope {"error": "evidence_not_found", ...}
    """
    rows = con.execute(
        "SELECT e.transaction_id, e.role, e.reason, t.amount_cents "
        "FROM evidence e JOIN transactions t ON t.id = e.transaction_id "
        "WHERE e.owner_type = ? AND e.owner_id = ? ORDER BY e.id",
        (OWNER_TYPE, result_id),
    ).fetchall()
    # JOIN transactions -> every evidence row must point at a real transaction,
    # and gives us its amount to recompute the sum.
    # ORDER BY e.id -> rows come back in the order they were saved.
    if not rows:
        raise ToolError(error_envelope(
            ERROR_EVIDENCE_NOT_FOUND, "explain_total",
            f"No evidence is saved for result {result_id}.",
            [{"loc": ["result_id"], "msg": "no evidence rows for this result_id", "input": result_id}],
        ))
    included = [r for r in rows if r["role"] == "included"]
    excluded = tuple(Exclusion(transaction_id=r["transaction_id"], reason=r["reason"])
                     for r in rows if r["role"] == "excluded")
    return ExplainResult(
        result_id=result_id,
        tool="explain_total",
        evidence_ids=tuple(r["transaction_id"] for r in included),
        excluded=excluded,
        included_sum_cents=validate_cents(sum(r["amount_cents"] for r in included)),
        # -575 - 625 - 4000 + 1500 = -3700 for the October spending result.
    )


# ---------------------------------------------------------------------------
# 5. Minimal reference tools
# ---------------------------------------------------------------------------

def _period_rows(con: sqlite3.Connection, period: DateRange,
                 category: str | None = None, merchant: str | None = None,
                 limit: int | None = None) -> list[sqlite3.Row]:
    """Rows in [start, end), optionally filtered by exact category / merchant.

        _period_rows(con, october)                      -> T1..T6 (T7 is Nov 4, outside)
        _period_rows(con, october, category="Coffee")   -> T1, T2
        _period_rows(con, october, merchant="Amazon")   -> T3, T4
    """
    filters, params = [], [period.start.isoformat(), period.end.isoformat()]
    if category is not None:
        filters.append("AND d.effective_category = ?")
        params.append(category)
    if merchant is not None:
        filters.append("AND m.merchant = ?")
        params.append(merchant)
    sql = _PERIOD_ROWS_SQL.format(filters=" ".join(filters))
    # Only our own fixed "AND ... = ?" strings go into the SQL text; user values go in params.
    if limit is not None:
        sql += " LIMIT ?"
        params.append(limit)
    return con.execute(sql, params).fetchall()


def _txn(row: sqlite3.Row) -> Txn:
    """Database row -> money.py's Txn, so money.py's rules can be applied.

    kind = effective type, i.e. a user's correction wins over the prediction.
    """
    return Txn(id=row["id"], posted_date=row["posted_date"], kind=row["effective_type"],
               amount_cents=row["amount_cents"])


def _get_transactions(con: sqlite3.Connection, args: GetTransactionsArgs) -> TransactionsResult:
    """List rows. Fetches limit+1 rows: if the extra one exists, the list was cut short."""
    rows = _period_rows(con, args.period, args.category, args.merchant, args.limit + 1)
    truncated = len(rows) > args.limit
    rows = rows[: args.limit]
    # Example: limit=2 on October -> fetch 3, truncated=True, keep T1, T2.
    result_id = make_result_id("get_transactions", args, data_version(con))
    ids = tuple(r["id"] for r in rows)
    save_evidence(con, result_id, ids, ())
    return TransactionsResult(
        result_id=result_id,
        tool="get_transactions",
        period=args.period,
        rows=tuple(
            TransactionRow(id=r["id"], posted_date=date.fromisoformat(r["posted_date"]),
                           description=r["description"], merchant=r["merchant"],
                           amount_cents=r["amount_cents"], type=r["effective_type"],
                           category=r["effective_category"])
            for r in rows),
        net_cents=validate_cents(sum(r["amount_cents"] for r in rows)),
        truncated=truncated,
        evidence_ids=ids,
        excluded=(),
        coverage=coverage_for(con, args.period),
    )


def _summary(con: sqlite3.Connection, args: MerchantSummaryArgs | CategorySummaryArgs,
             tool: str, group_by: str) -> SummaryResult:
    """Shared body of merchant_summary and category_summary.

    group_by is the row column to group on: 'merchant' or 'effective_category'.
    October category_summary:
        included T1..T4 -> Coffee 1200 (T1, T2), Shopping 2500 (T3, T4); total 3700
        excluded T5 transfer, T6 income
    """
    if tool == "merchant_summary":
        rows = _period_rows(con, args.period, merchant=args.merchant)
    else:
        rows = _period_rows(con, args.period, category=args.category)
    included = [r for r in rows if r["effective_type"] in SPENDING_KINDS]
    # Only expense + refund count as spending (money.py rule).
    excluded = tuple(Exclusion(transaction_id=r["id"], reason=r["effective_type"])
                     for r in rows if r["effective_type"] not in SPENDING_KINDS)
    # Everything else in the period is disclosed with its type as the reason.
    groups: dict[str, list[sqlite3.Row]] = {}
    for r in included:
        groups.setdefault(r[group_by], []).append(r)
        # setdefault: create an empty list the first time a key is seen, then append.
    lines = sorted(
        (SummaryLine(key=k, spending_cents=spending_cents([_txn(r) for r in g]), count=len(g),
                     evidence_ids=tuple(r["id"] for r in g))
         for k, g in groups.items()),
        key=lambda line: (-line.spending_cents, line.key),
    )
    # Biggest spending first; ties broken by name so the order is always the same.
    result_id = make_result_id(tool, args, data_version(con))
    evidence_ids = tuple(r["id"] for r in included)
    save_evidence(con, result_id, evidence_ids, excluded)
    return SummaryResult(
        result_id=result_id,
        tool=tool,
        period=args.period,
        total_spending_cents=spending_cents([_txn(r) for r in included]),
        lines=tuple(lines[: args.top_n]),
        lines_truncated=len(lines) > args.top_n,
        evidence_ids=evidence_ids,
        excluded=excluded,
        coverage=coverage_for(con, args.period),
    )


def run_tool(con: sqlite3.Connection, args: ToolArgs) -> ToolResult:
    """Run an already-validated tool call. Dispatch is on the args' class, never on text.

        run_tool(con, CategorySummaryArgs(...)) -> SummaryResult
        run_tool(con, ExplainTotalArgs(...))    -> ExplainResult (or ToolError)
    """
    if isinstance(args, GetTransactionsArgs):
        return _get_transactions(con, args)
    if isinstance(args, MerchantSummaryArgs):
        return _summary(con, args, "merchant_summary", "merchant")
    if isinstance(args, CategorySummaryArgs):
        return _summary(con, args, "category_summary", "effective_category")
    if isinstance(args, ExplainTotalArgs):
        return resolve_evidence(con, args.result_id)
    raise TypeError(f"not a tool args model: {type(args).__name__}")
    # Only reachable through a programming error, never through model input.


def call_tool(con: sqlite3.Connection, name: str, raw_json: str | bytes) -> ToolResult | dict:
    """The full path for one model tool call: validate -> run -> result, or an error envelope.

        call_tool(con, "category_summary", '{"period": {"start": "2026-10-01", "end": "2026-11-01"}}')
            -> SummaryResult(total_spending_cents=3700, ...)
        call_tool(con, "explain_total", '{"result_id": "res_000000000000"}')
            -> {"error": "evidence_not_found", ...}
    Public callers use compass/tools.py (typed functions + handle_tool_call), which wraps this.
    """
    args = validate_call(name, raw_json)
    if isinstance(args, dict):
        return args                 # validation failed: pass the envelope straight back
    try:
        return run_tool(con, args)
    except ToolError as exc:
        return exc.envelope         # e.g. evidence_not_found
