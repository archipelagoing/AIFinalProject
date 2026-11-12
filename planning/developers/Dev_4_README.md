# Dev 4 implementation guide

**Product slice:** Runtime to reliable journey — safe tool execution, adapter/runtime integration, consumer-device performance, and end-to-end reliability.

> This guide lists your 24 primary tickets and required risk-partner work. It is generated from the authoritative planning backlog; do not mark a ticket complete without the specified evidence and cross-owner review.

## Definition of done for every ticket

- Implement only the approved scope and retain the product's local-first/evidence-backed guarantees.
- Run the stated verification command using synthetic fixtures.
- Link the PR, test output, and screenshot/log/JSON evidence.
- Obtain the named cross-owner review and record pass/fail against acceptance criteria.

## Required risk-partner contributions

- **CMP-1112-D2-04 — Tool schemas and evidence IDs** (primary: Dev 2): Implement and test the user-visible invalid-tool/evidence error state.
- **CMP-1126-D2-01 — Finance 100-case benchmark** (primary: Dev 2): Automate the benchmark artifact view and verify a clean-machine run.

## Primary ticket backlog

## Gate 1 — Foundations

### CMP-1112-D4-01 — Compass design system

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver compass design system for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement brand tokens, typography, spacing, dark/light contrast, accessible components.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Tokens documented; contrast checked.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D4-02 — Navigation and import flow

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver navigation and import flow for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build routes, home, import and transaction review shell with fixture-backed data.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Keyboard accessible and responsive.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D4-03 — Chat visual language

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver chat visual language for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Create assistant/user messages, local-AI badge, evidence chips and tone selector.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Chat shell supports mocked and real API states.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D4-04 — Constrained tool-call parser

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver constrained tool-call parser for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement model output schema, allowlist, argument validation, bounded retries and safe abstention.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Malformed model outputs cannot execute tools.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D4-05 — End-to-end smoke harness

**Priority/type/estimate:** P0 · Test · 5 hours

**Goal:** Deliver end-to-end smoke harness for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Set up Playwright or equivalent and screenshot baseline across import/home/chat.

**Target code areas:** `compass/importer.py`, `compass/mapping.py`, `compass/db.py`, `fixtures/`, `tests/python/`

**Contract and safeguards:** Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

**Non-goals:** Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** CI executes one navigable browser test.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 2 — Vertical Slice

### CMP-1114-D4-01 — Home-to-Wrapped navigation

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver home-to-wrapped navigation for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build Wrapped entry, story progress, resume and empty-state components.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Accessible on mobile and desktop.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D4-02 — Chart primitives

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver chart primitives for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement reusable bar, heatmap, slope and guess-versus-actual components with accessible tables.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Fixtures render correctly with no misleading axes.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D4-03 — Cross-team integrated demo

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver cross-team integrated demo for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Own import -> correct -> chat -> X-Ray smoke run and defect list.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** All four flows demonstrated on one fixture.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 3 — Wrapped Alpha

### CMP-1119-D4-01 — Model adapter inference service

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver model adapter inference service for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Load tuned adapter and connect chat API, with explicit model identity.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D4-03 — Previous gate integration for Dev 4

**Risk partner:** Dev 3 — Verify model identity, fixture-only responses, and safe handoff to constrained tools.

**Acceptance:** Model can answer on fixture and logs model version only.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D4-02 — Pig state machine and chat integration

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver pig state machine and chat integration for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Define idle/listening/thinking/reveal/supportive states and connect to chat lifecycle.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No arbitrary model-generated code; states validated.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D4-03 — Wrapped seven-card flow

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver wrapped seven-card flow for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Assemble shared components into story progression, skip/revisit and drilldowns.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** All cards load from real API.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D4-04 — Confessional screen and context controls

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver confessional screen and context controls for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build optional user explanation input, consented memory control and follow-up UX.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** User can decline; explanation not treated as verified transaction fact.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D4-05 — Cross-dev Wrapped integration

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver cross-dev wrapped integration for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Merge Dev1 heatmap, Dev2 awards/guess, Dev3 narration and Dev4 flow.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Single story renders correctly end-to-end.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 4 — End-to-End Beta

