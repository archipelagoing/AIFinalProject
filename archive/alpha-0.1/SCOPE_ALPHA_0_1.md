# Compass Alpha 0.1 — Product Scope and Build Contract

**Status:** Tonight's runnable local prototype specification  
**Timebox:** 3–5 focused hours (estimate, not guarantee)  
**Team:** Initially one builder; designed for four-developer expansion  
**Source idea:** Pranav's second proposal: privacy-first statement importer, SQLite financial records, local small language model, and conversational analysis.

## 1. What Compass is

Compass is a **local-first personal financial assistant**. A person imports a supported bank-statement CSV, checks how the transactions were interpreted, sees accurate monthly financial summaries, asks common questions about spending, and models a hypothetical change to income or expenses. The only new product capability beyond the original assistant is a small **What If?** calculator. The local language model is optional tonight; financial arithmetic never depends on generated text.

**Product promise:** “Understand your money, inspect the numbers, and test your next move—on your own computer.”

**Not the promise:** autonomous financial advice, bank synchronization, investment recommendations, guaranteed forecasts, or production-grade bank security.

## 2. Target user and job to be done

A student or early-career adult with downloadable bank statements who wants to answer: “Where did my money go, and how would a new recurring expense affect my monthly cash flow?”

**Tonight's hero journey:**
1. Open Streamlit locally.
2. Load the included fictional checking statement (and optionally savings statement).
3. Confirm date, description, amount, and account columns.
4. Review categorized transactions and monthly summary.
5. Ask “How much did I spend on restaurants in May 2026?” and inspect the matching rows.
6. Correct one category; see summaries update.
7. Enter a proposed new monthly rent, specifying whether it **replaces existing rent** or is **additional**.
8. View projected monthly surplus and six-month linear projection, with assumptions shown.
9. Restart the app; imported transactions persist in local SQLite.

## 3. User-visible modules

### A. Import & review
- CSV uploader, with date/description/amount/account mapping for the bundled format.
- Supports signed amount convention: positive inflows, negative outflows. If a different CSV format is ambiguous, require mapping instead of guessing.
- Show file-level import count, rejected rows, and duplicates.
- Show editable category and transaction type; default ambiguous entries to **Needs review**.
- Store original values alongside normalized values.

### B. Snapshot
- Month selector; income, net expenses, and surplus.
- Spending by category and a searchable/filterable transaction table.
- Transfers between own accounts excluded from both income and expense.
- Refunds offset the original expense category rather than count as wages.
- Warnings for incomplete data, uncertain transaction types, and partial months.

### C. Ask Compass
- A chat-like input supporting **five deterministic intents**: monthly income, monthly expenses, spending by category, largest expenses, and monthly surplus.
- Answers must include date range and transaction evidence; unknown questions get a supported-question suggestion.
- Optional Ollama adapter for intent extraction and wording; never let it compute or invent dollar amounts. If Ollama is absent, deterministic routing still works.

### D. What If?
- User inputs: baseline month, proposed rent, **replace vs add**, extra monthly expenses, optional monthly income change, and optional savings target.
- Calculate: projected monthly surplus = historical income − historical net expenses + adjustments. Replacing rent requires identifying existing rent; if unknown, ask the user to supply it rather than silently subtracting it.
- Six-month projection = six × monthly surplus **only as a static illustrative estimate**; not a forecast with validated uncertainty.
- Show baseline vs proposed and the arithmetic; flag negative surplus or missed savings target.

## 4. Data contract

**Normalized transaction:** `transaction_id`, `date` (ISO), `description`, `amount` (signed decimal), `account`, `category`, `transaction_type` (`income|expense|refund|transfer|unknown`), `source_file`, `import_batch`, `original_row_json`, `user_edited`.

**SQLite tables (minimum):** `imports`, `transactions`; optional `scenario_runs` if time remains. Use `Decimal` or integer cents for money. Do not use binary floating point for production arithmetic.

