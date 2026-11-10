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
from compass.analytics import summarize_month
from compass.classification import classify
from compass.contracts import Transaction
from compass.mapping import CANONICAL_MAPPING, ColumnMapping

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
    warnings: tuple[str, ...] = ()
    review_required: bool = False

    @property
    def ok(self) -> bool:
        return not self.issues

    @property
    def rejected_rows(self) -> int:
        """Atomic rejection includes valid rows withheld with an invalid file."""
        return self.total_rows if self.issues else 0


def read_headers(data: bytes) -> list[str]:
    if len(data) > MAX_FILE_BYTES:
        raise ValueError("Choose a CSV no larger than 5 MB.")
    try:
        headers = next(csv.reader(io.StringIO(data.decode("utf-8-sig"), newline=""), strict=True))
    except UnicodeDecodeError as error:
        raise ValueError("Save the statement as UTF-8 CSV and try again.") from error
    except (StopIteration, csv.Error) as error:
        raise ValueError("The CSV needs a readable header and transaction rows.") from error
    if not headers or any(not header.strip() for header in headers) or len(set(headers)) != len(headers):
        raise ValueError("CSV headers must be nonempty and unique.")
    return headers


def _parse(data: bytes, namespace: str, mapping: ColumnMapping | None = None) -> tuple[list[Transaction], list[ImportIssue], int]:
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
    if mapping is None and (len(headers) != len(REQUIRED_COLUMNS) or set(headers) != set(REQUIRED_COLUMNS)):
        return [], [ImportIssue(1, 1, "Use exactly these unique columns: " + ",".join(REQUIRED_COLUMNS))], 0
    try:
        if not headers or any(not header.strip() for header in headers) or len(set(headers)) != len(headers):
            raise ValueError("CSV headers must be nonempty and unique.")
        selected_mapping = mapping or CANONICAL_MAPPING
        selected_mapping.validate(headers)
    except ValueError as error:
        return [], [ImportIssue(1, 1, str(error))], 0
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
            normalized = selected_mapping.normalize(raw)
            posted_date, amount = normalized["posted_date"], normalized["amount_cents"]
            description, account = normalized["description"], normalized["account"]
            if not description or not account:
                raise ValueError("Description and account must be nonempty.")
            source_id = normalized["source_id"]
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


def import_statement(connection: sqlite3.Connection, data: bytes, filename: str, *, source_namespace: str = "default", mapping: ColumnMapping | None = None, confirm_distinct: bool = False) -> ImportResult:
    """Validate first, then commit the whole statement under a SQLite savepoint.

    With an outer transaction the caller owns its final commit. Without one,
    releasing the savepoint durably commits this import. Existing caller writes
    are never committed or rolled back by this operation.
    """
    if not isinstance(data, bytes):
        raise TypeError("Statement input must be original file bytes.")
    transactions, issues, count = _parse(data, source_namespace, mapping)
    if issues:
        invalid = sum(issue.row_number is not None and issue.row_number > 1 for issue in issues)
        return ImportResult(count, len(transactions), invalid, issues=tuple(issues))
    if not isinstance(filename, str) or not filename.strip():
        return ImportResult(count, count, issues=(ImportIssue(None, None, "A source filename is required."),))
    digest = hashlib.sha256(data).hexdigest()
    interpretation = (mapping or CANONICAL_MAPPING).to_json()
    notices = ()
    current_row = None
    connection.execute("SAVEPOINT compass_statement_import")
    try:
        saved = db.list_transactions(connection)
        if connection.execute("SELECT 1 FROM imports WHERE sha256 = ?", (digest,)).fetchone():
            previous = [row for row in saved if row.import_id == digest]
            metadata = connection.execute("SELECT * FROM import_settings WHERE import_id = ?", (digest,)).fetchone()
            same_settings = metadata is None or (metadata["source_namespace"] == source_namespace.strip() and metadata["mapping_json"] == interpretation)
            if not same_settings or not _same_source_rows(previous, transactions):
                connection.execute("RELEASE SAVEPOINT compass_statement_import")
                return ImportResult(count, count, issues=(ImportIssue(None, None, "These file bytes were already imported with a different bank/source or column interpretation. Reuse the original settings; saved records and corrections were not changed."),))
            connection.execute("RELEASE SAVEPOINT compass_statement_import")
            return ImportResult(count, count, duplicate=True, import_id=digest)
        conflicts, uncertain = _check_overlap(saved, transactions, db.list_imports(connection), filename)
        if conflicts or (uncertain and not confirm_distinct):
            connection.execute("RELEASE SAVEPOINT compass_statement_import")
            return ImportResult(count, count, issues=tuple(conflicts or uncertain),
                                review_required=not conflicts and bool(uncertain))
        if uncertain:
            notices = (f"You confirmed {len(uncertain)} overlap/look-alike warning(s) as distinct source activity. All incoming rows were kept; nothing was merged or silently dropped.",)
        db.add_import(connection, digest, filename, digest)
        connection.execute(
            "INSERT INTO import_settings(import_id,source_namespace,mapping_json,confirmed_distinct) VALUES(?,?,?,?)",
            (digest, source_namespace.strip(), interpretation, int(bool(uncertain))),
        )
        for transaction in transactions:
            current_row = transaction.source_row_number
            db.add_transaction(connection, transaction)
        # Reject totals outside the exact money contract before committing.
        saved = db.list_transactions(connection)
        for month in {row.posted_date[:7] for row in saved}:
            summary = summarize_month(saved, month)
            summary.category_totals
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
    return ImportResult(count, count, imported_rows=count, import_id=digest, warnings=notices)


