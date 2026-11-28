"""SQLite schema, source preservation, and queries shared by imports and reports."""

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
import json

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
CREATE TABLE IF NOT EXISTS import_settings (
    import_id TEXT PRIMARY KEY REFERENCES imports(id),
    source_namespace TEXT NOT NULL,
    mapping_json TEXT NOT NULL CHECK(json_valid(mapping_json)),
    confirmed_distinct INTEGER NOT NULL CHECK(confirmed_distinct IN (0,1))
);
CREATE TRIGGER IF NOT EXISTS immutable_import_settings
BEFORE UPDATE ON import_settings
BEGIN SELECT RAISE(ABORT, 'Source interpretation is immutable'); END;
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
CREATE VIEW IF NOT EXISTS transaction_details AS
SELECT *,
    COALESCE(corrected_type, predicted_type) AS effective_type,
    COALESCE(corrected_category, predicted_category) AS effective_category,
    (corrected_type IS NOT NULL OR corrected_category IS NOT NULL) AS has_correction
FROM transactions;
""" + f"""
CREATE TRIGGER IF NOT EXISTS immutable_transaction_source
BEFORE UPDATE OF {','.join(SOURCE_FIELDS)} ON transactions
BEGIN SELECT RAISE(ABORT, 'Source fields are immutable; edit classification overrides only'); END;
"""


# ---------------------------------------------------------------------------
# Dev 2 additions (CMP-1112-D2-01). This block is new. The only other edits are in
# connect() and clear_all_data(), each marked "Dev 2". No existing line was removed.
#
# In plain English:
#   * These are extra tables Compass needs for evidence-backed numbers.
#   * "IF NOT EXISTS" means: create it the first time, skip it every time after.
#     So connect() can run this on every start-up safely.
#   * No existing table is changed, so existing data and tests keep working.
#   * REFERENCES links rows to other tables; SQLite refuses broken links
#     (connect() switches that checking on).
# ---------------------------------------------------------------------------
DEV2_SCHEMA = """
-- IMPORT_COVERAGE: which dates each import covers.
--   Lets later code say "November is only partly loaded" instead of
--   pretending November was cheap.
--   Example: covered_start '2026-10-01', covered_end '2026-11-05'
--            = Oct 1 through Nov 4 (the end date itself is NOT included).
CREATE TABLE IF NOT EXISTS import_coverage (
    import_id     TEXT PRIMARY KEY REFERENCES imports(id),
    covered_start TEXT NOT NULL CHECK(covered_start GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    covered_end   TEXT NOT NULL CHECK(covered_end   GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    CHECK(covered_start < covered_end)
);
-- Coverage describes the source file, so like other source metadata it can't be edited.
CREATE TRIGGER IF NOT EXISTS immutable_import_coverage
BEFORE UPDATE ON import_coverage
BEGIN SELECT RAISE(ABORT, 'Import coverage is immutable'); END;

-- MERCHANT_ALIASES: rules that turn messy bank text into a clean merchant name.
--   '%' means "anything here".
--   Example: 'STARBUCKS%' matches 'STARBUCKS #1234' -> merchant 'Starbucks'.
CREATE TABLE IF NOT EXISTS merchant_aliases (
    pattern  TEXT PRIMARY KEY NOT NULL CHECK(length(trim(pattern)) > 0),
    merchant TEXT NOT NULL CHECK(length(trim(merchant)) BETWEEN 1 AND 80)
);

-- CONVERSATIONS and MESSAGES: chat history with the assistant.
--   Each answer is its own message, so evidence can point at exactly
--   which answer used which transactions.
CREATE TABLE IF NOT EXISTS conversations (
    id         TEXT PRIMARY KEY NOT NULL,
    started_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS messages (
    id              TEXT PRIMARY KEY NOT NULL,
    conversation_id TEXT NOT NULL REFERENCES conversations(id),
    role            TEXT NOT NULL CHECK(role IN ('user','assistant','tool')),
    content         TEXT NOT NULL,
    created_at      TEXT NOT NULL
);

-- INSIGHTS: saved findings, e.g. "Coffee spending fell 50% in November".
--   payload_json holds the details and must be valid JSON.
CREATE TABLE IF NOT EXISTS insights (
    id           TEXT PRIMARY KEY NOT NULL,
    kind         TEXT NOT NULL,
    period_start TEXT NOT NULL,
    period_end   TEXT NOT NULL,
    payload_json TEXT NOT NULL CHECK(json_valid(payload_json)),
    created_at   TEXT NOT NULL
);

-- EVIDENCE: the receipts behind every number.
--   Each row says "this insight / message / tool result used (or left out) this transaction".
--   Example for "You spent $37.00 in October":
--     ('tool_result', 'res_9b0d33e1aa42', 'T1', 'included', NULL)
--     ('tool_result', 'res_9b0d33e1aa42', 'T5', 'excluded', 'transfer')
--   owner_id can point at three different tables, so it can't have one
--   REFERENCES rule; tests check those links instead.
CREATE TABLE IF NOT EXISTS evidence (
    id             INTEGER PRIMARY KEY,
    owner_type     TEXT NOT NULL CHECK(owner_type IN ('insight','message','tool_result')),
    owner_id       TEXT NOT NULL,
    transaction_id TEXT NOT NULL REFERENCES transactions(id),
    role           TEXT NOT NULL CHECK(role IN ('included','excluded')),
    reason         TEXT
);
CREATE INDEX IF NOT EXISTS ix_evidence_owner ON evidence(owner_type, owner_id);
CREATE INDEX IF NOT EXISTS ix_evidence_transaction ON evidence(transaction_id);

-- TRANSACTION_MERCHANTS (a view = a saved query that looks like a table):
--   the clean merchant name for each transaction, from merchant_aliases.
--   If several patterns match, the longest (most specific) one wins.
--   If none match, the bank description is used as-is.
--   Example: 'STARBUCKS #1234' -> 'Starbucks';  'CORNER DELI' -> 'CORNER DELI'
--   Done as a view so the existing transactions table doesn't change.
CREATE VIEW IF NOT EXISTS transaction_merchants AS
SELECT t.id AS transaction_id,
       COALESCE(
           (SELECT a.merchant FROM merchant_aliases a
            WHERE t.description LIKE a.pattern
            ORDER BY length(a.pattern) DESC, a.pattern
            LIMIT 1),
           t.description) AS merchant
FROM transactions t;
"""


def connect(path: str | Path) -> sqlite3.Connection:
    if str(path) != ":memory:":
        Path(path).parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(str(path))
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    # Dev 2: stop if this SQLite build can't enforce links between tables.
    if connection.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
        connection.close()
        raise RuntimeError("SQLite foreign key enforcement could not be enabled")
    connection.executescript(SCHEMA)
    connection.executescript(DEV2_SCHEMA)  # Dev 2: extra tables, created only if missing
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


def list_transactions(connection: sqlite3.Connection) -> list[Transaction]:
    return [Transaction(**dict(row)) for row in connection.execute("SELECT * FROM transactions ORDER BY posted_date, id")]


def list_imports(connection: sqlite3.Connection) -> list[dict]:
    return [dict(row) for row in connection.execute("""
        SELECT imports.*, source_namespace, mapping_json, confirmed_distinct
        FROM imports LEFT JOIN import_settings ON imports.id = import_settings.import_id
        ORDER BY created_at, id
    """)]


def clear_all_data(connection: sqlite3.Connection) -> None:
    """Delete only Compass records atomically; callers provide explicit UI confirmation.

    Keep the schema and bundled fixtures. No uploaded files are persisted by this
    app. SQLite secure_delete overwrites deleted cells, not external backups or
    filesystem snapshots; this is not a guarantee of forensic erasure.
    """
    if connection.in_transaction:
        raise ValueError("Finish the current database operation before clearing data.")
    connection.execute("PRAGMA secure_delete = ON")
    with connection:
        # Dev 2: delete rows that POINT AT transactions/imports first,
        # otherwise the foreign-key links would block the delete.
        # Chat history and insights are derived from the user's money data, so they go too.
        # merchant_aliases are naming rules, not personal records, so they stay.
        connection.execute("DELETE FROM evidence")
        connection.execute("DELETE FROM messages")
        connection.execute("DELETE FROM conversations")
        connection.execute("DELETE FROM insights")
        connection.execute("DELETE FROM transactions")
        connection.execute("DELETE FROM import_settings")
        connection.execute("DELETE FROM import_coverage")
        connection.execute("DELETE FROM imports")


def account_label(transaction: Transaction, metadata: dict) -> str:
    if metadata.get("mapping_json"):
        mapping = json.loads(metadata["mapping_json"])
        if mapping.get("account_column"):
            return transaction.original_row[mapping["account_column"]]
        if mapping.get("fixed_account"):
            return mapping["fixed_account"]
    return transaction.original_row.get("account", transaction.account_id)


def correct_classification(connection: sqlite3.Connection, transaction_id: str, kind: TransactionType | str, category: str) -> Transaction:
    corrected = get_transaction(connection, transaction_id).with_classification(kind, category)
    _store_override(connection, corrected)
    return corrected


def restore_classification(connection: sqlite3.Connection, transaction_id: str) -> Transaction:
    from dataclasses import replace

    original = replace(get_transaction(connection, transaction_id), corrected_type=None, corrected_category=None)
    _store_override(connection, original)
    return original


def _store_override(connection: sqlite3.Connection, transaction: Transaction) -> None:
    from compass.analytics import summarize_month

    connection.execute("SAVEPOINT compass_classification")
    try:
        connection.execute(
            "UPDATE transactions SET corrected_type = ?, corrected_category = ? WHERE id = ?",
            (transaction.corrected_type.value if transaction.corrected_type is not None else None,
             transaction.corrected_category, transaction.id),
        )
        month = transaction.posted_date[:7]
        # Validate both headline and category totals before committing an edit.
        summary = summarize_month(list_transactions(connection), month)
        summary.category_totals
        connection.execute("RELEASE SAVEPOINT compass_classification")
    except (ValueError, sqlite3.Error):
        connection.execute("ROLLBACK TO SAVEPOINT compass_classification")
        connection.execute("RELEASE SAVEPOINT compass_classification")
        raise