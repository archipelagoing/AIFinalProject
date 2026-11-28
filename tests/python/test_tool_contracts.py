# tests/python/test_tool_contracts.py
#
# Ticket CMP-1112-D2-04: tests for compass/tool_contracts.py - the schemas alone, no database.
# Acceptance criterion covered here: "invalid tool args are rejected".
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/tests/python/test_tool_contracts.py (new file)
#   Tests:     compass/tool_contracts.py
#   Uses:      compass/contracts.py (TransactionType, to check exclusion reasons stay in sync)
#   Runs with: the repo's pytest setup in pyproject.toml (testpaths = tests/python,
#              pythonpath = ".", so "import compass..." works from the repo root)
#
# HOW TO RUN
#   python -m pytest -v tests/python/test_tool_contracts.py
#
# READING THE TESTS
#   call("get_transactions", {...}) sends the dict as JSON text, exactly like the model would.
#   On failure validate_call returns an error envelope (a dict) instead of raising, so most
#   tests assert on that dict.

import json
# json.dumps turns a Python dict into the JSON text the model would send.

from datetime import date
# To compare parsed dates: DateRange(...).start == date(2026, 10, 1).

import pytest
# Test runner. @pytest.mark.parametrize runs one test once per listed input.

from pydantic import ValidationError
# What Pydantic raises when you construct a model directly with bad data
# (validate_call converts it to an envelope, but direct construction raises).

from compass.contracts import TransactionType
from compass.tool_contracts import (
    ERROR_CODES,
    ERROR_INVALID_ARGS,
    ERROR_UNKNOWN_TOOL,
    GET_TRANSACTIONS_MAX_LIMIT,
    MAX_RANGE_DAYS,
    RESULT_ID_PATTERN,
    TOOLS,
    CategorySummaryArgs,
    DateRange,
    ExclusionReason,
    ExplainTotalArgs,
    GetTransactionsArgs,
    MerchantSummaryArgs,
    SummaryLine,
    error_envelope,
    is_error,
    make_result_id,
    tool_definitions,
    validate_call,
)

OCT = {"start": "2026-10-01", "end": "2026-11-01"}
# October 2026 as a half-open period: Oct 1 included, Nov 1 not.

VALID_CALLS = {
    "get_transactions": {"period": OCT},
    "merchant_summary": {"period": OCT},
    "category_summary": {"period": OCT},
    "explain_total": {"result_id": "res_0123456789ab"},
}
# The smallest valid call for each tool. Tests add one bad thing to these,
# so each failure has exactly one cause.

EXPECTED_ARGS_CLASS = {
    "get_transactions": GetTransactionsArgs,
    "merchant_summary": MerchantSummaryArgs,
    "category_summary": CategorySummaryArgs,
    "explain_total": ExplainTotalArgs,
}


def call(name, payload):
    """Send a dict to validate_call as JSON text.

    call("explain_total", {"result_id": "res_0123456789ab"})
      == validate_call("explain_total", '{"result_id": "res_0123456789ab"}')
    """
    return validate_call(name, json.dumps(payload))


def locs(envelope):
    """Just the 'loc' of each problem, e.g. [['limit']] - the part tests usually care about."""
    return [d["loc"] for d in envelope["details"]]


# ---------------------------------------------------------------------------
# DateRange
# ---------------------------------------------------------------------------

def test_october_range_parses_to_real_dates():
    r = DateRange.model_validate_json(json.dumps(OCT))
    assert (r.start, r.end) == (date(2026, 10, 1), date(2026, 11, 1))
    # The JSON text "2026-10-01" became a real date object.


@pytest.mark.parametrize("start, end, why", [
    ("2026-11-01", "2026-10-01", "reversed"),
    ("2026-10-01", "2026-10-01", "empty: end is exclusive, so start == end covers no days"),
    ("2025-01-01", "2026-06-01", "516 days, over the 366-day cap"),
    ("2026-02-30", "2026-03-01", "no such calendar day"),
    ("10/01/2026", "2026-11-01", "not ISO YYYY-MM-DD"),
    ("2026-10-01T00:00:00", "2026-11-01", "a timestamp, not a date"),
])
def test_bad_ranges_are_rejected(start, end, why):
    env = call("category_summary", {"period": {"start": start, "end": end}})
    assert env["error"] == ERROR_INVALID_ARGS, why
    assert locs(env)[0][0] == "period", why
    # Every problem is reported under "period" (or a field inside it).


