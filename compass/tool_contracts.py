# compass/tool_contracts.py
#
# Ticket CMP-1112-D2-04 (Gate 1): tool schemas and evidence IDs.
#
# WHAT THIS FILE IS
#   The "contract" between the language model and Compass's money code.
#   The model may only ASK for a tool by name with JSON arguments, e.g.
#       category_summary  {"period": {"start": "2026-10-01", "end": "2026-11-01"}}
#   This file decides whether that request is allowed. It never does money math
#   itself; it only checks shapes, types and limits, and defines what a result
#   must look like (integer cents + evidence IDs + what was left out + coverage).
#
# WHY IT IS ONE SELF-CONTAINED FILE
#   Dev 1 confirmed (Q2) it lives here, not inside compass/contracts.py. It only imports
#   from the repo (never the other way round), so no existing module has to change.
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/compass/tool_contracts.py  (new file, nothing existing is edited)
#   Uses:      compass/contracts.py  -> TransactionType, validate_cents (reused, not copied)
#   Used by:   compass/evidence.py   -> builds results in these shapes, writes their evidence
#              tests/python/test_tool_contracts.py, test_tool_error_cases.py, test_evidence_ids.py
#              compass/tools.py      -> the 4 tools as plain Python functions (Dev 1, Q3)
#              (later) Dev 1's model loop  -> tool_definitions() + tools.handle_tool_call()
#              (later) Dev 4's UI          -> renders the error envelope defined here
#   Sits next to: compass/questions.py, the repo's existing 5 month-only tools
#              (Request/Answer dataclasses, plain ValueError). This file does NOT replace
#              them; it adds date-range tools with result IDs, evidence and error codes.
#              Same safety idea as questions.execute(): fixed dispatch, model text never
#              becomes code, SQL or a money value.
#   Style:     the repo uses frozen dataclasses (contracts.Transaction); Pydantic is used
#              here only because it gives strict JSON parsing + JSON Schema export for free.
#
# DEV 1 DECISIONS (11/25) - this file now follows all five:
#   Q1 Pydantic v2: approved -> pydantic>=2.14,<3 added to requirements.txt
#   Q2 Location:    schemas stay here, in compass/tool_contracts.py
#   Q3 Calling:     plain Python functions (local app) -> see compass/tools.py
#   Q4 Errors:      the guide's JSON envelope {error, tool, message, details[loc,msg,input]}
#   Q5 IDs:         evidence IDs reuse the existing transaction IDs; results add result_id
#                   'res_' + 12 hex (constants below, unchanged)
#
# NEEDS: pydantic>=2.14,<3 (in requirements.txt).

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------

from __future__ import annotations
# Lets type hints mention classes defined further down the file.
# Example: a method can return "SummaryResult" before SummaryResult exists.

import hashlib
# Standard-library hashing. Used for sha256 in make_result_id().
# Example: hashlib.sha256(b"abc").hexdigest() -> 'ba7816bf8f01cfea...'

import json
# Standard-library JSON. Used to turn arguments into one canonical text before hashing.
# Example: json.dumps({"b": 1, "a": 2}, sort_keys=True) -> '{"a": 2, "b": 1}'

from dataclasses import dataclass
# Plain-Python record type, used for the small ToolSpec registry entry below.
# (The repo itself uses dataclasses for Transaction, so this matches its style.)

from datetime import date
# The calendar-date type. Pydantic turns JSON text "2026-10-01" into date(2026, 10, 1)
# and rejects impossible dates like "2026-02-30".

from typing import Annotated, Any, Literal, Union
# Annotated[int, Field(ge=1)] = "an int, plus these extra rules".
# Literal["a", "b"]           = "only exactly these values".
# Any                          = "anything" (used for raw error inputs).
# Union[A, B]                  = "A or B".

