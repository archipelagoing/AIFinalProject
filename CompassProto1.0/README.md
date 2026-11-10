# Compass Alpha 0.1

**A private, local-first financial assistant with an inspectable What If? calculator.**

> **Status:** This repository package is a **build specification and synthetic test dataset**, not yet a completed Streamlit app. The commands below work **after** the application and dependency files have been implemented. All bundled financial data is fictional. Compass Alpha is experimental software, not a security-audited banking application or a source of personalized financial advice.

## 1. What exactly is Compass?

Compass preserves the central idea of **Pranav's second proposal**: import downloadable bank statements, normalize and categorize transactions, store them in a **local SQLite database**, and answer questions with a **local small language model** (optional in the first alpha). The one main extension is **What If?**, a deterministic scenario calculator that helps the user understand how a proposed change in income or recurring expenses would affect a historical monthly surplus.

**Promise:** Understand your money. Inspect the calculations. Test a possible next move—on your computer.

**Target user:** A student or early-career person with a downloadable statement who wants to understand spending and explore a rent or other recurring-cost change.

**Core product loop:** `Import → Review → Snapshot → Ask → What If? → Inspect evidence → Correct → Recalculate`.

**Tonight's acceptance story:** A user loads the fictional checking and savings statements, sees the May 2026 financial summary, asks about spending, corrects a category, compares replacement versus additional rent, closes and reopens the app, and sees persisted data.

## 2. Included files

| File | Purpose | Production runtime? |
|---|---|---|
| `SCOPE.md` | Product scope and non-goals | Developer reference |
| `TODO.md` | Prioritized implementation tasks and acceptance tests | Developer reference |
| `synthetic_checking_2026_Jan-Jun.csv` | Fictional checking account statement | Demo input |
| `synthetic_savings_2026_Jan-Jun.csv` | Fictional savings account statement | Demo input |
| `synthetic_ground_truth.csv` | Expected classifications by transaction ID | **Tests only** |
| `expected_monthly_totals.json` | Expected verified monthly totals | **Tests only** |

**Important:** Never use `synthetic_ground_truth.csv` or `expected_monthly_totals.json` to compute user-facing answers. They are independent evaluation oracles, not a shortcut to make the app pass.

## 3. Planned application structure

```text
compass-alpha/
├── app.py                         # Streamlit entry point
├── requirements.txt               # Dependencies (created by implementation)
├── README.md
├── SCOPE.md
├── TODO.md
├── .gitignore
├── compass/
│   ├── __init__.py
│   ├── db.py                       # SQLite schema and queries
│   ├── importer.py                 # CSV validation and normalization
│   ├── classification.py           # Transparent category/type rules
│   ├── analytics.py                # Verified financial aggregation
│   ├── questions.py                # Deterministic financial tools
│   ├── scenarios.py                # Pure What If? calculations
│   └── ollama_adapter.py           # OPTIONAL local intent routing
├── fixtures/
│   ├── synthetic_checking_2026_Jan-Jun.csv
│   ├── synthetic_savings_2026_Jan-Jun.csv
│   ├── synthetic_ground_truth.csv
│   └── expected_monthly_totals.json
├── tests/
│   ├── test_importer.py
│   ├── test_classification.py
│   ├── test_analytics.py
│   ├── test_questions.py
│   ├── test_scenarios.py
│   └── test_persistence.py
└── .local/                          # Ignored app database / uploads, if used
```

The current package keeps the four fixture files alongside this README; the implementer may move/copy them into `fixtures/` and update test paths consistently.

## 4. Installation and local run (once implemented)

Requires **Python 3.11+** and a local machine. No cloud key should be required.

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Tests:

```bash
python -m pytest -q
```

If Ollama is installed, its integration is **optional**. The app must work without it using deterministic question templates and approved calculation tools. Any model calls must be local, validated, and restricted to tool selection/explanation—not monetary arithmetic.

