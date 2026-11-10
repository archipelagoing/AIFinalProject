import csv
from dataclasses import replace
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from compass import db
from compass.analytics import reconcile_transfers, summarize_month
from compass.contracts import TransactionType, parse_amount_cents
from compass.importer import import_statement, read_headers
from compass.mapping import ColumnMapping

ROOT = Path(__file__).resolve().parents[2]
CHECKING = (ROOT / "fixtures/synthetic_checking_2026_Jan-Jun.csv").read_bytes()
SAVINGS = (ROOT / "fixtures/synthetic_savings_2026_Jan-Jun.csv").read_bytes()
HEADER = "date,description,amount,account,transaction_id\n"


def statement(*rows):
    return (HEADER + "\n".join(rows)).encode()


@pytest.fixture
def connection():
    conn = db.connect(":memory:")
    yield conn
    conn.close()


def load_both(conn):
    assert import_statement(conn, CHECKING, "checking.csv", source_namespace="demo").imported_rows == 158
    assert import_statement(conn, SAVINGS, "savings.csv", source_namespace="demo").imported_rows == 6
    return db.list_transactions(conn)


def counts(conn):
    return tuple(conn.execute(f"SELECT count(*) FROM {table}").fetchone()[0] for table in ("imports", "transactions", "import_settings"))


def test_combined_statements_match_all_five_metrics_and_every_reference_label(connection):
    rows = load_both(connection)
    assert len(rows) == 164
    expected = json.loads((ROOT / "fixtures/expected_monthly_totals.json").read_text(), parse_float=Decimal)
    for month, wanted in expected.items():
        summary = summarize_month(rows, month)
        actual = summary.totals
        assert actual.income_cents == parse_amount_cents(str(wanted["income"]))
        assert actual.net_expenses_cents == parse_amount_cents(str(wanted["expenses_net_of_refunds"]))
        assert actual.surplus_cents == parse_amount_cents(str(wanted["surplus_before_transfers_and_unknown"]))
        assert actual.transfer_net_cents == 0
        assert actual.unknown_net_cents == parse_amount_cents(str(wanted["unknown_net_excluded"]))
        evidence = reconcile_transfers(summary.rows)
        assert len(evidence.pairs) == 1
        assert sum(row.amount_cents for row in evidence.pairs[0]) == 0
        assert evidence.pairs[0][0].account_id != evidence.pairs[0][1].account_id
        assert sum(summary.category_totals.values()) == actual.net_expenses_cents
    with (ROOT / "fixtures/synthetic_ground_truth.csv").open(newline="") as source:
        truth = {row["transaction_id"]: row for row in csv.DictReader(source)}
    assert len(truth) == len(rows)
    for row in rows:
        assert row.predicted_type.value == truth[row.source_transaction_id]["expected_type"]
        assert row.predicted_category == truth[row.source_transaction_id]["expected_category"]


def test_transfer_pair_evidence_does_not_infer_from_zero_net_or_ambiguous_groups(connection):
    rows = load_both(connection)
    march = summarize_month(rows, "2026-03")
    assert march.totals.transfer_net_cents == 0
    assert len(reconcile_transfers(march.rows).unmatched) == 2  # Peer transfers, no cross-account proof.
    may = summarize_month(rows, "2026-05")
    pair = reconcile_transfers(may.rows).pairs[0]
    ambiguous = [*pair, replace(pair[0], id="third"), replace(pair[1], id="fourth")]
    result = reconcile_transfers(ambiguous)
    assert not result.pairs and len(result.unmatched) == 4
    same_account = [pair[0], replace(pair[1], account_id=pair[0].account_id)]
    assert len(reconcile_transfers(same_account).unmatched) == 2


def test_identical_and_renamed_reimport_preserve_rows_metadata_and_overrides(connection):
    rows = load_both(connection)
    row = next(row for row in rows if "ATM" in row.description)
    corrected = db.correct_classification(connection, row.id, "expense", "Cash spending")
    before = counts(connection)
    for data, filename in [(CHECKING, "renamed-checking.csv"), (SAVINGS, "renamed-savings.csv")]:
        result = import_statement(connection, data, filename, source_namespace="demo")
        assert result.ok and result.duplicate and result.imported_rows == 0
    assert counts(connection) == before == (2, 164, 2)
    assert db.get_transaction(connection, row.id) == corrected
    assert {item["filename"] for item in db.list_imports(connection)} == {"checking.csv", "savings.csv"}


