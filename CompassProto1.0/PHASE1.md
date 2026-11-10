# Phase 1 — Import to monthly snapshot

Implemented on 2026-11-10. The Python application now imports the fictional checking statement into local SQLite and displays a selected month's computed financial snapshot. [ProtoToDo.md](ProtoToDo.md) is the authoritative checklist; later phases remain open.

## Try it

Use the repository-root README's virtual-environment instructions, then run:

```sh
streamlit run app.py
```

Choose **Load fictional checking statement**. All 158 checking transactions are imported in one operation. May 2026 is selected by default when available:

| Income | Net expenses | Surplus |
| ---: | ---: | ---: |
| $3,700.00 | $2,952.94 | $747.06 |

The month selector also supports the other imported months. Income, net-expense, and surplus panels expose their calculation and contributing source rows. The selected-month table includes transfers and unresolved transactions; these are excluded from verified totals and explained separately. June retains the $80 ATM withdrawal as unknown.

The original-row inspector shows preserved input values and the classification rule explanation. There is no category-edit UI in this phase. Reopening the app uses the same `.local/compass.db` (or `COMPASS_DB_PATH`) and reads persisted transactions without reimporting them.

## CSV validation and counts

The upload form accepts UTF-8 CSVs up to 5 MB. The file selector is outside the submit form so choosing a file can rerun the app and enable submission. Supply exactly these five unique header names; column order may vary:

```csv
date,description,amount,account,transaction_id
2026-05-01,OAK TERRACE APARTMENTS RENT,-1275.00,Checking,example-1
```

Dates must be valid ISO calendar dates. Amounts are signed plain decimals with at most two fractional digits, converted directly to integer cents. NaN, infinity, exponent notation, currency symbols, thousands separators, fractional cents, empty dates, unsupported dates, incorrect column counts, repeated IDs within an account, and empty accounts/descriptions are rejected. Whitespace around normalized field values is trimmed; originals remain unchanged.

Quoted commas, escaped quotes, multiline descriptions, UTF-8 BOM, and CRLF are supported. Source row numbers are record ordinals including the header as row 1. Validation errors also report the starting physical CSV line, which can differ after multiline records. Malformed quoting or header/encoding errors are visible file-level failures.

The UI distinguishes:

- **Accepted rows:** rows actually committed by this operation.
- **Rejected rows:** all rows in an atomically rejected statement, including otherwise valid rows.
- **Already imported:** rows skipped because the identical file bytes were previously imported.
- **Valid/invalid CSV rows:** separate validation counts, shown in the report caption.

For example, a file containing one valid row followed by one invalid row reports 0 accepted, 2 rejected, 1 valid, and 1 invalid, with an error at row 3. No import metadata or transactions from that file are saved. Database failures can reject syntactically valid rows; their report explains the storage/constraint failure rather than labeling them invalid CSV data.

## Atomic storage and provenance

Imports are identified by SHA-256 of original file bytes; the original filename, digest, and import timestamp are preserved. Transaction primary keys are deterministic hashes of file digest and source row ordinal. Local account identities derive from the bank/source namespace and source account label. Source-provided IDs are scoped by local account; missing IDs are NULL and retain file-row identity.

Normalization and validation finish before database insertion. A SQLite savepoint wraps import metadata, all transactions, and exact-range aggregation checks. Releasing the savepoint durably commits an otherwise standalone import; an outer caller-owned transaction retains its own final commit/rollback authority. A failed insertion rolls back every inserted row and its import record. Existing records and correction overrides remain unchanged.

Identical-byte reimport is safe, including a renamed file or repeated Streamlit button press. Conflicting existing source IDs reject the entire incoming statement with an overlap warning. Full overlapping-statement resolution and possible-duplicate detection when source IDs differ are later work; this phase does not claim comprehensive deduplication.

SQLite retains the Phase 0 foreign keys and source-immutability triggers. The `transaction_details` view exposes effective type/category and a correction flag. Python objects expose the same effective fields and `has_correction` flag. The evidence table links records to file, row, source ID, and import digest.

## Classification and accounting

`compass/classification.py` contains ordered, inspectable description rules. Positive payroll/freelance payments are income; recognized negative purchases are expenses; a positive grocery return is a refund; recognized savings and peer transfers are excluded. Unknown merchants and ambiguous cash withdrawals remain unknown instead of being guessed into spending or income. Rules target the supplied synthetic vocabulary and require user review before relying on arbitrary bank descriptions.

`compass/analytics.py` applies the effective classification:

```text
income = sum(classified income)
net expenses = sum(negative expense magnitudes) − sum(positive refunds)
surplus = income − net expenses
```

Transfers and unknowns contribute to neither income nor expenses. All arithmetic uses integer cents; out-of-range sums reject the import before commit. Month coverage remains unverified because activity dates do not establish a complete statement period. Surplus is not a bank balance or available cash.

The app, importer, classifier, and financial aggregation never read expected classifications or expected monthly totals. Those remain evaluation-only inputs to tests and the independent audit. May's values are computed from the imported checking records and production rules, not looked up from a reference file.

## Verification

Run from the repository root with the virtual environment active:

```sh
python -m pytest -q
python scripts/audit_fixtures.py
npm test
```

The Python suite verifies checking import/provenance, all checking reference classifications, all six checking income/expense/surplus totals, malformed and invalid inputs, exact cents, row and physical-line errors, atomic rejection before insertion, forced second-insert rollback, outer-transaction ownership, stable IDs after a real Python subprocess restart, effective fields/correction flags, renamed-file reimport, and source-preserving corrections.

Streamlit AppTest exercises the demo button, visible May metrics and evidence tables, month switching, the June unresolved warning, safe reimport, fresh app-session persistence, and the real upload submit/error path. For the upload test, AppTest substitutes the uploaded-file object because it does not drive an OS file picker. It also guards the uploader/form boundary against leaving submission permanently disabled. This is automated UI verification, not a claim of native browser or physical-phone testing of the Python app.

The independent fixture audit still matches all original expectations, which have not been edited. The existing 17 JavaScript tests cover the separate GitHub Pages implementation.

## Remaining work

Phase 2 adds the complete savings/import-review workflow, category/type editing, transfer reconciliation, and more comprehensive overlap handling. Ask Compass and What If? integration remain Phases 3 and 4. CSV column mapping, PDF/OCR, local model routing, and later research tasks remain deferred. The original Phase 0 verification report is historical; this report describes the current Python vertical slice.