from pydantic import (
    AfterValidator,   # run our own check AFTER Pydantic's type check passes
    BaseModel,        # base class for every schema model
    ConfigDict,       # model-wide settings (strict, frozen, extra="forbid")
    Field,            # per-field rules: min/max, length, regex pattern, description
    ValidationError,  # what Pydantic raises when input breaks the rules
    model_validator,  # a check that looks at several fields at once (start vs end)
)

from compass.contracts import TransactionType, validate_cents
# Reused from the repo instead of re-implemented:
#   TransactionType - income / expense / refund / transfer / unknown
#   validate_cents  - money must be a real int (not float, not bool) inside SQLite's
#                     signed 64-bit range. validate_cents(575) -> 575;
#                     validate_cents(5.75) -> ValueError


# ---------------------------------------------------------------------------
# Constants (the knobs Dev 1 may still turn)
# ---------------------------------------------------------------------------

RESULT_ID_PREFIX = "res_"
# Every result ID starts with this, so a human (or the model) can tell it apart
# from a transaction ID at a glance.  Example: 'res_9b0d33e1aa42'

RESULT_ID_HEX_LEN = 12
# How many hex characters follow the prefix. 12 hex = 48 bits = ~281 trillion
# possible IDs, plenty for one person's local database.
# If Dev 1 wants 16, change this one number; the regex below follows automatically.

RESULT_ID_PATTERN = rf"^{RESULT_ID_PREFIX}[0-9a-f]{{{RESULT_ID_HEX_LEN}}}$"
# The regex every result_id must match. The rf-string builds it from the constants:
#   '^res_[0-9a-f]{12}$'
# ({{ and }} are literal braces inside an f-string; {RESULT_ID_HEX_LEN} is filled in.)
# Matches 'res_9b0d33e1aa42'; rejects 'res_9B0D33E1AA42' (uppercase), 'res_123' (short).

MAX_RANGE_DAYS = 366
# Longest period one tool call may cover. 366 so a full leap year still fits.
# Stops the model asking for "all of history" in one go.

MAX_LABEL_LEN = 80
# Same 80-character cap the repo puts on categories (validate_classification and the
# CHECK on transactions.predicted_category in db.py).

GET_TRANSACTIONS_MAX_LIMIT = 500
# Most rows get_transactions may return in one call (ticket spec: limit 1-500).

SUMMARY_MAX_TOP_N = 50
# Most merchant/category lines a summary may return.

# Error codes. The guide's starting three for ticket 3 (Dev 1, Q4). The guide adds data
# codes in ticket 6, evidence codes in ticket 7 and unsupported_claim in Gate 4.
# Never rename a code once it's in use - UI logic branches on it.
ERROR_INVALID_ARGS = "invalid_tool_arguments"  # tool exists, but its JSON args break the rules
ERROR_UNKNOWN_TOOL = "unknown_tool"             # the model asked for a tool that doesn't exist
ERROR_EVIDENCE_NOT_FOUND = "evidence_not_found" # a result_id has no saved evidence
ERROR_CODES = (ERROR_INVALID_ARGS, ERROR_UNKNOWN_TOOL, ERROR_EVIDENCE_NOT_FOUND)
# Tuple of every code, so tests can check "only known codes are ever produced".

ToolName = Literal["get_transactions", "merchant_summary", "category_summary", "explain_total"]
# The only four tool names. Used as a field type, so a result claiming
# tool="get_balance" is rejected.

ExclusionReason = Literal["income", "transfer", "unknown"]
# Why a row was left out of a spending total. These are exactly the
# TransactionType values money.py leaves out of spending (everything except
# expense and refund). A test checks they stay in sync with TransactionType.


# ---------------------------------------------------------------------------
# Reusable field types
# ---------------------------------------------------------------------------

Cents = Annotated[int, AfterValidator(validate_cents)]
# A money amount: strict int first (Pydantic rejects 37.0, True and "3700"),
# then the repo's validate_cents adds the SQLite 64-bit range check.
# Examples:  3700 -> OK    37.0 -> rejected    2**63 -> rejected (too big for SQLite)

