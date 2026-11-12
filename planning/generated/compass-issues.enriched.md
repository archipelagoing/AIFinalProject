# Compass enriched GitHub Issue review

> Local review artifact. Validate proposed priorities, paths, dependencies, estimates, and labels before creating GitHub Issues.

# [CMP-1112-D1-01] Repository and shared API contract

## Goal

Deliver repository and shared api contract for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Create monorepo, Python/TS formatting, CI, issue templates, typed transaction/import schemas and integration mock.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- No blocking issue inferred; confirm shared contracts at kickoff.

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Clean checkout installs; CI green; example request validated.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:task`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 167](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L167)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D1-02] Synthetic two-persona dataset

## Goal

Deliver synthetic two-persona dataset for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Generate two months per persona with refunds, transfers, merchant aliases, duplicate files, incomplete account and 100+ rows.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Golden cents totals independently documented.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 169](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L169)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D1-03] CSV import and preview endpoint

## Goal

Deliver csv import and preview endpoint for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Parse two explicit layouts, retain raw row IDs, handle dates and debit-credit sign conventions.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Two fixtures import; bad rows are identified without silent loss.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** Dev 3
- **Partner contribution:** Verify imported-row identity is compatible with model evidence references and safe tool inputs.
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 171](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L171)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D1-04] PDF import and unsupported-file UX

## Goal

Deliver pdf import and unsupported-file ux for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Support one text PDF format, error on scanned PDFs; wire frontend file-preview component.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

PDF fixture exact; unsupported format shows clear warning.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 173](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L173)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D1-05] Privacy and deletion vertical slice

## Goal

Deliver privacy and deletion vertical slice for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add local file-hash/provenance, no raw statement logs, delete-import endpoint and deletion confirmation UI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Deleted rows cannot be queried; privacy test passes.

## Candidate requirement mapping

- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 175](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L175)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D2-01] SQLite schema and seed

## Goal

Deliver sqlite schema and seed for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Migrations for accounts/imports/transactions/aliases/corrections/conversations/insights/evidence.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Seed command and foreign keys verified.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:task`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 179](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L179)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D2-02] Monetary conventions and golden tests

## Goal

Deliver monetary conventions and golden tests for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Define integer cents, income/refund/transfer handling, periods and currencies.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Ten edge cases have expected outputs.

## Candidate requirement mapping

- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 1
- **Partner contribution:** Add edge-case fixtures and independently verify cents/sign/refund/transfer expectations.
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 181](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L181)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D2-03] Core spending tool endpoints

## Goal

Deliver core spending tool endpoints for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement merchant/category totals, count, average and net recorded cash flow.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Exact cents match golden fixtures.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:task`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 183](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L183)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D2-04] Tool schemas and evidence IDs

## Goal

Deliver tool schemas and evidence ids for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Pydantic schemas for get_transactions, merchant_summary, category_summary, explain_total.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Invalid tool arguments rejected; evidence references resolve.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 4
- **Partner contribution:** Implement and test the user-visible invalid-tool/evidence error state.
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:task`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 185](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L185)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D2-05] Financial overview frontend card

## Goal

Deliver financial overview frontend card for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build responsive spending summary and merchant table consuming real API.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Displays totals and coverage, not mocked numbers.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 187](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L187)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D3-01] Colab hardware and training decision

## Goal

Deliver colab hardware and training decision for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Record nvidia-smi, VRAM, dependencies, Qwen3-1.7B revision/license and 4B feasibility.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Reproducible hardware notebook and model decision record.

## Candidate requirement mapping

- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 191](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L191)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D3-02] Benchmark set and leakage policy

## Goal

Deliver benchmark set and leakage policy for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Create held-out synthetic dialogue split by persona/scenario; label intents, tool calls, tone, grounding.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

At least 150 test cases; no train/test overlap.

## Candidate requirement mapping