## 5. The synthetic statements and their limits

The package includes **164 fictional transactions** over January–June 2026, across checking and savings. They include payroll, rent, groceries, utilities, phone, insurance, restaurants, subscriptions, transportation, refunds, savings transfers, irregular costs, and an ambiguous ATM withdrawal.

- CSV columns: `date,description,amount,account,transaction_id`.
- Dates: `YYYY-MM-DD`.
- Signed amounts: positive = money entering the account, negative = money leaving.
- A checking-to-savings transfer appears as a negative checking transaction and a positive savings transaction; neither is earned income nor spending.
- The statement data **does not include opening balances**. Therefore Compass cannot calculate the user's actual account balance or available cash on hand from these fixtures.
- June contains an intentionally **unresolved $80 ATM withdrawal**. It must remain visible as unknown and be excluded from *verified* totals until reviewed.
- April includes a **$24.99 grocery refund**, which offsets grocery expense rather than increasing earned income.

### Expected monthly results

| Month | Verified income | Net expenses | Verified surplus |
|---|---:|---:|---:|
| 2026-01 | $3,700.00 | $2,273.84 | $1,426.16 |
| 2026-02 | $3,700.00 | $2,373.11 | $1,326.89 |
| 2026-03 | $3,700.00 | $2,259.09 | $1,440.91 |
| 2026-04 | $3,700.00 | $2,239.12 | $1,460.88 |
| 2026-05 | $3,700.00 | $2,952.94 | $747.06 |
| 2026-06 | $3,925.00 | $2,213.55 | $1,711.45 |

These values are test expectations, not actual balances. **Verified surplus = classified income − classified net expenses**, excluding transfers and unresolved transactions. If a user changes classifications, displayed totals should change accordingly; the fixture expectations only apply to the supplied reference classifications.

## 6. Data and accounting contracts

### Money

Represent all monetary amounts as **integer cents** internally (recommended) or `Decimal` with exact rounding. Do **not** calculate dollars with binary floating point. Display two decimal places with a minus sign for negative values.

### Transaction schema

Minimum normalized fields:

```text
id                  internal unique primary key
account_id          stable local account identity
source_transaction_id   source-provided ID, scoped to account/source
import_id           foreign key to imports table
source_row_number   row ordinal in original file
posted_date         ISO YYYY-MM-DD
description         normalized description
amount_cents        signed integer, immutable source amount
original_row_json   original input values, immutable
predicted_type      income | expense | refund | transfer | unknown
predicted_category  e.g. Housing, Groceries, Restaurants
corrected_type      nullable user override
corrected_category  nullable user override
created_at          import timestamp
```

`effective_type = corrected_type if present else predicted_type`, and similarly for category. Keep source fields immutable. Preserve the original file digest and filename in the `imports` table.

### Accounting classification

| Type | Treatment | Example |
|---|---|---|
| `income` | Positive inflow included in verified income | Payroll |
| `expense` | Negative outflow increases positive expense total | Rent, groceries |
| `refund` | Positive inflow **reduces net expenses** in its category | Grocery refund |
| `transfer` | Excluded from income, expenses and surplus | Checking → savings |
| `unknown` | Excluded from **verified** income/expenses/surplus; shown separately | Ambiguous ATM withdrawal |

A refund must not be counted twice. A transfer between two imported accounts must not be counted as income or spending. If only one side of a transfer is present, flag the evidence as limited rather than assuming an unverified matching account entry. Categorization rules should be transparent and editable.

### Import and duplicate handling

- Reimporting the **same source statement** must not create new transactions.
- Two legitimate transactions with identical date/merchant/amount must both survive.
- Use account-scoped source IDs when reliable, or a file digest plus source row identity when IDs are absent.
- If a file is renamed but contents are identical, recognize the digest. If two statements overlap or source IDs conflict, warn/review rather than silently dropping rows.
- Reject invalid rows with a visible reason. Import must be atomic, or have a clearly documented explicit partial-import mode (atomic is preferred tonight).
- Never use the ground-truth classification CSV in the production classifier.