def _same_source_rows(previous: list[Transaction], incoming: list[Transaction]) -> bool:
    fields = ("source_row_number", "account_id", "source_transaction_id", "posted_date", "description", "amount_cents", "original_row_json")
    return (sorted(tuple(getattr(row, name) for name in fields) for row in previous)
            == sorted(tuple(getattr(row, name) for name in fields) for row in incoming))


def _fingerprint(row: Transaction) -> tuple:
    return row.account_id, row.posted_date, " ".join(row.description.casefold().split()), row.amount_cents


def _check_overlap(saved: list[Transaction], incoming: list[Transaction], imports: list[dict], filename: str) -> tuple[list[ImportIssue], list[ImportIssue]]:
    known_ids = {(row.account_id, row.source_transaction_id): row for row in saved if row.source_transaction_id is not None}
    fingerprints = {_fingerprint(row) for row in saved}
    conflicts, uncertain = [], []
    for row in incoming:
        existing = known_ids.get((row.account_id, row.source_transaction_id)) if row.source_transaction_id is not None else None
        if existing is not None:
            same = (existing.posted_date, existing.description, existing.amount_cents) == (row.posted_date, row.description, row.amount_cents)
            reason = "Overlapping statement: this account/source ID is already imported." if same else "Conflicting source ID: its date, description, or amount differs from the saved source."
            conflicts.append(ImportIssue(row.source_row_number, None, reason + " The entire incoming statement is blocked. Review the source file; confirmation cannot overwrite an existing ID."))
        elif _fingerprint(row) in fingerprints:
            uncertain.append(ImportIssue(row.source_row_number, None, "Possible cross-file duplicate: account, date, description and amount match an imported row, but reliable shared IDs are absent or differ. Verify the source; confirm distinct activity only if these are separate transactions."))
    # An edited copy may change IDs and amounts. A reused filename plus an
    # overlapping activity range is a warning, never an automatic merge.
    same_names = {item["id"] for item in imports if item["filename"].casefold() == filename.casefold()}
    old_ranges = {}
    new_ranges = {}
    for row in saved:
        if row.import_id in same_names:
            old_ranges.setdefault((row.import_id, row.account_id), []).append(row.posted_date)
    for row in incoming:
        new_ranges.setdefault(row.account_id, []).append(row.posted_date)
    if any(account in new_ranges and max(min(dates), min(new_ranges[account])) <= min(max(dates), max(new_ranges[account]))
           for (_, account), dates in old_ranges.items()):
        uncertain.append(ImportIssue(None, None, "A statement with this filename and overlapping activity dates already exists for an account. This may be an edited copy. Review the source before confirming distinct activity."))
    return conflicts, uncertain
