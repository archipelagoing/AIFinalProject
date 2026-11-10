# What is in this repo?

The repository has two working prototypes and one current product/execution specification. The proposed fine-tuned model and expanded Wrapped product are not already implemented by the existing code.

## Read these first

| File | Purpose / authority |
| --- | --- |
| `README.md` | Product specification, proposed brand/architecture/formulas, and commands for the current prototype. Consolidates the newly supplied complete execution README. |
| `COMPASS_ENGINEERING_PLAN.md` | Authoritative 96 tickets, Dev 1–4 ownership, six meeting gates, December 1 freeze, evidence/release requirements. Ticket definitions live here once. |
| `COMPASS_COVERAGE_MATRIX.csv` | 117 candidate requirement-to-ticket mappings. These are unverified planning records, not test results or bank data. Missing test/evidence columns must be completed as work is verified. |
| `REPOSITORY_GUIDE.md` | This inventory and the cleanup decisions. |

The two new plan/matrix files were retained without changing their contents. The supplied `Compass_Complete_Execution_README.md` was incorporated into `README.md`, with superseded schedules replaced by a link to the newer engineering plan. Its exact supplied bytes remain in `archive/proposals/` for provenance. The latest 96-ticket schedule takes precedence over that source snapshot's older freeze dates and 91-ticket plan.

## Working applications

| Path | What it does |
| --- | --- |
| `app.py` | Local Streamlit UI: imports, snapshot, classification review, Ask Compass, What If?, privacy/deletion controls. |
| `compass/__init__.py` | Python package marker. |
| `compass/contracts.py` | Transaction types, immutable source records, exact integer cents and date validation. |
| `compass/db.py` | SQLite schema, queries, classification overrides and atomic deletion. |
| `compass/importer.py` | Atomic CSV import, source identity, duplicate/overlap checks and demo loading. |
| `compass/mapping.py` | Explicit column/date/debit-credit mapping; no silent polarity inference. |
| `compass/classification.py` | Inspectable keyword classifications; unmatched activity remains unknown. |
| `compass/analytics.py` | Monthly/category totals, coverage/review metadata and transfer evidence. |
| `compass/questions.py` | Five deterministic question tools with filters and source evidence. |
| `compass/ollama.py` | Optional constrained loopback intent router and deterministic fallback; not a trained model. |
| `compass/scenarios.py` | Pure rent/income/spending scenario math and conservative rent evidence. |
| `docs/index.html`, `app.js`, `styles.css` | Separate static browser demo: interface and browser-side interaction. |
| `docs/engine.js`, `storage.js` | Browser financial calculations and localStorage persistence. |
| `docs/compass.svg` | Browser icon. |
| `docs/README.md` | Browser-specific running, deployment and privacy instructions. |
| `docs/demo/*.csv` | Two fictional statements fetched by the deployed Pages app. These copies are needed because only `docs/` is deployed; tests compare them with canonical fixtures. |

## Data, tests and checks

| Path | Purpose |
| --- | --- |
| `fixtures/synthetic_checking_2026_Jan-Jun.csv` | Canonical fictional checking input. |
| `fixtures/synthetic_savings_2026_Jan-Jun.csv` | Canonical fictional savings/transfer input. |
| `fixtures/synthetic_ground_truth.csv` | Expected transaction labels, used only in tests/audit. |
| `fixtures/expected_monthly_totals.json` | Expected six-month totals, used only in tests/audit. |
| `tests/python/test_phase0.py` … `test_phase5.py` | Existing Python contract/import/review/question/scenario/privacy regressions. Names record the historical implementation sequence, not current ticket status. |
| `tests/engine.test.js` | Tests the separate browser engine/storage and its deployed fixture copies. |
| `scripts/audit_fixtures.py` | Independent exact-cent fixture audit; never supplies app answers. |
| `scripts/audit_privacy.py` | Scoped secret/generated-file/config inspection; checks fictional CSVs and validates the declared planning matrix against actual ticket IDs. |
| `scripts/release_smoke.py` | Isolated Chromium desktop/mobile workflow, server restart, deletion and optional demo recording. |

## Configuration and automation

| File | Purpose |
| --- | --- |
| `requirements.txt` | Python runtime/test dependency ranges. |
| `requirements-dev.txt` | Optional Playwright tooling plus base requirements. |
| `pyproject.toml` | pytest discovery and Python path configuration. |
| `package.json` | Browser test/static-server commands and Node version requirement; no frontend build dependency installation is needed. |
| `.streamlit/config.toml` | Loopback binding, disabled usage telemetry, upload cap, error-display and theme settings. |
| `.github/workflows/python.yml` | Python 3.11/3.12 tests, audits and real-browser smoke. |
| `.github/workflows/pages.yml` | Browser tests and deployment of only `docs/` to GitHub Pages. |
| `.gitignore` | Keeps local DBs, uploads, environments, secrets, caches and generated recordings out of Git. |
| `LICENSE` | Repository license. |

## Historical or exploratory material

- `archive/alpha-0.1/`: phase 0–5 reports, original scope, historical checklist, browser QA and inspected demo media. This is evidence of past work, not a competing active roadmap.
- `archive/proposals/`: exact supplied complete-README source and the previously requested `ReadmeOld.md`. These are frozen snapshots; their historical relative links/schedules are not current instructions.
- `research/BNPL_Opportunity_Assessment.md`: separate BNPL product research. Kept because it contains distinct work; it is not part of the active build contract.
- `.venv/`, `.local/`, `artifacts/`, caches and any `node_modules/` are ignored local/generated directories, not source deliverables. Cleanup did not delete local databases, private uploads, installed tooling or Git history.

## What was removed or consolidated?

- Removed unused generic templates: `SHOW_BIBLE.md`, `todoSimple.md`, `rubricatm.md`, `ISSUE_TEMPLATE_SPEC.md`.
- Removed superseded `IssueTickets.md`, `DEVELOPMENT_PLAN.md`, and `BRAND_IDENTITY.md`; current tickets/brand requirements are in the new authoritative documents.
- Removed the obsolete Alpha 0.2 `SCOPE.md` and the stray `Microsoft.VisualStudio.Services.VSIXPackage` editor extension.
- Removed four redundant statement/oracle copies from the former `CompassProto1.0/` folder. `fixtures/` is the single canonical set; the deployed demo retains its two necessary copies.
- Moved useful reports/demo artifacts out of `CompassProto1.0/` into the archive, and moved BNPL research out of the root.
- Removed duplicate/contradictory schedules from the active README, preserving the product proposal and pointing to the 96-ticket plan.

Older committed versions remain recoverable through Git history. No current ticket was marked complete by this reorganization, and the original 117 matrix links remain candidates.
