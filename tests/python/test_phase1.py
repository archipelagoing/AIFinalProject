import csv
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from compass import db
from compass.analytics import summarize_month
from compass.classification import classify
from compass.contracts import TransactionType
from compass.importer import import_statement

ROOT = Path(__file__).resolve().parents[2]
CHECKING = (ROOT / "fixtures/synthetic_checking_2026_Jan-Jun.csv").read_bytes()
HEADER = "date,description,amount,account,transaction_id\n"


def statement(*rows):
    return (HEADER + "\n".join(rows)).encode()


@pytest.fixture
def connection():
    conn = db.connect(":memory:")
    yield conn
    conn.close()


def counts(conn):
    return tuple(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in ("imports", "transactions"))


def test_checking_vertical_slice_and_provenance(connection):
    result = import_statement(connection, CHECKING, "fictional-checking.csv", source_namespace="demo")
    assert result.ok and result.imported_rows == result.valid_rows == result.total_rows == 158
    assert result.invalid_rows == result.rejected_rows == 0
    assert counts(connection) == (1, 158)
    assert not connection.in_transaction  # Complete savepoint committed durably.
    digest = hashlib.sha256(CHECKING).hexdigest()
    imported = db.list_imports(connection)[0]
    assert imported["sha256"] == imported["id"] == digest
    assert imported["filename"] == "fictional-checking.csv"
    rows = db.list_transactions(connection)
    source = list(csv.DictReader(io.StringIO(CHECKING.decode())))
    by_source_id = {row.source_transaction_id: row for row in rows}
    for ordinal, raw in enumerate(source, start=2):
        row = by_source_id[raw["transaction_id"]]
        assert row.source_row_number == ordinal
        assert row.original_row == raw
        assert row.import_id == digest
        assert row.id == hashlib.sha256(f"{digest}:{ordinal}".encode()).hexdigest()
        assert row.account_id.startswith("csv:")
        assert not row.has_correction
    may = summarize_month(rows, "2026-05")
    assert (may.totals.income_cents, may.totals.net_expenses_cents, may.totals.surplus_cents) == (370000, 295294, 74706)
    assert sum(row.amount_cents for row in may.income_rows) == may.totals.income_cents
    assert sum(-row.amount_cents for row in may.expense_rows) == may.totals.net_expenses_cents
    assert {row.id for row in may.surplus_rows} == {row.id for row in may.income_rows + may.expense_rows}
    assert all(row.effective_type not in (TransactionType.TRANSFER, TransactionType.UNKNOWN) for row in may.surplus_rows)


@pytest.mark.parametrize("row", [
    "2026-05-01,RENT,NaN,Checking,bad", "2026-05-01,RENT,Infinity,Checking,bad",
    "2026-05-01,RENT,-Infinity,Checking,bad", "2026-05-01,RENT,1e3,Checking,bad",
    "2026-05-01,RENT,-1.001,Checking,bad", "2026-05-01,RENT,$10,Checking,bad",
    '2026-05-01,RENT,"1,000.00",Checking,bad', "2026-05-01,RENT,,Checking,bad",
    "2026-02-30,RENT,-10.00,Checking,bad", ",RENT,-10.00,Checking,bad",
    "05/01/2026,RENT,-10.00,Checking,bad", "20260501,RENT,-10.00,Checking,bad",
    "2026-05-01,,10.00,Checking,bad", "2026-05-01,RENT,-10.00,,bad",
    "2026-05-01,RENT,-10.00,Checking", "2026-05-01,RENT,-10.00,Checking,bad,extra",
])
def test_invalid_row_rejects_entire_statement_with_counts_and_row(connection, row):
    initial = import_statement(connection, statement("2026-04-01,PAYROLL,20,Checking,existing"), "existing.csv")
    assert initial.ok
    before = counts(connection)
    result = import_statement(connection, statement("2026-05-01,PAYROLL,10.25,Checking,valid", row), "bad.csv")
    assert not result.ok
    assert (result.total_rows, result.valid_rows, result.invalid_rows, result.imported_rows, result.rejected_rows) == (2, 1, 1, 0, 2)
    assert result.issues[0].row_number == result.issues[0].line_number == 3
    assert result.issues[0].reason
    assert counts(connection) == before