- `REQ-11` — End-to-end reliability and release (candidate; unverified)
- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:research`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 193](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L193)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D3-03] Baseline SLM runtime

## Goal

Deliver baseline slm runtime for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run original model on local or Colab benchmark; record latency, invalid calls, tool choice.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Baseline JSONL outputs and reproducible script.

## Candidate requirement mapping

- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 195](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L195)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D3-04] Wrapped story specification

## Goal

Deliver wrapped story specification for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Wireframe seven-card journey, chart encodings, empty states, interaction choreography.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Storyboard approved with each card tied to source metric.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 197](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L197)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D3-05] Chat frontend first slice

## Goal

Deliver chat frontend first slice for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build chat composer, message states, tool activity and evidence-link placeholders.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

User can submit a question and see response/loading/error.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 199](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L199)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D4-01] Compass design system

## Goal

Deliver compass design system for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement brand tokens, typography, spacing, dark/light contrast, accessible components.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Tokens documented; contrast checked.

## Candidate requirement mapping

- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 203](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L203)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D4-02] Navigation and import flow

## Goal

Deliver navigation and import flow for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build routes, home, import and transaction review shell with fixture-backed data.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Keyboard accessible and responsive.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 205](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L205)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D4-03] Chat visual language

## Goal

Deliver chat visual language for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Create assistant/user messages, local-AI badge, evidence chips and tone selector.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Chat shell supports mocked and real API states.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 207](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L207)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D4-04] Constrained tool-call parser

## Goal

Deliver constrained tool-call parser for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement model output schema, allowlist, argument validation, bounded retries and safe abstention.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Malformed model outputs cannot execute tools.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:task`, `needs:review`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 209](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L209)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1112-D4-05] End-to-end smoke harness

## Goal

Deliver end-to-end smoke harness for the Gate 1 — Foundations without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Set up Playwright or equivalent and screenshot baseline across import/home/chat.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

CI executes one navigable browser test.

## Candidate requirement mapping

- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 1 — Foundations
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 211](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L211)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D1-01] Transaction review and correction UI

## Goal

Deliver transaction review and correction ui for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement editable merchant/category/date/amount preview and correction provenance.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Corrected transaction changes aggregates after refresh.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 219](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L219)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D1-02] Duplicate import detection

## Goal

Deliver duplicate import detection for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Detect identical file hashes and repeated rows; distinguish duplicates from legitimate repeats.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No double count; user sees decision.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)
- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 221](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L221)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D1-03] Integration test: upload to chart

## Goal

Deliver integration test: upload to chart for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Write browser/API test from CSV upload to merchant total display.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Golden fixture visible on UI.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 223](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L223)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D2-01] Period comparison tools

## Goal

Deliver period comparison tools for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add compare_periods and category trend tools with missing-period warnings.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Correct month delta and zero-denominator behavior.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 227](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L227)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D2-02] Financial X-Ray panel

## Goal

Deliver financial x-ray panel for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement evidence drilldown listing source transactions, exclusions and coverage.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Every displayed total opens verifiable breakdown.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 229](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L229)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D2-03] Tool-to-UI contract tests

## Goal

Deliver tool-to-ui contract tests for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Generate typed client and contract fixtures for frontends.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No schema mismatch in CI.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 231](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L231)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D3-01] End-to-end tool conversation

## Goal

Deliver end-to-end tool conversation for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Connect SLM -> approved tools -> grounded response -> chat UI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Three questions answered with correct tool calls.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)
- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 235](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L235)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D3-02] Training data pipeline

## Goal

Deliver training data pipeline for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build SFT JSONL with tool traces, empathetic responses, uncertainty and tone variants.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

500+ reviewed/generated examples; schema and leakage checks.

## Candidate requirement mapping

- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** Dev 2
- **Partner contribution:** Audit financial examples, leakage boundaries, and deterministic tool-trace correctness.
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 237](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L237)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D3-03] Chat safety UX

