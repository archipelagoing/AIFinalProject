# Phase 0 — Python foundation

Implemented and locally verified on 2026-11-10. [ProtoToDo.md](ProtoToDo.md) remains the authoritative implementation checklist.

This is the historical foundation report. [Phase 1](PHASE1.md) now adds statement ingestion, production classification rules, persistence, and the monthly snapshot UI.

## Delivered structure

```text
app.py                         Streamlit setup and fictional-fixture inventory
requirements.txt               Streamlit >=1.67,<1.68; pytest >=9.2,<9.3
pyproject.toml                 Python test discovery (separate from JavaScript)
.streamlit/config.toml         Loopback-only server; usage statistics disabled
compass/
  __init__.py
  contracts.py                 Immutable transactions, dates, money, overrides
  db.py                        SQLite schema and source-preserving updates
  importer.py                  Fictional statement format inspection
  classification.py            Type vocabulary and unknown default
  analytics.py                 Exact accounting treatment for all five types
  questions.py                 Approved intent vocabulary; routing comes later
  scenarios.py                 Validated scenario input contract; engine comes later
fixtures/                      Copies of all four supplied reference files
scripts/audit_fixtures.py       Independent fixture-only audit and CLI
tests/python/test_phase0.py     Contract, database, audit, and Streamlit app tests
.github/workflows/python.yml   Python 3.11 / 3.12 CI matrix
```

The existing root `.gitignore` already protects `.venv`, `.local/`, `*.db`, `*.sqlite*`, `.env*`, uploads, caches, and bytecode. Fixture copies are tracked. Source fixture originals remain intact for the Pages regression suite. The separate BNPL assessment is unchanged.

## Run and test