@pytest.mark.parametrize("source_ids", [("first", "second"), ("", "")])
def test_distinct_identical_looking_rows_survive_in_one_file(connection, source_ids):
    data = statement(*(f"2026-05-01,ALDI,-10.00,Checking,{identity}" for identity in source_ids))
    result = import_statement(connection, data, "purchases.csv")
    assert result.imported_rows == 2
    rows = db.list_transactions(connection)
    assert len({row.id for row in rows}) == 2
    assert summarize_month(rows, "2026-05").category_totals["Groceries"] == 2000


@pytest.mark.parametrize("with_ids", [True, False])
def test_cross_file_look_alikes_require_confirmation_and_preserve_both(connection, with_ids):
    first = statement(f"2026-05-01,ALDI,-10,Checking,{'a' if with_ids else ''}")
    second = statement(f"2026-05-01,ALDI,-10.00,Checking,{'b' if with_ids else ''}")
    assert import_statement(connection, first, "first.csv").ok
    blocked = import_statement(connection, second, "second.csv")
    assert not blocked.ok and blocked.review_required and "Possible cross-file duplicate" in blocked.issues[0].reason
    assert counts(connection) == (1, 1, 1)
    accepted = import_statement(connection, second, "second.csv", confirm_distinct=True)
    assert accepted.ok and accepted.imported_rows == 1 and accepted.warnings
    assert counts(connection) == (2, 2, 2)
    assert sum(record["confirmed_distinct"] for record in db.list_imports(connection)) == 1
    assert len({row.id for row in db.list_transactions(connection)}) == 2


@pytest.mark.parametrize("replacement", [
    "2026-05-01,ALDI,-11,Checking,a", "2026-05-02,ALDI,-10,Checking,a",
    "2026-05-01,SHOPRITE,-10,Checking,a", "2026-05-01,ALDI,-10.00,Checking,a",
])
def test_overlap_and_edited_source_ids_are_never_overwritten(connection, replacement):
    original = statement("2026-05-01,ALDI,-10,Checking,a")
    assert import_statement(connection, original, "first.csv").ok
    saved = db.list_transactions(connection)
    result = import_statement(connection, statement(replacement), "edited.csv", confirm_distinct=True)
    assert not result.ok and not result.review_required
    assert "source ID" in result.issues[0].reason
    assert counts(connection) == (1, 1, 1)
    assert db.list_transactions(connection) == saved


def test_same_filename_with_changed_ids_and_amounts_flags_edited_copy(connection):
    first = statement("2026-05-01,ALDI,-10,Checking,a", "2026-05-03,ALDI,-12,Checking,b")
    second = statement("2026-05-02,ALDI,-15,Checking,new")
    assert import_statement(connection, first, "statement.csv").ok
    blocked = import_statement(connection, second, "statement.csv")
    assert blocked.review_required and "edited copy" in blocked.issues[0].reason
    assert counts(connection) == (1, 2, 1)
    accepted = import_statement(connection, second, "statement.csv", confirm_distinct=True)
    assert accepted.ok and counts(connection) == (2, 3, 2)


def test_source_account_namespace_is_part_of_identity_but_same_bytes_cannot_be_reinterpreted(connection):
    data = statement("2026-05-01,ALDI,-10,Checking,a")
    assert import_statement(connection, data, "first.csv", source_namespace="bank-a").ok
    blocked = import_statement(connection, data, "first.csv", source_namespace="bank-b")
    assert not blocked.ok and "different bank/source" in blocked.issues[0].reason
    changed_bytes = data + b"\n"
    assert import_statement(connection, changed_bytes, "second.csv", source_namespace="bank-b").ok
    assert len({row.account_id for row in db.list_transactions(connection)}) == 2