## Goal

Deliver chat safety ux for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement invalid-tool, unavailable-data and uncertainty messages in frontend.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

UI does not fabricate answer when model fails.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 239](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L239)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D4-01] Home-to-Wrapped navigation

## Goal

Deliver home-to-wrapped navigation for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build Wrapped entry, story progress, resume and empty-state components.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Accessible on mobile and desktop.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 243](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L243)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D4-02] Chart primitives

## Goal

Deliver chart primitives for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement reusable bar, heatmap, slope and guess-versus-actual components with accessible tables.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Fixtures render correctly with no misleading axes.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 245](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L245)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1114-D4-03] Cross-team integrated demo

## Goal

Deliver cross-team integrated demo for the Gate 2 — Vertical Slice without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Own import -> correct -> chat -> X-Ray smoke run and defect list.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1112-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

All four flows demonstrated on one fixture.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 2 — Vertical Slice
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 247](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L247)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D1-01] Wrapped data provenance API

## Goal

Deliver wrapped data provenance api for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Expose per-card evidence IDs, import coverage, filters and excluded transactions.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Every story card can open source rows.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 255](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L255)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D1-02] Merchant normalization and correction feedback

## Goal

Deliver merchant normalization and correction feedback for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Support alias overrides and recomputation of summaries.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Alias change updates story and audit trail.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:data`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 257](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L257)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D1-03] Spending calendar data + UI

## Goal

Deliver spending calendar data + ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement daily buckets, refunds and calendar heatmap component.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Correct date cells; screen-reader table available.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 259](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L259)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D1-04] Data quality badges and coverage UX

## Goal

Deliver data quality badges and coverage ux for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add account/date completeness indicators and explain missing imports.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Incomplete data never labeled complete.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 261](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L261)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D1-05] Wrapped contribution integration test

## Goal

Deliver wrapped contribution integration test for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add fixtures for top merchant and busiest day and browser test.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Card values exactly match source data.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:data`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 263](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L263)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D2-01] Insight ranking and deduplication

## Goal

Deliver insight ranking and deduplication for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement normalized ranking, eligibility, evidence thresholds and diversity rules.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No repeated same-merchant cards or unsupported claims.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 267](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L267)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D2-02] Guess the Damage engine and UI

## Goal

Deliver guess the damage engine and ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build estimate submission, absolute/relative error and animated reveal UI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

$80 vs $143 yields $63; edge cases tested.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 269](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L269)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D2-03] What If? tool and scenario widget

## Goal

Deliver what if? tool and scenario widget for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement k*average scenario with assumptions, editable input and disclaimer.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Conditional values exact and transparent.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)
- `REQ-09` — What If? and financial education (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 271](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L271)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D2-04] Money Awards generator

## Goal

Deliver money awards generator for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement deterministic award selection and award card UI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Award supported by named metrics and evidence.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 273](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L273)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D2-05] Wrapped metrics tests

## Goal

Deliver wrapped metrics tests for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Golden tests for MoM, share, streak, ranking, refunds and chart scale.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

100% of golden arithmetic cases pass.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)
- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 1
- **Partner contribution:** Add source-data and correction/recompute cases to the golden suite.
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 275](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L275)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D3-01] SFT/QLoRA training run

## Goal

Deliver sft/qlora training run for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Train Qwen3-1.7B adapter in Colab with pinned config and checkpoints.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Saved adapter, loss curve, GPU metadata, reproducible commands.

## Candidate requirement mapping

- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** Dev 2
- **Partner contribution:** Verify reproducibility metadata and evaluate numeric-grounding cases independently.
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 279](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L279)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D3-02] Tool and conversation specialization

## Goal