Count = Annotated[int, Field(ge=0)]
# A non-negative count of rows. Example: 4 -> OK, -1 -> rejected.

Label = Annotated[str, Field(min_length=1, max_length=MAX_LABEL_LEN)]
# A category or merchant name: 1-80 characters.
# Examples: 'Coffee' -> OK, '' -> rejected, 'x' * 81 -> rejected.

TransactionId = Annotated[str, Field(min_length=1)]
# A transaction's ID as stored in the database. Example: 'T1'. Empty '' is rejected.

ResultId = Annotated[str, Field(pattern=RESULT_ID_PATTERN)]
# A result ID such as 'res_9b0d33e1aa42'. The pattern ends up in the JSON Schema
# too, so the model is told the exact format it must send to explain_total.


# ---------------------------------------------------------------------------
# Strict base model
# ---------------------------------------------------------------------------

class Strict(BaseModel):
    """Base class for every model here. Three rules, all on purpose:

    extra="forbid"  Unknown fields are an error, not silently ignored.
                    {"period": {...}, "currency": "EUR"} -> rejected, because a
                    silently ignored "currency" would make the model think it got euros.
    strict=True     No type guessing. "5" is not 5, 5.0 is not 5, true is not 1.
                    Money code must never receive a float that "looked like" an int.
    frozen=True     Once parsed, an object can't be changed.
                    args.limit = 9999 -> error. Validated means validated forever.
    """

    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    # model_config is how Pydantic v2 reads model-wide settings.
    # Every subclass inherits these three rules automatically.


# ---------------------------------------------------------------------------
# Shared building blocks
# ---------------------------------------------------------------------------

class DateRange(Strict):
    """A half-open period [start, end): start is included, end is NOT.

    Same rule as money.in_period and import_coverage. October 2026 is:
        {"start": "2026-10-01", "end": "2026-11-01"}
    so a Nov 1 transaction belongs to November only and is never counted twice.
    """

    start: date = Field(description="First day included, YYYY-MM-DD.")
    # JSON "2026-10-01" -> date(2026, 10, 1).
    # Rejected: "2026-02-30" (no such day), "10/01/2026" (wrong format),
    # 1700000000 (a number, not a date), "2026-10-01T00:00:00" (a timestamp).

    end: date = Field(description="First day NOT included (exclusive), YYYY-MM-DD.")
    # Same parsing rules as start. The description is copied into the JSON Schema,
    # so the model is told "exclusive" in plain words.

    @model_validator(mode="after")
    # mode="after" = run once both fields have been parsed into real dates,
    # so we can compare them.
    def _check_order_and_length(self) -> "DateRange":
        if self.end <= self.start:
            # end == start would be an empty period; end < start is reversed.
            # Example: {"start": "2026-11-01", "end": "2026-10-01"} -> rejected.
            raise ValueError("end must be after start (end is exclusive)")
        if (self.end - self.start).days > MAX_RANGE_DAYS:
            # Subtracting two dates gives a timedelta; .days is whole days.
            # Example: 2025-01-01 -> 2026-06-01 is 516 days -> rejected.
            raise ValueError(f"period is longer than {MAX_RANGE_DAYS} days")
        return self
        # A model_validator in "after" mode must return the model itself.


class Exclusion(Strict):
    """One transaction left out of a total, and why.

    Totals must disclose what they left out, so the UI / X-Ray panel can show
    "1 transfer ($200.00) not counted".
    Example: Exclusion(transaction_id="T5", reason="transfer")
    """

    transaction_id: TransactionId
    reason: ExclusionReason