def test_legacy_phase1_imports_without_settings_remain_idempotent(connection):
    assert import_statement(connection, CHECKING, "checking.csv", source_namespace="demo").ok
    connection.execute("DELETE FROM import_settings")  # Simulate pre-Phase-2 metadata, in an isolated test DB.
    connection.commit()
    result = import_statement(connection, CHECKING, "renamed.csv", source_namespace="demo")
    assert result.ok and result.duplicate and counts(connection) == (1, 158, 0)
    bad = import_statement(connection, CHECKING, "renamed.csv", source_namespace="other")
    assert not bad.ok


def test_unknown_review_recalculates_totals_and_keeps_source_immutable(connection):
    rows = load_both(connection)
    june = summarize_month(rows, "2026-06")
    atm = next(row for row in june.rows if "ATM" in row.description)
    assert atm.effective_type == TransactionType.UNKNOWN
    assert (june.totals.surplus_cents, june.totals.unknown_net_cents) == (171145, -8000)
    edited = db.correct_classification(connection, atm.id, "expense", "Cash spending")
    updated = summarize_month(db.list_transactions(connection), "2026-06")
    assert updated.totals.surplus_cents == 163145 and updated.totals.unknown_net_cents == 0
    assert updated.category_totals["Cash spending"] == 8000
    for name in db.SOURCE_FIELDS:
        assert getattr(edited, name) == getattr(atm, name)
    assert edited.has_correction
    restored = db.restore_classification(connection, atm.id)
    assert restored == atm and not restored.has_correction
    assert summarize_month(db.list_transactions(connection), "2026-06").totals.surplus_cents == 171145


def test_refund_offsets_its_effective_category_and_never_becomes_wages(connection):
    rows = load_both(connection)
    april = summarize_month(rows, "2026-04")
    refund = next(row for row in april.expense_rows if row.effective_type == TransactionType.REFUND)
    assert refund.amount_cents == 2499 and refund.effective_category == "Groceries"
    assert refund not in april.income_rows
    gross = sum(-row.amount_cents for row in april.expense_rows if row.effective_category == "Groceries" and row.effective_type == TransactionType.EXPENSE)
    assert april.category_totals["Groceries"] == gross - 2499
    db.correct_classification(connection, refund.id, "refund", "Restaurants")
    updated = summarize_month(db.list_transactions(connection), "2026-04")
    assert updated.totals == april.totals
    assert updated.category_totals["Groceries"] == april.category_totals["Groceries"] + 2499
    assert updated.category_totals["Restaurants"] == april.category_totals["Restaurants"] - 2499


def test_correction_persists_after_real_process_restart_and_reimport(tmp_path):
    path = tmp_path / "restart.db"
    conn = db.connect(path)
    rows = load_both(conn)
    atm = next(row for row in rows if "ATM" in row.description)
    corrected = db.correct_classification(conn, atm.id, "expense", "Cash spending")
    conn.close()
    program = """
import json, sys
from pathlib import Path
from compass import db
from compass.importer import import_statement
from compass.analytics import summarize_month
c = db.connect(sys.argv[1])
before = db.get_transaction(c, sys.argv[2])
assert before.corrected_type.value == 'expense'
r = import_statement(c, Path(sys.argv[3]).read_bytes(), 'renamed.csv', source_namespace='demo')
assert r.ok and r.duplicate
after = db.get_transaction(c, sys.argv[2])
assert after == before
assert summarize_month(db.list_transactions(c), '2026-06').totals.surplus_cents == 163145
print(after.original_row_json)
c.close()
"""
    process = subprocess.run([sys.executable, "-c", program, str(path), atm.id, str(ROOT / "fixtures/synthetic_checking_2026_Jan-Jun.csv")], cwd=ROOT, text=True, capture_output=True, check=True)
    assert json.loads(process.stdout) == corrected.original_row


def test_invalid_sign_correction_does_not_change_saved_record(connection):
    row = load_both(connection)[0]
    with pytest.raises(ValueError):
        db.correct_classification(connection, row.id, "income", "Income")
    assert db.get_transaction(connection, row.id) == row


def test_out_of_range_correction_rolls_back_the_override(connection):
    data = statement("2026-05-01,PAYROLL,92233720368547758.07,Checking,pay", "2026-05-02,UNRESOLVED CREDIT,0.01,Checking,unknown")
    assert import_statement(connection, data, "large.csv").ok
    original = next(row for row in db.list_transactions(connection) if row.source_transaction_id == "unknown")
    with pytest.raises(ValueError, match="64-bit"):
        db.correct_classification(connection, original.id, "income", "Income")
    assert db.get_transaction(connection, original.id) == original
    assert not connection.in_transaction
    assert summarize_month(db.list_transactions(connection), "2026-05").totals.income_cents == 2**63 - 1