Deliver tool and conversation specialization for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Train on tool traces, corrections, nonjudgmental dialogue and context use.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Held-out examples never included in training.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-05` — SLM specialization and constrained orchestration (candidate; unverified)
- `REQ-06` — Everyday conversational experience (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 281](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L281)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D3-03] Piggy bank HTML/CSS prototype

## Goal

Deliver piggy bank html/css prototype for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Create literal ceramic piggy bank with large feather wings and coin slot, not cartoon mascot.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Review against user reference; reduced-motion supported.

## Candidate requirement mapping

- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 283](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L283)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D3-04] SLM-generated Wrapped commentary

## Goal

Deliver slm-generated wrapped commentary for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Generate grounded card narration and suggested follow-up from structured insight objects.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No fabricated numbers in scripted cards.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 285](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L285)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D3-05] Model-driven chat tone UI

## Goal

Deliver model-driven chat tone ui for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Connect Gentle/Direct/Roast to constrained responses and frontend selection.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Same facts in all tones; tone changes only style.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 287](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L287)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D4-01] Model adapter inference service

## Goal

Deliver model adapter inference service for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Load tuned adapter and connect chat API, with explicit model identity.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Model can answer on fixture and logs model version only.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** Dev 3
- **Partner contribution:** Verify model identity, fixture-only responses, and safe handoff to constrained tools.
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 291](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L291)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D4-02] Pig state machine and chat integration

## Goal

Deliver pig state machine and chat integration for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Define idle/listening/thinking/reveal/supportive states and connect to chat lifecycle.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No arbitrary model-generated code; states validated.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)
- `REQ-10` — Accessible, distinctive interface (candidate; unverified)
- `REQ-11` — End-to-end reliability and release (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 293](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L293)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D4-03] Wrapped seven-card flow

## Goal

Deliver wrapped seven-card flow for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Assemble shared components into story progression, skip/revisit and drilldowns.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

All cards load from real API.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 295](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L295)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D4-04] Confessional screen and context controls

## Goal

Deliver confessional screen and context controls for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build optional user explanation input, consented memory control and follow-up UX.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

User can decline; explanation not treated as verified transaction fact.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:privacy`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 297](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L297)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1119-D4-05] Cross-dev Wrapped integration

## Goal

Deliver cross-dev wrapped integration for the Gate 3 — Wrapped Alpha without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Merge Dev1 heatmap, Dev2 awards/guess, Dev3 narration and Dev4 flow.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1114-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Single story renders correctly end-to-end.

## Candidate requirement mapping

- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 3 — Wrapped Alpha
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 299](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L299)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D1-01] Statement formats and correction reliability

## Goal

Deliver statement formats and correction reliability for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add second PDF fixture/layout or robust explicit unsupported notice; reconcile edited imports.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Supported formats pass and unsupported formats fail clearly.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 307](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L307)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D1-02] Wrapped data coverage tests

## Goal

Deliver wrapped data coverage tests for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Test missing months, duplicate rows, partial accounts and refunds across all cards.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No false full-month claim.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)
- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 309](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L309)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D1-03] Privacy settings UI contribution

## Goal

Deliver privacy settings ui contribution for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build export/delete local records screen with confirmation and no telemetry default.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Deletion and export demonstrable.

## Candidate requirement mapping

- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Task
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:task`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 311](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L311)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D2-01] Financial X-Ray for every Wrapped card

## Goal

Deliver financial x-ray for every wrapped card for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Connect all cards and awards to drilldown, not just overview.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Seven-card source inspection works.

## Candidate requirement mapping

- `REQ-04` — Financial tools and source-backed X-Ray (candidate; unverified)
- `REQ-07` — Money Wrapped story and guessing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 315](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L315)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D2-02] Spending insights and trend charts

## Goal

Deliver spending insights and trend charts for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Implement month-over-month slope and cumulative spend with correct scale.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Comparisons handle missing baseline.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 317](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L317)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D2-03] Financial conversation regression

## Goal

Deliver financial conversation regression for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Test model calls against exact tool outputs and claim verifier.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Unsupported numeric claims blocked.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 1
- **Partner contribution:** Add evidence/provenance failure cases and inspect unsupported-claim blocks.
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 319](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L319)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D3-01] Pig integration and accessibility

## Goal

Deliver pig integration and accessibility for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Mount coded pig on chatbot, use semantic labels and static reduced-motion fallback.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Works across viewport and state transitions.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Test
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:model`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 323](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L323)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D3-02] Confessional contextual memory

