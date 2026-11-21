# tests/python/test_dev2_schema.py
#
# Ticket CMP-1112-D2-01: tests for Dev 2's additions to the repo's database
# (compass/db.py) and the synthetic seed (compass/seed_synthetic.py).
#
# HOW TO RUN
#   python -m pytest -v tests/python/test_dev2_schema.py
#
# HOW THESE TESTS STAY SAFE
#   Each test gets a brand-new database file in a temporary folder (tmp_path).
#   Your real .local/ databases are never touched.
#
# "with pytest.raises(X):" means "the code inside MUST fail with error X".
#   If it succeeds instead, the test fails.

import sqlite3

import pytest

from compass.db import clear_all_data, connect
from compass.money import Txn, excluded_from_spending, spending_cents
from compass.seed_synthetic import cents_to_plain, load_fixture, seed

DEV2_TABLES = {"import_coverage", "merchant_aliases", "conversations", "messages", "insights", "evidence"}
REPO_TABLES = {"imports", "import_settings", "transactions"}

OCTOBER_ROWS = (
    "SELECT id, posted_date, effective_type AS kind, amount_cents "
    "FROM transaction_details WHERE posted_date >= '2026-10-01' AND posted_date < '2026-11-01'"
)


# ---------- setup that tests ask for by name ----------

@pytest.fixture
def db_path(tmp_path):
    """Path to a database file that doesn't exist yet."""
    return tmp_path / "compass_test.db"


@pytest.fixture
def con(db_path):
    """A database with all tables and the 7 sample transactions. Closed after the test."""
    c = connect(db_path)
    seed(c, load_fixture())
    yield c
    c.close()


def october_txns(con):
    """October's rows as Txn records for money.py. kind = the type after any user fix."""
    return [Txn(**dict(r)) for r in con.execute(OCTOBER_ROWS)]


# ---------- schema: tables exist and connect() is safe to repeat ----------

