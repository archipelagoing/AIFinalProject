# compass/tools.py
#
# Ticket CMP-1112-D2-04 (Gate 1): the four tools as plain Python functions.
#
# WHY THIS FILE EXISTS (Dev 1's answers, 11/25)
#   Q3 "tools are called as python functions since it's a local app" -> no HTTP API.
#   The Streamlit app (and later the model loop) imports these functions and calls them.
#   Q4 "use the given json format, from the guide" -> every failure is the guide's
#   envelope {error, tool, message, details[loc, msg, input]} (built in tool_contracts.py).
#   Q5 "reuse transaction ids and add the result_id" -> evidence_ids are the existing
#   transaction IDs ('T1', ...), unchanged; each result also gets a result_id 'res_' + 12 hex.
#
# TWO WAYS IN, ONE SET OF RULES
#   1. App code (Streamlit) calls typed functions and gets a result model, or a ToolError:
#        category_summary(con, date(2026, 10, 1), date(2026, 11, 1)).total_spending_cents -> 3700
#   2. The model loop calls handle_tool_call() with the model's JSON and always gets a dict
#      back (the result as JSON values, or an error envelope) - it never raises for bad input:
#        handle_tool_call(con, "category_summary", '{"period": {...}}') -> {"result_id": ..., ...}
#   Both paths go through the SAME validate_call(), so app code can't skip a check the model
#   is held to (e.g. a float limit is rejected from both).
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/compass/tools.py (new file, nothing existing is edited)
#   Uses:      compass/tool_contracts.py -> args/result models, validate_call, error envelope
#              compass/evidence.py       -> call_tool (validate -> compute -> save evidence)
#   Used by:   app.py (Streamlit) and the Ollama model loop (compass/ollama.py) in later tickets;
#              tests/python/test_tools.py now.
#   Sits next to: compass/questions.py - same idea (fixed Python dispatch, model text never
#              becomes code/SQL/money) but for [start, end) periods with result IDs and evidence.
#              questions.py's five month-only tools are left as they are.

from __future__ import annotations
# Type hints are stored as text, so "TransactionsResult | dict" works on any Python 3.11+.

import json
# json.dumps turns the keyword arguments into the same JSON text the model would send.
# Example: {"period": {"start": "2026-10-01", ...}, "limit": 20} -> '{"period": {...}, "limit": 20}'

import sqlite3
# For the Connection type hint; the connection itself comes from compass.db.connect().

from datetime import date
# The functions take real date objects (what Streamlit's st.date_input returns),
# or ISO text like "2026-10-01". Both end up as JSON text "2026-10-01".

from typing import Any, Callable
# Any      = "any value" (for raw arguments from the model).
# Callable = "a function", for the TOOL_FUNCTIONS table.

from compass.evidence import call_tool
# call_tool(con, name, raw_json) -> result model, or an error envelope dict.

from compass.tool_contracts import (
    ERROR_INVALID_ARGS,
    ExplainResult,
    SummaryResult,
    ToolError,
    TransactionsResult,
    error_envelope,
    is_error,
)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _json_default(value: Any) -> str:
    """Tell json.dumps how to write a date: as ISO text.

        json.dumps({"d": date(2026, 10, 1)}, default=_json_default) -> '{"d": "2026-10-01"}'

    Anything else json can't write (Decimal, a custom object) raises TypeError, which
    _call() turns into an invalid_tool_arguments envelope instead of a crash.
    Note: a datetime IS a date in Python, so datetime(2026,10,1,9,30) becomes
    "2026-10-01T09:30:00" here - and the strict DateRange then rejects it, on purpose.
    """
    if isinstance(value, date):
        return value.isoformat()
    raise TypeError(f"{type(value).__name__} is not a JSON value")


def _call(con: sqlite3.Connection, name: str, payload: dict) -> Any:
    """Shared body of the four typed functions: dict -> JSON -> call_tool -> result or ToolError.

        _call(con, "explain_total", {"result_id": "res_0123456789ab"})
            -> ExplainResult(...)          if evidence exists
            -> raises ToolError(envelope)  if not (envelope["error"] == "evidence_not_found")
    """
    try:
        raw = json.dumps(payload, default=_json_default)
        # Going through JSON text (not passing the dict straight to Pydantic) makes the app
        # path byte-for-byte the same as the model path: same parser, same strict rules.
    except TypeError as exc:
        # e.g. limit=Decimal("5"): not a JSON value at all.
        raise ToolError(error_envelope(
            ERROR_INVALID_ARGS, name,
            "Arguments must be plain values: text, whole numbers or dates.",
            [{"loc": [], "msg": str(exc), "input": None}],
            # input is None: the bad value can't be put in JSON, which is the whole problem.
        )) from None
    result = call_tool(con, name, raw)
    if is_error(result):
        raise ToolError(result)
        # Python callers get an exception (normal Python style); e.envelope holds the
        # guide's JSON error for the UI to show.
    return result


