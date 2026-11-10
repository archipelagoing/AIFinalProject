"""Exact accounting contract used by later summaries and financial tools."""

from dataclasses import dataclass
from collections.abc import Iterable
import re

from compass.contracts import Transaction, TransactionType, validate_cents


@dataclass(frozen=True, slots=True)
class Totals:
    income_cents: int = 0
    net_expenses_cents: int = 0
    transfer_net_cents: int = 0
    unknown_net_cents: int = 0

    @property
    def surplus_cents(self) -> int:
        return validate_cents(self.income_cents - self.net_expenses_cents)


def aggregate(transactions: Iterable[Transaction]) -> Totals:
    income = expenses = transfers = unknown = 0
    for transaction in transactions:
        kind, amount = transaction.effective_type, transaction.amount_cents
        if kind == TransactionType.INCOME:
            income = validate_cents(income + amount)
        elif kind in (TransactionType.EXPENSE, TransactionType.REFUND):
            expenses = validate_cents(expenses - amount)
        elif kind == TransactionType.TRANSFER:
            transfers = validate_cents(transfers + amount)
        else:
            unknown = validate_cents(unknown + amount)
    totals = Totals(income, expenses, transfers, unknown)
    validate_cents(totals.surplus_cents)
    return totals


@dataclass(frozen=True, slots=True)
class MonthSummary:
    month: str
    rows: tuple[Transaction, ...]
    totals: Totals
    income_rows: tuple[Transaction, ...]
    expense_rows: tuple[Transaction, ...]
    excluded_rows: tuple[Transaction, ...]

    @property
    def surplus_rows(self) -> tuple[Transaction, ...]:
        return self.income_rows + self.expense_rows


def summarize_month(transactions: Iterable[Transaction], month: str) -> MonthSummary:
    if not re.fullmatch(r"\d{4}-(?:0[1-9]|1[0-2])", month, flags=re.ASCII):
        raise ValueError("Select an imported month in YYYY-MM format.")
    rows = tuple(row for row in transactions if row.posted_date.startswith(month + "-"))
    return MonthSummary(
        month, rows, aggregate(rows),
        tuple(row for row in rows if row.effective_type == TransactionType.INCOME),
        tuple(row for row in rows if row.effective_type in (TransactionType.EXPENSE, TransactionType.REFUND)),
        tuple(row for row in rows if row.effective_type in (TransactionType.TRANSFER, TransactionType.UNKNOWN)),
    )