class Coverage(Strict):
    """How much of the requested period the imported data actually covers.

    Without this, a half-loaded November would look like a cheap November.
    Example for October with data loaded Oct 1 - Nov 4:
        requested=Oct 1..Nov 1, covered_start=2026-10-01, covered_end=2026-11-05, complete=True
    Same data, asking about November:
        requested=Nov 1..Dec 1, covered_start=2026-10-01, covered_end=2026-11-05, complete=False
    """

    requested: DateRange
    # The period the tool was asked about (copied from the args).

    covered_start: date | None
    # Earliest covered day among imports that overlap the period.
    # None = no import touches this period at all.

    covered_end: date | None
    # Latest covered day (exclusive, like everywhere else). None if no data.

    complete: bool
    # True only if the data covers the WHOLE requested period.
    # Note: gaps BETWEEN two imports aren't detected yet (DRAFT simplification).


# ---------------------------------------------------------------------------
# Tool argument models (what the model is allowed to send)
# ---------------------------------------------------------------------------

class GetTransactionsArgs(Strict):
    """Arguments for get_transactions: list raw transactions in a period.

    Example JSON from the model:
        {"period": {"start": "2026-10-01", "end": "2026-11-01"},
         "category": "Coffee", "limit": 20}
    """

    period: DateRange
    # Nested object; all DateRange rules apply inside it.

    category: Label | None = Field(default=None, description="Exact category name to filter on.")
    # Optional. None (or leaving it out) = all categories. 'Coffee' = only Coffee rows.

    merchant: Label | None = Field(default=None, description="Exact clean merchant name, e.g. 'Starbucks'.")
    # Optional. Matched against the clean name from the transaction_merchants view.

    limit: Annotated[int, Field(ge=1, le=GET_TRANSACTIONS_MAX_LIMIT)] = 100
    # 1-500, default 100. Examples: 0 -> rejected, 501 -> rejected, 20.0 -> rejected (float).


class MerchantSummaryArgs(Strict):
    """Arguments for merchant_summary: spending per merchant in a period.

    Example: {"period": {"start": "2026-10-01", "end": "2026-11-01"}, "top_n": 5}
    """

    period: DateRange
    merchant: Label | None = Field(default=None, description="Only this merchant (exact clean name).")
    top_n: Annotated[int, Field(ge=1, le=SUMMARY_MAX_TOP_N)] = 10
    # How many merchant lines to return, biggest spending first. 1-50, default 10.


class CategorySummaryArgs(Strict):
    """Arguments for category_summary: spending per category in a period.

    Example: {"period": {"start": "2026-10-01", "end": "2026-11-01"}, "category": "Coffee"}
    """

    period: DateRange
    category: Label | None = Field(default=None, description="Only this category (exact name).")
    top_n: Annotated[int, Field(ge=1, le=SUMMARY_MAX_TOP_N)] = 10


class ExplainTotalArgs(Strict):
    """Arguments for explain_total: show the receipts behind an earlier result.

    Example: {"result_id": "res_9b0d33e1aa42"}
    The ID must come from an earlier tool result; a made-up but well-formed ID
    passes validation here and then fails later with evidence_not_found.
    """

    result_id: ResultId


ToolArgs = Union[GetTransactionsArgs, MerchantSummaryArgs, CategorySummaryArgs, ExplainTotalArgs]
# "Any one of the four argument models" - the type validate_call() returns on success.


# ---------------------------------------------------------------------------
# Tool result models (what Compass sends back)
# Every result carries: result_id, integer cents, evidence_ids, excluded, coverage.
# There is no float field anywhere - a test walks the JSON to prove it.
# ---------------------------------------------------------------------------

class TransactionRow(Strict):
    """One transaction as get_transactions returns it.

    Example: TransactionRow(id="T1", posted_date=date(2026,10,3), description="STARBUCKS #1234",
                            merchant="Starbucks", amount_cents=-575, type="expense", category="Coffee")
    """

    id: TransactionId
    posted_date: date
    description: str
    merchant: str
    amount_cents: Cents       # signed, bank-style: money out is negative (-575 = $5.75 spent)
    type: ExclusionReason | Literal["expense", "refund"]
    # Effective type (user correction if any, else prediction). All 5 TransactionType values.
    category: Label