@pytest.mark.parametrize("mode,source_value,expected", [
    ("inflow_positive", "-12.34", -1234), ("outflow_positive", "12.34", -1234),
    ("outflow_positive", "-12.34", 1234),
])
def test_explicit_signed_mapping_preserves_original_fields(connection, mode, source_value, expected):
    data = f"Date,Merchant,Value,Unused\n05/02/2026,ALDI,{source_value},original text\n".encode()
    mapping = ColumnMapping(date_column="Date", description_column="Merchant", amount_column="Value", amount_mode=mode, fixed_account="Card account", date_format="%m/%d/%Y")
    result = import_statement(connection, data, "provider.csv", mapping=mapping)
    assert result.ok
    row = db.list_transactions(connection)[0]
    assert row.amount_cents == expected and row.posted_date == "2026-05-02"
    assert row.source_transaction_id is None
    assert row.original_row == {"Date": "05/02/2026", "Merchant": "ALDI", "Value": source_value, "Unused": "original text"}
    metadata = db.list_imports(connection)[0]
    assert db.account_label(row, metadata) == "Card account"
    assert json.loads(metadata["mapping_json"])["amount_mode"] == mode
    assert import_statement(connection, data, "renamed.csv", mapping=mapping).duplicate
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        connection.execute("UPDATE import_settings SET source_namespace='other'")


@pytest.mark.parametrize("date_format,expected", [("%m/%d/%Y", "2026-02-03"), ("%d/%m/%Y", "2026-03-02")])
def test_date_order_is_explicit_not_guessed(connection, date_format, expected):
    mapping = ColumnMapping(date_column="Date", description_column="Merchant", amount_column="Value", amount_mode="inflow_positive", fixed_account="Card", date_format=date_format)
    result = import_statement(connection, b"Date,Merchant,Value\n02/03/2026,ALDI,-1\n", "date.csv", mapping=mapping)
    assert result.ok and db.list_transactions(connection)[0].posted_date == expected


def test_debit_credit_mapping_and_account_id_columns(connection):
    data = b"Posted,Details,Debit,Credit,Account,ID\n2026-05-01,ALDI,20.25,,Checking,a\n2026-05-02,PAYROLL,,100.50,Checking,b\n"
    mapping = ColumnMapping(date_column="Posted", description_column="Details", debit_column="Debit", credit_column="Credit", account_column="Account", transaction_id_column="ID", amount_mode="debit_credit")
    result = import_statement(connection, data, "debit-credit.csv", mapping=mapping)
    assert result.ok and result.imported_rows == 2
    summary = summarize_month(db.list_transactions(connection), "2026-05")
    assert summary.totals.income_cents == 10050 and summary.totals.net_expenses_cents == 2025
    assert {row.source_transaction_id for row in summary.rows} == {"a", "b"}


@pytest.mark.parametrize("debit,credit", [("-1", ""), ("", "-1"), ("1", "1"), ("", ""), ("NaN", ""), ("Infinity", "")])
def test_ambiguous_debit_credit_rows_are_rejected_atomically(connection, debit, credit):
    mapping = ColumnMapping(date_column="Date", description_column="Details", debit_column="Debit", credit_column="Credit", fixed_account="Card", amount_mode="debit_credit")
    data = f"Date,Details,Debit,Credit\n2026-05-01,ALDI,1,\n2026-05-02,ALDI,{debit},{credit}\n".encode()
    result = import_statement(connection, data, "bad-debit.csv", mapping=mapping)
    assert not result.ok and result.issues[0].row_number == 3
    assert counts(connection) == (0, 0, 0)


