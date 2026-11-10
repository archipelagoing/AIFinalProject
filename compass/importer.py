"""Phase 0 CSV format validation; statement ingestion is the next phase."""

import csv
from pathlib import Path

from compass.contracts import parse_amount_cents, validate_posted_date

REQUIRED_COLUMNS = ("date", "description", "amount", "account", "transaction_id")
DEMO_STATEMENTS = (
    "synthetic_checking_2026_Jan-Jun.csv",
    "synthetic_savings_2026_Jan-Jun.csv",
)


def inspect_demo_statement(path: Path) -> dict[str, str | int]:
    """Validate a bundled statement for the setup screen, without importing it."""
    with path.open(encoding="utf-8-sig", newline="") as source:
        reader = csv.DictReader(source, strict=True)
        if reader.fieldnames is None or len(set(reader.fieldnames)) != len(reader.fieldnames) or not set(REQUIRED_COLUMNS).issubset(reader.fieldnames):
            raise ValueError(f"{path.name}: required unique columns are {','.join(REQUIRED_COLUMNS)}")
        count = 0
        for ordinal, row in enumerate(reader, start=2):
            try:
                if None in row or any(row[name] is None for name in REQUIRED_COLUMNS):
                    raise ValueError("Row has an incorrect number of columns.")
                validate_posted_date(row["date"])
                parse_amount_cents(row["amount"])
                if not row["description"].strip() or not row["account"].strip():
                    raise ValueError("Description and account are required.")
                count += 1
            except ValueError as error:
                raise ValueError(f"{path.name}, row {ordinal}: {error}") from error
    if not count:
        raise ValueError(f"{path.name}: no transactions found.")
    return {"Statement": path.name, "Transactions": count, "Data": "Fictional"}