### Data quality and trust

Show the selected date range, unknown transaction count/value, and potential incomplete-month warnings. Labels such as **Reviewed** mean the user has reviewed classifications; they do **not** imply reconciliation against bank balances. Do not claim bank balance reconciliation without actual balance data.

## 7. Ask Compass — deterministic first

Five supported question intents:

1. `get_income(month)` — verified income and contributing rows.
2. `get_expenses(month)` — net expenses and contributing expenses/refunds.
3. `get_category_spending(month, category)` — net category spending and supporting rows.
4. `get_largest_expenses(month, n)` — sorted expense transactions and amounts.
5. `get_surplus(month)` — verified income less verified net expenses, with exclusions noted.

Example user questions:

- “How much did I earn in May 2026?”
- “What were my expenses in May?”
- “How much did I spend on restaurants in April?”
- “What were my five largest expenses in May?”
- “What was my surplus in June?”

Each answer must display the **period**, **actual calculation**, **source transaction rows**, and any **unknown or incomplete-data warnings**. Unsupported questions should be declined with examples rather than answered by an unconstrained language model.

## 8. What If? engine — exact specification

This is the **signature extension** beyond the original local financial assistant. It is a transparent deterministic scenario calculator, **not** a predictive ML model, a bank balance estimator, or financial advice.

### 8.1 Inputs

| Input | Type | Default / validation |
|---|---|---|
| `baseline_month` | YYYY-MM | Selected imported month; require imported data |
| `new_rent_cents` | integer ≥ 0 | Explicit user input; no hidden assumption |
| `rent_mode` | `replace` or `additional` | User must choose |
| `existing_rent_cents` | integer ≥ 0 | Derived from reviewed historical Housing/Rent expenses; require confirmation if missing or ambiguous |
| `added_spending_cents` | integer ≥ 0 | 0 |
| `income_adjustment_cents` | signed integer | 0; negative means lower income |
| `savings_target_cents` | integer ≥ 0 or null | Optional, P1 |
| `horizon_months` | integer | Fixed 6 for Alpha 0.1 |

**Important:** `existing_rent_cents` represents the **rent expense already included in the historical baseline**, not a hypothetical rent or total Housing category that may include unrelated expenses. If rent cannot be identified unambiguously, do not silently substitute $0 or the full Housing category. Ask for confirmation.

### 8.2 Baseline

From the same verified analytics used by Snapshot:

```text
baseline_income_cents  = sum(positive classified income)
baseline_expense_cents = sum(abs(negative classified expense))
                         - sum(positive classified refunds)
baseline_surplus_cents = baseline_income_cents - baseline_expense_cents
```

Exclude transfers and unknowns. Show any unresolved transaction amounts as separate warnings. If selected month may be incomplete, label results accordingly.

### 8.3 Rent delta

```text
if rent_mode == "replace":
    rent_delta_cents = new_rent_cents - existing_rent_cents
elif rent_mode == "additional":
    rent_delta_cents = new_rent_cents
else:
    raise ValidationError("Choose replace or additional rent")
```

- **Replace**: the new rent takes the place of an already-counted rent payment; only the **difference** changes monthly surplus.
- **Additional**: the new rent is an entirely new recurring expense on top of the baseline; subtract its **full amount**.
- A negative rent delta is allowed for cheaper replacement rent and **increases** surplus.
- Do not subtract existing rent twice. Do not add new rent twice.

### 8.4 Projected monthly surplus

```text
projected_surplus_cents = (
    baseline_surplus_cents
    + income_adjustment_cents
    - added_spending_cents
    - rent_delta_cents
)

change_vs_baseline_cents = projected_surplus_cents - baseline_surplus_cents
static_six_month_surplus_cents = 6 * projected_surplus_cents
```