Use the [root README](../../README.md#run-the-local-python-foundation) for macOS/Linux and Windows virtual-environment commands. Start from the repository root with `streamlit run app.py`. The setup screen initializes an empty local SQLite schema and validates the two fictional statement files; it does not import transactions or show hard-coded financial answers.

After activating the virtual environment:

```sh
python -m pip check
python scripts/audit_fixtures.py
python scripts/audit_fixtures.py --json
python -m pytest -q
```

`npm test` remains the separate Pages engine regression suite. No JavaScript package installation is necessary for it.

## Locked transaction contract

`Transaction` is a frozen, slotted dataclass with these fields:

```text
id, account_id, source_transaction_id, import_id, source_row_number,
posted_date, description, amount_cents, original_row_json,
predicted_type, predicted_category, corrected_type, corrected_category,
created_at
```

- All money is signed integer cents within SQLite's 64-bit range. Floats, booleans, exponent notation, nonfinite values, currency symbols, ambiguous separators, and excess decimal places are rejected. Display conversion uses integer division and remainder.
- Dates must be real ISO `YYYY-MM-DD` calendar dates. Timestamps include a timezone.
- `account_id` is a stable, nonempty source/account identity chosen by the future importer; use source namespace plus account identity to distinguish accounts from different institutions. Source IDs are scoped by account, not globally unique.
- Types are `income`, `expense`, `refund`, `transfer`, `unknown`. Category is a separate nonempty label. Unclassified records default to `unknown` / `Uncategorized`.
- Positive income adds to income. Negative expense increases expense totals. Positive refunds reduce expenses. Transfers and unknowns are tracked separately and excluded from verified surplus.
- Income/refund classification requires a positive source amount; expense requires a negative source amount. Corrections obey the same rules.
- Effective type/category prefer the corresponding user override when present, otherwise the prediction.
- `with_classification(type, category)` returns a new record and accepts no source-field changes. Original row JSON is an immutable string; its decoded accessor returns a fresh copy.

## SQLite contract

Default database: `.local/compass.db`, resolved relative to `app.py`, not the shell working directory. `COMPASS_DB_PATH` can override the path for isolated tests or local development.

`imports` preserves ID, original filename, SHA-256 digest, and timezone-aware timestamp. `transactions` stores the normalized fields, links to imports with enforced foreign keys, and enforces account-scoped source IDs and import/row identity. Missing source IDs use SQL NULL so legitimate rows are not collapsed by an empty-string ID.

SQLite triggers reject updates to preserved import metadata and transaction source fields, including original amount/date/description and predicted labels. Classification updates modify only `corrected_type` and `corrected_category`. Parameterized statements are used for record values. Transaction commit boundaries belong to the caller, allowing atomic multi-row ingestion in Phase 1.

This is a new-database foundation, not a general migration system. Direct filesystem access or deletion of a record is outside the protection offered by update triggers. The foundation does not claim encryption, tamper-proof storage, or a security audit.

## Independent fixture audit

The four files under `fixtures/` are byte-for-byte copies of the supplied originals:

- `synthetic_checking_2026_Jan-Jun.csv`: 158 fictional transactions.
- `synthetic_savings_2026_Jan-Jun.csv`: 6 fictional transactions.
- `synthetic_ground_truth.csv`: reference classifications, evaluation only.
- `expected_monthly_totals.json`: expected totals, evaluation only.

The audit uses the standard library (`csv`, `Decimal`, date validation, and JSON) and does not import `compass`, the UI, or the Pages engine. It joins the supplied reference labels to statement IDs and independently recomputes all five monthly metrics. This verifies fixture accounting consistency, not production classifier quality; keyword classification belongs to Phase 1.

Results:

| Month | Income | Net expenses | Surplus |
| --- | ---: | ---: | ---: |
| January 2026 | $3,700.00 | $2,273.84 | $1,426.16 |
| February 2026 | $3,700.00 | $2,373.11 | $1,326.89 |
| March 2026 | $3,700.00 | $2,259.09 | $1,440.91 |
| April 2026 | $3,700.00 | $2,239.12 | $1,460.88 |
| May 2026 | $3,700.00 | $2,952.94 | $747.06 |
| June 2026 | $3,925.00 | $2,213.55 | $1,711.45 |

Transfer net across both accounts is zero for every month. June has a separate −$80.00 unknown amount. Tests intentionally change a copied source transaction, verify that the audit reports the specific mismatched metrics with a failing exit status, and verify that the expected JSON is unchanged.

Only statement files are read by the setup UI. Test oracles are read exclusively by tests and the separate audit tool; no user-facing answer is derived from them.

## Verification evidence

- Fresh `.venv` created with Python 3.12.2; requirements installed successfully. Installed direct dependencies: Streamlit 1.67.0 and pytest 9.2.0. Bounded minor-version ranges are recorded in `requirements.txt`.
- `python -m pip check`: no broken requirements.
- `python -m pytest -q`: 58 passed, including the Streamlit `AppTest` script run, all five accounting types, source immutability in Python and SQLite, foreign keys/account identity, saved correction reopening, identical fixture copies, and independent audit mismatch detection.
- `npm test`: existing 17 Pages regression tests passed.
- `.venv/bin/streamlit run app.py`: server started on `127.0.0.1:8501`; `/_stcore/health` returned `ok`.
- Runtime files are ignored and demo fixtures remain visible to Git.

The filesystem sandbox blocks local server sockets and some PyArrow CPU queries. The initial sandboxed Streamlit app test timed out; the same suite passed outside the sandbox without changing test expectations or extending the timeout. Dependency download and the local server also required the environment's network/socket approval. This is an execution-environment limitation, not a bypass in the application.

The CI workflow is configured to test Python 3.11 and 3.12; local verification alone does not prove an unexecuted CI matrix or native Windows installation.

## Next phase

Phase 1 is the checking-CSV → SQLite → May summary vertical slice. Full statement ingestion, production classification rules, duplicate/overlap handling, user review UI, deterministic question routing, and scenario calculations are not implemented in this Python foundation. The existing JavaScript Pages prototype implements a separate browser workflow; it does not execute this Python app.
