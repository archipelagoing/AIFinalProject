"""SQLite schema and source-preserving classification updates (no importer yet)."""

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sqlite3

from compass.contracts import Transaction, TransactionType


SOURCE_FIELDS = (
    "id", "account_id", "source_transaction_id", "import_id", "source_row_number",
    "posted_date", "description", "amount_cents", "original_row_json",
    "predicted_type", "predicted_category", "created_at",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS imports (
    id TEXT PRIMARY KEY NOT NULL,
    filename TEXT NOT NULL CHECK(length(trim(filename)) > 0),
    sha256 TEXT UNIQUE NOT NULL CHECK(length(sha256) = 64),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS transactions (
    id TEXT PRIMARY KEY NOT NULL,
    account_id TEXT NOT NULL CHECK(length(trim(account_id)) > 0),
    source_transaction_id TEXT,
    import_id TEXT NOT NULL REFERENCES imports(id),
    source_row_number INTEGER NOT NULL CHECK(source_row_number > 0),
    posted_date TEXT NOT NULL,
    description TEXT NOT NULL CHECK(length(trim(description)) > 0),
    amount_cents INTEGER NOT NULL CHECK(typeof(amount_cents) = 'integer'),
    original_row_json TEXT NOT NULL CHECK(json_valid(original_row_json)),
    predicted_type TEXT NOT NULL CHECK(predicted_type IN ('income','expense','refund','transfer','unknown')),
    predicted_category TEXT NOT NULL CHECK(length(trim(predicted_category)) BETWEEN 1 AND 80),
    corrected_type TEXT CHECK(corrected_type IN ('income','expense','refund','transfer','unknown')),
    corrected_category TEXT CHECK(length(trim(corrected_category)) BETWEEN 1 AND 80),
    created_at TEXT NOT NULL,
    UNIQUE(account_id, source_transaction_id),
    UNIQUE(import_id, source_row_number),
    CHECK(source_transaction_id IS NULL OR length(trim(source_transaction_id)) > 0),
    CHECK(predicted_type NOT IN ('income','refund') OR amount_cents > 0),
    CHECK(predicted_type != 'expense' OR amount_cents < 0),
    CHECK(COALESCE(corrected_type,predicted_type) NOT IN ('income','refund') OR amount_cents > 0),
    CHECK(COALESCE(corrected_type,predicted_type) != 'expense' OR amount_cents < 0)
);
CREATE TRIGGER IF NOT EXISTS immutable_import_source
BEFORE UPDATE ON imports
BEGIN SELECT RAISE(ABORT, 'Import source metadata is immutable'); END;
""" + f"""
CREATE TRIGGER IF NOT EXISTS immutable_transaction_source
BEFORE UPDATE OF {','.join(SOURCE_FIELDS)} ON transactions
BEGIN SELECT RAISE(ABORT, 'Source fields are immutable; edit classification overrides only'); END;
"""


def connect(path: str | Path) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(SCHEMA)
    return connection


def add_import(connection: sqlite3.Connection, import_id: str, filename: str, sha256: str) -> None:
    connection.execute(
        "INSERT INTO imports(id,filename,sha256,created_at) VALUES(?,?,?,?)",
        (import_id, filename, sha256, datetime.now(timezone.utc).isoformat()),
    )


def add_transaction(connection: sqlite3.Connection, transaction: Transaction) -> None:
    record = asdict(transaction)
    for name in ("predicted_type", "corrected_type"):
        if isinstance(record[name], TransactionType):
            record[name] = record[name].value
    fields = tuple(record)
    connection.execute(
        f"INSERT INTO transactions({','.join(fields)}) VALUES({','.join('?' for _ in fields)})",
        tuple(record[name] for name in fields),
    )


def get_transaction(connection: sqlite3.Connection, transaction_id: str) -> Transaction:
    row = connection.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,)).fetchone()
    if row is None:
        raise KeyError("Transaction not found.")
    return Transaction(**dict(row))


def correct_classification(connection: sqlite3.Connection, transaction_id: str, kind: TransactionType | str, category: str) -> Transaction:
    corrected = get_transaction(connection, transaction_id).with_classification(kind, category)
    connection.execute(
        "UPDATE transactions SET corrected_type = ?, corrected_category = ? WHERE id = ?",
        (corrected.corrected_type.value, corrected.corrected_category, transaction_id),
    )
    return corrected