## Goal

Deliver confessional contextual memory for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Use opt-in local user statements, separate from factual transaction data; support forgetting.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No fabricated motives; opt-out honored.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 325](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L325)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D3-03] Conversation-to-Wrapped integration

## Goal

Deliver conversation-to-wrapped integration for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Enable SLM follow-up from story cards, clarifications and What If? tools.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

User can switch between card and chat without losing context.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 327](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L327)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D4-01] Tuned vs baseline interim evaluation

## Goal

Deliver tuned vs baseline interim evaluation for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run identical held-out cases for base and tuned model.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Preliminary paired metrics and failure examples saved.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)
- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** Dev 3
- **Partner contribution:** Audit held-out split integrity and reproduce the paired failure examples.
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 331](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L331)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D4-02] Full Wrapped UI beta

## Goal

Deliver full wrapped ui beta for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Polish guessing, charts, awards, receipts and chat handoff.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

First-time user completes seven-card story.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 333](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L333)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1121-D4-03] End-to-end beta test and triage

## Goal

Deliver end-to-end beta test and triage for the Gate 4 — End-to-End Beta without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run scripted upload -> correction -> chat -> Wrapped -> Confessional -> What If -> delete.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `tests/`
- `scripts/`
- `.github/workflows/`
- `docs/`

## Contract and safeguards

Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1119-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Failures filed with severity and owner.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q && npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Test
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:qa`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 4 — End-to-End Beta
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 335](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L335)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D1-01] Import and privacy robustness

## Goal

Deliver import and privacy robustness for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Fuzz malformed CSV/PDF, malicious filenames, file size, duplicate detection and local logs.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Security/privacy regression documented.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)
- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 343](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L343)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D1-02] Data export and deletion verification

## Goal

Deliver data export and deletion verification for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Ensure database, imports, conversation memory and caches obey delete behavior.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No recoverable app-level records after deletion on test.

## Candidate requirement mapping

- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 345](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L345)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D1-03] Cross-device setup and data UI

## Goal

Deliver cross-device setup and data ui for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Document and test clean install; build import-format helper in UI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Supported laptop demo works without developer fixes.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 347](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L347)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D1-04] Wrapped coverage/error handling

## Goal

Deliver wrapped coverage/error handling for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Test and fix all incomplete-period and bad merchant scenarios.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No misleading chart or false confidence.

## Candidate requirement mapping

- `REQ-02` — Transaction correctness and editing (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 349](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L349)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D1-05] Data quality benchmark and artifact

## Goal

Deliver data quality benchmark and artifact for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Compute parse accuracy, coverage, correction success on labeled synthetic corpus.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D1-03 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Machine-readable benchmark and UI chart exported.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:data`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 351](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L351)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D2-01] Finance 100-case benchmark

## Goal