# ---------------------------------------------------------------------------
# The four tools (public API for app code)
# ---------------------------------------------------------------------------

def get_transactions(con: sqlite3.Connection, start: date | str, end: date | str, *,
                     category: str | None = None, merchant: str | None = None,
                     limit: int = 100) -> TransactionsResult:
    """Transactions in [start, end), optionally filtered by exact category or merchant.

    The * makes everything after it keyword-only, so calls read clearly:
        get_transactions(con, date(2026, 10, 1), date(2026, 11, 1), category="Coffee")
            -> TransactionsResult(evidence_ids=('T1', 'T2'), net_cents=-1200, ...)
        get_transactions(con, "2026-10-01", "2026-11-01", limit=0)
            -> ToolError: invalid_tool_arguments, loc ["limit"]
    """
    return _call(con, "get_transactions", {
        "period": {"start": start, "end": end},
        "category": category, "merchant": merchant, "limit": limit,
    })


def merchant_summary(con: sqlite3.Connection, start: date | str, end: date | str, *,
                     merchant: str | None = None, top_n: int = 10) -> SummaryResult:
    """Spending per clean merchant name in [start, end).

        merchant_summary(con, date(2026, 10, 1), date(2026, 11, 1))
            -> lines Amazon 2500, Starbucks 1200; total_spending_cents 3700;
               excluded T5 (transfer), T6 (income)
    """
    return _call(con, "merchant_summary", {
        "period": {"start": start, "end": end}, "merchant": merchant, "top_n": top_n,
    })


def category_summary(con: sqlite3.Connection, start: date | str, end: date | str, *,
                     category: str | None = None, top_n: int = 10) -> SummaryResult:
    """Spending per category in [start, end).

        category_summary(con, date(2026, 10, 1), date(2026, 11, 1))
            -> lines Shopping 2500, Coffee 1200; total_spending_cents 3700
        category_summary(con, date(2026, 11, 1), date(2026, 10, 1))
            -> ToolError: invalid_tool_arguments, "end must be after start (end is exclusive)"
    """
    return _call(con, "category_summary", {
        "period": {"start": start, "end": end}, "category": category, "top_n": top_n,
    })


def explain_total(con: sqlite3.Connection, result_id: str) -> ExplainResult:
    """The receipts behind an earlier result (for the Financial X-Ray panel).

        r = category_summary(con, date(2026, 10, 1), date(2026, 11, 1))
        explain_total(con, r.result_id)
            -> ExplainResult(evidence_ids=('T1','T2','T3','T4'), excluded=(T5, T6),
                             included_sum_cents=-3700)
        explain_total(con, "res_000000000000") -> ToolError: evidence_not_found
    """
    return _call(con, "explain_total", {"result_id": result_id})


TOOL_FUNCTIONS: dict[str, Callable[..., Any]] = {
    "get_transactions": get_transactions,
    "merchant_summary": merchant_summary,
    "category_summary": category_summary,
    "explain_total": explain_total,
}
# Name -> function. A test checks these names match tool_contracts.TOOLS exactly,
# so a tool can't exist in the schema list but not here (or the other way round).


# ---------------------------------------------------------------------------
# Entry point for the model loop
# ---------------------------------------------------------------------------

def handle_tool_call(con: sqlite3.Connection, name: str, arguments: str | bytes | dict) -> dict:
    """Run one tool call proposed by the model. ALWAYS returns a JSON-ready dict, never raises
    for bad model input - the dict is either the result or the guide's error envelope.

        handle_tool_call(con, "category_summary",
                         '{"period": {"start": "2026-10-01", "end": "2026-11-01"}}')
            -> {"result_id": "res_...", "tool": "category_summary", "total_spending_cents": 3700, ...}
        handle_tool_call(con, "merchant_sumary", "{}")
            -> {"error": "unknown_tool", "tool": "merchant_sumary", "message": "...", "details": []}

    arguments may be JSON text (most model runtimes) or an already-parsed dict (some
    runtimes parse it for you). A dict is turned back into JSON text so it is checked by
    exactly the same strict JSON parser.
    """
    raw = json.dumps(arguments) if isinstance(arguments, dict) else arguments
    # A dict parsed from model JSON only holds JSON values, so json.dumps can't fail here.
    result = call_tool(con, name, raw)
    if is_error(result):
        return result
    return result.model_dump(mode="json")
    # mode="json": dates -> "2026-10-01", tuples -> lists. Ready to json.dumps and send back
    # to the model, or render in the UI. Cents stay ints.
