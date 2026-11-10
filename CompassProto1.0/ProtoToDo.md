# Compass Alpha 0.1 — Implementation TODO

> **Two implementations:** The browser prototype lives in [`../docs/`](../docs/README.md). The repository-root Python/Streamlit application implements [Phase 0](PHASE0.md) and [Phase 1](PHASE1.md). Checkboxes below refer to Python requirements; separate browser evidence remains at the end of this file.

**Status (2026-11-10):** Python Phases 0 and 1 implemented and locally verified; later Python phases remain incomplete. **Target:** local runnable alpha (timeboxes below are estimates). **Source:** Pranav's local-first statement analysis assistant, extended by one deterministic What If? engine.

## Rules and priorities

- **P0-A** = first vertical slice; get it working before parallelizing.
- **P0-B** = mandatory for a trustworthy alpha; do not claim release-ready without it.
- **P1** = optional if time remains; must not block the P0 flow.
- **P2** = subsequent sprints, explicitly excluded tonight.
- A checkbox is complete **only if its stated acceptance test passes**. No placeholder functionality, hard-coded answers, silent fallbacks, or using ground-truth files as production inputs.
- The app is **local and experimental**. No public hosting with real financial statements and no claims of audited security or financial advice.

## Phase 0 — Repo, contracts, and fixture audit (0:00–0:30)

- [x] **P0-A** Create `app.py`, `requirements.txt`, `compass/{db,importer,classification,analytics,questions,scenarios}.py`, `tests/`, `.gitignore`, `README.md`. **Pass:** `streamlit run app.py` starts without import errors.
- [x] **P0-A** Pin compatible dependency ranges; use Python 3.11+; provide macOS/Linux and Windows commands. **Pass:** fresh virtual environment can install and start app.
- [x] **P0-A** Keep demo fixtures in `fixtures/`; copy the provided two statement CSVs, `synthetic_ground_truth.csv`, and `expected_monthly_totals.json`. **Pass:** fixture files can be read; app UI labels them fictional.
- [x] **P0-A** Lock amount conventions: signed inflow `+`, outflow `−`, integer cents internally; ISO date; account identity; type `income|expense|refund|transfer|unknown`; category separate from type. **Pass:** contract tests pass for each type.
- [x] **P0-A** Lock normalized fields and immutable source fields (see README). **Pass:** source amount/date/description cannot be overwritten by a user classification edit.
- [x] **P0-A** Check fixture totals against supplied expected JSON independently of app; don't change expected values to make tests pass. **Pass:** discrepancies are reported rather than silently corrected.

**Phase 0 evidence (2026-11-10):** Fresh Python 3.12.2 virtual environment installed Streamlit 1.67.0 / pytest 9.2.0; `pip check` clean; 58 Python tests passed, including Streamlit AppTest and Python/SQLite source immutability. Independent standard-library audit passed for 164 transactions and all six monthly totals; an intentionally altered fixture fails with explicit mismatches and unchanged expected JSON. The live Streamlit process started on `127.0.0.1:8501` and its health endpoint returned `ok`. Existing 17 JavaScript tests passed. See [PHASE0.md](PHASE0.md). Next: Phase 1 checking-CSV ingestion and May snapshot. Native Windows execution is not claimed.

## Phase 1 — First vertical slice: import → May summary (0:30–1:30)

- [x] **P0-A** Parse bundled checking CSV headers `date,description,amount,account,transaction_id`; validate exact required fields and row values. **Pass:** accepted/rejected counts shown; invalid amount/date rejected with row number.
- [x] **P0-A** Normalize to signed integer cents; reject NaN, infinity, empty dates, unsupported date strings, and ambiguous amounts. **Pass:** tests cover negatives, decimals, and invalid input.
- [x] **P0-A** Create SQLite `imports` and `transactions` with foreign keys, stable internal primary keys, source IDs, row ordinals, import hashes, original raw fields, effective category/type, and correction flags. **Pass:** data persists after process restart.
- [x] **P0-A** Import all valid rows atomically; rollback on a failed import rather than leaving partial records. **Pass:** deliberately malformed import doesn't create partial data.
- [x] **P0-A** Implement transparent keyword classification; separate payroll, expenses, refunds, transfers, and unresolved transactions. **Pass:** May fixture income = `$3,700.00`, net expenses = `$2,952.94`, surplus = `$747.06` using actual classification logic, not ground-truth lookup.
- [x] **P0-A** Show month selector and May snapshot. **Pass:** all three values are visible and traceable to rows.

