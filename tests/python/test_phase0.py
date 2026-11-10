from dataclasses import FrozenInstanceError, replace
import hashlib
import importlib
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys

import pytest

from compass.analytics import aggregate
from compass.contracts import Transaction, TransactionType, format_money, parse_amount_cents, validate_posted_date
from compass import db
from compass.importer import DEMO_STATEMENTS, inspect_demo_statement
from scripts.audit_fixtures import audit_fixtures

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def transaction():
    return Transaction(
        id="local-1", account_id="bank-a:checking", source_transaction_id="source-1",
        import_id="import-1", source_row_number=2, posted_date="2026-05-01",
        description="ORIGINAL RENT", amount_cents=-127500,
        original_row_json=json.dumps({"date": "2026-05-01", "description": "ORIGINAL RENT", "amount": "-1275.00", "account": "Checking", "transaction_id": "source-1"}),
        predicted_type=TransactionType.EXPENSE, predicted_category="Housing",
    )


@pytest.mark.parametrize("text,cents", [("+1850.00", 185000), ("-1275.00", -127500), ("24.99", 2499), ("0", 0), ("0.01", 1), ("10.5", 1050), (" 5.00 ", 500)])
def test_exact_signed_money(text, cents):
    assert parse_amount_cents(text) == cents


@pytest.mark.parametrize("value", ["NaN", "Infinity", "", "1e3", "$1", "1,000.00", "1.001", "1.", ".50", "１２.００", "900000000000000000.00", 1.0, True])
def test_money_rejects_ambiguous_or_noninteger_inputs(value):
    with pytest.raises(ValueError):
        parse_amount_cents(value)


@pytest.mark.parametrize("value", ["2026-02-30", "2026-2-01", "05/01/2026", "20260501", "", "2026-05-01T00:00:00Z"])
def test_iso_calendar_date_required(value):
    with pytest.raises(ValueError):
        validate_posted_date(value)


def test_valid_date_and_money_display():
    assert validate_posted_date("2024-02-29") == "2024-02-29"
    assert format_money(-127500) == "−$1,275.00"
    assert format_money(1) == "$0.01"


@pytest.mark.parametrize("kind,amount,income,expenses,transfer,unknown,surplus", [
    ("income", 10000, 10000, 0, 0, 0, 10000),
    ("expense", -1000, 0, 1000, 0, 0, -1000),
    ("refund", 2499, 0, -2499, 0, 0, 2499),
    ("transfer", -30000, 0, 0, -30000, 0, 0),
    ("transfer", 30000, 0, 0, 30000, 0, 0),
    ("unknown", -8000, 0, 0, 0, -8000, 0),
])
def test_each_accounting_type(transaction, kind, amount, income, expenses, transfer, unknown, surplus):
    row = replace(transaction, predicted_type=kind, amount_cents=amount)
    totals = aggregate([row])
    assert (totals.income_cents, totals.net_expenses_cents, totals.transfer_net_cents, totals.unknown_net_cents, totals.surplus_cents) == (income, expenses, transfer, unknown, surplus)


@pytest.mark.parametrize("patch", [
    {"amount_cents": 1.5}, {"amount_cents": True}, {"amount_cents": 2**63},
    {"account_id": ""}, {"source_transaction_id": ""}, {"source_row_number": 0},
    {"predicted_type": "not-a-type"}, {"predicted_type": "income"},
    {"predicted_category": ""}, {"corrected_category": ""},
    {"original_row_json": "[]"}, {"created_at": "2026-05-01T00:00:00"},
])
def test_normalized_record_rejects_invalid_fields(transaction, patch):
    with pytest.raises(ValueError):
        replace(transaction, **patch)


def test_classification_edits_cannot_overwrite_sources(transaction):
    corrected = transaction.with_classification("unknown", "Needs review")
    assert corrected.effective_type == TransactionType.UNKNOWN
    assert corrected.effective_category == "Needs review"
    assert corrected.predicted_type == TransactionType.EXPENSE
    for field in db.SOURCE_FIELDS:
        assert getattr(corrected, field) == getattr(transaction, field)
    for field, value in [("amount_cents", -1), ("posted_date", "2026-06-01"), ("description", "changed")]:
        with pytest.raises(FrozenInstanceError):
            setattr(corrected, field, value)
    original = corrected.original_row
    original["description"] = "changed"
    assert corrected.original_row["description"] == "ORIGINAL RENT"
    assert aggregate([corrected]).surplus_cents == 0
    assert aggregate([transaction]).surplus_cents == -127500
    with pytest.raises(TypeError):
        transaction.with_classification("expense", "Housing", amount_cents=-1)


@pytest.mark.parametrize("kind,category", [("income", "Income"), ("refund", "Housing"), ("expense", ""), ("invalid", "Housing")])
def test_invalid_override_rejected(transaction, kind, category):
    with pytest.raises(ValueError):
        transaction.with_classification(kind, category)