class TransactionsResult(Strict):
    """Result of get_transactions."""

    result_id: ResultId
    tool: Literal["get_transactions"]
    period: DateRange
    rows: tuple[TransactionRow, ...]
    # tuple, not list: frozen models need immutable containers.
    net_cents: Cents
    # Signed sum of the returned rows, bank-style. Example: T1..T6 -> -575-625-4000+1500-20000+200000 = 176300.
    truncated: bool
    # True if more rows matched than `limit` allowed, so the model knows the list is partial.
    evidence_ids: tuple[TransactionId, ...]
    # IDs of the returned rows, in the same order.
    excluded: tuple[Exclusion, ...]
    # Always empty for a plain listing (nothing is left out by type); kept so every
    # result has the same keys.
    coverage: Coverage


class SummaryLine(Strict):
    """One line of a summary: a merchant or a category and its spending.

    Example: SummaryLine(key="Coffee", spending_cents=1200, count=2, evidence_ids=("T1", "T2"))
    """

    key: str
    spending_cents: Cents
    # POSITIVE = money spent (money.py convention: spending = -(expense + refund)).
    # Negative = net refund for that line.
    count: Count
    evidence_ids: tuple[TransactionId, ...]


class SummaryResult(Strict):
    """Result of merchant_summary or category_summary.

    Example for October (category_summary): total_spending_cents=3700,
    lines Coffee 1200 and Shopping 2500, excluded T5 (transfer) and T6 (income).
    """

    result_id: ResultId
    tool: Literal["merchant_summary", "category_summary"]
    period: DateRange
    total_spending_cents: Cents
    lines: tuple[SummaryLine, ...]
    lines_truncated: bool
    # True if top_n cut off some lines. total_spending_cents still counts ALL lines.
    evidence_ids: tuple[TransactionId, ...]
    # Every row counted in total_spending_cents.
    excluded: tuple[Exclusion, ...]
    coverage: Coverage


class ExplainResult(Strict):
    """Result of explain_total: the saved receipts behind an earlier result.

    Example for the October spending result:
        evidence_ids=("T1","T2","T3","T4"), excluded=(T5 transfer, T6 income),
        included_sum_cents=-3700  (bank-style signed sum; spending = 3700)
    """

    result_id: ResultId              # the result being explained (not a new ID)
    tool: Literal["explain_total"]
    evidence_ids: tuple[TransactionId, ...]
    excluded: tuple[Exclusion, ...]
    included_sum_cents: Cents
    # Signed sum of the included rows' amounts, recomputed from the database,
    # so a reviewer can check it against the original total.


ToolResult = Union[TransactionsResult, SummaryResult, ExplainResult]


# ---------------------------------------------------------------------------
# Result IDs
# ---------------------------------------------------------------------------

def canonical_json(value: Any) -> str:
    """One exact text for a JSON value, whatever order its keys were in.

        canonical_json({"b": 1, "a": 2}) -> '{"a":2,"b":1}'
        canonical_json({"a": 2, "b": 1}) -> '{"a":2,"b":1}'   (same text)
    sort_keys      -> key order never matters
    separators     -> no spaces, so formatting never matters
    ensure_ascii=False -> 'Café' stays 'Café' instead of 'Caf\\u00e9' (both fine, just pick one)
    """
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def make_result_id(tool: str, args: BaseModel | dict, data_version: str) -> str:
    """Deterministic ID for one tool result: same question + same data = same ID.

    tool          'category_summary'
    args          the parsed args model (or a plain dict of JSON values)
    data_version  fingerprint of the transactions (see evidence.data_version);
                  it changes when a row is added or re-classified, so a stale
                  ID never points at numbers that are no longer true.

    Example:
        make_result_id("category_summary", args_for_october, "a1b2c3d4e5f6a7b8")
        -> 'res_' + first 12 hex chars of sha256('{"args":{...},"data_version":"a1b2...","tool":"category_summary"}')
    """
    args_json = args.model_dump(mode="json") if isinstance(args, BaseModel) else args
    # model_dump(mode="json") turns dates into "2026-10-01" text and tuples into
    # lists, i.e. only plain JSON values, so json.dumps can't fail on them.
    # Defaults are included, so {"period":...} and {"period":..., "limit": 100}
    # give the SAME ID (they mean the same thing).
    payload = canonical_json({"tool": tool, "args": args_json, "data_version": data_version})
    # One canonical string holding all three inputs.
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    # sha256 -> 64 lowercase hex characters. Any change to the input changes it completely.
    return RESULT_ID_PREFIX + digest[:RESULT_ID_HEX_LEN]
    # Keep the first 12: 'res_9b0d33e1aa42'.