### CMP-1121-D4-01 — Tuned vs baseline interim evaluation

**Priority/type/estimate:** P1 · Research · 3 hours

**Goal:** Deliver tuned vs baseline interim evaluation for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run identical held-out cases for base and tuned model.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D4-05 — Previous gate integration for Dev 4

**Risk partner:** Dev 3 — Audit held-out split integrity and reproduce the paired failure examples.

**Acceptance:** Preliminary paired metrics and failure examples saved.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D4-02 — Full Wrapped UI beta

**Priority/type/estimate:** P2 · Feature · 3 hours

**Goal:** Deliver full wrapped ui beta for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Polish guessing, charts, awards, receipts and chat handoff.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** First-time user completes seven-card story.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D4-03 — End-to-end beta test and triage

**Priority/type/estimate:** P1 · Test · 5 hours

**Goal:** Deliver end-to-end beta test and triage for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run scripted upload -> correction -> chat -> Wrapped -> Confessional -> What If -> delete.

**Target code areas:** `tests/`, `scripts/`, `.github/workflows/`, `docs/`

**Contract and safeguards:** Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

**Non-goals:** Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Failures filed with severity and owner.

**Verify:** `python -m pytest -q && npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 5 — Release Candidate

### CMP-1126-D4-01 — Complete user-journey E2E tests

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver complete user-journey e2e tests for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Automate import, correction, chat, Wrapped, X-Ray, What If, settings, deletion.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Green on clean supported machine.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D4-02 — Accessible charts and responsive audit

**Priority/type/estimate:** P2 · Feature · 3 hours

**Goal:** Deliver accessible charts and responsive audit for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Keyboard, labels, contrast, reduced motion, screen-reader alternatives.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Documented WCAG-oriented checks.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D4-03 — Local quantization benchmark

**Priority/type/estimate:** P1 · Research · 5 hours

**Goal:** Deliver local quantization benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Measure quantized model on actual available consumer device; memory, p50/p95 latency.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D4-03 — Previous gate integration for Dev 4

**Risk partner:** Dev 3 — Reproduce the device measurement and check the model/config evidence.

**Acceptance:** Hardware specified and results reproducible.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D4-04 — Pig refinement and fallback

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver pig refinement and fallback for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Refine realistic ceramic design, ensure it does not block chat.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Approved appearance or neutral fallback.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D4-05 — Product performance and onboarding

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver product performance and onboarding for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Optimize load, navigation, install, first-run demo; add helpful empty states.

**Target code areas:** `docs/index.html`, `docs/app.js`, `docs/styles.css`, `app.py`, `tests/`

**Contract and safeguards:** Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

**Non-goals:** Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D4-03 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** 10-minute scripted demo succeeds.

**Verify:** `npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 6 — Robustness Review

### CMP-1128-D4-01 — Model release hardening

**Priority/type/estimate:** P1 · Test · 2 hours

**Goal:** Deliver model release hardening for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Freeze adapter revision, test offline, error handling, and recoverability.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D4-05 — Previous gate integration for Dev 4

**Risk partner:** Dev 3 — Test offline recovery, adapter identity, and model-integration failure handling.

**Acceptance:** No P0/P1 in model integration.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D4-02 — Pilot and UX benchmark finalization

**Priority/type/estimate:** P1 · Research · 5 hours

**Goal:** Deliver pilot and ux benchmark finalization for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run additional short fictional-data user sessions or complete pilot analysis.

**Target code areas:** `tests/`, `scripts/`, `.github/workflows/`, `docs/`

**Contract and safeguards:** Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

**Non-goals:** Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Task outcomes and judgment survey recorded.

**Verify:** `python -m pytest -q && npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D4-03 — Cross-platform smoke and mascot fallback

**Priority/type/estimate:** P2 · Test · 5 hours

**Goal:** Deliver cross-platform smoke and mascot fallback for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Fix responsive, browser and pig animation issues; rehearse complete flow.

**Target code areas:** `tests/`, `scripts/`, `.github/workflows/`, `docs/`

**Contract and safeguards:** Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

**Non-goals:** Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D4-05 — Previous gate integration for Dev 4

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Supported device demo passes.

**Verify:** `python -m pytest -q && npm test`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.
