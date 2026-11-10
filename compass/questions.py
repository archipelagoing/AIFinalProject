"""Bounded questions and evidence-bearing tools; all arithmetic is integer cents."""

import calendar
from dataclasses import dataclass
import re

from compass.analytics import summarize_month
from compass.contracts import Transaction, TransactionType as Kind, format_money, validate_cents

SUPPORTED_INTENTS = (
    "get_income", "get_expenses", "get_category_spending",
    "get_largest_expenses", "get_surplus",
)

EXAMPLES = (
    "What was my income in May 2026?",
    "What were my expenses in May 2026?",
    "How much did I spend on Groceries in April 2026?",
    "Show my top 3 expenses in May 2026",
    "What was my surplus in June 2026?",
)


@dataclass(frozen=True, slots=True)
class Request:
    tool: str
    month: str
    category: str | None = None
    limit: int = 5


@dataclass(frozen=True, slots=True)
class Answer:
    request: Request
    amount_cents: int
    start_date: str
    end_date: str
    covered_start: str
    covered_end: str
    included_rows: tuple[Transaction, ...]
    excluded_rows: tuple[Transaction, ...]
    formula: str


def _answer(transactions, request: Request) -> Answer:
    if request.tool not in SUPPORTED_INTENTS:
        raise ValueError("Choose one of the five supported tools.")
    if type(request.limit) is not int or not 1 <= request.limit <= 20:
        raise ValueError("Largest-expense count must be an integer from 1 to 20.")
    summary = summarize_month(transactions, request.month)
    if not summary.rows:
        raise ValueError("That month has no imported activity. Select an imported month.")
    if request.tool != "get_category_spending" and request.category is not None:
        raise ValueError("Category filters are supported only by category spending.")
    if request.tool == "get_income":
        included, amount, formula = summary.income_rows, summary.totals.income_cents, "Sum of classified income"
    elif request.tool == "get_expenses":
        included, amount, formula = summary.expense_rows, summary.totals.net_expenses_cents, "Expense outflows − refunds"
    elif request.tool == "get_surplus":
        included, amount, formula = summary.surplus_rows, summary.totals.surplus_cents, "Classified income − net expenses"
    elif request.tool == "get_category_spending":
        if request.category not in {row.effective_category for row in summary.rows}:
            raise ValueError("Choose an exact category present in this month.")
        included = tuple(row for row in summary.expense_rows if row.effective_category == request.category)
        amount = validate_cents(sum(-row.amount_cents for row in included))
        formula = "Category expense outflows − category refunds"
    else:
        included = tuple(sorted(
            (row for row in summary.expense_rows if row.effective_type == Kind.EXPENSE),
            key=lambda row: (row.amount_cents, row.posted_date, row.id),
        )[:request.limit])
        amount = validate_cents(sum(-row.amount_cents for row in included))
        formula = "Sum of listed largest expense outflows; refunds excluded from ranking"
    if request.tool in {"get_expenses", "get_category_spending"}:
        gross = sum(-row.amount_cents for row in included if row.effective_type == Kind.EXPENSE)
        refunds = sum(row.amount_cents for row in included if row.effective_type == Kind.REFUND)
        formula += f": {format_money(gross)} − {format_money(refunds)}"
    elif request.tool == "get_surplus":
        formula += f": {format_money(summary.totals.income_cents)} − {format_money(summary.totals.net_expenses_cents)}"
    year, month = map(int, request.month.split("-"))
    dates = sorted(row.posted_date for row in summary.rows)
    return Answer(request, amount, request.month + "-01",
                  f"{request.month}-{calendar.monthrange(year, month)[1]:02}",
                  dates[0], dates[-1], included, summary.excluded_rows, formula)


def get_income(transactions, month: str) -> Answer:
    return _answer(transactions, Request("get_income", month))


def get_expenses(transactions, month: str) -> Answer:
    return _answer(transactions, Request("get_expenses", month))


def get_category_spending(transactions, month: str, category: str) -> Answer:
    return _answer(transactions, Request("get_category_spending", month, category))


def get_largest_expenses(transactions, month: str, limit: int = 5) -> Answer:
    return _answer(transactions, Request("get_largest_expenses", month, limit=limit))


def get_surplus(transactions, month: str) -> Answer:
    return _answer(transactions, Request("get_surplus", month))


def execute(transactions, request: Request) -> Answer:
    """Fixed dispatch; model text never becomes code, SQL, or a monetary result."""
    if request.tool not in SUPPORTED_INTENTS:
        raise ValueError("Unsupported tool.")
    return _answer(transactions, request)


def parse_question(question: str, transactions, selected_month: str) -> Request:
    """Match complete phrases, so trailing filters cannot be silently discarded."""
    if not isinstance(question, str) or not 1 <= len(question.strip()) <= 500:
        raise ValueError("Enter a question of 1–500 characters.")
    rows = tuple(transactions)
    text = " ".join(question.casefold().strip().rstrip("?.!").split())
    month = selected_month
    suffix = re.search(r"(?: in| for)? (\d{4}-(?:0[1-9]|1[0-2]))$", text)
    if suffix:
        month = suffix[1]
        text = text[:suffix.start()]
    else:
        names = "|".join(calendar.month_name[1:]).lower()
        suffix = re.search(rf"(?: in| for)? ({names})(?: (\d{{4}}))?$", text)
        if suffix:
            number = list(name.casefold() for name in calendar.month_name).index(suffix[1])
            candidates = sorted({row.posted_date[:7] for row in rows
                                 if int(row.posted_date[5:7]) == number})
            if suffix[2]:
                month = f"{suffix[2]}-{number:02}"
            elif len(candidates) == 1:
                month = candidates[0]
            else:
                raise ValueError("Please specify the year as well as the month.")
            text = text[:suffix.start()]
    if month not in {row.posted_date[:7] for row in rows}:
        raise ValueError("That month has no imported activity. Select an imported month.")
    text = re.sub(r"^(?:please )?(?:what (?:was|were|is|are) (?:my |the )?|show (?:me )?(?:my |the )?|how much (?:did i |was )?)", "", text)
    text = re.sub(r"^my ", "", text)
    if text in {"income", "earn", "earned", "total income"}:
        return Request("get_income", month)
    if text in {"expenses", "net expenses", "total expenses", "spend", "spending"}:
        return Request("get_expenses", month)
    if text in {"surplus", "verified surplus", "left over"}:
        return Request("get_surplus", month)
    largest = re.fullmatch(r"(?:top (\d{1,2})|largest|biggest)(?: expenses| expense)(?: (\d{1,2}))?", text)
    if largest:
        if largest[1] and largest[2]:
            raise ValueError("Specify one largest-expense count.")
        limit = int(largest[1] or largest[2] or 5)
        if not 1 <= limit <= 20:
            raise ValueError("Choose 1–20 largest expenses.")
        return Request("get_largest_expenses", month, limit=limit)
    category = re.fullmatch(r"(?:spend on|spending on|spending for|category spending for) (.+)", text)
    if category:
        matches = {row.effective_category for row in rows
                   if row.posted_date.startswith(month + "-")
                   and row.effective_category.casefold() == category[1]}
        if len(matches) == 1:
            return Request("get_category_spending", month, next(iter(matches)))
        raise ValueError("Please use an exact category from this month's category table.")
    raise ValueError("Please ask one supported question for one month. Account filters, date ranges, comparisons, forecasts and bank balances are not supported yet.")