def test_sqlite_sources_immutable_and_corrections_persist(transaction, tmp_path):
    path = tmp_path / "compass.db"
    conn = db.connect(path)
    assert conn.execute("PRAGMA foreign_keys").fetchone()[0] == 1
    with conn:
        db.add_import(conn, "import-1", "source.csv", "a" * 64)
        db.add_transaction(conn, transaction)
    for field in db.SOURCE_FIELDS:
        with pytest.raises(sqlite3.IntegrityError, match="immutable"):
            conn.execute(f"UPDATE transactions SET {field} = {field} WHERE id = ?", (transaction.id,))
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        conn.execute("UPDATE imports SET filename = 'renamed.csv'")
    with conn:
        db.correct_classification(conn, transaction.id, "unknown", "Uncategorized")
    conn.close()
    reopened = db.connect(path)
    saved = db.get_transaction(reopened, transaction.id)
    assert saved.effective_type == TransactionType.UNKNOWN
    for field in db.SOURCE_FIELDS:
        assert getattr(saved, field) == getattr(transaction, field)
    reopened.close()


def test_account_scoped_identity_and_foreign_keys(transaction):
    conn = db.connect(":memory:")
    with pytest.raises(sqlite3.IntegrityError):
        db.add_transaction(conn, transaction)
    with conn:
        db.add_import(conn, "import-1", "source.csv", "b" * 64)
        db.add_transaction(conn, transaction)
        db.add_transaction(conn, replace(transaction, id="local-2", account_id="bank-b:checking", source_row_number=3))
    assert conn.execute("SELECT count(*) FROM transactions").fetchone()[0] == 2
    with pytest.raises(sqlite3.IntegrityError):
        db.add_transaction(conn, replace(transaction, id="local-3", source_row_number=4))
    conn.close()


def test_fixture_copies_are_identical_and_readable():
    for name in (*DEMO_STATEMENTS, "synthetic_ground_truth.csv", "expected_monthly_totals.json"):
        copied = (ROOT / "fixtures" / name).read_bytes()
        assert copied == (ROOT / "CompassProto1.0" / name).read_bytes()
        assert copied.decode("utf-8")
    assert [inspect_demo_statement(ROOT / "fixtures" / name)["Transactions"] for name in DEMO_STATEMENTS] == [158, 6]


def test_independent_audit_matches_all_six_months():
    report = audit_fixtures(ROOT / "fixtures")
    assert report["ok"], report
    assert report["transaction_count"] == 164
    assert report["accounts"] == ["Checking", "Savings"]
    assert len(report["totals_cents"]) == 6
    assert report["totals_cents"]["2026-05"]["surplus_before_transfers_and_unknown"] == 74706
    assert report["totals_cents"]["2026-06"]["unknown_net_excluded"] == -8000
    assert all(row["transfer_net_across_accounts"] == 0 for row in report["totals_cents"].values())


def test_audit_reports_mismatch_without_changing_expected_values(tmp_path):
    fixtures = tmp_path / "fixtures"
    shutil.copytree(ROOT / "fixtures", fixtures)
    expected_path = fixtures / "expected_monthly_totals.json"
    original_digest = hashlib.sha256(expected_path.read_bytes()).hexdigest()
    checking = fixtures / DEMO_STATEMENTS[0]
    checking.write_text(checking.read_text().replace("-1275.00", "-1276.00", 1))
    report = audit_fixtures(fixtures)
    assert not report["ok"]
    assert {entry["metric"] for entry in report["discrepancies"]} == {"expenses_net_of_refunds", "surplus_before_transfers_and_unknown"}
    assert report["discrepancies"][0]["month"] == "2026-01"
    assert hashlib.sha256(expected_path.read_bytes()).hexdigest() == original_digest
    result = subprocess.run([sys.executable, str(ROOT / "scripts/audit_fixtures.py"), "--fixtures", str(fixtures), "--json"], capture_output=True, text=True)
    assert result.returncode == 1
    assert not json.loads(result.stdout)["ok"]


def test_audit_does_not_depend_on_production_modules():
    source = (ROOT / "scripts/audit_fixtures.py").read_text()
    assert "from compass" not in source
    assert "import compass" not in source
    for path in [ROOT / "app.py", *(ROOT / "compass").glob("*.py")]:
        assert "synthetic_ground_truth" not in path.read_text()
        assert "expected_monthly_totals" not in path.read_text()


def test_all_planned_modules_import():
    for name in ("db", "importer", "classification", "analytics", "questions", "scenarios"):
        importlib.import_module(f"compass.{name}")


def test_streamlit_app_starts_without_script_errors(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "app.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not app.exception, [entry.message for entry in app.exception]
    assert not app.error
    assert any("fictional" in entry.value.lower() for entry in app.warning)
    assert any("Phase 0" in entry.value for entry in app.info)
    assert len(app.table) == 1
    conn = db.connect(path)
    assert conn.execute("SELECT count(*) FROM transactions").fetchone()[0] == 0
    conn.close()
