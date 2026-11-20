# compass/money.py
#
# One place for every money rule in Compass.
# Core idea: floats can't store most decimals exactly (0.1 + 0.2 == 0.30000000000000004),
# so money is stored as INTEGER CENTS ($5.75 -> 575) and any math that needs
# fractions (averages, percentages) uses Decimal, which does exact base-10 math.

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
# dataclass        -> quick way to define the Txn record below
# Decimal          -> exact decimal number type
# ROUND_HALF_UP    -> "school" rounding: .5 always rounds away from zero (2.5 -> 3, -2.5 -> -3)
# InvalidOperation -> error Decimal raises when given text that isn't a number

# Kinds of transaction that count toward spending. Transfers and income never do.
SPENDING_KINDS = ("purchase", "refund")


@dataclass(frozen=True)
class Txn:
    """One transaction, as the money rules see it.

    frozen=True makes it read-only: money code must never change source data.
    """
    id: str
    posted_date: str      # 'YYYY-MM-DD' - ISO text, so string order == date order
    kind: str             # 'purchase' | 'refund' | 'income' | 'transfer'
    amount_cents: int     # signed, bank-style: money out is negative
    currency: str = "USD"


def parse_amount(text: str) -> int:
    """Turn bank text like '-$1,234.56' into signed integer cents (-123456)."""

    # 1. Refuse floats (and anything else that isn't text).
    #    A float like 5.75 may already be slightly wrong in memory,
    #    so we never try to "fix" it - we make the caller pass the original text.
    if not isinstance(text, str):
        raise TypeError("amount must be a string, never a float")

    # 2. Strip formatting a bank export might include:
    #    ' -$1,234.56 '  ->  '-1234.56'
    cleaned = text.replace("$", "").replace(",", "").strip()

    # 3. Convert to an exact Decimal.
    #    Non-numbers like 'abc' or '' raise InvalidOperation; we re-raise as a
    #    clearer ValueError. {text!r} shows the ORIGINAL input with quotes,
    #    so an empty string appears as '' in the message.
    #    'from None' hides the internal InvalidOperation traceback.
    try:
        d = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f"not a number: {text!r}") from None

    # 4. Sanity checks:
    #    - is_finite(): Decimal happily parses 'NaN' and 'Infinity'; neither is money.
    #    - exponent: the number of decimal places, as a negative number.
    #        '5.75'  -> exponent -2  -> OK
    #        '1.005' -> exponent -3  -> rejected (a fraction of a cent would be
    #                                   silently lost in step 5 otherwise)
    if not d.is_finite() or d.as_tuple().exponent < -2:
        raise ValueError(f"invalid amount: {text!r}")

    # 5. Dollars -> cents. Exact, because we know there are at most 2 decimals.
    #    int() turns Decimal('-123456') into the plain integer -123456.
    return int(d * 100)
    # Examples:
    #   parse_amount("-5.75")     -> -575
    #   parse_amount("$1,234.56") -> 123456
    #   parse_amount("1.005")     -> ValueError
    #   parse_amount(5.75)        -> TypeError


def format_cents(cents: int) -> str:
    """Turn integer cents into display text: -575 -> '-$5.75'."""

    # 1. Remember the sign, then work with the positive value.
    sign = "-" if cents < 0 else ""

    # 2. Split into whole dollars and leftover cents in one step.
    #    divmod(575, 100) -> (5, 75)
    dollars, rem = divmod(abs(cents), 100)

    # 3. Build the string:
    #    {dollars:,}  -> thousands separators   (2000 -> '2,000')
    #    {rem:02d}    -> always 2 digits        (5 -> '05', so $0.05 not $0.5)
    #    Pure integer math: no rounding can happen here.
    return f"{sign}${dollars:,}.{rem:02d}"
    # Examples:
    #   format_cents(-575)   -> '-$5.75'
    #   format_cents(200000) -> '$2,000.00'
    #   format_cents(5)      -> '$0.05'