Deliver finance 100-case benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run exact money tests incl refunds/transfers/rounding and record results.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Reproducible pass/fail table.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 4
- **Partner contribution:** Automate the benchmark artifact view and verify a clean-machine run.
- **Priority:** P0
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:research`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 355](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L355)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D2-02] Grounding validator and claims UI

## Goal

Deliver grounding validator and claims ui for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Show evidence for amounts and safe abstention for unsupported claims.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Zero unsupported numeric claims in release suite.

## Candidate requirement mapping

- `REQ-06` — Everyday conversational experience (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 357](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L357)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D2-03] Insights ranking ablation

## Goal

Deliver insights ranking ablation for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Compare ranking with/without diversity and user relevance; generate charts.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Document ranking sensitivity and limitations.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)
- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 359](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L359)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D2-04] Scenario/award bug fixes

## Goal

Deliver scenario/award bug fixes for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Fix edge cases and integrate missing source links.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No P0/P1 finance issues.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)
- `REQ-09` — What If? and financial education (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 361](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L361)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D2-05] Investor metrics dashboard component

## Goal

Deliver investor metrics dashboard component for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build small local demo page for benchmark scorecards and caveats.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D2-03 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

All numbers pulled from result JSON, not hardcoded.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 363](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L363)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D3-01] Final paired model benchmark

## Goal

Deliver final paired model benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run base vs tuned on fixed held-out cases; report tool exact match, groundedness, tone.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

JSONL, confidence intervals and error taxonomy.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** Dev 1
- **Partner contribution:** Audit synthetic-data provenance, split integrity, and evidence artifacts.
- **Priority:** P0
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 367](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L367)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D3-02] Usability pilot

## Goal

Deliver usability pilot for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run 3-5 consented fictional-data sessions and collect task, comfort, comprehension.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Anonymized data and limitations.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:privacy`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 369](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L369)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D3-03] Privacy/offline network test

## Goal

Deliver privacy/offline network test for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Test no outbound inference or raw statement telemetry; document model-download exception.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Offline after install works on target machine.

## Candidate requirement mapping

- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)
- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** Dev 2
- **Partner contribution:** Verify no financial-data transmission and document the model-download exception.
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 371](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L371)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D3-04] Failure repair and regression

## Goal

Deliver failure repair and regression for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Fix invalid tools, context overflow, hallucination and unsafe humor.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No P0/P1 model issues.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 373](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L373)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D3-05] SLM explanation UI improvement

## Goal

Deliver slm explanation ui improvement for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Build model status, local-processing disclosure and uncertainty indicators.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D3-03 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Users can tell when AI vs deterministic tool acts.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 375](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L375)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D4-01] Complete user-journey E2E tests

## Goal

Deliver complete user-journey e2e tests for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Automate import, correction, chat, Wrapped, X-Ray, What If, settings, deletion.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Green on clean supported machine.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:test`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 379](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L379)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D4-02] Accessible charts and responsive audit

## Goal

Deliver accessible charts and responsive audit for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Keyboard, labels, contrast, reduced motion, screen-reader alternatives.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Documented WCAG-oriented checks.

## Candidate requirement mapping

- `REQ-08` — Awards, charts and insight ranking (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 381](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L381)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D4-03] Local quantization benchmark

## Goal

Deliver local quantization benchmark for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Measure quantized model on actual available consumer device; memory, p50/p95 latency.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Hardware specified and results reproducible.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** Dev 3
- **Partner contribution:** Reproduce the device measurement and check the model/config evidence.
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 383](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L383)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D4-04] Pig refinement and fallback

## Goal

Deliver pig refinement and fallback for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Refine realistic ceramic design, ensure it does not block chat.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Approved appearance or neutral fallback.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 385](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L385)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1126-D4-05] Product performance and onboarding

## Goal

Deliver product performance and onboarding for the Gate 5 — Release Candidate without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Optimize load, navigation, install, first-run demo; add helpful empty states.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `docs/index.html`
- `docs/app.js`
- `docs/styles.css`
- `app.py`
- `tests/`

## Contract and safeguards

Represent loading, empty, error, and partial-coverage states. Do not present unverified data as a bank-balance reconciliation or a financial recommendation.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not add new product scope, hide data-quality warnings, or substitute mock totals for verified calculations.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1121-D4-03 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

10-minute scripted demo succeeds.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:frontend`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 5 — Release Candidate
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 387](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L387)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D1-01] Import stretch: additional CSV format

## Goal

Deliver import stretch: additional csv format for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add a third supported mapping and UI format selector if P0/P1 cleared.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Fixture import passes or ticket explicitly descoped.

