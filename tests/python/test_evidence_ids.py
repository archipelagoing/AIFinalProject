# tests/python/test_evidence_ids.py
#
# Ticket CMP-1112-D2-04: result IDs and evidence on a real (temporary) SQLite database.
# Acceptance criterion covered here: "evidence refs resolve".
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/tests/python/test_evidence_ids.py (new file)
#   Tests:     compass/evidence.py (+ the result models in compass/tool_contracts.py)
#   Uses:      compass/db.py connect()          -> creates repo + ticket 2 tables
#              compass/seed_synthetic.py (t2)   -> loads tests/python/fixtures/synthetic_oct.json
#              compass/db.py correct_classification -> the repo's own "user fixes a type" path
#              compass/money.py net_cash_flow_cents -> ticket 1's rule, to check $1,963.00
#   Same setup style as tests/python/test_dev2_schema.py (ticket 2): one fresh DB per test.
#
# THE FIXTURE (T1-T7), for reading the numbers below
#   T1 Oct 03 STARBUCKS #1234   -575    expense  Coffee
#   T2 Oct 10 STARBUCKS #0987   -625    expense  Coffee
#   T3 Oct 15 AMZN MKTP US     -4000    expense  Shopping
#   T4 Oct 20 AMZN REFUND      +1500    refund   Shopping
#   T5 Oct 25 XFER TO SAVINGS -20000    transfer Transfer
#   T6 Oct 31 ACME PAYROLL   +200000    income   Income
#   T7 Nov 04 STARBUCKS #1234   -600    expense  Coffee     (outside October)
#   October spending = 575 + 625 + 4000 - 1500 = 3700 ($37.00)
#   October net cash flow = 200000 - 3700 = 196300 ($1,963.00)   (T5 transfer left out)
#
# HOW TO RUN
#   python -m pytest -v tests/python/test_evidence_ids.py

import json
import sqlite3

import pytest

from compass.db import connect, correct_classification
from compass.evidence import call_tool, data_version, resolve_evidence, save_evidence
from compass.money import Txn, net_cash_flow_cents
from compass.seed_synthetic import load_fixture, seed
from compass.tool_contracts import (
    ERROR_EVIDENCE_NOT_FOUND,
    TOOLS,
    Exclusion,
    ToolError,
    is_error,
)

OCT = {"start": "2026-10-01", "end": "2026-11-01"}
NOV = {"start": "2026-11-01", "end": "2026-12-01"}
MAR = {"start": "2026-03-01", "end": "2026-04-01"}


@pytest.fixture
def con(tmp_path):
    """A brand-new database in a temp folder, seeded with T1-T7. Closed after the test."""
    c = connect(tmp_path / "compass_test.db")
    seed(c, load_fixture())
    yield c
    c.close()


def run(con, name, payload):
    """call_tool with a dict payload; fail loudly if it returned an error envelope."""
    result = call_tool(con, name, json.dumps(payload))
    assert not is_error(result), result
    return result


def evidence_rows(con, result_id):
    return con.execute(
        "SELECT transaction_id, role, reason FROM evidence WHERE owner_id = ? ORDER BY id",
        (result_id,)).fetchall()


# ---------------------------------------------------------------------------
# Golden numbers on the shared fixture
# ---------------------------------------------------------------------------

def test_october_category_summary_matches_the_golden_fixture(con):
    r = run(con, "category_summary", {"period": OCT})
    assert r.total_spending_cents == 3700                                   # $37.00
    assert [(l.key, l.spending_cents, l.evidence_ids) for l in r.lines] == [
        ("Shopping", 2500, ("T3", "T4")),      # 4000 - 1500 refund, biggest first
        ("Coffee", 1200, ("T1", "T2")),        # 575 + 625
    ]
    assert r.evidence_ids == ("T1", "T2", "T3", "T4")
    assert r.excluded == (Exclusion(transaction_id="T5", reason="transfer"),
                          Exclusion(transaction_id="T6", reason="income"))
    assert r.coverage.complete is True


def test_october_merchant_summary_uses_clean_merchant_names(con):
    r = run(con, "merchant_summary", {"period": OCT})
    assert [(l.key, l.spending_cents) for l in r.lines] == [("Amazon", 2500), ("Starbucks", 1200)]
    # 'AMZN MKTP US' / 'STARBUCKS #1234' became 'Amazon' / 'Starbucks' via ticket 2's aliases.


def test_october_net_cash_flow_is_196300(con):
    r = run(con, "get_transactions", {"period": OCT})
    txns = [Txn(id=row.id, posted_date=row.posted_date.isoformat(), kind=row.type,
                amount_cents=row.amount_cents) for row in r.rows]
    assert net_cash_flow_cents(txns) == 196300                              # $1,963.00
    assert r.net_cents == 176300       # raw signed sum incl. the -20000 transfer, as documented


def test_filters_and_period_edges(con):
    coffee = run(con, "get_transactions", {"period": OCT, "category": "Coffee"})
    assert coffee.evidence_ids == ("T1", "T2")                  # T7 is Nov 4: outside [Oct 1, Nov 1)
    amazon = run(con, "merchant_summary", {"period": OCT, "merchant": "Amazon"})
    assert amazon.total_spending_cents == 2500


