# tests/python/test_tools.py
#
# Ticket CMP-1112-D2-04: the four tools as plain Python functions (Dev 1, Q3) and the
# model-loop entry point handle_tool_call().
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/tests/python/test_tools.py (new file)
#   Tests:     compass/tools.py
#   Uses:      compass/db.py connect() + compass/seed_synthetic.py (ticket 2's T1-T7 fixture),
#              same per-test temporary database as test_dev2_schema.py / test_evidence_ids.py
#
# HOW TO RUN
#   python -m pytest -v tests/python/test_tools.py

import json
from datetime import date, datetime
from decimal import Decimal

import pytest

from compass.db import connect
from compass.seed_synthetic import load_fixture, seed
from compass.tool_contracts import (
    ERROR_EVIDENCE_NOT_FOUND,
    ERROR_INVALID_ARGS,
    ERROR_UNKNOWN_TOOL,
    TOOLS,
    SummaryResult,
    ToolError,
)
from compass.tools import (
    TOOL_FUNCTIONS,
    category_summary,
    explain_total,
    get_transactions,
    handle_tool_call,
    merchant_summary,
)

OCT_START, OCT_END = date(2026, 10, 1), date(2026, 11, 1)
OCT_JSON = {"start": "2026-10-01", "end": "2026-11-01"}


@pytest.fixture
def con(tmp_path):
    """Fresh database seeded with T1-T7; closed after each test."""
    c = connect(tmp_path / "compass_test.db")
    seed(c, load_fixture())
    yield c
    c.close()


# ---------------------------------------------------------------------------
# Python function path (app code)
# ---------------------------------------------------------------------------

def test_function_names_match_the_schema_registry():
    assert set(TOOL_FUNCTIONS) == set(TOOLS)


def test_category_summary_with_date_objects(con):
    r = category_summary(con, OCT_START, OCT_END)
    assert isinstance(r, SummaryResult)
    assert r.total_spending_cents == 3700                              # $37.00
    assert [(l.key, l.spending_cents) for l in r.lines] == [("Shopping", 2500), ("Coffee", 1200)]


def test_iso_text_dates_give_the_same_result_id(con):
    a = category_summary(con, OCT_START, OCT_END)
    b = category_summary(con, "2026-10-01", "2026-11-01")
    assert a.result_id == b.result_id               # date objects and ISO text mean the same thing


def test_merchant_summary_and_get_transactions(con):
    assert [l.key for l in merchant_summary(con, OCT_START, OCT_END).lines] == ["Amazon", "Starbucks"]
    coffee = get_transactions(con, OCT_START, OCT_END, category="Coffee")
    assert coffee.evidence_ids == ("T1", "T2") and coffee.net_cents == -1200


def test_evidence_ids_are_the_existing_transaction_ids(con):
    # Dev 1, Q5: reuse transaction IDs; add only the result_id.
    r = category_summary(con, OCT_START, OCT_END)
    stored = {row[0] for row in con.execute("SELECT id FROM transactions")}
    assert set(r.evidence_ids) <= stored
    assert r.result_id.startswith("res_") and len(r.result_id) == 16       # 'res_' + 12 hex


def test_explain_total_round_trip(con):
    r = category_summary(con, OCT_START, OCT_END)
    e = explain_total(con, r.result_id)
    assert e.evidence_ids == r.evidence_ids
    assert e.included_sum_cents == -3700


@pytest.mark.parametrize("call, loc", [
    (lambda c: category_summary(c, OCT_END, OCT_START), ["period"]),             # reversed
    (lambda c: get_transactions(c, OCT_START, OCT_END, limit=5.0), ["limit"]),   # float
    (lambda c: get_transactions(c, OCT_START, OCT_END, limit=True), ["limit"]),  # bool
    (lambda c: merchant_summary(c, OCT_START, OCT_END, top_n=0), ["top_n"]),     # out of range
    (lambda c: category_summary(c, datetime(2026, 10, 1, 9, 30), OCT_END), ["period", "start"]),  # timestamp
    (lambda c: explain_total(c, "res_XYZ"), ["result_id"]),                      # malformed ID
])
def test_bad_python_arguments_raise_tool_error_with_the_guide_envelope(con, call, loc):
    with pytest.raises(ToolError) as info:
        call(con)
    env = info.value.envelope
    assert env["error"] == ERROR_INVALID_ARGS
    assert set(env) == {"error", "tool", "message", "details"}       # the guide's format (Q4)
    assert env["details"][0]["loc"] == loc


def test_non_json_value_becomes_an_envelope_not_a_crash(con):
    with pytest.raises(ToolError) as info:
        get_transactions(con, OCT_START, OCT_END, limit=Decimal("5"))
    assert info.value.envelope["error"] == ERROR_INVALID_ARGS
    assert json.dumps(info.value.envelope)            # still JSON-safe for the UI


def test_unknown_result_id_raises_evidence_not_found(con):
    with pytest.raises(ToolError) as info:
        explain_total(con, "res_000000000000")
    assert info.value.envelope["error"] == ERROR_EVIDENCE_NOT_FOUND


# ---------------------------------------------------------------------------
# Model-loop path
# ---------------------------------------------------------------------------

def test_handle_tool_call_returns_plain_json_for_a_good_call(con):
    out = handle_tool_call(con, "category_summary", json.dumps({"period": OCT_JSON}))
    assert out["total_spending_cents"] == 3700
    assert out["period"] == OCT_JSON                   # dates came back as ISO text
    assert json.loads(json.dumps(out)) == out          # fully JSON-serialisable


def test_handle_tool_call_accepts_a_parsed_dict(con):
    a = handle_tool_call(con, "category_summary", {"period": OCT_JSON})
    b = handle_tool_call(con, "category_summary", json.dumps({"period": OCT_JSON}))
    assert a == b


@pytest.mark.parametrize("name, arguments, code", [
    ("merchant_sumary", "{}", ERROR_UNKNOWN_TOOL),                                  # typo'd tool
    ("category_summary", "{bad", ERROR_INVALID_ARGS),                               # broken JSON
    ("get_transactions", {"period": OCT_JSON, "limit": 5.0}, ERROR_INVALID_ARGS),   # float
    ("explain_total", {"result_id": "res_000000000000"}, ERROR_EVIDENCE_NOT_FOUND),
])
def test_handle_tool_call_never_raises_for_bad_model_input(con, name, arguments, code):
    out = handle_tool_call(con, name, arguments)
    assert out["error"] == code


def test_model_and_python_paths_agree(con):
    py = category_summary(con, OCT_START, OCT_END).model_dump(mode="json")
    model = handle_tool_call(con, "category_summary", {"period": OCT_JSON})
    assert py == model