**Phase 1 evidence (2026-11-10):** Checking import commits 158 rows with original fields, account-scoped IDs, source ordinals and SHA-256 lineage. All six monthly income/expense/surplus regressions and all checking reference classifications pass using production rules. Invalid CSV rows report their ordinal/physical line and reject the whole file; a simulated second-insert database failure also rolls back the first inserted row and import metadata. A separate Python process reopens the database with identical IDs and May totals. Streamlit AppTest verifies visible counts, May metrics/evidence, month changes, safe reimport, reload persistence and actual upload submit/error handling. See [PHASE1.md](PHASE1.md). Next: complete the Phase 2 savings/import-review workflow.

## Phase 2 — Complete importer and review (1:30–2:15)

- [ ] **P0-B** Import savings CSV into same database. **Pass:** transfer outflow and matching savings inflow are excluded from income/expenses; combined transfer net = `$0.00` in each month.
- [ ] **P0-B** Idempotence at file/account/row level; reimporting same file must not duplicate. **Pass:** row count unchanged after identical import.
- [ ] **P0-B** Preserve legitimate repeated transactions even if merchant, amount, and date match; use source transaction ID scoped by account or file-row identity. **Pass:** two distinct identical-looking rows survive.
- [ ] **P0-B** Handle same file renamed, conflicting source IDs, overlapping statements, and edited copies safely: detect/flag uncertainty rather than silently dropping or merging rows. **Pass:** visible warning and deterministic handling.
- [ ] **P0-B** Preserve original source row and raw signed amount; store category/type overrides separately from predicted labels. **Pass:** corrections persist across restart and same-file reimport.
- [ ] **P0-B** Editable effective category/type, including `unknown` review. **Pass:** correcting a row recalculates all affected aggregates; original raw data unchanged.
- [ ] **P0-B** June `$80` ATM transaction remains `unknown`, visible in unresolved section and excluded from verified totals. **Pass:** June verified surplus `$1,711.45` with separate `$80` unresolved outflow notice.
- [ ] **P0-B** Refund offsets expenses in its category rather than increasing earned income. **Pass:** April `$24.99` grocery refund handled correctly.
- [ ] **P0-B** Import error UX: empty CSV, missing column, bad encoding, malformed row, duplicate file, and partial coverage. **Pass:** actionable visible message; no stack trace exposed as financial answer.
- [ ] **P1** Add explicit column mapping for common third-party CSV variants; never infer debit/credit polarity silently.

## Phase 3 — Snapshot and deterministic Ask Compass (2:15–3:00)

- [ ] **P0-A** Month selector, income, net expense, verified surplus, category summary, source-row table. **Pass:** all months reconcile with supplied expected JSON in automated tests.
- [ ] **P0-B** Show data quality: reviewed/unreviewed rows, unknown dollar amount, covered date range, and warning if month may be incomplete. **Pass:** never label unverified import as bank-balance reconciled.
- [ ] **P0-A** Implement five tool functions: `get_income`, `get_expenses`, `get_category_spending`, `get_largest_expenses`, `get_surplus`. **Pass:** fixed question test set returns correct amounts and date ranges.
- [ ] **P0-B** Questions use deterministic parsing/routing when Ollama unavailable; unsupported or ambiguous queries elicit a clarification or supported examples. **Pass:** no invented figures.
- [ ] **P0-B** Answers show query filters, covered period, included transaction IDs/rows, and excluded unknowns where relevant. **Pass:** clicking/viewing evidence agrees with answer.
- [ ] **P0-B** UI refresh after edit/import and across Streamlit reruns. **Pass:** no stale cached totals or duplicated inserts.
- [ ] **P1** Local Ollama structured intent router using explicit tool allowlist, JSON schema validation, bounded inputs, timeout and deterministic fallback. Never ask model to calculate monetary totals. **Pass:** app works with Ollama service stopped.

## Phase 4 — What If? engine (3:00–3:45)

