# Dev 3 implementation guide

**Product slice:** Model science to interaction — training, evaluation, grounded conversation, and meaningful model-driven interaction.

> This guide lists your 24 primary tickets and required risk-partner work. It is generated from the authoritative planning backlog; do not mark a ticket complete without the specified evidence and cross-owner review.

## Definition of done for every ticket

- Implement only the approved scope and retain the product's local-first/evidence-backed guarantees.
- Run the stated verification command using synthetic fixtures.
- Link the PR, test output, and screenshot/log/JSON evidence.
- Obtain the named cross-owner review and record pass/fail against acceptance criteria.

## Required risk-partner contributions

- **CMP-1112-D1-03 — CSV import and preview endpoint** (primary: Dev 1): Verify imported-row identity is compatible with model evidence references and safe tool inputs.
- **CMP-1119-D4-01 — Model adapter inference service** (primary: Dev 4): Verify model identity, fixture-only responses, and safe handoff to constrained tools.
- **CMP-1121-D4-01 — Tuned vs baseline interim evaluation** (primary: Dev 4): Audit held-out split integrity and reproduce the paired failure examples.
- **CMP-1126-D4-03 — Local quantization benchmark** (primary: Dev 4): Reproduce the device measurement and check the model/config evidence.
- **CMP-1128-D4-01 — Model release hardening** (primary: Dev 4): Test offline recovery, adapter identity, and model-integration failure handling.

## Primary ticket backlog

## Gate 1 — Foundations

### CMP-1112-D3-01 — Colab hardware and training decision

**Priority/type/estimate:** P1 · Research · 3 hours

**Goal:** Deliver colab hardware and training decision for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Record nvidia-smi, VRAM, dependencies, Qwen3-1.7B revision/license and 4B feasibility.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Reproducible hardware notebook and model decision record.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D3-02 — Benchmark set and leakage policy

**Priority/type/estimate:** P0 · Research · 5 hours

**Goal:** Deliver benchmark set and leakage policy for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Create held-out synthetic dialogue split by persona/scenario; label intents, tool calls, tone, grounding.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** At least 150 test cases; no train/test overlap.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D3-03 — Baseline SLM runtime

**Priority/type/estimate:** P0 · Research · 5 hours

**Goal:** Deliver baseline slm runtime for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run original model on local or Colab benchmark; record latency, invalid calls, tool choice.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Baseline JSONL outputs and reproducible script.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D3-04 — Wrapped story specification

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver wrapped story specification for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Wireframe seven-card journey, chart encodings, empty states, interaction choreography.

**Target code areas:** `compass/contracts.py`, `compass/analytics.py`, `compass/questions.py`, `compass/scenarios.py`, `tests/python/`

**Contract and safeguards:** Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

**Non-goals:** Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Storyboard approved with each card tied to source metric.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1112-D3-05 — Chat frontend first slice

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver chat frontend first slice for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build chat composer, message states, tool activity and evidence-link placeholders.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** User can submit a question and see response/loading/error.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 2 — Vertical Slice

### CMP-1114-D3-01 — End-to-end tool conversation

**Priority/type/estimate:** P0 · Feature · 5 hours

**Goal:** Deliver end-to-end tool conversation for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Connect SLM -> approved tools -> grounded response -> chat UI.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Three questions answered with correct tool calls.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D3-02 — Training data pipeline

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver training data pipeline for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build SFT JSONL with tool traces, empathetic responses, uncertainty and tone variants.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D3-05 — Previous gate integration for Dev 3

**Risk partner:** Dev 2 — Audit financial examples, leakage boundaries, and deterministic tool-trace correctness.

**Acceptance:** 500+ reviewed/generated examples; schema and leakage checks.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1114-D3-03 — Chat safety UX

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver chat safety ux for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Implement invalid-tool, unavailable-data and uncertainty messages in frontend.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1112-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** UI does not fabricate answer when model fails.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 3 — Wrapped Alpha

### CMP-1119-D3-01 — SFT/QLoRA training run

**Priority/type/estimate:** P1 · Research · 5 hours

**Goal:** Deliver sft/qlora training run for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Train Qwen3-1.7B adapter in Colab with pinned config and checkpoints.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D3-03 — Previous gate integration for Dev 3

**Risk partner:** Dev 2 — Verify reproducibility metadata and evaluate numeric-grounding cases independently.

**Acceptance:** Saved adapter, loss curve, GPU metadata, reproducible commands.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D3-02 — Tool and conversation specialization

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver tool and conversation specialization for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Train on tool traces, corrections, nonjudgmental dialogue and context use.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Held-out examples never included in training.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D3-03 — Piggy bank HTML/CSS prototype

