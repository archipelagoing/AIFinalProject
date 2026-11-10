# Phase 4 — What If? engine

Implemented on 2026-11-10 in the root Python/Streamlit application. All eight P0 items and both optional P1 features are implemented and covered by acceptance tests. Run `streamlit run app.py` after installing requirements and load both fictional statements. This Python app runs locally; GitHub Pages continues serving the separate JavaScript prototype.

## Try the May acceptance story

Open **What If?** and choose May 2026 as **Scenario baseline month**. The baseline uses `analytics.summarize_month`, exactly like the snapshot: $3,700.00 classified income, $2,952.94 net expenses, and $747.06 verified surplus. The scenario month selector is independent of the snapshot selector; it initially follows the selected snapshot month. Baseline source rows and activity coverage remain visible.

The proposed rent input initially shows `1500.00`; explicitly choose a rent mode to calculate. With no income or spending adjustment:

| Mode | Existing rent in baseline | Rent delta | Monthly surplus | Six-month static extrapolation |
| --- | ---: | ---: | ---: | ---: |
| Replace | $1,275.00 | $225.00 | $522.06 | $3,132.36 |
| Additional | $1,275.00 remains | $1,500.00 | −$752.94 | −$4,517.64 |

Cheaper replacement rent of $1,000.00 gives a −$275.00 rent delta and $1,022.06 monthly surplus. Additional mode subtracts all proposed rent while retaining historical rent in baseline expenses.

## Exact inputs and rent evidence

`compass/scenarios.py` separates immutable inputs, pure calculation, and historical rent evidence. Dollar text uses the shared exact parser and becomes signed integer cents, never floating-point money. Rent, added spending, confirmed existing rent, and optional savings target must be nonnegative. Income adjustment and an explicitly supplied starting balance can be signed. Empty/malformed values, NaN/infinity, currency/grouping/exponent syntax, fractional cents, booleans/floats passed to the pure API, invalid modes, and signed-64-bit output overflow are rejected. Invalid input hides the prior scenario result while leaving the historical snapshot available.

Rent identification considers only effective expense rows. An explicit `Rent` or `Housing/Rent` category identifies a candidate; broad `Housing` additionally requires the whole word `rent` in the description. Other Housing costs, refunds, transfers, and unknowns are not silently substituted as rent. The evidence table retains source IDs/rows/import hashes.

A single qualifying expense supplies the existing rent. With no candidates or multiple candidates, replacement is blocked until the user enters and confirms the rent expense already counted in the selected baseline. Split/repeated payments are not automatically summed. A user can also choose to confirm a different amount when there is one candidate. Confirmation of zero is allowed only as an explicit user assertion; missing data never silently becomes zero. Confirmed rent cannot exceed all expense outflows in that baseline. Confirmation is tied to the month, entered amount, and current baseline records/effective classifications; changing that context requires confirmation again. Additional mode does not require identified existing rent.

## Formulas and assumptions

The rendered result displays baseline income/expenses/surplus, existing rent and whether it was user-confirmed, proposed rent, mode, income adjustment, added spending, rent delta, complete numeric formula, projected surplus, and difference from baseline:

```text
replace:    rent_delta = new_rent − existing_rent
additional: rent_delta = new_rent
projected_surplus = baseline_surplus + income_adjustment − added_spending − rent_delta
difference_from_baseline = projected_surplus − baseline_surplus
six_month_static = 6 × projected_surplus
```

Every rerun derives the baseline from current effective transactions. Corrections, imports, month changes and reimports recalculate without changing the stored transactions. Imports/corrections retain existing persistence across restart; hypothetical inputs are session controls, not saved scenarios. The baseline is classified activity, not bank-balance reconciliation.

Negative projected surplus has a visible warning. Unknown value stays excluded with a separate notice. Full statement coverage remains unverified, so every scenario warns of partial coverage and a possibly atypical historical month. The six-month result repeats identical monthly income/expenses; it is explicitly a static extrapolation, not an account balance or statistically validated forecast. It omits moving costs, deposits, bill timing, inflation, interest and income volatility. No available-cash claim is made.

## Optional savings target and starting balance

**Compare a monthly savings target** shows `projected_surplus − target` and whether the target is met under the assumptions. The target is a comparison only; it is not deducted again as an expense and does not establish that funds are available.

**Show six months from a user-supplied starting balance** requires an explicit valid value. Without one, no cumulative table is produced. Exactly six rows show month number, `month_number × projected_surplus`, and `user_starting_value + cumulative_change`. Starting values never come from statement net activity. The UI labels these as illustrative arithmetic and unverified balances. This table does not change the separate six-month change metric.

## Verification and remaining work

Verified **265 Python tests**, including **50 Phase 4 cases**, **17 JavaScript tests**, the independent fixture audit, and dependency validation. Run `python -m pytest -q`, `npm test`, `python scripts/audit_fixtures.py`, and `python -m pip check` with the virtual environment active.

Tests cover all-month baseline consistency, exact May results and signed adjustments, cheaper/zero/additional rent, strict input types/nonfinite values and overflow, rent evidence and effective overrides, ambiguous/missing-rent confirmation and invalidation, baseline/source immutability, targets, cumulative arithmetic, and Streamlit edits/month changes/reimport/fresh-session behavior. Streamlit AppTest exercises rendered controls and real handlers. A native-browser walkthrough was not performed for this phase.

Phase 5 release/privacy work remains, including confirmed local-data deletion and a broader release smoke test. Saved scenarios, automatic rent schedule inference, account-balance reconciliation, and statistical forecasting remain outside this implementation.
