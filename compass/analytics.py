"""Exact accounting contract used by later summaries and financial tools."""

from dataclasses import dataclass
from collections.abc import Iterable

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