**Interpretation:** This is an illustrative repeated-month scenario holding all unmodified assumptions constant. It does **not** account for one-time moving costs, security deposits, inflation, income volatility, interest, timing of bills, starting cash balance, or account restrictions. The six-month result is **not** an account balance and is **not** a calibrated forecast.

### 8.5 Exact test cases using May 2026

The fictional May baseline is:

```text
Income                 $3,700.00
Net expenses           $2,952.94
Baseline surplus         $747.06
Existing rent          $1,275.00  (already in expenses)
```

| Scenario | Calculation | Result |
|---|---|---:|
| No change | 747.06 | **$747.06** |
| Replace rent with $1,500 | 747.06 − (1,500 − 1,275) | **$522.06** |
| Add $1,500 rent | 747.06 − 1,500 | **−$752.94** |
| Replace rent with $1,000 | 747.06 − (1,000 − 1,275) | **$1,022.06** |
| Replace with $1,500, add $100 spending, +$200 income | 747.06 + 200 − 100 − 225 | **$622.06** |
| Replace with $1,500, six static months | 6 × 522.06 | **$3,132.36** |
| Add $1,500, six static months | 6 × (−752.94) | **−$4,517.64** |

All results must be computed from imported records and user inputs. The numbers in this table are **tests**, not hard-coded production values.

### 8.6 UI output requirements

Show:

1. Baseline month and coverage/unknown warning.
2. Historical verified income, net expenses, and baseline surplus.
3. Existing rent detected and whether it was user-confirmed.
4. Rent mode and proposed rent.
5. Rent delta, added spending, and income adjustment.
6. Projected monthly surplus and difference from baseline.
7. Six-month static extrapolation with explicit assumptions.
8. Warning when projected monthly surplus is negative; optional savings-target shortfall.
9. A **source details** panel linking baseline values to included transactions.

Do not display a confidence percentage unless supported by a real statistical calibration method. Do not imply the scenario is a recommendation to sign a lease.

### 8.7 Edge cases and failure behavior

| Case | Required behavior |
|---|---|
| Missing rent in replacement mode | Ask for existing rent; no definitive output until confirmed |
| Multiple plausible rent charges | Show candidates and require selection/confirmation |
| Rent becomes cheaper | Negative delta increases surplus |
| Additional mode with existing rent | Both rents count; clearly warn about interpretation |
| Unknown $80 ATM withdrawal | Exclude from verified baseline; show warning |
| Partial historical month | Allow illustrative calculation only with prominent partial-data warning |
| No imported month | Disable scenario, prompt import |
| Invalid/nonfinite input | Reject; never silently coerce |
| Corrections to income/expense/type | Recalculate baseline and scenario from current effective records |
| User enters income adjustment below zero | Subtract income accordingly |
| Repeated Streamlit reruns | No repeated imports or state corruption |

### 8.8 Pure function interface (suggested)

```python
from dataclasses import dataclass
from typing import Literal

@dataclass(frozen=True)
class ScenarioInputs:
    baseline_surplus_cents: int
    new_rent_cents: int
    rent_mode: Literal["replace", "additional"]
    existing_rent_cents: int | None
    added_spending_cents: int = 0
    income_adjustment_cents: int = 0

@dataclass(frozen=True)
class ScenarioResult:
    rent_delta_cents: int
    projected_surplus_cents: int
    change_vs_baseline_cents: int
    six_month_static_surplus_cents: int

# calculate_scenario(inputs: ScenarioInputs) -> ScenarioResult
# This function must not call the LLM or access Streamlit state.
```

Validate `existing_rent_cents` only as required for replacement mode; validate all money types as integer cents. Keep pure calculation independent from database and UI so it can be unit-tested thoroughly.

## 9. Local data, privacy, and deletion

