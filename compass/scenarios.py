"""Exact-cent, pure What If? calculations and conservative historical rent evidence."""

from dataclasses import dataclass
from typing import Literal
import re

from compass.contracts import Transaction, TransactionType, validate_cents


@dataclass(frozen=True, slots=True)
class ScenarioInputs:
    baseline_surplus_cents: int
    new_rent_cents: int
    rent_mode: Literal["replace", "additional"]
    existing_rent_cents: int | None
    added_spending_cents: int = 0
    income_adjustment_cents: int = 0
    savings_target_cents: int | None = None
    starting_balance_cents: int | None = None

    def __post_init__(self) -> None:
        for value in (self.baseline_surplus_cents, self.new_rent_cents, self.added_spending_cents, self.income_adjustment_cents):
            validate_cents(value)
        if self.new_rent_cents < 0 or self.added_spending_cents < 0:
            raise ValueError("New rent and added spending must be nonnegative.")
        if self.rent_mode not in ("replace", "additional"):
            raise ValueError("Choose replace or additional rent.")
        if self.existing_rent_cents is not None:
            validate_cents(self.existing_rent_cents)
            if self.existing_rent_cents < 0:
                raise ValueError("Existing rent cannot be negative.")
        if self.rent_mode == "replace" and self.existing_rent_cents is None:
            raise ValueError("Replacement mode requires confirmed existing rent.")
        if self.savings_target_cents is not None:
            validate_cents(self.savings_target_cents)
            if self.savings_target_cents < 0:
                raise ValueError("Savings target must be nonnegative.")
        if self.starting_balance_cents is not None:
            validate_cents(self.starting_balance_cents)


@dataclass(frozen=True, slots=True)
class RentEvidence:
    candidates: tuple[Transaction, ...]

    @property
    def existing_rent_cents(self) -> int | None:
        return -self.candidates[0].amount_cents if len(self.candidates) == 1 else None


def identify_rent(rows) -> RentEvidence:
    """Never substitute the Housing category total for an identifiable rent charge.

    Explicit Rent/Housing-Rent categories identify rent; broad Housing requires
    the whole word 'rent' in the description. Effective labels govern eligibility.
    Multiple candidates require user confirmation even when their amounts match.
    """
    candidates = []
    for row in rows:
        category = row.effective_category.strip().casefold()
        if (row.effective_type == TransactionType.EXPENSE
                and (category in {"rent", "housing/rent"}
                     or (category == "housing" and re.search(r"\brent\b", row.description, re.I)))):
            candidates.append(row)
    return RentEvidence(tuple(sorted(candidates, key=lambda row: (row.posted_date, row.id))))


@dataclass(frozen=True, slots=True)
class CumulativeMonth:
    month_number: int
    cumulative_change_cents: int
    starting_value_plus_change_cents: int


@dataclass(frozen=True, slots=True)
class ScenarioResult:
    inputs: ScenarioInputs
    rent_delta_cents: int
    projected_surplus_cents: int
    difference_from_baseline_cents: int
    six_month_static_cents: int
    savings_target_gap_cents: int | None
    cumulative_months: tuple[CumulativeMonth, ...]


def calculate_scenario(inputs: ScenarioInputs) -> ScenarioResult:
    """All outputs validated before returning; no DB writes or monetary floats."""
    rent_delta = validate_cents(inputs.new_rent_cents - inputs.existing_rent_cents
                                if inputs.rent_mode == "replace" else inputs.new_rent_cents)
    projected = validate_cents(inputs.baseline_surplus_cents + inputs.income_adjustment_cents
                               - inputs.added_spending_cents - rent_delta)
    difference = validate_cents(projected - inputs.baseline_surplus_cents)
    six_month = validate_cents(6 * projected)
    gap = (None if inputs.savings_target_cents is None
           else validate_cents(projected - inputs.savings_target_cents))
    cumulative = ()
    if inputs.starting_balance_cents is not None:
        cumulative = tuple(CumulativeMonth(number, validate_cents(number * projected),
                            validate_cents(inputs.starting_balance_cents + number * projected))
                           for number in range(1, 7))
    return ScenarioResult(inputs, rent_delta, projected, difference, six_month, gap, cumulative)