@pytest.mark.parametrize("patch", [
    {"amount_mode": "guess"}, {"account_column": "Value"}, {"amount_column": "Missing"},
    {"description_column": "Date"}, {"date_format": "%y/%m/%d"},
])
def test_invalid_mapping_is_actionable_and_writes_nothing(connection, patch):
    mapping = ColumnMapping(date_column="Date", description_column="Merchant", amount_column="Value", amount_mode="inflow_positive", fixed_account="Card")
    result = import_statement(connection, b"Date,Merchant,Value\n2026-05-01,ALDI,-1\n", "bad.csv", mapping=replace(mapping, **patch))
    assert not result.ok and result.issues[0].row_number == 1
    assert counts(connection) == (0, 0, 0)


def test_same_bytes_cannot_silently_flip_amount_direction(connection):
    mapping = ColumnMapping(date_column="Date", description_column="Merchant", amount_column="Value", amount_mode="inflow_positive", fixed_account="Card")
    data = b"Date,Merchant,Value\n2026-05-01,ALDI,-10\n"
    assert import_statement(connection, data, "one.csv", mapping=mapping).ok
    changed = import_statement(connection, data, "two.csv", mapping=replace(mapping, amount_mode="outflow_positive"))
    assert not changed.ok and "different bank/source or column interpretation" in changed.issues[0].reason
    assert db.list_transactions(connection)[0].amount_cents == -1000


def test_read_headers_never_guesses_or_accepts_duplicate_names():
    assert read_headers(b"Posted,Merchant,Value\n2026-05-01,x,1\n") == ["Posted", "Merchant", "Value"]
    for data in (b"", b"a,a\n1,2", b"a,\n1,2", b"a,\xff\n1,2"):
        with pytest.raises(ValueError):
            read_headers(data)


def button(app, label):
    return next(item for item in app.button if item.label == label)


