# Phase 5 — Quality, privacy, release

Completed on 2026-11-10 for the local Compass Alpha 0.1 release candidate. All nine required P0-B checks and the optional UI/integration item have evidence below. Later sprint features and the limits described here remain deferred. The [root README](../../README.md) provides installation, demo, schema, formulas, verification, deletion and privacy instructions.

## Verification

| Check | Evidence |
| --- | --- |
| Python contracts, accounting, scenarios and UI | **271 tests pass** with `python -m pytest -q` |
| Separate GitHub Pages prototype | **17 tests pass** with `npm test` |
| Independent fixture audit | 164 fictional rows; exact Jan–Jun totals; expected files unchanged |
| Classification regression | All 164 reference labels checked in tests; no oracle lookup in production |
| Dependencies | `python -m pip check` passes; runtime manifest reviewed separately from optional browser tooling |
| Deletion | Transactional failure rollback; real-process restart stays empty; fixtures survive and can be reimported |
| Offline privacy inspection | Current tracked text secret-pattern scan, fictional-CSV allowlist, generated-file and config/network-import checks pass |
| Actual browser | Import → snapshot → question/evidence → category correction → replace/add scenario → actual server restart; saved correction retained |
| Responsive layout | Chromium 1280×900 and emulated 390×844; no page horizontal overflow; scenario arithmetic/warnings readable |
| Runtime network boundary | Browser requests monitored with non-loopback routes blocked; temporary backend guarded against non-loopback socket connections; no external attempts observed with Ollama disabled |
| Recorded demo | [72.76-second fictional-data MP4 and screenshots](demo/README.md) |

The pure-money suite covers signs, decimal precision/rejection of fractional cents, refunds, transfers, unknowns, category overrides, date/category filtering, and exact What If? arithmetic. Import regressions cover malformed input, interrupted insertion rollback, repeated files, legitimate same-day identical purchases, conflicting IDs and correction-preserving reimports. Invalid values and signed-integer overflow cannot produce an old financial result as a new answer.

The six Phase 5 tests add logical deletion, failure rollback and nested-transaction protection, true-process persistence, fixture preservation, ignore/config checks, redacted secret-pattern findings, deletion error UX, and one complete clean AppTest story. The browser smoke adds actual Chromium controls, process restart, mobile layout, and confirmation/deletion/reload checks. The optional local-model router remains tested through simulated protocol/failure cases; no real installed-model inference is claimed.

## Local deletion

Open **Privacy and local data**, acknowledge deletion, type **DELETE**, and press **Clear all local data**. The button is disabled until both acknowledgments are present. `db.clear_all_data` enables SQLite deleted-cell overwriting and atomically deletes transactions, import settings and import metadata in foreign-key-safe order. Failures roll back every table; pending caller transactions are not committed implicitly. The schema remains available for fresh imports.

After success, the current session's uploaded-file widget is replaced, all session keys are cleared, app cache APIs are cleared, and the app reruns into empty state. Compass persists no uploaded CSV copies and has no app-owned persisted financial caches beyond SQLite, so it never traverses arbitrary upload directories or deletes users' original statements. Fixtures, virtual environments, optional browser binaries, fictional demo artifacts and unrelated files remain untouched.

This is logical deletion. It does not promise forensic erasure from operating-system backups/snapshots, old SQLite journals or RAM. Close/reload other open sessions, which may still hold previously rendered data. The user's actual default database was not cleared during testing; all destructive tests and recordings used temporary databases.

## Privacy inspection and configuration

Production financial code uses local files and SQLite. Its only explicit model-network module is `compass/ollama.py`, using fixed loopback HTTP without proxy/redirect following. It rejects remote-model metadata and requires local-only daemon confirmation; the daemon must actually have cloud disabled. Only the bounded question and validated intent are sent, and monetary totals remain deterministic. An incorrectly configured daemon, external browser extensions and OS/network services are outside the app's guarantee.

Streamlit usage statistics are disabled. The server binds loopback; CORS and XSRF protection remain enabled; upload size is capped at 5 MB; browser exception detail is suppressed. Built-in fonts add no external font URL. Application code does not log full statement contents. Runtime dependencies are Streamlit, JSON Schema validation and their normal dependencies; SQLite is stdlib. pytest is test tooling, and Playwright/browser downloads are optional development tooling. Dependency installation and model/browser downloads require network access separately from financial processing.

`.gitignore` excludes virtual environments, DB/journal/WAL/SHM files, SQLite variants, environment files, private uploads, Python/pytest caches, Streamlit secrets, local data and generated test/recording artifacts. Approved fictional fixtures remain tracked. Only inspected fictional demo media/report files are deliberately copied into `demo/` for publication.

`scripts/audit_privacy.py` reports matched locations without printing possible secret values, inventories installed dependency versions with `--json`, checks configured protections, and rejects tracked CSVs outside approved matching fictional fixtures. This is a heuristic current-file/source/config inspection. It is not a Git-history/binary-secret scan, vulnerability assessment, packet capture, or certification that all dependencies and operating systems are secure. No secret-pattern findings or tracked private/generated data were found in the release candidate; all tracked statement CSVs are the approved fictional copies.

## Reproduction and CI

With the environment active, run:

```sh
python -m pip check
python scripts/audit_fixtures.py
python scripts/audit_privacy.py
python -m pytest -q
npm test
```

Follow the [root README browser-tooling commands](../../README.md#release-smoke-and-recorded-demo) for `scripts/release_smoke.py` and `--record`. The script owns a temporary database and browser profile, never the normal workspace. Video uses eight timed checkpoints; mobile/deletion checks follow the recording. Reports/screenshots are generated in ignored `artifacts/release/`. CI runs Python 3.11/3.12 contract/privacy checks plus a Chromium smoke job, and publishes only fictional smoke artifacts.

## Known limits

No authentication, encryption at rest, account-balance reconciliation, PDF/OCR, currency conversion, arbitrary question/date/account filters, saved scenarios, or statistically validated forecasting is provided. Data coverage may be incomplete; unknowns stay excluded and visible. Rent identification is conservative and can require manual confirmation. UI layout was checked in Chromium emulation, not on a physical phone or every browser. Fresh install steps are documented for macOS/Linux/Windows, but this release's local execution used macOS/Python 3.12 and CI targets Linux. Real Ollama inference remains an optional follow-up smoke test. These limitations are disclosed rather than presented as production readiness.