**Priority/type/estimate:** P2 · Feature · 3 hours

**Goal:** Deliver piggy bank html/css prototype for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Create literal ceramic piggy bank with large feather wings and coin slot, not cartoon mascot.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Review against user reference; reduced-motion supported.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D3-04 — SLM-generated Wrapped commentary

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver slm-generated wrapped commentary for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Generate grounded card narration and suggested follow-up from structured insight objects.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No fabricated numbers in scripted cards.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1119-D3-05 — Model-driven chat tone UI

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver model-driven chat tone ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Connect Gentle/Direct/Roast to constrained responses and frontend selection.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1114-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Same facts in all tones; tone changes only style.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 4 — End-to-End Beta

### CMP-1121-D3-01 — Pig integration and accessibility

**Priority/type/estimate:** P2 · Test · 5 hours

**Goal:** Deliver pig integration and accessibility for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Mount coded pig on chatbot, use semantic labels and static reduced-motion fallback.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Works across viewport and state transitions.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D3-02 — Confessional contextual memory

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver confessional contextual memory for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Use opt-in local user statements, separate from factual transaction data; support forgetting.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No fabricated motives; opt-out honored.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1121-D3-03 — Conversation-to-Wrapped integration

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver conversation-to-wrapped integration for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Enable SLM follow-up from story cards, clarifications and What If? tools.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1119-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** User can switch between card and chat without losing context.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 5 — Release Candidate

### CMP-1126-D3-01 — Final paired model benchmark

**Priority/type/estimate:** P0 · Research · 5 hours

**Goal:** Deliver final paired model benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run base vs tuned on fixed held-out cases; report tool exact match, groundedness, tone.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D3-03 — Previous gate integration for Dev 3

**Risk partner:** Dev 1 — Audit synthetic-data provenance, split integrity, and evidence artifacts.

**Acceptance:** JSONL, confidence intervals and error taxonomy.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D3-02 — Usability pilot

**Priority/type/estimate:** P1 · Research · 3 hours

**Goal:** Deliver usability pilot for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Run 3-5 consented fictional-data sessions and collect task, comfort, comprehension.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Anonymized data and limitations.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D3-03 — Privacy/offline network test

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver privacy/offline network test for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Test no outbound inference or raw statement telemetry; document model-download exception.

**Target code areas:** `compass/db.py`, `app.py`, `scripts/audit_privacy.py`, `tests/python/`

**Contract and safeguards:** Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

**Non-goals:** Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D3-03 — Previous gate integration for Dev 3

**Risk partner:** Dev 2 — Verify no financial-data transmission and document the model-download exception.

**Acceptance:** Offline after install works on target machine.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D3-04 — Failure repair and regression

**Priority/type/estimate:** P0 · Test · 2 hours

**Goal:** Deliver failure repair and regression for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Fix invalid tools, context overflow, hallucination and unsafe humor.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No P0/P1 model issues.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1126-D3-05 — SLM explanation UI improvement

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver slm explanation ui improvement for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Build model status, local-processing disclosure and uncertainty indicators.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1121-D3-03 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Users can tell when AI vs deterministic tool acts.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Gate 6 — Robustness Review

### CMP-1128-D3-01 — Model ablation and uncertainty

**Priority/type/estimate:** P1 · Feature · 3 hours

**Goal:** Deliver model ablation and uncertainty for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Compare base/tuned and prompt-only baseline if time; error analysis and CI.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Honest table with N and limitations.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D3-02 — Stretch: smarter follow-up suggestions

**Priority/type/estimate:** P0 · Feature · 3 hours

**Goal:** Deliver stretch: smarter follow-up suggestions for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add safe evidence-grounded next-question suggestions in chat.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** Suggestions execute valid tools only.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.

### CMP-1128-D3-03 — Stretch: polished story transitions

**Priority/type/estimate:** P2 · Feature · 3 hours

**Goal:** Deliver stretch: polished story transitions for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

**Scope:** Add restrained transitions and keyboard/reduced-motion parity.

**Target code areas:** `compass/ollama.py`, `training/ (planned)`, `evaluation/ (planned)`, `tests/python/`

**Contract and safeguards:** The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

**Non-goals:** Do not grant arbitrary tool/network access or train on real user statements.

**Dependencies to confirm:** CMP-1112-D1-01 — Repository and shared API contract; CMP-1126-D3-05 — Previous gate integration for Dev 3

**Risk partner:** No risk delivery partner; obtain the standard cross-owner review.

**Acceptance:** No accessibility regressions.

**Verify:** `python -m pytest -q`; attach PR + test result + screenshot/JSON artifact + reviewer sign-off.