## Candidate requirement mapping

- `REQ-01` — Supported CSV/PDF import and rejection (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:data`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 395](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L395)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D1-02] Privacy adversarial check

## Goal

Deliver privacy adversarial check for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Attempt logs/export/deletion and malicious import failures; patch defects.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Signed privacy checklist and fixes.

## Candidate requirement mapping

- `REQ-03` — Privacy, local operation and deletion (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:privacy`, `type:feature`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 397](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L397)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D1-03] Wrapped integration polish

## Goal

Deliver wrapped integration polish for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Fix heatmap labels, receipts navigation and source coverage regressions.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/importer.py`
- `compass/mapping.py`
- `compass/db.py`
- `fixtures/`
- `tests/python/`

## Contract and safeguards

Preserve raw source fields and row identity. Reject unsupported or ambiguous inputs visibly; never silently infer monetary polarity or discard rows.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not expand supported statement formats beyond the plan or alter immutable source values while implementing this ticket.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D1-05 — Previous gate integration for Dev 1

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No P0/P1 in owned cards.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 1
- **Cross-owner reviewer role:** Dev 2 (financial/data-contract review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:data`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 399](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L399)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D2-01] Benchmark robustness and CIs

## Goal

Deliver benchmark robustness and cis for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Compute bootstrap CIs and confusion matrices for finance/tool metrics.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Scripts and raw outputs reproducible.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:finance`, `type:research`, `needs:review`, `risk:financial-correctness`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 403](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L403)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D2-02] Stretch: recurring subscription story

## Goal

Deliver stretch: recurring subscription story for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add recurring merchant frequency story card and UI if core green.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Card sourced and inspectable or descoped.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 405](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L405)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D2-03] Final numerical audit

## Goal

Deliver final numerical audit for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Audit every demo dollar and chart axis, patch defects.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/contracts.py`
- `compass/analytics.py`
- `compass/questions.py`
- `compass/scenarios.py`
- `tests/python/`

## Contract and safeguards

Use signed integer cents/Decimal conventions and deterministic calculations. Every displayed number must reconcile to source transactions or disclose exclusions.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not replace deterministic arithmetic with model output, estimate missing facts, or change transaction source data.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D2-05 — Previous gate integration for Dev 2

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

All demo values match golden fixtures.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 2
- **Cross-owner reviewer role:** Dev 1 (data/provenance review)
- **Risk delivery partner:** Dev 1
- **Partner contribution:** Independently reconcile every displayed demo amount and chart axis to golden fixtures.
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:finance`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 407](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L407)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D3-01] Model ablation and uncertainty

## Goal

Deliver model ablation and uncertainty for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Compare base/tuned and prompt-only baseline if time; error analysis and CI.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Honest table with N and limitations.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 411](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L411)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D3-02] Stretch: smarter follow-up suggestions

## Goal

Deliver stretch: smarter follow-up suggestions for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add safe evidence-grounded next-question suggestions in chat.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Suggestions execute valid tools only.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P0
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P0`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 413](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L413)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D3-03] Stretch: polished story transitions

## Goal

Deliver stretch: polished story transitions for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Add restrained transitions and keyboard/reduced-motion parity.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/ollama.py`
- `training/ (planned)`
- `evaluation/ (planned)`
- `tests/python/`

## Contract and safeguards

The model may route approved tools and write non-numeric language only. Tool arguments require schema validation; exact monetary calculations remain deterministic.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not grant arbitrary tool/network access or train on real user statements.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D3-05 — Previous gate integration for Dev 3

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No accessibility regressions.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 3
- **Cross-owner reviewer role:** Dev 4 (interaction and safety-state review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Feature
- **Estimate:** 3 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:model`, `type:feature`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 415](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L415)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D4-01] Model release hardening

## Goal