@pytest.mark.parametrize("content", [
    b"", HEADER.encode(), b"date,description,amount,account\n2026-05-01,x,-1,Checking",
    b"date,description,amount,account,account\n2026-05-01,x,-1,Checking,Checking",
    b"date,description,amount,account,transaction_id,extra\n2026-05-01,x,-1,Checking,a,x",
    HEADER.encode() + b"2026-05-01,\xff,-1,Checking,a",
    HEADER.encode() + b'2026-05-01,"never closed,-1,Checking,a',
])
def test_invalid_file_has_no_partial_import(connection, content):
    result = import_statement(connection, content, "bad.csv")
    assert not result.ok and result.imported_rows == 0
    assert counts(connection) == (0, 0)


def test_csv_bom_crlf_multiline_and_physical_error_line(connection):
    data = ('\ufeff' + HEADER.replace('\n', '\r\n') + '2026-05-01,"PAYROLL,\r\nWITH ""QUOTES""",+10.25,Checking,a\r\n2026-05-02,RENT,NaN,Checking,b\r\n').encode()
    result = import_statement(connection, data, "quoted.csv")
    assert result.valid_rows == 1 and result.invalid_rows == 1
    assert result.issues[0].row_number == 3
    assert result.issues[0].line_number == 4
    assert counts(connection) == (0, 0)
    good = data.replace(b"NaN", b"-0.01")
    accepted = import_statement(connection, good, "quoted.csv")
    assert accepted.imported_rows == 2
    assert sorted(row.amount_cents for row in db.list_transactions(connection)) == [-1, 1025]
    assert any('WITH "QUOTES"' in row.description for row in db.list_transactions(connection))


def test_actual_database_failure_rolls_back_prior_rows_and_import_metadata(connection):
    connection.executescript("""
        CREATE TRIGGER simulate_failed_second_insert BEFORE INSERT ON transactions
        WHEN NEW.source_transaction_id = 'fail-second'
        BEGIN SELECT RAISE(ABORT, 'simulated failure'); END;
    """)
    data = statement("2026-05-01,PAYROLL,100,Checking,first", "2026-05-02,ALDI,-10,Checking,fail-second")
    result = import_statement(connection, data, "failure.csv")
    assert not result.ok and result.imported_rows == 0
    assert result.issues[0].row_number == 3
    assert "rolled back" in result.issues[0].reason
    assert counts(connection) == (0, 0)


def test_atomic_conflicting_source_id_preserves_existing_data(connection):
    assert import_statement(connection, statement("2026-05-01,PAYROLL,10,Checking,known"), "first.csv").ok
    prior = db.list_transactions(connection)
    result = import_statement(connection, statement("2026-05-02,ALDI,-1,Checking,new", "2026-05-03,PAYROLL,20,Checking,known"), "overlap.csv")
    assert not result.ok and result.rejected_rows == 2
    assert counts(connection) == (1, 1)
    assert db.list_transactions(connection) == prior


def test_import_savepoint_does_not_commit_or_rollback_callers_transaction(connection):
    db.add_import(connection, "callers-import", "unrelated.csv", "a" * 64)
    assert connection.in_transaction
    result = import_statement(connection, statement("2026-05-01,PAYROLL,10,Checking,a"), "one.csv")
    assert result.ok and connection.in_transaction
    assert counts(connection) == (2, 1)
    connection.rollback()
    assert counts(connection) == (0, 0)