- Store records in a local SQLite file in a clearly documented location (e.g. `.local/compass.db`).
- Never send imported financial rows to remote LLMs, hosted APIs, analytics, or telemetry in Alpha 0.1.
- If Ollama is enabled, connect only to an explicitly local endpoint and document model download behavior separately from inference.
- Do not log full financial statement content or expose it in exception traces.
- Clear-all-data requires confirmation and must delete app-owned imported records and persisted uploaded copies. Bundled fictional fixtures remain intact.
- `.gitignore` must protect local DB files, uploaded personal statements, virtual environments, `.env` files, and caches.
- **Local does not automatically mean secure:** no claims of encryption-at-rest, bank-grade security, or commercial readiness without testing.

## 10. Acceptance checklist and demo

Run `python -m pytest -q` and verify:

- [ ] Fresh app opens locally with empty state and fictional-demo option.
- [ ] Checking and savings CSVs import without losing valid rows.
- [ ] Reimport is idempotent; distinct identical-looking purchases survive.
- [ ] All six expected monthly summaries match **exact cents**.
- [ ] Transfers excluded; April refund offsets expense; June unknown flagged.
- [ ] Five question handlers return correct values with evidence rows.
- [ ] User category/type correction changes summaries and survives restart.
- [ ] May rent **replace** = `$522.06`; **additional** = `−$752.94`.
- [ ] Six-month projection is correct and labeled static.
- [ ] Bad input, missing rent, partial months, and unsupported questions fail safely.
- [ ] Clear-all-data works after restart.
- [ ] No unapproved cloud calls or real bank statement data in source control.

**60–90 second demo script:** Launch → load checking → load savings → select May → show `$747.06` surplus → ask category question and open evidence → correct a transaction and show refresh → What If? replace `$1,275` with `$1,500` → show `$522.06` → toggle additional → show `−$752.94` → restart and confirm persistence.

## 11. Tonight versus later

**P0 tonight:** CSV import, SQLite, review/corrections, accurate monthly summary, deterministic Q&A, transparent What If?, tests, local deletion.

**P1 if time:** Ollama structured routing, arbitrary CSV column mapper, savings target, visual polish.

**Sprint 1 later:** one text-PDF format, robust multi-bank parsing, tested Ollama, saved scenarios and goals.

**Sprint 2 later:** automatic plan re-evaluation after import, improved audit history, forecasting experiments, user research, packaging, security review.

**Non-goals:** Bank synchronization, investment advice, automatic payment initiation, subscription billing, advanced ML forecasts tonight, multi-agent system, general-purpose financial optimization, public upload hosting.

## 12. Codex implementation instruction

Copy this into Codex after opening the folder:

> Read `README.md`, `SCOPE.md`, and `TODO.md` completely. Build a runnable local Streamlit application for Compass Alpha 0.1. Start with the first P0-A vertical slice: import the fictional checking CSV, store transactions in SQLite, and display the correct May 2026 summary. Then add savings transfers, correction persistence, deterministic financial questions, and the exact What If? engine. Implement pure money arithmetic in integer cents. Use `synthetic_ground_truth.csv` and `expected_monthly_totals.json` **only in tests**; never use them to answer the app's financial questions. Do not add cloud services or make Ollama mandatory. After each phase, run tests and mark TODO boxes complete only when their acceptance tests pass. Deliver source files, tests, dependency manifest, and a final report of completed and incomplete P0 items. Do not claim this is a production-secure finance app.

## 13. Team handoff after tonight

| Developer | Responsibility | First deliverable |
|---|---|---|
| Data | CSV import, SQLite, idempotence, source preservation | Import regression suite |
| ML | Categorization, cash-flow baselines, evaluation | Classification error analysis |
| AI | Financial tool routing, optional local LLM, grounded answers | Five reliable Q&A intents |
| Product | Streamlit experience, What If? engine, integration | End-to-end May scenario demo |

**Product direction:** Keep the original private assistant intact. Improve it with inspectable financial calculations and a small, reusable decision-planning experience. Competitive differentiation remains a hypothesis to test, not a proven market advantage.