Deliver model release hardening for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Freeze adapter revision, test offline, error handling, and recoverability.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `compass/db.py`
- `app.py`
- `scripts/audit_privacy.py`
- `tests/python/`

## Contract and safeguards

Keep statement data local by default. Do not add telemetry, cloud financial-data transmission, or real statements to fixtures, logs, or model training data.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not claim irreversible erasure from backups or add authentication/encryption scope not approved in the product specification.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

No P0/P1 in model integration.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** Dev 3
- **Partner contribution:** Test offline recovery, adapter identity, and model-integration failure handling.
- **Priority:** P1
- **Issue type:** Test
- **Estimate:** 2 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:privacy`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 419](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L419)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D4-02] Pilot and UX benchmark finalization

## Goal

Deliver pilot and ux benchmark finalization for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Run additional short fictional-data user sessions or complete pilot analysis.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `tests/`
- `scripts/`
- `.github/workflows/`
- `docs/`

## Contract and safeguards

Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Task outcomes and judgment survey recorded.

## Candidate requirement mapping

- `REQ-12` — Evaluation and ACL evidence (candidate; unverified)

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q && npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P1
- **Issue type:** Research
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P1`, `area:qa`, `type:research`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 421](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L421)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.


---

# [CMP-1128-D4-03] Cross-platform smoke and mascot fallback

## Goal

Deliver cross-platform smoke and mascot fallback for the Gate 6 — Robustness Review without weakening Compass's local-first, evidence-backed guarantees.

## Scope

Fix responsive, browser and pig animation issues; rehearse complete flow.

## Implementation map

**Target code areas (confirm in the architecture ticket before implementation):**
- `tests/`
- `scripts/`
- `.github/workflows/`
- `docs/`

## Contract and safeguards

Use synthetic fixtures only. Record reproducible commands and results; failure evidence is as important as a passing screenshot.

## UX and design requirements

Use the relevant interaction and brand requirements in `planning/PRODUCT_SPEC.md`; attach a reviewed screenshot or wireframe when this changes a user-facing screen.

## Non-goals

Do not change fixtures, thresholds, or evaluation splits merely to turn a failing check green.

## Proposed dependency review

- CMP-1112-D1-01 — Repository and shared API contract
- CMP-1126-D4-05 — Previous gate integration for Dev 4

> These are planning dependencies inferred from the delivery sequence. Confirm, remove, or replace them in technical kickoff; do not block work on an unverified link.

## Acceptance criteria

Supported device demo passes.

## Candidate requirement mapping

- No candidate requirement mapping recorded.

> These matrix links are planning candidates, not proof of implementation or verification.

## Evidence and review checklist

- [ ] Automated test or documented manual test completed
- [ ] Verification command run: `python -m pytest -q && npm test`
- [ ] Synthetic fixture or safe test data used
- [ ] Screenshot, log, or JSON artifact attached/linked
- [ ] Pull request linked
- [ ] Cross-owner reviewer recorded
- [ ] Acceptance result marked pass or fail

**Required evidence from plan:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

## Ownership and source

- **Planned owner:** Dev 4
- **Cross-owner reviewer role:** Dev 3 (model-state and accessibility review)
- **Risk delivery partner:** None; standard cross-owner review applies.
- **Partner contribution:** N/A
- **Priority:** P2
- **Issue type:** Test
- **Estimate:** 5 hours (planning estimate; revise after technical kickoff)
- **Suggested labels:** `priority:P2`, `area:qa`, `type:test`, `needs:review`
- **Deadline milestone:** Gate 6 — Robustness Review
- **Plan source:** [`planning/COMPASS_ENGINEERING_PLAN.md` line 423](../blob/main/planning/COMPASS_ENGINEERING_PLAN.md#L423)
- **Product context:** [`planning/PRODUCT_SPEC.md`](../blob/main/planning/PRODUCT_SPEC.md)

Do not mark this issue complete solely because this description exists. Completion requires the acceptance evidence above.

