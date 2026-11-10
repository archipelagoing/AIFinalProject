"""Strict CSV normalization and atomic statement ingestion into local SQLite."""

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sqlite3

from compass import db
from compass.analytics import aggregate
from compass.classification import classify
from compass.contracts import Transaction, parse_amount_cents, validate_posted_date

REQUIRED_COLUMNS = ("date", "description", "amount", "account", "transaction_id")
DEMO_STATEMENTS = (
    "synthetic_checking_2026_Jan-Jun.csv",
    "synthetic_savings_2026_Jan-Jun.csv",
)
MAX_FILE_BYTES = 5 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class ImportIssue:
    row_number: int | None
    line_number: int | None
    reason: str


@dataclass(frozen=True, slots=True)
class ImportResult:
    total_rows: int = 0
    valid_rows: int = 0
    invalid_rows: int = 0
    imported_rows: int = 0
    issues: tuple[ImportIssue, ...] = ()
    duplicate: bool = False
    import_id: str | None = None

    @property
    def ok(self) -> bool:
        return not self.issues

    @property
    def rejected_rows(self) -> int:
        """Atomic rejection includes valid rows withheld with an invalid file."""
        return self.total_rows if self.issues else 0


def _parse(data: bytes, namespace: str) -> tuple[list[Transaction], list[ImportIssue], int]:
    issues, transactions = [], []
    digest = hashlib.sha256(data).hexdigest()
    if not namespace.strip():
        return [], [ImportIssue(None, None, "Choose a nonempty bank/source identity.")], 0
    if len(data) > MAX_FILE_BYTES:
        return [], [ImportIssue(None, None, "Choose a CSV no larger than 5 MB.")], 0
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError:
        return [], [ImportIssue(None, None, "Save the statement as UTF-8 CSV and try again.")], 0
    reader = csv.reader(io.StringIO(text, newline=""), strict=True)
    try:
        headers = next(reader)
    except (StopIteration, csv.Error):
        return [], [ImportIssue(1, 1, "The CSV needs a header and at least one transaction.")], 0
    if len(headers) != len(REQUIRED_COLUMNS) or set(headers) != set(REQUIRED_COLUMNS):
        return [], [ImportIssue(1, 1, "Use exactly these unique columns: " + ",".join(REQUIRED_COLUMNS))], 0
    ordinal, seen = 1, set()
    timestamp = datetime.now(timezone.utc).isoformat()
    while True:
        line_number = reader.line_num + 1
        try:
            cells = next(reader)
        except StopIteration:
            break
        except csv.Error:
            ordinal += 1
            issues.append(ImportIssue(ordinal, line_number, "Malformed CSV quoting; no rows imported."))
            break
        ordinal += 1
        try:
            if len(cells) != len(headers):
                raise ValueError("Row column count does not match the header.")
            raw = dict(zip(headers, cells))
            posted_date = validate_posted_date(raw["date"].strip())
            amount = parse_amount_cents(raw["amount"])
            description, account = raw["description"].strip(), raw["account"].strip()
            if not description or not account:
                raise ValueError("Description and account must be nonempty.")
            source_id = raw["transaction_id"].strip() or None
            account_id = "csv:" + hashlib.sha256(json.dumps([namespace.strip(), account], ensure_ascii=False).encode()).hexdigest()
            if source_id is not None:
                identity = (account_id, source_id)
                if identity in seen:
                    raise ValueError("Repeated source transaction ID in this account; review the statement.")
                seen.add(identity)
            prediction = classify(description, amount)
            transactions.append(Transaction(
                id=hashlib.sha256(f"{digest}:{ordinal}".encode()).hexdigest(),
                account_id=account_id, source_transaction_id=source_id, import_id=digest,
                source_row_number=ordinal, posted_date=posted_date,
                description=description, amount_cents=amount,
                original_row_json=json.dumps(raw, ensure_ascii=False, sort_keys=True),
                predicted_type=prediction.kind, predicted_category=prediction.category,
                created_at=timestamp,
            ))
        except ValueError as error:
            issues.append(ImportIssue(ordinal, line_number, str(error)))
    if ordinal == 1:
        issues.append(ImportIssue(None, None, "The CSV contains no transaction rows."))
    return transactions, issues, ordinal - 1


def inspect_demo_statement(path: Path) -> dict[str, str | int]:
    transactions, issues, _ = _parse(path.read_bytes(), "fictional-demo")
    if issues:
        issue = issues[0]
        raise ValueError(f"{path.name}, row {issue.row_number}: {issue.reason}")
    return {"Statement": path.name, "Transactions": len(transactions), "Data": "Fictional"}


def import_statement(connection: sqlite3.Connection, data: bytes, filename: str, *, source_namespace: str = "default") -> ImportResult:
    """Validate first, then commit the whole statement under a SQLite savepoint.

    With an outer transaction the caller owns its final commit. Without one,
    releasing the savepoint durably commits this import. Existing caller writes
    are never committed or rolled back by this operation.
    """
    if not isinstance(data, bytes):
        raise TypeError("Statement input must be original file bytes.")
    transactions, issues, count = _parse(data, source_namespace)
    if issues:
        invalid = sum(issue.row_number is not None and issue.row_number > 1 for issue in issues)
        return ImportResult(count, len(transactions), invalid, issues=tuple(issues))
    if not isinstance(filename, str) or not filename.strip():
        return ImportResult(count, count, issues=(ImportIssue(None, None, "A source filename is required."),))
    digest = hashlib.sha256(data).hexdigest()
    current_row = None
    connection.execute("SAVEPOINT compass_statement_import")
    try:
        if connection.execute("SELECT 1 FROM imports WHERE sha256 = ?", (digest,)).fetchone():
            connection.execute("RELEASE SAVEPOINT compass_statement_import")
            return ImportResult(count, count, duplicate=True, import_id=digest)
        db.add_import(connection, digest, filename, digest)
        for transaction in transactions:
            current_row = transaction.source_row_number
            db.add_transaction(connection, transaction)
        # Reject totals outside the exact money contract before committing.
        saved = db.list_transactions(connection)
        for month in {row.posted_date[:7] for row in saved}:
            aggregate(row for row in saved if row.posted_date.startswith(month + "-"))
        connection.execute("RELEASE SAVEPOINT compass_statement_import")
    except (sqlite3.Error, ValueError) as error:
        connection.execute("ROLLBACK TO SAVEPOINT compass_statement_import")
        connection.execute("RELEASE SAVEPOINT compass_statement_import")
        if isinstance(error, sqlite3.IntegrityError):
            reason = "A source ID, import row, or database constraint conflicts with existing data. Review overlapping statements. The entire import was rolled back."
        elif isinstance(error, ValueError):
            reason = "Combined amounts exceed the supported integer-cent range. The entire import was rolled back."
        else:
            reason = "The database could not save this statement. The entire import was rolled back; check local storage access."
        return ImportResult(count, count, issues=(ImportIssue(current_row, None, reason),))
    return ImportResult(count, count, imported_rows=count, import_id=digest)