**Duplicate policy:** identical re-import of a file must not create new rows; distinct transactions with same date/merchant/amount must not be silently merged. Prefer stable source transaction IDs when provided; otherwise use a source-file/row identity and flag cross-file possible duplicates for review.

**Privacy boundary:** no cloud inference, telemetry, or external account access; local database and uploaded bytes remain on the device. This is an experimental prototype, **not** a security-audited financial application.

## 5. Included fictional statements

- `synthetic_checking_2026_Jan-Jun.csv`: six complete months of fictional checking activity.
- `synthetic_savings_2026_Jan-Jun.csv`: matching savings-side transfers, so account reconciliation can be tested.
- `synthetic_ground_truth.csv`: expected category/type for every transaction; **test fixture only**, not imported into the app as user data.
- `expected_monthly_totals.json`: known-correct totals by month; **test fixture only**.

The statements intentionally contain payroll, rent, utilities, phone/internet, insurance, groceries, restaurants, transportation, subscriptions, a student loan payment, a refund, paired savings transfers, a peer reimbursement, a car repair, irregular freelance income, and an ambiguous cash withdrawal. Merchant names and all amounts are fictional.

**Important:** the fixture includes a real existing rent expense. The UI must distinguish **new rent replacing current rent** from **rent added on top of existing expenses**. The older illustrative $3,200/$2,450 example is *not* the ground truth for these statements.

## 6. Non-goals for tonight

- PDF import; live bank integration; authentication; hosting real statements; advanced ML forecasting; calibrated uncertainty; automatic optimization; plan-monitoring notifications; billing; investment or credit recommendations; generalized bank-format parsing; production encryption/security claims.

## 7. Definition of done (must all pass)

1. App starts locally using documented commands.
2. Both included statement CSVs import; no data leaves the machine.
3. Re-import does not duplicate rows; same-amount genuine purchases remain distinct.
4. Monthly totals match `expected_monthly_totals.json` after expected classifications are applied.
5. Savings transfers do not inflate income or spending; refunds reduce expense totals.
6. Unknown cash withdrawal is visibly flagged, not silently treated as confirmed spending.
7. User edits a category and sees the affected report update.
8. At least five supported questions produce correct, evidence-backed responses.
9. Rent replacement/addition calculations are distinguishable and tested.
10. SQLite persistence works after restart; clear-all-data control requires confirmation.

**Cut order if running late:** optional Ollama → advanced visual polish → multiple arbitrary CSV formats. **Never cut** arithmetic correctness, basic import, evidence, or the What If? calculation.

## 8. Acceptance scenarios / examples

- Import both files, select 2026-05: income **$3,700.00**, net expenses **$2,952.94**, surplus **$747.06** before transfers and unknowns.
- Select 2026-06: income **$3,925.00**, net expenses **$2,213.55**, surplus **$1,711.45**; show **$80.00 ATM withdrawal as unresolved**, excluded from the verified surplus definition.
- April's $24.99 grocery refund offsets groceries; it is not wage income.
- Each $300 checking-to-savings transfer has an equal $300 savings inflow; neither is an expense/income.
- If May's existing rent is $1,275 and proposed rent is $1,500 **replacement**, surplus becomes $747.06 − ($1,500 − $1,275) = **$522.06**.
- If $1,500 rent is **additional**, surplus becomes $747.06 − $1,500 = **−$752.94**.

## 9. Four-week roadmap (not tonight's acceptance criteria)

**Sprint 1 (Weeks 1–2):** stabilize ingestion and normalization; support one PDF template; expand local AI tool calling; persistent goals and saved scenarios; regression tests; end-to-end user flow.

**Sprint 2 (Weeks 3–4):** plan re-evaluation after new imports; better source provenance and correction propagation; risk/sensitivity checks; compare categorization and forecasting baselines; user tests; reproducible demo and report.

## 10. Commercial positioning and validation

Competitors already provide financial analysis, planning, and chat. Compass must **test**, not assume, a differentiator: local ownership + inspectable calculations + reusable what-if scenarios. Tonight's release proves the interaction, not market demand. Test with representative users before claiming sellability. Never present synthetic data as a real person's finances.