def test_connect_creates_repo_and_dev2_tables(db_path):
    c = connect(db_path)
    names = {r["name"] for r in c.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
    assert REPO_TABLES | DEV2_TABLES <= names           # all of them are there
    assert {"transaction_details", "transaction_merchants"} <= names
    c.close()


def test_connect_twice_keeps_data(db_path):
    # connect() re-runs the schema every time. "IF NOT EXISTS" must make that harmless.
    c = connect(db_path); seed(c, load_fixture()); c.close()
    c = connect(db_path)
    assert c.execute("SELECT count(*) FROM transactions").fetchone()[0] == 7
    c.close()


def test_foreign_keys_on_for_every_new_connection(db_path):
    # SQLite switches this off for each new connection, so check two.
    for _ in range(2):
        c = connect(db_path)
        assert c.execute("PRAGMA foreign_keys").fetchone()[0] == 1
        c.close()


# ---------- seed ----------

def test_seed_inserts_expected_rows(db_path):
    c = connect(db_path)
    assert seed(c, load_fixture()) == {"imports": 1, "import_coverage": 1,
                                       "merchant_aliases": 4, "transactions": 7}
    c.close()


def test_seed_twice_inserts_nothing_new(con):
    # `con` is already seeded once; seeding again adds nothing and there are still 7 rows, not 14.
    assert seed(con, load_fixture()) == {"imports": 0, "import_coverage": 0,
                                         "merchant_aliases": 0, "transactions": 0}
    assert con.execute("SELECT count(*) FROM transactions").fetchone()[0] == 7


def test_seed_refuses_database_with_other_imports(con):
    # Pretend the user already imported a real bank file.
    with con:
        con.execute("INSERT INTO imports(id, filename, sha256, created_at) VALUES(?,?,?,?)",
                    ("imp_real", "my_bank.csv", "a" * 64, "2026-11-01T00:00:00+00:00"))
    with pytest.raises(RuntimeError, match="refusing"):
        seed(con, load_fixture())
    # ...unless explicitly allowed
    assert seed(con, load_fixture(), allow_other_data=True)["transactions"] == 0


def test_bad_type_in_fixture_raises_and_saves_nothing(db_path):
    # 'purchase' is not one of the repo's types. It must fail loudly, and
    # because the seed is all-or-nothing, not even the import row is saved.
    fixture = load_fixture()
    fixture["transactions"][0]["predicted_type"] = "purchase"
    c = connect(db_path)
    with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
        seed(c, fixture)
    assert c.execute("SELECT count(*) FROM imports").fetchone()[0] == 0
    assert c.execute("SELECT count(*) FROM transactions").fetchone()[0] == 0
    c.close()


def test_float_amount_in_fixture_is_refused(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text('{"imports": [], "transactions": '
                   '[{"id": "X", "amount_cents": -5.75, "source_row_number": 1}]}')
    with pytest.raises(ValueError, match="integer"):
        load_fixture(bad)


def test_original_row_is_kept_as_csv_style_json(con):
    import json
    row = con.execute("SELECT original_row_json FROM transactions WHERE id = 'T1'").fetchone()
    assert json.loads(row[0]) == {"date": "2026-10-03", "description": "STARBUCKS #1234",
                                  "amount": "-5.75", "account": "Synthetic Checking",
                                  "transaction_id": "SYN-0001"}


@pytest.mark.parametrize("cents, text", [(-575, "-5.75"), (200000, "2000.00"), (5, "0.05"), (0, "0.00")])
def test_cents_to_plain(cents, text):
    assert cents_to_plain(cents) == text


# ---------- links between tables (foreign keys) ----------

def test_foreign_key_check_is_empty_after_seed(con):
    # SQLite's own health check: empty = every link is valid.
    assert con.execute("PRAGMA foreign_key_check").fetchall() == []


def test_evidence_for_unknown_transaction_is_rejected(con):
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
        with con:
            con.execute("INSERT INTO evidence(owner_type, owner_id, transaction_id, role) "
                        "VALUES('tool_result', 'res_x', 'T999', 'included')")


def test_coverage_for_unknown_import_is_rejected(con):
    with pytest.raises(sqlite3.IntegrityError, match="FOREIGN KEY"):
        with con:
            con.execute("INSERT INTO import_coverage VALUES('imp_missing', '2026-10-01', '2026-11-01')")


def test_coverage_end_must_be_after_start(con):
    with con:
        con.execute("INSERT INTO imports(id, filename, sha256, created_at) VALUES(?,?,?,?)",
                    ("imp_2", "x.csv", "b" * 64, "2026-11-01T00:00:00+00:00"))
    with pytest.raises(sqlite3.IntegrityError, match="CHECK"):
        with con:
            con.execute("INSERT INTO import_coverage VALUES('imp_2', '2026-11-01', '2026-10-01')")


def test_coverage_cannot_be_edited(con):
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        with con:
            con.execute("UPDATE import_coverage SET covered_end = '2026-12-01'")


def test_evidence_rows_can_be_saved_and_read(con):
    with con:
        con.executemany("INSERT INTO evidence(owner_type, owner_id, transaction_id, role, reason) "
                        "VALUES('tool_result', 'res_oct', ?, ?, ?)",
                        [("T1", "included", None), ("T5", "excluded", "transfer")])
    rows = con.execute("SELECT transaction_id, role FROM evidence WHERE owner_id = 'res_oct' "
                       "ORDER BY transaction_id").fetchall()
    assert [tuple(r) for r in rows] == [("T1", "included"), ("T5", "excluded")]


# ---------- money stored as whole numbers ----------

def test_all_amounts_are_stored_as_integers(con):
    types = {r[0] for r in con.execute("SELECT typeof(amount_cents) FROM transactions")}
    assert types == {"integer"}


@pytest.mark.parametrize("bad_amount", [-5.75, "-5.75", "abc"])
def test_non_integer_amounts_are_rejected(con, bad_amount):
    # The repo's CHECK(typeof(amount_cents) = 'integer') refuses all of these.
    with pytest.raises(sqlite3.IntegrityError):
        with con:
            con.execute(
                "INSERT INTO transactions(id, account_id, import_id, source_row_number, posted_date, "
                "description, amount_cents, original_row_json, predicted_type, predicted_category, created_at) "
                "VALUES('BAD', 'acct_synth_1', 'imp_synth_oct', 99, '2026-10-05', 'X', ?, '{}', "
                "'expense', 'Other', '2026-11-05T09:00:00+00:00')", (bad_amount,))


# ---------- corrections (the repo's override columns) and views ----------

def test_category_correction_shows_in_view_and_source_is_unchanged(con):
    # User says Amazon order T3 was a gift.
    with con:
        con.execute("UPDATE transactions SET corrected_category = 'Gifts' WHERE id = 'T3'")
    view = con.execute("SELECT effective_category, has_correction FROM transaction_details "
                       "WHERE id = 'T3'").fetchone()
    raw = con.execute("SELECT predicted_category FROM transactions WHERE id = 'T3'").fetchone()
    assert view["effective_category"] == "Gifts"
    assert view["has_correction"] == 1
    assert raw["predicted_category"] == "Shopping"        # original kept


def test_source_amount_cannot_be_edited(con):
    # The repo's trigger protects source fields; seeded rows must obey it too.
    with pytest.raises(sqlite3.IntegrityError, match="immutable"):
        with con:
            con.execute("UPDATE transactions SET amount_cents = -1 WHERE id = 'T1'")


def test_merchant_view_uses_aliases(con):
    rows = dict(con.execute("SELECT transaction_id, merchant FROM transaction_merchants").fetchall())
    assert rows["T1"] == "Starbucks" and rows["T2"] == "Starbucks"
    assert rows["T3"] == "Amazon" and rows["T4"] == "Amazon"


def test_merchant_view_falls_back_to_description(con):
    with con:
        con.execute(
            "INSERT INTO transactions(id, account_id, import_id, source_row_number, posted_date, "
            "description, amount_cents, original_row_json, predicted_type, predicted_category, created_at) "
            "VALUES('T8', 'acct_synth_1', 'imp_synth_oct', 8, '2026-10-12', 'CORNER DELI', -900, '{}', "
            "'expense', 'Food', '2026-11-05T09:00:00+00:00')")
    merchant = con.execute("SELECT merchant FROM transaction_merchants WHERE transaction_id = 'T8'").fetchone()[0]
    assert merchant == "CORNER DELI"


# ---------- works together with the ticket 1 money rules ----------

def test_october_spending_matches_golden_value(con):
    # $37.00 = 575 + 625 + 4000 - 1500. Transfer T5 and income T6 are left out.
    txns = october_txns(con)
    assert spending_cents(txns) == 3700
    assert excluded_from_spending(txns) == ["T5", "T6"]


def test_reclassifying_expense_as_transfer_changes_spending(con):
    # If T3 ($40 Amazon) was really a transfer, it stops counting:
    #   coffee 1200 - refund 1500 = -300 (a small net refund)
    with con:
        con.execute("UPDATE transactions SET corrected_type = 'transfer' WHERE id = 'T3'")
    assert spending_cents(october_txns(con)) == -300


def test_unknown_type_is_excluded_from_spending(con):
    # 'unknown' isn't counted; it's listed so the user can classify it.
    with con:
        con.execute("UPDATE transactions SET corrected_type = 'unknown' WHERE id = 'T1'")
    txns = october_txns(con)
    assert spending_cents(txns) == 3125            # 3700 - 575
    assert "T1" in excluded_from_spending(txns)


# ---------- clearing data still works with the new tables ----------

def test_clear_all_data_removes_evidence_and_keeps_aliases(con):
    with con:
        con.execute("INSERT INTO evidence(owner_type, owner_id, transaction_id, role) "
                    "VALUES('tool_result', 'res_oct', 'T1', 'included')")
        con.execute("INSERT INTO conversations VALUES('c1', '2026-11-20T10:00:00')")
        con.execute("INSERT INTO messages VALUES('m1', 'c1', 'assistant', 'You spent $37.00', '2026-11-20T10:00:01')")
    clear_all_data(con)          # must not fail on the links from evidence/messages
    for table in ("transactions", "imports", "import_coverage", "evidence", "messages", "conversations"):
        assert con.execute(f"SELECT count(*) FROM {table}").fetchone()[0] == 0, table
    assert con.execute("SELECT count(*) FROM merchant_aliases").fetchone()[0] == 4