def test_renamed_reimport_and_streamlit_reruns_are_idempotent(connection):
    first = import_statement(connection, CHECKING, "original.csv")
    row = db.list_transactions(connection)[0]
    with connection:
        corrected = db.correct_classification(connection, row.id, "unknown", "Needs review")
    result = import_statement(connection, CHECKING, "renamed.csv")
    assert first.ok and result.ok and result.duplicate
    assert result.imported_rows == result.rejected_rows == 0
    assert counts(connection) == (1, 158)
    assert db.get_transaction(connection, row.id) == corrected


def test_legitimate_repeated_purchases_and_account_identity(connection):
    data = statement("2026-05-01,ALDI,-1,Checking,a", "2026-05-01,ALDI,-1,Checking,b", "2026-05-01,ALDI,-1,Savings,a", "2026-05-01,ALDI,-1,Checking,", "2026-05-01,ALDI,-1,Checking,")
    result = import_statement(connection, data, "repeated.csv")
    assert result.ok and result.imported_rows == 5
    assert len({row.id for row in db.list_transactions(connection)}) == 5
    assert len({row.account_id for row in db.list_transactions(connection)}) == 2


def test_effective_fields_and_correction_flags_are_queryable(connection):
    assert import_statement(connection, CHECKING, "checking.csv").ok
    row = db.list_transactions(connection)[0]
    with connection:
        corrected = db.correct_classification(connection, row.id, "unknown", "Review")
    details = connection.execute("SELECT * FROM transaction_details WHERE id = ?", (row.id,)).fetchone()
    assert details["effective_type"] == "unknown" and details["effective_category"] == "Review"
    assert details["has_correction"] == 1
    assert corrected.has_correction and corrected.original_row_json == row.original_row_json


@pytest.mark.parametrize("description,amount,kind,category", [
    ("NORTHSTAR DESIGN PAYROLL", 185000, "income", "Income"),
    ("OAK TERRACE APARTMENTS RENT", -127500, "expense", "Housing"),
    ("SHOPRITE RETURN", 2499, "refund", "Groceries"),
    ("AUTOMATIC SAVINGS TRANSFER", -30000, "transfer", "Transfer"),
    ("ATM CASH WITHDRAWAL", -8000, "unknown", "Uncategorized"),
    ("UNRECOGNIZED MERCHANT", -100, "unknown", "Uncategorized"),
    ("PAYROLL", -100, "unknown", "Uncategorized"),
])
def test_keyword_classification_has_explanations(description, amount, kind, category):
    prediction = classify(description, amount)
    assert prediction.kind.value == kind and prediction.category == category
    assert prediction.explanation


def test_reference_classifications_and_monthly_totals_are_test_only(connection):
    assert import_statement(connection, CHECKING, "checking.csv").ok
    rows = db.list_transactions(connection)
    with (ROOT / "fixtures/synthetic_ground_truth.csv").open(newline="") as source:
        reference = {item["transaction_id"]: item for item in csv.DictReader(source)}
    for row in rows:
        expected = reference[row.source_transaction_id]
        assert row.predicted_type.value == expected["expected_type"], row.source_transaction_id
        assert row.predicted_category == expected["expected_category"], row.source_transaction_id
    expected_totals = json.loads((ROOT / "fixtures/expected_monthly_totals.json").read_text())
    from compass.contracts import parse_amount_cents
    for month, expected in expected_totals.items():
        totals = summarize_month(rows, month).totals
        assert totals.income_cents == parse_amount_cents(str(expected["income"]))
        assert totals.net_expenses_cents == parse_amount_cents(str(expected["expenses_net_of_refunds"]))
        assert totals.surplus_cents == parse_amount_cents(str(expected["surplus_before_transfers_and_unknown"]))