# ---------------------------------------------------------------------------
# Error envelope
# ---------------------------------------------------------------------------

def error_envelope(code: str, tool: str | None, message: str, details: list[dict] | None = None) -> dict:
    """Build the one error shape every tool failure uses (hand-off to Dev 4).

        {"error": "invalid_tool_arguments",
         "tool": "category_summary",
         "message": "Arguments for category_summary failed validation (1 problem).",
         "details": [{"loc": ["period"], "msg": "Value error, end must be after start (end is exclusive)",
                      "input": {"start": "2026-11-01", "end": "2026-10-01"}}]}

    error    machine-readable code (one of ERROR_CODES)
    tool     the tool name the model asked for (None if it couldn't even be read)
    message  one human sentence
    details  one entry per problem: where (loc), what (msg), what was sent (input)
    """
    if code not in ERROR_CODES:
        # Guard against typos such as "invalid_tool_args" leaking to Dev 4's UI.
        raise ValueError(f"unknown error code: {code!r}")
    return {"error": code, "tool": tool, "message": message, "details": list(details or [])}
    # list(details or []) -> always a fresh list, never None, never shared.


def details_from_validation_error(exc: ValidationError) -> list[dict]:
    """Turn Pydantic's error list into our {loc, msg, input} entries.

    Pydantic gives: {'type': 'int_type', 'loc': ('limit',), 'msg': 'Input should be a valid integer',
                     'input': 5.0, 'url': ...}
    We keep:        {'loc': ['limit'], 'msg': 'Input should be a valid integer', 'input': 5.0}
    loc becomes a list (JSON has no tuples); 'type', 'url' and 'ctx' are dropped
    because they are Pydantic internals Dev 4 shouldn't depend on.
    """
    return [
        {"loc": list(err["loc"]), "msg": err["msg"], "input": err.get("input")}
        for err in exc.errors(include_url=False)
        # include_url=False -> no link to Pydantic's docs in each error.
    ]


class ToolError(Exception):
    """An exception that carries an error envelope.

    Raised deep inside (e.g. resolve_evidence) and caught at the edge, where
    .envelope is returned to the model instead of a crash.
        try: ...
        except ToolError as e: return e.envelope
    """

    def __init__(self, envelope: dict):
        super().__init__(envelope["message"])   # str(e) shows the human message
        self.envelope = envelope


# ---------------------------------------------------------------------------
# Tool registry
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ToolSpec:
    """Everything Compass knows about one tool.

    Example: TOOLS["explain_total"].args_model is ExplainTotalArgs.
    """

    name: str
    description: str          # shown to the model so it can pick the right tool
    args_model: type[Strict]  # validates the model's JSON arguments
    result_model: type[Strict]