- [ ] **P0-A** Baseline month selector; derive **verified** income, net expense, and surplus from the same analytics engine. **Pass:** baseline equals snapshot exactly.
- [ ] **P0-A** Input proposed rent (nonnegative), mode `replace` or `additional`, added monthly spending (nonnegative), and signed monthly income adjustment. **Pass:** invalid/nonfinite values rejected; cents remain exact.
- [ ] **P0-B** For replacement mode, identify effective historical **Housing/Rent** expense for selected month; if none or multiple ambiguous rents, ask user to confirm the existing rent instead of guessing. **Pass:** unresolved rent blocks a definitive replacement result.
- [ ] **P0-A** Implement `rent_delta = new_rent - existing_rent` for replace, `rent_delta = new_rent` for additional; `projected_surplus = baseline_surplus + income_adjustment - added_spending - rent_delta`. **Pass:** pure function tests; no float drift.
- [ ] **P0-A** May 2026 test: baseline `$747.06`; replace `$1,275` rent with `$1,500` → `$522.06`; add `$1,500` rent → `−$752.94`. **Pass:** UI and unit tests match.
- [ ] **P0-B** Display complete formula, baseline rent, rent delta, income adjustment, added spending, projected surplus, and difference from baseline. **Pass:** displayed arithmetic reconstructs output exactly.
- [ ] **P0-B** Show six-month **static extrapolation** (`6 × projected monthly surplus`), not an account balance or statistically validated forecast; label constant-income/expense assumptions. **Pass:** no implied certainty or cash-on-hand claim.
- [ ] **P0-B** Negative surplus warning and warning if selected month contains unknowns/partial coverage; include clear disclaimer that historical month may be atypical. **Pass:** negative May additional-rent scenario flagged.
- [ ] **P1** Optional monthly savings target; compare projected monthly surplus to target without claiming funds are available as bank balance.
- [ ] **P1** Optional six-row cumulative change table relative to a **user-supplied starting balance**, never inferred from statement activity.

## Phase 5 — Quality, privacy, release (3:45–5:00+)

- [ ] **P0-B** Unit tests: amount sign, rounding, refund handling, transfers, unknowns, category overrides, date filtering, category totals, What If? pure function. **Pass:** `pytest -q` green.
- [ ] **P0-B** Import tests: malformed rows, interrupted transaction rollback, duplicate reimport, same-day identical legitimate purchases, conflicting source IDs, reimport after correction. **Pass:** no silent data loss.
- [ ] **P0-B** Fixture regression tests for all Jan–Jun months against `expected_monthly_totals.json`, plus expected transaction classifications from ground-truth file **only in tests**. **Pass:** all exact cents match; classifier mismatches surfaced rather than concealed.
- [ ] **P0-B** UI smoke test: checking → savings → May snapshot → question → edit → scenario → restart. **Pass:** every step works in a clean local run.
- [ ] **P0-B** Clear-all-data confirmation deletes local SQLite records and app-owned persisted uploaded copies/caches, if any. **Pass:** restart yields empty state; bundled synthetic fixtures remain available as fixtures.
- [ ] **P0-B** Privacy inspection: no network financial-data transmission, no analytics/telemetry, no cloud model API; use local-only Ollama endpoint if enabled. **Pass:** dependencies/configuration reviewed; no secret keys or real statements committed.
- [ ] **P0-B** `.gitignore` includes `.venv/`, `*.db`, `*.sqlite*`, `.env*`, private uploads, `__pycache__/`, `.pytest_cache/`; ensure synthetic fixture path is not ignored. **Pass:** `git status` shows no sensitive generated artifacts.
- [ ] **P0-B** README documents install/run, demo steps, schema, exact scenario formulas, test commands, data deletion, limitations, privacy boundary, and known issues. **Pass:** fresh user can follow without oral instructions.
- [ ] **P0-B** Record 60–90 second demo on fictional data. **Pass:** import → May snapshot → evidence-backed question → correction → replace/add rent → restart shown.
- [ ] **P1** Visual polish, responsive layout, helpful empty states, optional Ollama integration.

## Stop-ship checks (all mandatory)

- [ ] **GATE** All required P0-A and P0-B checks pass or are explicitly documented as unresolved; **do not claim complete alpha if unresolved**.
- [ ] **GATE** No incorrect or invented financial totals in supplied regression cases.
- [ ] **GATE** No double-counted internal transfers, refunds as wages, or replacement rent.
- [ ] **GATE** No silent deletion/merging of distinct source transactions; corrections remain durable.
- [ ] **GATE** No undisclosed financial-data upload to remote service.
- [ ] **GATE** All displayed projections labeled illustrative and conditional on inputs.

