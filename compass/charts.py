"""Deterministic, accessible chart data built from verified Compass values.

Chart payloads keep the exact values and a complete table representation together.
Renderers must use the supplied domain (including zero) and labels rather than
silently rescaling or inferring missing values.
"""

from dataclasses import dataclass
from typing import Literal

from compass.contracts import validate_cents


@dataclass(frozen=True, slots=True)
class ChartRow:
    label: str
    value_cents: int
    detail: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.label, str) or not self.label.strip():
            raise ValueError("Chart labels must be nonempty.")
        validate_cents(self.value_cents)


@dataclass(frozen=True, slots=True)
class Chart:
    kind: Literal["bar", "heatmap", "slope", "guess_actual"]
    title: str
    description: str
    rows: tuple[ChartRow, ...]
    value_label: str = "Amount (cents)"
    minimum_cents: int | None = None
    maximum_cents: int | None = None
    exclusions: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in {"bar", "heatmap", "slope", "guess_actual"}:
            raise ValueError("Unsupported chart type.")
        if not self.title.strip() or not self.description.strip():
            raise ValueError("Charts require a title and accessible description.")
        if not self.rows:
            raise ValueError("A chart needs at least one data row.")
        labels = [row.label for row in self.rows]
        if len(labels) != len(set(labels)):
            raise ValueError("Chart row labels must be unique.")
        for value in (self.minimum_cents, self.maximum_cents):
            if value is not None:
                validate_cents(value)
        low = min(0, *(row.value_cents for row in self.rows))
        high = max(0, *(row.value_cents for row in self.rows))
        if self.minimum_cents is not None and self.minimum_cents > low:
            raise ValueError("Chart minimum must include zero and every value.")
        if self.maximum_cents is not None and self.maximum_cents < high:
            raise ValueError("Chart maximum must include zero and every value.")


def _chart(kind, title, description, rows, *, value_label="Amount (cents)", exclusions=()):
    rows = tuple(rows)
    if not rows:
        return None
    # Domain always includes zero, so negative values and baselines are not clipped.
    return Chart(kind, title, description, rows, value_label,
                 min(0, *(r.value_cents for r in rows)),
                 max(0, *(r.value_cents for r in rows)), tuple(exclusions))


def bar_chart(rows, title="Spending by category", exclusions=()):
    """Ranked exact-cent bars. Negative net-refund categories remain visible."""
    return _chart("bar", title, "Ranked values in cents; the axis includes zero.",
                  sorted(rows, key=lambda row: (-row.value_cents, row.label.casefold())), exclusions=exclusions)


def heatmap_chart(rows, title="Daily spending", exclusions=()):
    """Daily values; callers supply only days with source activity."""
    return _chart("heatmap", title, "Daily values in cents; blank days mean no included source rows.",
                  sorted(rows, key=lambda row: row.label), exclusions=exclusions)


def slope_chart(rows, title="Monthly comparison", exclusions=()):
    """Ordered period values; zero values must be explicit rows, never missing data."""
    return _chart("slope", title, "Ordered period values in cents; zero baseline shown.", rows, exclusions=exclusions)


def guess_actual_chart(guess_cents: int, actual_cents: int, *, actual_label="Actual", exclusions=()):
    """Compare a user-entered guess with deterministic actual, without estimating either."""
    validate_cents(guess_cents)
    validate_cents(actual_cents)
    return _chart("guess_actual", "Your guess and actual", "User estimate compared with transaction-derived actual; zero baseline shown.",
                  (ChartRow("Your guess", guess_cents), ChartRow(actual_label, actual_cents)), exclusions=exclusions)
