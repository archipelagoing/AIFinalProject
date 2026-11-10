# Compass browser walkthrough

Verified on 2026-11-10 against the [published prototype](https://archipelagoing.github.io/AIFinalProject/), application source at commit `b6436d9`. This report records observed behavior; the authoritative implementation checklist remains [ProtoToDo.md](ProtoToDo.md).

## Verified behavior

| Check | Observed result |
| --- | --- |
| Fresh workspace | Empty state, disabled month selector, import and fictional-demo controls appeared. |
| Demo import | Loaded 164 transactions across two accounts; May selected. |
| May summary | Income $3,700.00; net expenses $2,952.94; verified surplus $747.06. |
| Missing rent confirmation | Replacement scenario withheld its result and requested confirmation. |
| Replacement rent | Replacing confirmed $1,275 rent with $1,500 produced $522.06 monthly and $3,132.36 over six static months. |
| Additional rent | Adding $1,500 produced −$752.94 monthly and −$4,517.64 over six static months. Shortfall and both-rents-count warnings appeared. |
| Restaurant question | May answer was $81.86. Expanded evidence listed T0112 ($12.79), T0119 ($27.38), T0124 ($9.60), and T0132 ($32.09). |
| Category correction | Changed T0132 (Starbucks) from Restaurants to Groceries. Table showed the correction and reviewed flag. Restaurant answer recalculated to $49.77 with three source rows. |
| Browser persistence | Reloaded the page and asked again; $49.77 remained, confirming that the correction and imported data survived reload. |
| June warning | “What was my surplus in June?” returned $1,711.45 and explicitly flagged one unresolved transaction with $80.00 excluded. |
| Restore classification | Restored T0132's rule classification. Table returned to Restaurants, unchanged −$32.09 source amount, and 0/28 May rows reviewed. |
| Narrow layout | Resized the native Chrome window to approximately 520 pixels wide at 100% zoom. Navigation, month/import controls, three metrics, stacked charts, and clear-data dialog were readable in screenshots. |
| Dialog keyboard controls | Opening clear-data focused the close control; Tab moved to the confirmation checkbox; Escape closed the dialog without deleting data. |

The desktop overview and both scenario outputs were also inspected in screenshots. No functional defect was identified in the exercised flow. This is a bounded smoke test, not an exhaustive accessibility, mobile-device, security, or cross-browser assessment.

## Remaining verification

- End-to-end uploaded-file selection and visible malformed-file/overlap errors. The parser and atomic rejection paths pass automated tests; the OS file-picker journey was not exercised.
- Actual confirmed browser data deletion, followed by reload and demo reimport. Only the dialog and non-destructive keyboard dismissal were exercised. Storage deletion passes the automated adapter test.
- Physical phone testing and narrower widths, including horizontally scrolling transaction tables.
- Complete keyboard-only task completion and screen-reader testing. Tab and Escape in one native dialog do not establish accessibility conformance.
- A 60–90 second demo recording. Existing README instructions provide a script; no recording was created.

## Automated baseline

`npm test` passed all 17 tests before this walkthrough. That includes all 164 reference classifications, six exact monthly summaries, atomic and duplicate imports, source-preserving corrections, five question intents, scenario arithmetic, and storage-adapter behavior.

## Suggested next work

Finish uploaded-file and deletion walkthroughs, then record the fictional-data demo. Keep the separate BNPL opportunity assessment outside this prototype's scope until that product direction is explicitly selected. Python/SQLite and local-SLM research remain later work under the original specification.
