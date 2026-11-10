"""Scenario input contract. Calculation/UI integration is scheduled for Phase 4."""

from dataclasses import dataclass
from typing import Literal

from compass.contracts import validate_cents


@dataclass(frozen=True, slots=True)
class ScenarioInputs:
    baseline_surplus_cents: int
    new_rent_cents: int
    rent_mode: Literal["replace", "additional"]
    existing_rent_cents: int | None
    added_spending_cents: int = 0
    income_adjustment_cents: int = 0

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
