# Dev 2 implementation guide

**Product slice:** Spending to decisions — financial correctness, deterministic tools, and evidence-backed decision flows.

> This guide lists your 24 primary tickets and required risk-partner work. It is generated from the authoritative planning backlog; do not mark a ticket complete without the specified evidence and cross-owner review.

## Definition of done for every ticket

- Implement only the approved scope and retain the product's local-first/evidence-backed guarantees.
- Run the stated verification command using synthetic fixtures.
- Link the PR, test output, and screenshot/log/JSON evidence.
- Obtain the named cross-owner review and record pass/fail against acceptance criteria.

## Required risk-partner contributions

- **CMP-1114-D3-02 — Training data pipeline** (primary: Dev 3): Audit financial examples, leakage boundaries, and deterministic tool-trace correctness.
- **CMP-1119-D3-01 — SFT/QLoRA training run** (primary: Dev 3): Verify reproducibility metadata and evaluate numeric-grounding cases independently.
- **CMP-1126-D3-03 — Privacy/offline network test** (primary: Dev 3): Verify no financial-data transmission and document the model-download exception.

## Primary ticket backlog

## Gate 1 — Foundations

### CMP-1112-D2-01 — SQLite schema and seed

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver sqlite schema and seed for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Migrations for accounts/imports/transactions/aliases/corrections/conversations/insights/evidence.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Seed command and foreign keys verified.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D2-02 — Monetary conventions and golden tests

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver monetary conventions and golden tests for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Define integer cents, income/refund/transfer handling, periods and currencies.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** Dev 1 — Add edge-case fixtures and independently verify cents/sign/refund/transfer expectations.

**Acceptance:** Ten edge cases have expected outputs.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D2-03 — Core spending tool endpoints

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver core spending tool endpoints for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement merchant/category totals, count, average and net recorded cash flow.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Exact cents match golden fixtures.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D2-04 — Tool schemas and evidence IDs

**Priority/type/estimate:** P0 · Task · 2 hours

**Goal:** Deliver tool schemas and evidence ids for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Pydantic schemas for get_transactions, merchant_summary, category_summary, explain_total.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** Dev 4 — Implement and test the user-visible invalid-tool/evidence error state.

**Acceptance:** Invalid tool arguments rejected; evidence references resolve.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D2-05 — Financial overview frontend card

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver financial overview frontend card for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build responsive spending summary and merchant table consuming real API.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Displays totals and coverage, not mocked numbers.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 2 — Vertical Slice

### CMP-1114-D2-01 — Period comparison tools

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver period comparison tools for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add compare_periods and category trend tools with missing-period warnings.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Correct month delta and zero-denominator behavior.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D2-02 — Financial X-Ray panel

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver financial x-ray panel for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement evidence drilldown listing source transactions, exclusions and coverage.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Every displayed total opens verifiable breakdown.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D2-03 — Tool-to-UI contract tests

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver tool-to-ui contract tests for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Generate typed client and contract fixtures for frontends.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No schema mismatch in CI.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 3 — Wrapped Alpha

### CMP-1119-D2-01 — Insight ranking and deduplication

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver insight ranking and deduplication for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement normalized ranking, eligibility, evidence thresholds and diversity rules.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No repeated same-merchant cards or unsupported claims.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D2-02 — Guess the Damage engine and UI

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver guess the damage engine and ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build estimate submission, absolute/relative error and animated reveal UI.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** $80 vs $143 yields $63; edge cases tested.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D2-03 — What If? tool and scenario widget

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver what if? tool and scenario widget for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement k*average scenario with assumptions, editable input and disclaimer.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Conditional values exact and transparent.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D2-04 — Money Awards generator

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver money awards generator for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement deterministic award selection and award card UI.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Award supported by named metrics and evidence.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D2-05 — Wrapped metrics tests

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver wrapped metrics tests for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Golden tests for MoM, share, streak, ranking, refunds and chart scale.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D2-03 — Previous gate integration for Dev 2

**Risk partner:** Dev 1 — Add source-data and correction/recompute cases to the golden suite.

**Acceptance:** 100% of golden arithmetic cases pass.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 4 — End-to-End Beta

### CMP-1121-D2-01 — Financial X-Ray for every Wrapped card

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver financial x-ray for every wrapped card for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Connect all cards and awards to drilldown, not just overview.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Seven-card source inspection works.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D2-02 — Spending insights and trend charts

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver spending insights and trend charts for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement month-over-month slope and cumulative spend with correct scale.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Comparisons handle missing baseline.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D2-03 — Financial conversation regression

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver financial conversation regression for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Test model calls against exact tool outputs and claim verifier.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D2-05 — Previous gate integration for Dev 2

**Risk partner:** Dev 1 — Add evidence/provenance failure cases and inspect unsupported-claim blocks.

**Acceptance:** Unsupported numeric claims blocked.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 5 — Release Candidate

### CMP-1126-D2-01 — Finance 100-case benchmark

**Priority/type/estimate:** P0 · Research · 5 hours

**Goal:** Deliver finance 100-case benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run exact money tests incl refunds/transfers/rounding and record results.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D2-03 — Previous gate integration for Dev 2

**Risk partner:** Dev 4 — Automate the benchmark artifact view and verify a clean-machine run.

**Acceptance:** Reproducible pass/fail table.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D2-02 — Grounding validator and claims UI

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver grounding validator and claims ui for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Show evidence for amounts and safe abstention for unsupported claims.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Zero unsupported numeric claims in release suite.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D2-03 — Insights ranking ablation

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver insights ranking ablation for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Compare ranking with/without diversity and user relevance; generate charts.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Document ranking sensitivity and limitations.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D2-04 — Scenario/award bug fixes

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver scenario/award bug fixes for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Fix edge cases and integrate missing source links.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No P0/P1 finance issues.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D2-05 — Investor metrics dashboard component

**Priority/type/estimate:** P1 · Research · 5 hours

**Goal:** Deliver investor metrics dashboard component for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build small local demo page for benchmark scorecards and caveats.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D2-03 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** All numbers pulled from result JSON, not hardcoded.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 6 — Robustness Review

### CMP-1128-D2-01 — Benchmark robustness and CIs

**Priority/type/estimate:** P0 · Research · 5 hours

**Goal:** Deliver benchmark robustness and cis for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Compute bootstrap CIs and confusion matrices for finance/tool metrics.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Scripts and raw outputs reproducible.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D2-02 — Stretch: recurring subscription story

**Priority/type/estimate:** P2 · Feature · 3 hours

**Goal:** Deliver stretch: recurring subscription story for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add recurring merchant frequency story card and UI if core green.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D2-05 — Previous gate integration for Dev 2

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Card sourced and inspectable or descoped.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D2-03 — Final numerical audit

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver final numerical audit for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Audit every demo dollar and chart axis, patch defects.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D2-05 — Previous gate integration for Dev 2

**Risk partner:** Dev 1 — Independently reconcile every displayed demo amount and chart axis to golden fixtures.

**Acceptance:** All demo values match golden fixtures.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.