def test_range_cap_is_inclusive_of_a_leap_year():
    leap_year = {"start": "2024-01-01", "end": "2025-01-01"}       # 366 days - allowed
    one_more = {"start": "2024-01-01", "end": "2025-01-02"}        # 367 days - rejected
    assert not is_error(call("category_summary", {"period": leap_year}))
    assert is_error(call("category_summary", {"period": one_more}))
    assert MAX_RANGE_DAYS == 366


# ---------------------------------------------------------------------------
# Good calls parse into the right class
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name", list(VALID_CALLS))
def test_minimal_valid_call_parses(name):
    args = call(name, VALID_CALLS[name])
    assert isinstance(args, EXPECTED_ARGS_CLASS[name])
    # Not a dict envelope, but the exact args model for that tool.


def test_defaults_are_filled_in():
    args = call("get_transactions", {"period": OCT})
    assert (args.category, args.merchant, args.limit) == (None, None, 100)


# ---------------------------------------------------------------------------
# extra="forbid": unknown fields are errors, at every level
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name", list(VALID_CALLS))
def test_extra_field_rejected_on_every_tool(name):
    env = call(name, {**VALID_CALLS[name], "currency": "EUR"})
    # {**a, "k": v} = copy of a with one extra key.
    assert env["error"] == ERROR_INVALID_ARGS
    assert locs(env) == [["currency"]]


def test_extra_field_inside_period_rejected():
    env = call("category_summary", {"period": {**OCT, "timezone": "UTC"}})
    assert locs(env) == [["period", "timezone"]]
    # loc is a path: the field "timezone" inside "period".


# ---------------------------------------------------------------------------
# strict=True: no type guessing
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad", [5.0, True, "5", None])
def test_limit_must_be_a_real_int(bad):
    # 5.0 (float), True (bool - a subclass of int in Python!), "5" (text), null: all rejected.
    env = call("get_transactions", {"period": OCT, "limit": bad})
    assert env["error"] == ERROR_INVALID_ARGS
    assert locs(env) == [["limit"]]


@pytest.mark.parametrize("limit, ok", [(0, False), (1, True), (500, True), (501, False)])
def test_limit_bounds(limit, ok):
    # Boundaries checked on both sides: the edges 1 and 500 are allowed, one past them is not.
    assert GET_TRANSACTIONS_MAX_LIMIT == 500
    assert is_error(call("get_transactions", {"period": OCT, "limit": limit})) is not ok


@pytest.mark.parametrize("top_n, ok", [(0, False), (1, True), (50, True), (51, False)])
def test_top_n_bounds(top_n, ok):
    assert is_error(call("merchant_summary", {"period": OCT, "top_n": top_n})) is not ok


@pytest.mark.parametrize("category", ["", "x" * 81, 7])
def test_category_must_be_1_to_80_chars_of_text(category):
    env = call("category_summary", {"period": OCT, "category": category})
    assert locs(env) == [["category"]]


def test_money_fields_reject_floats_even_when_built_in_python():
    # Results are built by our own code, not the model - they're still strict.
    with pytest.raises(ValidationError):
        SummaryLine(key="Coffee", spending_cents=12.0, count=2, evidence_ids=("T1", "T2"))


# ---------------------------------------------------------------------------
# frozen=True: validated objects can't be changed afterwards
# ---------------------------------------------------------------------------

def test_parsed_args_are_frozen():
    args = call("get_transactions", {"period": OCT})
    with pytest.raises(ValidationError):
        args.limit = 9999            # Pydantic raises ValidationError for frozen fields
    with pytest.raises(ValidationError):
        args.period.end = date(2030, 1, 1)   # nested models are frozen too


# ---------------------------------------------------------------------------
# validate_call edge cases
# ---------------------------------------------------------------------------

def test_unknown_tool():
    env = validate_call("get_balance", "{}")
    assert env["error"] == ERROR_UNKNOWN_TOOL
    assert env["tool"] == "get_balance"
    assert env["details"] == []
    assert "category_summary" in env["message"]     # the message lists the real tools


@pytest.mark.parametrize("raw", ["{bad", "", "[]", '"text"', "null"])
def test_malformed_or_non_object_json(raw):
    # Broken JSON, empty text, an array, a string, null: none is an arguments object.
    env = validate_call("category_summary", raw)
    assert env["error"] == ERROR_INVALID_ARGS


def test_bytes_input_is_accepted():
    # Some model runtimes hand over bytes, not str.
    assert isinstance(validate_call("explain_total", b'{"result_id": "res_0123456789ab"}'), ExplainTotalArgs)


def test_is_error():
    assert is_error({"error": "unknown_tool"})
    assert not is_error(call("explain_total", VALID_CALLS["explain_total"]))


# ---------------------------------------------------------------------------
# Error envelope shape (the Dev 4 hand-off contract)
# ---------------------------------------------------------------------------