def test_data_survives_real_python_process_restart(tmp_path):
    database = tmp_path / "persist.db"
    writer = """
import json, sys
from pathlib import Path
from compass import db
from compass.importer import import_statement
c = db.connect(sys.argv[1])
r = import_statement(c, Path(sys.argv[2]).read_bytes(), 'checking.csv')
assert r.ok and r.imported_rows == 158
print(json.dumps(sorted(row.id for row in db.list_transactions(c))))
c.close()
"""
    reader = """
import json, sys
from compass import db
from compass.analytics import summarize_month
c = db.connect(sys.argv[1])
rows = db.list_transactions(c)
s = summarize_month(rows, '2026-05')
assert s.totals.income_cents == 370000
assert s.totals.net_expenses_cents == 295294
assert s.totals.surplus_cents == 74706
print(json.dumps(sorted(row.id for row in rows)))
c.close()
"""
    first = subprocess.run([sys.executable, "-c", writer, str(database), str(ROOT / "fixtures/synthetic_checking_2026_Jan-Jun.csv")], cwd=ROOT, check=True, text=True, capture_output=True)
    second = subprocess.run([sys.executable, "-c", reader, str(database)], cwd=ROOT, check=True, text=True, capture_output=True)
    assert json.loads(first.stdout) == json.loads(second.stdout)


def test_streamlit_demo_snapshot_evidence_month_switch_and_restart(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    monkeypatch.setenv("COMPASS_DB_PATH", str(tmp_path / "ui.db"))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not app.exception and not app.error
    app.button(key="load_checking").click().run(timeout=30)
    assert not app.exception and not app.error
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Accepted rows"] == "158" and metrics["Rejected rows"] == "0"
    assert metrics["Verified income"] == "$3,700.00"
    assert metrics["Net expenses"] == "$2,952.94"
    assert metrics["Verified surplus"] == "$747.06"
    assert app.selectbox(key="summary_month").value == "2026-05"
    frames = [item.value for item in app.dataframe]
    assert any(len(frame) == 2 and "Source ID" in frame.columns for frame in frames)
    assert any("T0109" in frame["Source ID"].values for frame in frames if "Source ID" in frame.columns)
    app.selectbox(key="summary_month").select("2026-06").run(timeout=30)
    assert not app.exception and not app.error
    assert any("$80.00" in item.value for item in app.warning)
    assert {item.label: item.value for item in app.metric}["Verified surplus"] == "$1,711.45"
    app.button(key="load_checking").click().run(timeout=30)
    assert any("already imported" in item.value for item in app.info)
    fresh = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not fresh.exception and not fresh.error
    assert {item.label: item.value for item in fresh.metric}["Verified surplus"] == "$747.06"


def test_streamlit_shows_atomic_rejection_counts_and_row_error(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "invalid-ui.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    upload = io.BytesIO(statement("2026-05-01,PAYROLL,1,Checking,a", "2026-05-02,ALDI,NaN,Checking,b"))
    upload.name = "invalid.csv"
    # AppTest has no OS file picker: supply its uploaded-file boundary while
    # still exercising the real submit handler, importer, database and UI.
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file(str(ROOT / "app.py"))
    app.run(timeout=30)
    next(button for button in app.button if button.label == "Import CSV").click().run(timeout=30)
    assert not app.exception
    assert any("Statement rejected" in item.value for item in app.error)
    metrics = {item.label: item.value for item in app.metric}
    assert metrics["Accepted rows"] == "0" and metrics["Rejected rows"] == "2"
    errors = app.dataframe[0].value
    assert errors.iloc[0]["Row"] == "3" and errors.iloc[0]["CSV line"] == "3"
    assert "decimal" in errors.iloc[0]["Reason"]
    conn = db.connect(path)
    assert counts(conn) == (0, 0)
    conn.close()


def test_uploader_can_rerun_before_enabling_form_submission(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    monkeypatch.setenv("COMPASS_DB_PATH", str(tmp_path / "form.db"))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not app.exception
    assert not app.get("file_uploader")[0].proto.form_id
    assert next(button for button in app.button if button.label == "Import CSV").disabled
