# Phase 2 — Complete importer and review

Implemented on 2026-11-10 for the local Python/Streamlit application. [ProtoToDo.md](ProtoToDo.md) remains the authoritative checklist. This phase includes all nine required P0-B items and the optional explicit column mapper. Ask Compass and What If? integration remain future phases.

## Demo and review

Run `streamlit run app.py` from the repository root after activating the virtual environment. Choose **Load fictional checking statement**, then **Load fictional savings statement**. Both import into the same database under the same fictional source namespace: 158 checking rows plus 6 savings rows, 164 total.

Every supplied month retains its expected income, expenses, and surplus. Transfer net across both accounts is $0.00 each month. One unique same-date/opposite-amount savings pair per month is supported by the imported records. Pair detection requires exactly two opposite nonzero amounts across distinct local accounts. Ambiguous groups and unpaired peer payments remain explicitly flagged; a zero net alone is not proof of reconciliation. No account balance reconciliation is claimed.

June initially shows $1,711.45 verified surplus and one unresolved $80.00 ATM outflow. Expand **Review and correct classifications**, filter to unresolved rows if desired, and save the ATM as an expense in a category such as `Cash spending`. The surplus becomes $1,631.45, the unknown exclusion disappears, and category spending updates by $80.00. **Restore rule classification** returns it to unknown and restores the original baseline.

The review form edits only effective type/category overrides. Original dates, amounts, descriptions, account identities, source IDs, file/row references, raw JSON, timestamps, and predictions remain unchanged. Overrides persist in SQLite across app and process restarts and same-file reimport. Invalid sign/type changes are rejected with an explanation. Updates validate monthly headline and category totals inside a savepoint; a failing edit rolls back without corrupting saved data. Reviewed classifications are not bank reconciliation.

April's positive $24.99 grocery refund reduces Groceries spending and net expenses, not earned income. Changing a refund's category moves its offset to the selected effective category without counting it twice. All calculations continue to use exact integer cents; unsupported amount/subtotal ranges reject the operation before commit.

## Import identity and overlap policy

- Identical file bytes are recognized by SHA-256 even after a rename. Reimport adds no rows, preserves corrections, and keeps the original filename/provenance.
- Local account identities use the explicit bank/source namespace and account label. Keep those values consistent across statements; different banks need different namespaces. Source IDs are scoped by account.
- Distinct IDs with identical merchant/date/amount survive within a statement. Rows with no IDs use file-digest/row identity, so repeated legitimate purchases within a file also survive.
- Existing account/source IDs block an entire overlapping incoming statement. The message distinguishes repeated source activity from conflicting source values. Confirmation cannot overwrite an existing source ID, and no overlap rows are silently discarded to make the rest fit.
- A cross-file match on normalized account/date/description/amount, without a shared reliable ID, is uncertain. No rows are saved until the user verifies that the purchases are distinct and checks **Keep flagged look-alike rows as distinct activity**. Then all incoming rows are retained, a warning explains the decision, and the confirmation is recorded in import metadata.
- A reused filename plus overlapping activity dates for an account also flags a possible edited copy, even when IDs and amounts changed. Confirm only after reviewing the source.
- Reusing identical bytes with a different source identity or column interpretation is blocked. Saved financial records cannot silently flip sign or move accounts.

These are evidence-based checks, not a guarantee of detecting every edited or fraudulent statement. For example, changing names, IDs, dates, and values simultaneously may remove every detectable relationship. Whole-file rejection of overlapping source IDs is conservative; a selective overlap-resolution/merge UI is not implemented.

Every operation is atomic. CSV validation happens before writes; storage and range checks are covered by a SQLite savepoint. A failure preserves prior statements and corrections and rolls back new import metadata/settings as well as any newly inserted rows. The caller retains control of an existing outer transaction.

## Explicit CSV mapping

The default format still requires exactly the five canonical headers. For variants, choose the file and enable **Map a different CSV layout**. Then explicitly select:

1. Date and description columns.
2. An account column, or a fixed account name.
3. A source transaction ID column, or no supplied IDs.
4. Date order: `YYYY-MM-DD`, `MM/DD/YYYY`, or `DD/MM/YYYY`.
5. Amount convention: positive inflows, positive outflows, or separate nonnegative debit/credit columns.
6. The corresponding amount/debit/credit columns.

The amount convention begins unselected; Compass never guesses it. Each mapped field must use a distinct existing column. Submission remains disabled until the mapping, date order, and amount direction are explicitly confirmed. Changing the interpretation requires new confirmation.

Signed amount mapping can reverse the sign only when positive-outflow mode was explicitly chosen. Separate debit/credit mapping calculates `credit − debit`, rejects negative column values, rejects rows with both columns nonzero, and rejects rows with neither supplied. Dates must exactly match the selected format; ambiguous US/European ordering is never guessed. Numeric values must still be plain exact decimals; currency symbols, thousands separators, exponent notation, nonfinite values, and fractional cents are not automatically cleaned up. The app is a single-currency USD prototype, not an exchange-rate tool.

Original field names and values—including debit/credit fields and unused extra columns—are preserved in source JSON. Evidence tables label their signed values **Normalized amount**; the original-row inspector shows the unmodified source signs. `import_settings` stores the source namespace, mapping JSON, and distinct-activity confirmation alongside the immutable import record. Existing Phase 1 databases gain the new metadata table without rewriting source rows; legacy imports without settings remain recognized by their saved source values.

## Error and coverage UX

Empty files, missing/repeated columns, bad UTF-8, malformed quoting, invalid dates/amounts, and source conflicts produce visible explanations and accepted/rejected counts, with row/physical-line references where available. They do not expose a stack trace or fabricate an answer. Duplicate files display a separate already-imported count. Look-alike warnings explain the verification needed before import.

Every snapshot prominently warns that activity dates do not establish full statement coverage and that the month may be incomplete. Unresolved transaction value and limited transfer evidence remain separate warnings. Users are prompted to import missing statements before relying on totals. Surplus is not cash on hand or a bank balance.

## Verification

With the virtual environment active:

```sh
python -m pytest -q
python scripts/audit_fixtures.py
npm test
```

Tests cover all 164 reference classifications and all five expected monthly metrics; unique/ambiguous transfer evidence; repeated and renamed files; distinct identical-looking purchases with and without IDs; overlap conflicts and edited-copy warnings; explicit confirmation preserving both records; original-source immutability; unknown review and refund category offsets; correction rollback; real-process restart and reimport; legacy metadata compatibility; signed/debit-credit/date mapping; and atomic rejection of bad mappings or values.

Streamlit AppTest exercises both demo buttons, review/save/restore and recalculation, fresh-session persistence, actionable import errors, duplicate/coverage warnings, look-alike confirmation, invalid correction feedback, and mapping confirmation/direction changes. Uploaded-file objects are supplied at the AppTest boundary because these tests do not drive an OS file picker. They verify real handlers and rendered values, not a native-browser/physical-phone walkthrough.

Production code never reads the ground-truth CSV or expected-totals JSON. Those files remain unchanged and are used only by tests and the independent fixture audit. No remote service or language model is required.

## Remaining work

Phase 3 adds deterministic financial question routing, richer data-quality reporting, and answer evidence. Phase 4 integrates What If? calculations. PDF/OCR, generalized bank adapters, account-balance reconciliation, and advanced overlap resolution remain outside this phase.