def test_limit_truncates_and_says_so(con):
    r = run(con, "get_transactions", {"period": OCT, "limit": 2})
    assert r.evidence_ids == ("T1", "T2") and r.truncated is True
    assert run(con, "get_transactions", {"period": OCT}).truncated is False


def test_top_n_cuts_lines_but_not_the_total(con):
    r = run(con, "category_summary", {"period": OCT, "top_n": 1})
    assert [l.key for l in r.lines] == ["Shopping"] and r.lines_truncated is True
    assert r.total_spending_cents == 3700                       # still counts Coffee


# ---------------------------------------------------------------------------
# Coverage
# ---------------------------------------------------------------------------

def test_partial_and_missing_coverage(con):
    nov = run(con, "category_summary", {"period": NOV})
    assert nov.coverage.complete is False                       # data stops at Nov 4
    assert nov.total_spending_cents == 600                      # only T7 - and the UI must say "partial"
    mar = run(con, "get_transactions", {"period": MAR})
    assert mar.rows == () and mar.coverage.covered_start is None


# ---------------------------------------------------------------------------
# Evidence resolves (the acceptance criterion)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("name, payload", [
    ("get_transactions", {"period": OCT}),
    ("merchant_summary", {"period": OCT}),
    ("category_summary", {"period": OCT}),
    ("category_summary", {"period": NOV}),
])
def test_every_evidence_id_resolves(con, name, payload):
    r = run(con, name, payload)
    explained = run(con, "explain_total", {"result_id": r.result_id})
    assert explained.result_id == r.result_id
    assert explained.evidence_ids == r.evidence_ids              # same rows, same order
    assert explained.excluded == r.excluded
    all_ids = {row[0] for row in con.execute("SELECT id FROM transactions")}
    assert set(r.evidence_ids) | {e.transaction_id for e in r.excluded} <= all_ids
    # Every referenced ID is a real transaction.


def test_explain_sum_reconciles_with_the_total(con):
    r = run(con, "category_summary", {"period": OCT})
    explained = resolve_evidence(con, r.result_id)
    assert explained.included_sum_cents == -r.total_spending_cents         # -3700 vs 3700


def test_unknown_result_id_gives_evidence_not_found(con):
    env = call_tool(con, "explain_total", json.dumps({"result_id": "res_000000000000"}))
    assert env["error"] == ERROR_EVIDENCE_NOT_FOUND
    assert env["details"] == [{"loc": ["result_id"], "msg": "no evidence rows for this result_id",
                               "input": "res_000000000000"}]
    with pytest.raises(ToolError):
        resolve_evidence(con, "res_000000000000")               # same failure, raised form


# ---------------------------------------------------------------------------
# result_id stability and data_version
# ---------------------------------------------------------------------------

def test_same_question_same_data_same_id_and_no_duplicate_evidence(con):
    a = run(con, "category_summary", {"period": OCT})
    b = run(con, "category_summary", {"top_n": 10, "period": {"end": "2026-11-01", "start": "2026-10-01"}})
    assert a.result_id == b.result_id
    assert len(evidence_rows(con, a.result_id)) == 6            # 4 included + 2 excluded, not 12


def test_user_correction_changes_data_version_and_result_id(con):
    before_version = data_version(con)
    before = run(con, "category_summary", {"period": OCT})
    correct_classification(con, "T5", "expense", "Savings")      # repo's own correction path
    con.commit()
    after = run(con, "category_summary", {"period": OCT})
    assert data_version(con) != before_version
    assert after.result_id != before.result_id
    assert after.total_spending_cents == 23700                   # 3700 + the 20000 now called expense
    assert resolve_evidence(con, before.result_id).evidence_ids == ("T1", "T2", "T3", "T4")
    # The OLD result's receipts are still intact under the OLD ID.


# ---------------------------------------------------------------------------
# Result shape
# ---------------------------------------------------------------------------

def _floats(node):
    """Every float anywhere inside parsed JSON."""
    if isinstance(node, float):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _floats(v)
    elif isinstance(node, list):
        for v in node:
            yield from _floats(v)


@pytest.mark.parametrize("name", ["get_transactions", "merchant_summary", "category_summary"])
def test_results_have_no_floats_and_match_their_declared_model(con, name):
    r = run(con, name, {"period": OCT})
    assert type(r) is TOOLS[name].result_model
    data = json.loads(r.model_dump_json())
    assert list(_floats(data)) == []
    assert {"result_id", "evidence_ids", "excluded", "coverage"} <= set(data)


# ---------------------------------------------------------------------------
# save_evidence guards
# ---------------------------------------------------------------------------

def test_save_evidence_refuses_malformed_ids_and_unknown_transactions(con):
    with pytest.raises(ValueError):
        save_evidence(con, "res_BAD", ["T1"], [])
    with pytest.raises(sqlite3.IntegrityError):
        save_evidence(con, "res_0123456789ab", ["T999"], [])     # REFERENCES transactions(id)
    assert evidence_rows(con, "res_0123456789ab") == []           # rolled back: nothing half-saved