TOOLS: dict[str, ToolSpec] = {
    spec.name: spec
    for spec in (
        ToolSpec(
            "get_transactions",
            "List transactions in a period [start, end), optionally filtered by exact category or merchant.",
            GetTransactionsArgs, TransactionsResult),
        ToolSpec(
            "merchant_summary",
            "Spending per merchant in a period [start, end). Transfers, income and unknown are excluded and listed.",
            MerchantSummaryArgs, SummaryResult),
        ToolSpec(
            "category_summary",
            "Spending per category in a period [start, end). Transfers, income and unknown are excluded and listed.",
            CategorySummaryArgs, SummaryResult),
        ToolSpec(
            "explain_total",
            "Show the transactions included in and excluded from an earlier result, by its result_id.",
            ExplainTotalArgs, ExplainResult),
    )
}
# A dict keyed by name, built from a tuple so each name is written only once.
# TOOLS["category_summary"].description -> 'Spending per category in a period ...'


def tool_definitions() -> list[dict]:
    """JSON Schema for every tool, in the shape most local-model tool APIs expect.

    [{"name": "get_transactions",
      "description": "List transactions in a period ...",
      "parameters": {"type": "object", "additionalProperties": false,
                     "properties": {"period": {"$ref": "#/$defs/DateRange"}, ...},
                     "required": ["period"], "$defs": {...}}},
     ...]
    Tools run as local Python functions (Dev 1, Q3); this list is what gets handed to
    the local model so it knows which tools exist and what JSON each one accepts.
    """
    return [
        {"name": spec.name, "description": spec.description, "parameters": spec.args_model.model_json_schema()}
        # model_json_schema() produces standard JSON Schema from the model:
        # extra="forbid" -> "additionalProperties": false, Field(ge=1) -> "minimum": 1, etc.
        for spec in TOOLS.values()
    ]


# ---------------------------------------------------------------------------
# validate_call: the single gate every model tool call passes through
# ---------------------------------------------------------------------------

def validate_call(name: str, raw_json: str | bytes) -> ToolArgs | dict:
    """Check one tool call from the model. Returns parsed args, or an error envelope.

        validate_call("category_summary", '{"period": {"start": "2026-10-01", "end": "2026-11-01"}}')
            -> CategorySummaryArgs(period=DateRange(...), category=None, top_n=10)
        validate_call("get_balance", '{}')
            -> {"error": "unknown_tool", "tool": "get_balance", ...}
        validate_call("get_transactions", '{"period": {...}, "limit": 5.0}')
            -> {"error": "invalid_tool_arguments", "tool": "get_transactions",
                "details": [{"loc": ["limit"], "msg": "Input should be a valid integer", "input": 5.0}], ...}

    The model's text is never executed, never pasted into SQL and never becomes a
    money value - it either fits a schema exactly or is rejected.
    """
    spec = TOOLS.get(name)
    # .get returns None instead of raising KeyError for unknown names.
    if spec is None:
        return error_envelope(
            ERROR_UNKNOWN_TOOL, name,
            f"Unknown tool {name!r}. Known tools: {', '.join(TOOLS)}.")
            # ', '.join(TOOLS) joins the dict's keys:
            # 'get_transactions, merchant_summary, category_summary, explain_total'
    try:
        return spec.args_model.model_validate_json(raw_json)
        # Parses the JSON text AND checks every rule in one step.
        # Strict JSON mode still accepts "2026-10-01" for a date (JSON has no date type),
        # but rejects 5.0 / true / "5" for an int.
    except ValidationError as exc:
        details = details_from_validation_error(exc)
        problems = "problem" if len(details) == 1 else "problems"
        return error_envelope(
            ERROR_INVALID_ARGS, name,
            f"Arguments for {name} failed validation ({len(details)} {problems}).",
            details)
        # Malformed JSON like '{bad' lands here too (Pydantic reports it as
        # loc [] with msg 'Invalid JSON: ...'), so the model gets one consistent shape.


def is_error(value: Any) -> bool:
    """True if a validate_call / call_tool return value is an error envelope.

        is_error({"error": "unknown_tool", ...}) -> True
        is_error(CategorySummaryArgs(...))       -> False
    """
    return isinstance(value, dict) and "error" in value
