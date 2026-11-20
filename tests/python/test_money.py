# tests/python/test_money.py
#
# Golden tests for compass/money.py (CMP-1112-D2-02).
# Each case lives in fixtures/golden_money.json so reviewers (Dev 1) can check
# expected values without reading code. This file only RUNS the cases; it must
# not contain money logic of its own.

import builtins
import json
from pathlib import Path

import pytest

from compass.money import (
    Txn,
    average_cents,
    excluded_from_spending,
    format_cents,
    in_period,
    net_cash_flow_cents,
    parse_amount,
    pct_change,
    spending_by_currency,
    spending_cents,
    spending_label,
)

GOLDEN_PATH = Path(__file__).parent / "fixtures" / "golden_money.json"
GOLDEN = json.loads(GOLDEN_PATH.read_text())
CASES = GOLDEN["cases"]


# ---------- helpers: turn JSON input into Txn objects ----------

def _txns_for(inp: dict) -> list[Txn]:
    """Build the transaction list a case asks for.

    - "txns": inline transactions written in the case itself
    - "fixture": a named shared fixture, optionally narrowed by
      "txn_ids" (pick specific rows) and/or "period" ([start, end))
    """
    if "txns" in inp:
        rows = inp["txns"]
    else:
        rows = GOLDEN["fixtures"][inp["fixture"]]
        if "txn_ids" in inp:
            wanted = set(inp["txn_ids"])
            rows = [r for r in rows if r["id"] in wanted]
    txns = [Txn(**r) for r in rows]
    if "period" in inp:
        start, end = inp["period"]
        txns = [t for t in txns if in_period(t.posted_date, start, end)]
    return txns


# ---------- the golden cases ----------

@pytest.mark.parametrize("case", CASES, ids=[f"{c['id']:02d}-{c['name']}" for c in CASES])
def test_golden_case(case):
    op, inp = case["op"], case["input"]

    # Cases that must FAIL: check the right error type is raised.
    if "expected_error" in case:
        error_type = getattr(builtins, case["expected_error"])
        with pytest.raises(error_type):
            parse_amount(inp["text"])
        return

    if op == "parse_amount":
        assert parse_amount(inp["text"]) == case["expected"]

    elif op == "parse_sum":
        assert sum(parse_amount(t) for t in inp["texts"]) == case["expected"]

    elif op == "spending":
        txns = _txns_for(inp)
        total = spending_cents(txns)
        assert total == case["expected"]
        if "expected_label" in case:
            assert spending_label(total) == case["expected_label"]
        if "expected_excluded" in case:
            assert excluded_from_spending(txns) == case["expected_excluded"]

    elif op == "net_cash_flow":
        assert net_cash_flow_cents(_txns_for(inp)) == case["expected"]

    elif op == "period_filter":
        assert [t.id for t in _txns_for(inp)] == case["expected"]

    elif op == "spending_by_currency":
        totals = spending_by_currency(_txns_for(inp))
        assert totals == case["expected"]
        assert (len(totals) > 1) == case["expected_mixed_currency"]

    elif op == "empty_and_zero":
        avg, pct = inp["average"], inp["pct_change"]
        assert average_cents(avg["total"], avg["n"]) == case["expected"]["average"]
        assert pct_change(pct["old"], pct["new"]) == case["expected"]["pct_change"]

    else:
        pytest.fail(f"unknown op {op!r} in case {case['id']}")


# ---------- guards on the golden file itself ----------

def test_golden_file_has_ten_unique_cases():
    ids = [c["id"] for c in CASES]
    assert len(ids) == 10
    assert len(set(ids)) == len(ids), "case ids must be unique"


def test_golden_amounts_are_integers():
    # A float like -5.75 sneaking into the fixtures would defeat the point.
    rows = [r for fx in GOLDEN["fixtures"].values() for r in fx]
    rows += [r for c in CASES for r in c["input"].get("txns", [])]
    for r in rows:
        assert type(r["amount_cents"]) is int, f"{r['id']} amount is not an int"


# ---------- extra edge checks (cheap, and they catch regressions) ----------

@pytest.mark.parametrize("text, expected", [
    ("$1,234.56", 123456),
    ("  -5.75  ", -575),
    ("0", 0),
    ("5", 500),
])
def test_parse_amount_formats(text, expected):
    assert parse_amount(text) == expected


@pytest.mark.parametrize("bad", ["abc", "", "NaN", "Infinity", "5.750"])
def test_parse_amount_rejects(bad):
    with pytest.raises(ValueError):
        parse_amount(bad)


def test_parse_amount_rejects_float():
    with pytest.raises(TypeError):
        parse_amount(5.75)


@pytest.mark.parametrize("cents, text", [
    (-575, "-$5.75"),
    (200000, "$2,000.00"),
    (5, "$0.05"),
    (0, "$0.00"),
])
def test_format_cents(cents, text):
    assert format_cents(cents) == text


def test_average_rounds_half_up_not_bankers():
    # Python's round(500.5) == 500; money rule says 501.
    assert average_cents(1001, 2) == 501
    assert average_cents(1000, 3) == 333


def test_pct_change_negative_baseline_keeps_direction():
    # From a -1000 net refund month to +500 spending is an INCREASE.
    assert pct_change(-1000, 500) > 0