def average_cents(total: int, n: int) -> int | None:
    """Average of n items, rounded to the nearest cent. None if there are no items."""

    # 1. No items -> no average. Returning 0 would falsely claim "$0.00 average",
    #    and returning early also avoids a divide-by-zero crash.
    if n == 0:
        return None

    # 2. Exact division:  Decimal(1000) / 3 -> 333.333...
    # 3. quantize(Decimal(1), ROUND_HALF_UP) -> round to a whole number of cents.
    #    We avoid Python's built-in round(), which uses "banker's rounding":
    #    round(500.5) == 500, which users would see as wrong.
    # 4. int() -> back to a plain integer.
    return int((Decimal(total) / n).quantize(Decimal(1), ROUND_HALF_UP))
    # Examples:
    #   average_cents(1200, 2) -> 600
    #   average_cents(1000, 3) -> 333
    #   average_cents(1001, 2) -> 501   (500.5 rounds up)
    #   average_cents(500, 0)  -> None


def pct_change(old: int, new: int) -> Decimal | None:
    """Percent change from old to new, to 1 decimal place. None if old is zero."""

    # 1. Zero baseline: going from $0 to $30 has no meaningful percentage,
    #    and dividing by zero would crash. None means "no baseline".
    if old == 0:
        return None

    # 2. Formula: (new - old) * 100 / |old|
    #    abs(old) matters when the old period is negative (a net-refund month):
    #    dividing by a negative number would flip the sign and show a rise as a drop.
    # 3. quantize(Decimal("0.1"), ROUND_HALF_UP) -> round to one decimal place.
    #    Returned as Decimal, not float - send it to the frontend as a string ("-50.0").
    return (Decimal(new - old) * 100 / abs(old)).quantize(Decimal("0.1"), ROUND_HALF_UP)
    # Examples:
    #   pct_change(1200, 600)  -> Decimal('-50.0')
    #   pct_change(1000, 1333) -> Decimal('33.3')
    #   pct_change(0, 3000)    -> None


def spending_cents(txns) -> int:
    """Total spending as a POSITIVE number of cents.

    Each txn needs .amount_cents (signed, bank-style: purchases negative,
    refunds positive) and .kind ('purchase', 'refund', 'income' or 'transfer').
    Note: sqlite3.Row uses t["amount_cents"], not t.amount_cents - convert rows
    to objects/dataclasses first, or switch this to dict-style access.
    """

    # 1. Keep only purchases and refunds; transfers and income are NOT spending.
    # 2. Sum them: purchases (negative) and refunds (positive) net out naturally.
    #      -575 - 625 - 4000 + 1500 = -3700
    # 3. Negate: -3700 -> 3700, because users expect "you spent $37.00".
    #    The (... for t in txns ...) is a generator expression: values are added
    #    one at a time without building a list in memory first.
    return -sum(t.amount_cents for t in txns if t.kind in SPENDING_KINDS)


def excluded_from_spending(txns) -> list[str]:
    """IDs of transactions left out of spending (transfers, income).

    Every total must be able to disclose what it excluded, so this list
    travels with the number to the UI and the X-Ray panel.
    """
    return [t.id for t in txns if t.kind not in SPENDING_KINDS]


def spending_label(cents: int) -> str:
    """Human label for a spending total.

    A period where refunds outweigh purchases has negative spending.
    Show it as a 'net refund' instead of a confusing '-$15.00 spent'.
    """
    if cents < 0:
        return f"net refund {format_cents(-cents)}"
    return f"{format_cents(cents)} spent"
    # Examples:
    #   spending_label(3700)  -> '$37.00 spent'
    #   spending_label(-1500) -> 'net refund $15.00'


def net_cash_flow_cents(txns) -> int:
    """Net recorded cash flow: income + purchases + refunds, transfers excluded.

    Transfers move money between YOUR OWN accounts, so they are neither
    money in nor money out. 'Recorded' = only what is in the data; nothing estimated.
    """
    return sum(t.amount_cents for t in txns if t.kind != "transfer")


def in_period(posted_date: str, start: str, end: str) -> bool:
    """Half-open period [start, end): start is included, end is NOT.

    So October is in_period(d, '2026-10-01', '2026-11-01') and a
    transaction on Nov 1 belongs to November only - never counted twice.
    """
    return start <= posted_date < end


def spending_by_currency(txns) -> dict[str, int]:
    """Spending per currency. Never adds dollars to euros.

    More than one key in the result means mixed currencies:
    the caller must show separate totals and a warning.
    """
    totals: dict[str, int] = {}
    for t in txns:
        if t.kind in SPENDING_KINDS:
            totals[t.currency] = totals.get(t.currency, 0) - t.amount_cents
    return totals