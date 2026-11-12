# Dev 1 implementation guide

**Product slice:** Import to insight — data provenance, import/review experience, and financial evidence.

> This guide lists your 24 primary tickets and required risk-partner work. It is generated from the authoritative planning backlog; do not mark a ticket complete without the specified evidence and cross-owner review.

## Definition of done for every ticket

- Implement only the approved scope and retain the product's local-first/evidence-backed guarantees.
- Run the stated verification command using synthetic fixtures.
- Link the PR, test output, and screenshot/log/JSON evidence.
- Obtain the named cross-owner review and record pass/fail against acceptance criteria.

## Required risk-partner contributions

- **CMP-1112-D2-02 — Monetary conventions and golden tests** (primary: Dev 2): Add edge-case fixtures and independently verify cents/sign/refund/transfer expectations.
- **CMP-1119-D2-05 — Wrapped metrics tests** (primary: Dev 2): Add source-data and correction/recompute cases to the golden suite.
- **CMP-1121-D2-03 — Financial conversation regression** (primary: Dev 2): Add evidence/provenance failure cases and inspect unsupported-claim blocks.
- **CMP-1126-D3-01 — Final paired model benchmark** (primary: Dev 3): Audit synthetic-data provenance, split integrity, and evidence artifacts.
- **CMP-1128-D2-03 — Final numerical audit** (primary: Dev 2): Independently reconcile every displayed demo amount and chart axis to golden fixtures.

## Primary ticket backlog

## Gate 1 — Foundations

### CMP-1112-D1-01 — Repository and shared API contract

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver repository and shared api contract for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Create monorepo, Python/TS formatting, CI, issue templates, typed transaction/import schemas and integration mock.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** Confirm at technical kickoff; no inferred blocker.

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Clean checkout installs; CI green; example request validated.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D1-02 — Synthetic two-persona dataset

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver synthetic two-persona dataset for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Generate two months per persona with refunds, transfers, merchant aliases, duplicate files, incomplete account and 100+ rows.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Golden cents totals independently documented.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D1-03 — CSV import and preview endpoint

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver csv import and preview endpoint for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Parse two explicit layouts, retain raw row IDs, handle dates and debit-credit sign conventions.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** Dev 3 — Verify imported-row identity is compatible with model evidence references and safe tool inputs.

**Acceptance:** Two fixtures import; bad rows are identified without silent loss.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D1-04 — PDF import and unsupported-file UX

**Priority/type/estimate:** P0 · Feature · 5 hours

**Goal:** Deliver pdf import and unsupported-file ux for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Support one text PDF format, error on scanned PDFs; wire frontend file-preview component.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** PDF fixture exact; unsupported format shows clear warning.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D1-05 — Privacy and deletion vertical slice

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver privacy and deletion vertical slice for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add local file-hash/provenance, no raw statement logs, delete-import endpoint and deletion confirmation UI.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Deleted rows cannot be queried; privacy test passes.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 2 — Vertical Slice

### CMP-1114-D1-01 — Transaction review and correction UI

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver transaction review and correction ui for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement editable merchant/category/date/amount preview and correction provenance.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Corrected transaction changes aggregates after refresh.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D1-02 — Duplicate import detection

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver duplicate import detection for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Detect identical file hashes and repeated rows; distinguish duplicates from legitimate repeats.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No double count; user sees decision.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D1-03 — Integration test: upload to chart

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver integration test: upload to chart for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Write browser/API test from CSV upload to merchant total display.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Golden fixture visible on UI.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 3 — Wrapped Alpha

### CMP-1119-D1-01 — Wrapped data provenance API

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver wrapped data provenance api for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Expose per-card evidence IDs, import coverage, filters and excluded transactions.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Every story card can open source rows.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D1-02 — Merchant normalization and correction feedback

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver merchant normalization and correction feedback for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Support alias overrides and recomputation of summaries.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Alias change updates story and audit trail.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D1-03 — Spending calendar data + UI

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver spending calendar data + ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement daily buckets, refunds and calendar heatmap component.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Correct date cells; screen-reader table available.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D1-04 — Data quality badges and coverage UX

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver data quality badges and coverage ux for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add account/date completeness indicators and explain missing imports.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Incomplete data never labeled complete.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D1-05 — Wrapped contribution integration test

**Priority/type/estimate:** P1 · Test · 2 hours

**Goal:** Deliver wrapped contribution integration test for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add fixtures for top merchant and busiest day and browser test.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Card values exactly match source data.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 4 — End-to-End Beta

### CMP-1121-D1-01 — Statement formats and correction reliability

**Priority/type/estimate:** P0 · Feature · 5 hours

**Goal:** Deliver statement formats and correction reliability for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add second PDF fixture/layout or robust explicit unsupported notice; reconcile edited imports.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Supported formats pass and unsupported formats fail clearly.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D1-02 — Wrapped data coverage tests

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver wrapped data coverage tests for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Test missing months, duplicate rows, partial accounts and refunds across all cards.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No false full-month claim.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D1-03 — Privacy settings UI contribution

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver privacy settings ui contribution for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build export/delete local records screen with confirmation and no telemetry default.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Deletion and export demonstrable.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 5 — Release Candidate

### CMP-1126-D1-01 — Import and privacy robustness

**Priority/type/estimate:** P0 · Feature · 5 hours

**Goal:** Deliver import and privacy robustness for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Fuzz malformed CSV/PDF, malicious filenames, file size, duplicate detection and local logs.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Security/privacy regression documented.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D1-02 — Data export and deletion verification

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver data export and deletion verification for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Ensure database, imports, conversation memory and caches obey delete behavior.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No recoverable app-level records after deletion on test.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D1-03 — Cross-device setup and data UI

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver cross-device setup and data ui for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Document and test clean install; build import-format helper in UI.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Supported laptop demo works without developer fixes.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D1-04 — Wrapped coverage/error handling

**Priority/type/estimate:** P1 · Test · 2 hours

**Goal:** Deliver wrapped coverage/error handling for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Test and fix all incomplete-period and bad merchant scenarios.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No misleading chart or false confidence.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D1-05 — Data quality benchmark and artifact

**Priority/type/estimate:** P1 · Research · 5 hours

**Goal:** Deliver data quality benchmark and artifact for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Compute parse accuracy, coverage, correction success on labeled synthetic corpus.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D1-03 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Machine-readable benchmark and UI chart exported.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 6 — Robustness Review

### CMP-1128-D1-01 — Import stretch: additional CSV format

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver import stretch: additional csv format for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add a third supported mapping and UI format selector if P0/P1 cleared.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Fixture import passes or ticket explicitly descoped.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D1-02 — Privacy adversarial check

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver privacy adversarial check for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Attempt logs/export/deletion and malicious import failures; patch defects.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Signed privacy checklist and fixes.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D1-03 — Wrapped integration polish

**Priority/type/estimate:** P2 · Test · 2 hours

**Goal:** Deliver wrapped integration polish for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Fix heatmap labels, receipts navigation and source coverage regressions.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D1-05 — Previous gate integration for Dev 1

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No P0/P1 in owned cards.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.
