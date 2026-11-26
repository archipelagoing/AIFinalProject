"""Exact accounting contract used by later summaries and financial tools."""

from dataclasses import dataclass
from collections.abc import Iterable
import re

from compass.contracts import Transaction, TransactionType, validate_cents
from compass.charts import ChartRow, bar_chart, heatmap_chart, slope_chart


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
    gross_expenses = refunds = unknown_absolute = transfer_absolute = 0
    for transaction in transactions:
        kind, amount = transaction.effective_type, transaction.amount_cents
        if kind == TransactionType.INCOME:
            income = validate_cents(income + amount)
        elif kind in (TransactionType.EXPENSE, TransactionType.REFUND):
            if kind == TransactionType.EXPENSE:
                gross_expenses = validate_cents(gross_expenses - amount)
            else:
                refunds = validate_cents(refunds + amount)
            expenses = validate_cents(expenses - amount)
        elif kind == TransactionType.TRANSFER:
            transfers = validate_cents(transfers + amount)
            transfer_absolute = validate_cents(transfer_absolute + abs(amount))
        else:
            unknown = validate_cents(unknown + amount)
            unknown_absolute = validate_cents(unknown_absolute + abs(amount))
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

    @property
    def category_totals(self) -> dict[str, int]:
        totals = {}
        for row in self.expense_rows:
            totals[row.effective_category] = validate_cents(totals.get(row.effective_category, 0) - row.amount_cents)
        return dict(sorted(totals.items()))


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


def category_bar_chart(summary: MonthSummary):
    """Category bars reconcile to eligible expense/refund rows in the summary."""
    return bar_chart((ChartRow(category, cents, "Net expenses minus refunds")
                      for category, cents in summary.category_totals.items()),
                     exclusions=_chart_exclusions(summary))


def daily_heatmap(summary: MonthSummary):
    """Daily net expense cells; only days with eligible source transactions appear."""
    totals: dict[str, int] = {}
    for row in summary.expense_rows:
        totals[row.posted_date] = validate_cents(totals.get(row.posted_date, 0) - row.amount_cents)
    return heatmap_chart((ChartRow(day, cents, "Net eligible expenses and refunds")
                          for day, cents in totals.items()), exclusions=_chart_exclusions(summary))


def monthly_surplus_slope(transactions: Iterable[Transaction], months: Iterable[str]):
    """Compare explicit imported months; a month without rows is rejected, not guessed."""
    rows = tuple(transactions)
    selected = tuple(months)
    if len(selected) < 2 or len(set(selected)) != len(selected):
        raise ValueError("Choose at least two distinct imported months for a slope chart.")
    summaries = [summarize_month(rows, month) for month in selected]
    if any(not summary.rows for summary in summaries):
        raise ValueError("Every comparison month must contain imported activity.")
    exclusions = tuple(sorted({item for summary in summaries for item in _chart_exclusions(summary)}))
    return slope_chart((ChartRow(summary.month, summary.totals.surplus_cents,
                                 "Classified income minus net expenses") for summary in summaries),
                       exclusions=exclusions)


def _chart_exclusions(summary: MonthSummary) -> tuple[str, ...]:
    excluded = []
    transfers = sum(row.effective_type == TransactionType.TRANSFER for row in summary.excluded_rows)
    unknown = sum(row.effective_type == TransactionType.UNKNOWN for row in summary.excluded_rows)
    if transfers:
        excluded.append(f"{transfers} transfer transaction(s) excluded")
    if unknown:
        excluded.append(f"{unknown} unresolved transaction(s) excluded")
    return tuple(excluded)


@dataclass(frozen=True, slots=True)
class DataQuality:
    reviewed_rows: int
    unreviewed_rows: int
    unknown_absolute_cents: int
    unknown_outflow_cents: int
    unknown_inflow_cents: int
    covered_start: str | None
    covered_end: str | None


def data_quality(summary: MonthSummary) -> DataQuality:
    """Review means a saved classification override, never balance reconciliation."""
    reviewed = sum(row.has_correction for row in summary.rows)
    unknown = [row for row in summary.rows if row.effective_type == TransactionType.UNKNOWN]
    dates = sorted(row.posted_date for row in summary.rows)
    return DataQuality(reviewed, len(summary.rows) - reviewed,
                       validate_cents(sum(abs(row.amount_cents) for row in unknown)),
                       validate_cents(sum(-row.amount_cents for row in unknown if row.amount_cents < 0)),
                       validate_cents(sum(row.amount_cents for row in unknown if row.amount_cents > 0)),
                       dates[0] if dates else None, dates[-1] if dates else None)


@dataclass(frozen=True, slots=True)
class TransferEvidence:
    pairs: tuple[tuple[Transaction, Transaction], ...]
    unmatched: tuple[Transaction, ...]


def reconcile_transfers(transactions: Iterable[Transaction]) -> TransferEvidence:
    """Only pair unique same-date opposite amounts across distinct accounts.

    A zero net alone is not evidence of pairing. Ambiguous groups stay visible.
    """
    groups = {}
    for row in transactions:
        if row.effective_type == TransactionType.TRANSFER:
            groups.setdefault((row.posted_date, abs(row.amount_cents)), []).append(row)
    pairs, unmatched = [], []
    for group in groups.values():
        if (len(group) == 2 and group[0].amount_cents != 0
                and group[0].account_id != group[1].account_id
                and group[0].amount_cents + group[1].amount_cents == 0):
            pairs.append(tuple(group))
        else:
            unmatched.extend(group)
    return TransferEvidence(tuple(pairs), tuple(unmatched))
