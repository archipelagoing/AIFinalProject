"""Canonical source record, money, date, and classification contracts."""

from dataclasses import dataclass, field, replace
from datetime import date, datetime, timezone
from enum import Enum
import json
import re


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"
    REFUND = "refund"
    TRANSFER = "transfer"
    UNKNOWN = "unknown"


def validate_cents(value: int) -> int:
    """Reject floats, booleans, and integers outside SQLite's signed range."""
    if type(value) is not int:
        raise ValueError("Money must be integer cents, never float or bool.")
    if not -(2**63) <= value < 2**63:
        raise ValueError("Money exceeds SQLite's signed 64-bit integer range.")
    return value


def parse_amount_cents(value: str) -> int:
    if not isinstance(value, str) or not re.fullmatch(r"[+-]?\d+(?:\.\d{1,2})?", value.strip(), flags=re.ASCII):
        raise ValueError("Use a signed decimal such as -1275.00, with at most two decimal places.")
    value = value.strip()
    whole, _, fraction = value.lstrip("+-").partition(".")
    # Bound input length before int conversion; leading zeros do not affect value.
    whole = whole.lstrip("0") or "0"
    if len(whole) > 17:
        raise ValueError("Amount is too large.")
    cents = int(whole) * 100 + int(fraction.ljust(2, "0") or "0")
    return validate_cents(-cents if value.startswith("-") else cents)


def validate_posted_date(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value, flags=re.ASCII):
        raise ValueError("Date must be ISO YYYY-MM-DD.")
    date.fromisoformat(value)
    return value


def format_money(cents: int) -> str:
    validate_cents(cents)
    whole, fraction = divmod(abs(cents), 100)
    return f"{'−' if cents < 0 else ''}${whole:,}.{fraction:02d}"


def validate_classification(kind: TransactionType | str, category: str, amount_cents: int) -> TransactionType:
    kind = TransactionType(kind)
    validate_cents(amount_cents)
    if not isinstance(category, str) or not category.strip() or len(category) > 80:
        raise ValueError("Category must contain 1–80 characters.")
    if kind in (TransactionType.INCOME, TransactionType.REFUND) and amount_cents <= 0:
        raise ValueError("Income and refunds require positive source amounts.")
    if kind == TransactionType.EXPENSE and amount_cents >= 0:
        raise ValueError("Expenses require negative source amounts.")
    return kind


@dataclass(frozen=True, slots=True)
class Transaction:
    id: str
    account_id: str
    source_transaction_id: str | None
    import_id: str
    source_row_number: int
    posted_date: str
    description: str
    amount_cents: int
    original_row_json: str
    predicted_type: TransactionType = TransactionType.UNKNOWN
    predicted_category: str = "Uncategorized"
    corrected_type: TransactionType | None = None
    corrected_category: str | None = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        for name in ("id", "account_id", "import_id", "description"):
            value = getattr(self, name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string.")
        if self.source_transaction_id is not None and (not isinstance(self.source_transaction_id, str) or not self.source_transaction_id.strip()):
            raise ValueError("Source ID must be nonempty or None.")
        if type(self.source_row_number) is not int or self.source_row_number < 1:
            raise ValueError("Source row number must be a positive integer.")
        validate_posted_date(self.posted_date)
        validate_cents(self.amount_cents)
        if not isinstance(self.original_row_json, str) or not isinstance(json.loads(self.original_row_json), dict):
            raise ValueError("Original source values must be a JSON object string.")
        timestamp = datetime.fromisoformat(self.created_at)
        if timestamp.tzinfo is None:
            raise ValueError("Import timestamp must include a timezone.")
        object.__setattr__(self, "predicted_type", validate_classification(self.predicted_type, self.predicted_category, self.amount_cents))
        if self.corrected_type is not None:
            object.__setattr__(self, "corrected_type", TransactionType(self.corrected_type))
        validate_classification(self.effective_type, self.effective_category, self.amount_cents)

    @property
    def effective_type(self) -> TransactionType:
        return self.corrected_type if self.corrected_type is not None else self.predicted_type

    @property
    def effective_category(self) -> str:
        return self.corrected_category if self.corrected_category is not None else self.predicted_category

    @property
    def original_row(self) -> dict:
        """Return a fresh copy so nested edits cannot mutate preserved source JSON."""
        return json.loads(self.original_row_json)

    @property
    def has_correction(self) -> bool:
        return self.corrected_type is not None or self.corrected_category is not None

    def with_classification(self, kind: TransactionType | str, category: str) -> "Transaction":
        kind = validate_classification(kind, category, self.amount_cents)
        return replace(self, corrected_type=kind, corrected_category=category.strip())