## Explicitly deferred — Sprint 1 (Weeks 1–2)

- [ ] **P2** Text-based PDF import for one known layout, with parser validation and error handling.
- [ ] **P2** Multi-bank mapping, statement-period detection, balance reconciliation when available.
- [ ] **P2** Stable local LLM tool calling with structured outputs, reliability/latency tests.
- [ ] **P2** Saved goals, scenario persistence, and richer plan comparison.

## Explicitly deferred — Sprint 2 (Weeks 3–4)

- [ ] **P2** Re-evaluate saved plans after new statement imports.
- [ ] **P2** Stronger provenance, correction propagation, sensitivity and uncertainty checks.
- [ ] **P2** Compare rules vs learned categorization; historical average vs predictive baseline; LLM-only vs tool-grounded Q&A.
- [ ] **P2** Target-user tests, competitor workflow comparison, packaging, security review, research report.

## Four-developer handoff

| Owner | Core module | Definition of done |
|---|---|---|
| Data | importer, SQLite, source preservation, transfer reconciliation | Fixture import and idempotence tests green |
| ML | classification rules, analytics baselines, evaluation | Exact monthly totals and transparent misclassification report |
| AI | deterministic financial tools, optional Ollama adapter | Five grounded intents; no fabricated figures |
| Product | Streamlit, scenario pure function, UX and integration | May rent tests and full hero journey green |

**First checkpoint:** correctly import the checking CSV and show May 2026 income `$3,700.00`, net expenses `$2,952.94`, surplus `$747.06` **without reading the expected totals file inside the app**.

## GitHub Pages browser checkpoint

Verified by `npm test` (Node 22+; no dependency installation):

- [x] Checking-only May vertical slice computes the specified totals through production classification rules.
- [x] Both fictional statements yield 164 records and every reference classification matches in tests.
- [x] All six monthly summaries and category sums match the supplied exact-cent expectations.
- [x] Atomic CSV validation, renamed-file idempotence, account-scoped IDs, repeated legitimate purchases, overlapping-file rejection, and conflicting-ID rejection.
- [x] Transfers and refunds have correct accounting treatment; June ATM stays unknown and excluded.
- [x] Classification overrides preserve source rows and change aggregates; storage serialization preserves them on reopen.
- [x] Five deterministic question handlers expose matching source rows and reject unsupported/ambiguous periods.
- [x] Replacement/additional rent, cheaper rent, signed income changes, missing rent, and six-month arithmetic pass exact-cent tests.
- [x] Saved-state reopening, quota-failure preservation, and removal of only the Compass storage key pass storage-adapter tests.
- [x] Published demo copies match source statements; production code never reads classification/totals oracles.
- [x] Live browser walkthrough: empty state → fictional demo → May summary → evidence-backed question → correction → recalculated answer → reload persistence → restore reference classification. Native Chrome verification on 2026-11-10; see [BROWSER_QA.md](BROWSER_QA.md).
- [x] Live replacement/additional rent scenarios, missing-confirmation block, shortfall warning, and June $80 unresolved-transaction notice verified in native Chrome.
- [x] Narrow-screen smoke check at approximately 520 pixels and 100% zoom; navigation, metrics, stacked charts, and dialog inspected. Tab focus and Escape dismissal checked in the clear-data dialog. This does not establish full mobile or accessibility coverage.
- [ ] Uploaded-file picker and malformed-file/overlap error UX exercised end-to-end in the browser; automated importer coverage already passes.
- [ ] Actual confirmed browser deletion → reload empty state → demo reimport. Dialog behavior and storage-adapter deletion are verified separately; actual browser deletion remains unchecked.
- [ ] Physical-phone/narrower-width checks and a complete keyboard-only/screen-reader walkthrough.
- [x] Successful remote GitHub Pages deployment verified: [live prototype](https://archipelagoing.github.io/AIFinalProject/), [successful workflow](https://github.com/archipelagoing/AIFinalProject/actions/runs/42760426153). Public HTML, JavaScript, CSS, and both demo CSVs match the tested source bytes. An overlapping legacy branch deployment initially served the README; rerunning the configured Actions deployment resolved it.
- [ ] Recorded 60–90 second demo.

Python Phases 0 and 1 are tracked separately above; subsequent Python/SQLite workflows, optional AI work, and later sprints remain incomplete. These browser checks do not assert that the original local-app release gates passed.