def test_streamlit_savings_review_recalculation_restore_and_reopen(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "review-ui.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.button(key="load_checking").click().run(timeout=30)
    app.button(key="load_savings").click().run(timeout=30)
    assert not app.exception and not app.error
    assert any("Transfer net: $0.00" in item.value for item in app.info)
    app.selectbox(key="summary_month").select("2026-06").run(timeout=30)
    app.checkbox(key="review_only_unknown").check().run(timeout=30)
    conn = db.connect(path)
    atm = next(row for row in db.list_transactions(conn) if "ATM" in row.description)
    conn.close()
    app.selectbox(key=f"edit_type_{atm.id}_0").select("expense")
    app.text_input(key=f"edit_category_{atm.id}_0").input("Cash spending")
    button(app, "Save classification").click().run(timeout=30)
    assert not app.exception and not app.error
    assert {item.label: item.value for item in app.metric}["Verified surplus"] == "$1,631.45"
    assert any("No unresolved transactions" in item.value for item in app.info)
    assert not any("$80.00" in item.value for item in app.warning)
    reopened = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    reopened.selectbox(key="summary_month").select("2026-06").run(timeout=30)
    assert not reopened.exception and not reopened.error
    assert {item.label: item.value for item in reopened.metric}["Verified surplus"] == "$1,631.45"
    reopened.selectbox(key="review_row_2026-06").select(atm.id).run(timeout=30)
    button(reopened, "Restore rule classification").click().run(timeout=30)
    assert not reopened.exception and not reopened.error
    assert {item.label: item.value for item in reopened.metric}["Verified surplus"] == "$1,711.45"
    assert any("$80.00" in item.value for item in reopened.warning)


@pytest.mark.parametrize("data,reason", [
    (b"", "header"), (b"date,description\n2026-05-01,ALDI", "columns"),
    (HEADER.encode() + b"2026-05-01,\xff,1,Checking,a", "UTF-8"),
    (HEADER.encode() + b'2026-05-01,"unclosed,1,Checking,a', "quoting"),
])
def test_streamlit_import_errors_are_visible_without_stack_traces(monkeypatch, tmp_path, data, reason):
    from streamlit.testing.v1 import AppTest

    monkeypatch.setenv("COMPASS_DB_PATH", str(tmp_path / "error-ui.db"))
    upload = io.BytesIO(data)
    upload.name = "invalid.csv"
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    button(app, "Import CSV").click().run(timeout=30)
    assert not app.exception
    assert any("Statement rejected" in item.value for item in app.error)
    assert any(reason.lower() in str(frame.value).lower() for frame in app.dataframe)


def test_streamlit_duplicate_file_and_partial_coverage_messages(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "duplicate-ui.db"
    conn = db.connect(path)
    assert import_statement(conn, CHECKING, "first.csv", source_namespace="my-bank").ok
    conn.close()
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    upload = io.BytesIO(CHECKING)
    upload.name = "renamed.csv"
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    button(app, "Import CSV").click().run(timeout=30)
    assert not app.exception and not app.error
    assert any("already imported" in item.value for item in app.info)
    assert any("may be incomplete" in item.value for item in app.warning)
    assert {item.label: item.value for item in app.metric}["Already imported"] == "158"


def test_streamlit_mapping_requires_explicit_direction_before_submission(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    monkeypatch.setenv("COMPASS_DB_PATH", str(tmp_path / "mapping-ui.db"))
    upload = io.BytesIO(b"Date,Merchant,Value\n2026-05-01,ALDI,12.34\n")
    upload.name = "provider.csv"
    token = hashlib.sha256(upload.getvalue()).hexdigest()
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.checkbox(key="use_column_mapping").check().run(timeout=30)
    assert not app.exception
    assert button(app, "Import CSV").disabled
    app.text_input(key=f"map_fixed_{token}").input("Card").run(timeout=30)
    app.selectbox(key=f"map_mode_{token}").select("outflow_positive").run(timeout=30)
    app.selectbox(key=f"map_amount_{token}").select("Value").run(timeout=30)
    assert not app.exception
    confirmation = next(item for item in app.checkbox if item.label.startswith("I confirm this column mapping"))
    assert button(app, "Import CSV").disabled
    confirmation.check().run(timeout=30)
    button(app, "Import CSV").click().run(timeout=30)
    assert not app.exception and not app.error
    assert {item.label: item.value for item in app.metric}["Net expenses"] == "$12.34"
    assert any("Account" in frame.value.columns and "Card" in frame.value["Account"].values for frame in app.dataframe)
    app.selectbox(key=f"map_mode_{token}").select("inflow_positive").run(timeout=30)
    assert button(app, "Import CSV").disabled


def test_streamlit_look_alike_confirmation_preserves_distinct_purchases(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "look-alike-ui.db"
    conn = db.connect(path)
    assert import_statement(conn, statement("2026-05-01,ALDI,-10,Checking,a"), "first.csv", source_namespace="my-bank").ok
    conn.close()
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    upload = io.BytesIO(statement("2026-05-01,ALDI,-10.00,Checking,b"))
    upload.name = "second.csv"
    monkeypatch.setattr("streamlit.file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    button(app, "Import CSV").click().run(timeout=30)
    assert not app.exception
    assert any("Possible overlap needs source review" in item.value for item in app.warning)
    assert {item.label: item.value for item in app.metric}["Accepted rows"] == "0"
    confirmation = next(item for item in app.checkbox if item.label.startswith("Keep flagged look-alike"))
    confirmation.check()  # Form fields are sent together with the submit event.
    button(app, "Import CSV").click().run(timeout=30)
    assert not app.exception and not app.error
    assert {item.label: item.value for item in app.metric}["Accepted rows"] == "1"
    assert {item.label: item.value for item in app.metric}["Net expenses"] == "$20.00"
    assert any("nothing was merged" in item.value for item in app.warning)
    conn = db.connect(path)
    assert counts(conn) == (2, 2, 2)
    conn.close()


def test_streamlit_invalid_classification_edit_is_actionable_and_atomic(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "invalid-edit-ui.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.button(key="load_checking").click().run(timeout=30)
    conn = db.connect(path)
    original = next(row for row in db.list_transactions(conn) if row.source_transaction_id == "T0109")
    conn.close()
    app.selectbox(key="review_row_2026-05").select(original.id).run(timeout=30)
    app.selectbox(key=f"edit_type_{original.id}_0").select("income")
    app.text_input(key=f"edit_category_{original.id}_0").input("Income")
    button(app, "Save classification").click().run(timeout=30)
    assert not app.exception
    assert any("positive source amounts" in item.value for item in app.error)
    assert {item.label: item.value for item in app.metric}["Verified surplus"] == "$747.06"
    conn = db.connect(path)
    assert db.get_transaction(conn, original.id) == original
    conn.close()