def test_envelope_has_exactly_four_keys_and_json_serialises():
    env = call("get_transactions", {"period": OCT, "limit": 5.0})
    assert set(env) == {"error", "tool", "message", "details"}
    assert set(env["details"][0]) == {"loc", "msg", "input"}
    assert json.loads(json.dumps(env)) == env
    # Round-trips through JSON unchanged = safe to send to the UI.


def test_envelope_rejects_unknown_codes():
    assert error_envelope(ERROR_UNKNOWN_TOOL, "x", "m")["details"] == []
    with pytest.raises(ValueError):
        error_envelope("invalid_tool_args", "x", "m")      # typo of a real code


# ---------------------------------------------------------------------------
# result_id format and determinism
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("rid", [
    "res_0123456789AB",      # uppercase hex
    "res_0123456789a",       # 11 hex
    "res_0123456789abc",     # 13 hex
    "rid_0123456789ab",      # wrong prefix
    "0123456789ab",          # no prefix
    " res_0123456789ab",     # leading space
])
def test_explain_total_rejects_malformed_result_ids(rid):
    env = call("explain_total", {"result_id": rid})
    assert locs(env) == [["result_id"]]


def test_make_result_id_format():
    args = call("category_summary", {"period": OCT})
    import re
    assert re.fullmatch(RESULT_ID_PATTERN, make_result_id("category_summary", args, "v1"))


def test_make_result_id_ignores_key_order_and_explicit_defaults():
    a = validate_call("category_summary", '{"period": {"start": "2026-10-01", "end": "2026-11-01"}}')
    b = validate_call("category_summary", '{"top_n": 10, "period": {"end": "2026-11-01", "start": "2026-10-01"}}')
    # Different key order, and b spells out the default top_n=10: same meaning -> same ID.
    assert make_result_id("category_summary", a, "v1") == make_result_id("category_summary", b, "v1")


def test_make_result_id_changes_with_any_input():
    args = call("category_summary", {"period": OCT})
    other = call("category_summary", {"period": OCT, "category": "Coffee"})
    base = make_result_id("category_summary", args, "v1")
    assert make_result_id("category_summary", other, "v1") != base      # different args
    assert make_result_id("category_summary", args, "v2") != base       # different data
    assert make_result_id("merchant_summary", args, "v1") != base       # different tool


# ---------------------------------------------------------------------------
# Registry and JSON Schema export
# ---------------------------------------------------------------------------

def test_registry_has_exactly_the_four_tools():
    assert set(TOOLS) == set(VALID_CALLS)
    for name, spec in TOOLS.items():
        assert spec.args_model is EXPECTED_ARGS_CLASS[name]


def _walk(node):
    """Yield every dict inside a JSON Schema (including nested $defs)."""
    if isinstance(node, dict):
        yield node
        for v in node.values():
            yield from _walk(v)
    elif isinstance(node, list):
        for v in node:
            yield from _walk(v)


def test_tool_definitions_forbid_extra_fields_everywhere():
    defs = tool_definitions()
    assert [d["name"] for d in defs] == list(TOOLS)
    for d in defs:
        objects = [n for n in _walk(d["parameters"]) if n.get("type") == "object"]
        assert objects and all(n.get("additionalProperties") is False for n in objects)
        # Every object - top level AND the nested DateRange - says "no extra keys".


def test_tool_definitions_are_valid_json_schema_and_agree_with_pydantic():
    jsonschema = pytest.importorskip("jsonschema")
    # jsonschema is already in the repo's requirements.txt; skip cleanly if not installed.
    for d in tool_definitions():
        jsonschema.Draft202012Validator.check_schema(d["parameters"])
        validator = jsonschema.Draft202012Validator(d["parameters"])
        assert validator.is_valid(VALID_CALLS[d["name"]])
        assert not validator.is_valid({**VALID_CALLS[d["name"]], "currency": "EUR"})


def test_no_result_schema_contains_a_number_type():
    # JSON Schema "number" = float. Money and counts must be "integer" only.
    for spec in TOOLS.values():
        types = [n.get("type") for n in _walk(spec.result_model.model_json_schema())]
        assert "number" not in types, spec.result_model.__name__


def test_exclusion_reasons_are_exactly_the_non_spending_types():
    # If someone adds a TransactionType, this fails until ExclusionReason is updated too.
    non_spending = {t.value for t in TransactionType} - {"expense", "refund"}
    assert set(ExclusionReason.__args__) == non_spending


def test_every_error_code_is_snake_case_text():
    assert all(code.islower() and " " not in code for code in ERROR_CODES)
