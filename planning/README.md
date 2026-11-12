# Compass planning and GitHub Issue execution

> **Planning revision in progress:** The 96-ticket backlog and generated developer guides below are the existing allocation, not a newly balanced split. Developer roles remain unassigned for the revision. Thursday and Saturday are separate delivery checkpoints each week. Count integration, review, testing, and report work in each person's workload; Codex access does not assign extra work to its holder.

Start with the [build transition guide](BUILD_TRANSITION.md) to distinguish existing modules from proposed work. Do not regenerate or publish revised assignments until the revised source plan is ready.

This folder is the delivery planning source of truth. It keeps product intent, the 96-ticket backlog, requirement mappings, and the guarded GitHub Issue exporter together.

| File | Purpose |
| --- | --- |
| [Product specification](../PRODUCT_SPEC.md) | Full product, brand, architecture, and formula specification. |
| `COMPASS_ENGINEERING_PLAN.md` | Authoritative 96-ticket implementation plan. Every `CMP-...` item becomes one issue. |
| `COMPASS_COVERAGE_MATRIX.csv` | Candidate requirement-to-ticket mapping; it is not verification evidence. |
| `issue-assignees.example.json` | Copy/edit this with the repository, real Dev 1–4 handles, labels, and deadline milestones. |
| `scripts/markdown_to_github_issues.py` | Standard-library exporter and guarded GitHub Issue creator. |
| `developers/Dev_1_README.md` through `developers/Dev_4_README.md` | Generated per-developer execution guides: primary tickets, risk-partner commitments, acceptance, safeguards, and verification. |

## Issue format

Every implementation issue must have this format. The exporter fills the plan-derived sections; the team supplies concrete repository links, dependencies, estimates, and reviewers before work starts.

```md
# [CMP-1112-D1-03] CSV import and preview endpoint

## Goal
The user outcome this ticket enables.

## Scope
Exact behavior, modules/routes to change, and source-of-truth data.

## Contract
- Inputs and validation rules
- Outputs and example rows/payloads
- Empty, loading, and error behavior

## UX and design requirements
- Relevant Product Spec section
- Responsive and accessibility expectations
- Screenshot/component reference, if applicable

## Non-goals
Explicitly state what this issue must not change.

## Dependencies
- Blocked by: #...
- Blocks: #...
- Shared contract/design: #...

## Acceptance criteria
- [ ] Observable implementation requirement
- [ ] Exact expected result / edge case
- [ ] Test or manual verification result

## Verification and evidence
- [ ] Safe synthetic fixture used
- [ ] Test command and expected result recorded
- [ ] Screenshot/log/JSON artifact linked
- [ ] PR linked
- [ ] Cross-owner review recorded
- [ ] Acceptance marked pass or fail
```

## GitHub fields and conventions

Use the GitHub sidebar and Project fields as structured metadata; do not bury this information only in the body.

| GitHub feature | Required use |
| --- | --- |
| **Title** | `[CMP-ID] concise action title`; preserve the plan ID forever. |
| **Assignee** | One accountable developer, mapped from Dev 1–4. |
| **Labels** | One priority (`priority:P0`, `priority:P1`, `priority:P2`), one area, and one type. Add `needs:review` until cross-owner review passes. |
| **Issue type** | `Feature`, `Task`, `Research`, `Test`, or `Bug` where organization issue types are available. |
| **Milestone** | The deadline milestone assigned by the ticket’s meeting gate. Milestone due dates are the official deadline. |
| **Project** | Add every issue to the Compass MVP Project. Use Status, Owner, Gate, Estimate, Dependency state, Test status, and Evidence URL fields. |
| **Sub-issues** | Make each of the six meeting gates a parent issue. Attach that gate’s CMP tickets as its sub-issues. Do not split already atomic CMP tickets further unless the scope cannot land in one reviewable PR. |

Create these labels before automated issue creation:

```text
priority:P0  priority:P1  priority:P2
area:data  area:finance  area:model  area:frontend  area:qa  area:privacy  area:docs
type:feature  type:task  type:research  type:test  type:bug
needs:review  blocked  risk:financial-correctness
```

Create these deadline milestones before running `--create` (and set their due dates in GitHub):

| Milestone | Deadline / gate | Ticket prefixes |
| --- | --- | --- |
| `Gate 1 — Foundations` | Nov 12, 2026 | `CMP-1112-` |
| `Gate 2 — Vertical Slice` | Nov 14, 2026 | `CMP-1114-` |
| `Gate 3 — Wrapped Alpha` | Nov 19, 2026 | `CMP-1119-` |
| `Gate 4 — End-to-End Beta` | Nov 21, 2026 | `CMP-1121-` |
| `Gate 5 — Release Candidate` | Nov 26, 2026 | `CMP-1126-` |
| `Gate 6 — Robustness Review` | Nov 28, 2026 | `CMP-1128-` |

## Execution order

1. Review the product spec, then freeze the ticket text in the engineering plan.
2. Fill in dependencies, estimates, expected code locations, reviewer, type, priority, and test command for every ticket. Do not invent these at export time.
3. Create the labels, six milestones, and Compass MVP Project above. Set milestone due dates in GitHub.
4. Copy `issue-assignees.example.json` to `issue-assignees.json`; replace the repository and Dev 1–4 placeholder handles.
5. Export JSON and review it as a team. Confirm each ticket has the intended owner, milestone, scope, acceptance criteria, and candidate requirements.
6. Create a three-ticket pilot. Check title, body, labels, assignee, and milestone on GitHub.
7. Create the remaining tickets, then create six meeting-gate parent issues and attach the relevant CMP tickets as sub-issues.
8. Add all issues to the Project. During daily updates, populate Status, Estimate, Test status, and Evidence URL; do not close an issue without evidence and reviewer approval.

## Four-week ownership map

This is a balanced set of **end-to-end product slices**, not four functional silos. Each developer owns visible user-facing work, underlying implementation, automated tests, integration evidence, and cross-review. The individual `CMP-...` issues remain authoritative for implementation and acceptance details.

### Week 1 — Nov 10–14: Trustworthy foundations

**Dev 1 — Import to insight**

Deliver the user’s import → preview → correction journey, including fixtures, provenance, and visible import/review screens.

**Dev 2 — Spending to decisions**

Deliver the user’s first verified spending overview and X-Ray, from exact-cents database rules through real-data UI cards.

**Dev 3 — Model science to interaction**

Deliver the user’s first Ask Compass conversation, from a safe tool router and held-out benchmark through a working chat interface.

**Dev 4 — Runtime to reliable journey**

Deliver the user’s navigable application shell and safe runtime boundary, from shared design tokens and import/review/chat screens through constrained tool execution and a browser smoke test.

### Week 2 — Nov 16–21: Wrapped and beta

**Dev 1 — Import to insight**

Own the coverage/calendar portion of Wrapped: users see what data is included, explore activity, and correct it without losing provenance.

**Dev 2 — Spending to decisions**

Own the insight/decision portion of Wrapped: users guess, see evidence-backed awards, and explore What If? changes.

**Dev 3 — Model science to interaction**

Own the conversational portion of Wrapped: users receive grounded commentary, ask follow-ups, and use the Confessional safely.

**Dev 4 — Runtime to reliable journey**

Own the adapter/runtime portion of Wrapped: users move through a responsive seven-card journey backed by an explicit local model identity, safe state transitions, and accessible controls.

### Week 3 — Nov 23–28: Reliability and release candidate

**Dev 1 — Import to insight**

Make the import and review journey resilient: edge cases, privacy/deletion, missing-account warnings, and their UI evidence.

**Dev 2 — Spending to decisions**

Make every financial interaction defensible: golden calculations, chart/award/scenario checks, and understandable metric presentation.

**Dev 3 — Model science to interaction**

Make conversational behavior measurable: tuned-model comparison, safe tool use, latency, uncertainty, and reproducible model evidence.

**Dev 4 — Runtime to reliable journey**

Make the local product runtime reliable: base-versus-tuned evaluation presentation, consumer-device quantization, accessibility, mobile/responsive behavior, demo flow, and cross-feature end-to-end regression.

### Week 4 — Nov 29–Dec 3: Freeze and submission

**Dev 1 — Import to insight**

Re-run the full import-to-insight journey and document data, preprocessing, privacy, and ethics evidence.

**Dev 2 — Spending to decisions**

Re-run the financial experience and document tools, equations, exact validation, and final result tables.

**Dev 3 — Model science to interaction**

Freeze the conversational experience and document model, fine-tuning, experiments, and measured results.

**Dev 4 — Runtime to reliable journey**

Freeze and harden the model/runtime integration, re-run the full user journey, polish the submission demo, integrate the report, and document UX/runtime evidence.

**Shared gate rule:** Thursday and Saturday meetings are review gates, not start dates. Before each gate, every developer posts completed ticket IDs, a reproducible test/evidence link, a short demo of their user-facing slice, blockers, and the next planned ticket. All four developers must contribute frontend code, tests, integration, and release evidence; no developer is assigned “QA only,” “data only,” or “AI only.” After the Dec. 1 noon ET freeze, no feature work proceeds without all four developers approving and recording an emergency exception.

### Risk and lighter-work balance

The primary-owner count is 24 tickets per developer, but equal ticket counts do not guarantee equal risk. Finance correctness and model behavior are paired across the team. A delivery partner is not a passive reviewer: they must make a visible code, test, benchmark, or integration contribution and co-sign the issue evidence.

| Risk area | Primary owner | Delivery partner | Required partner contribution |
| --- | --- | --- | --- |
| Monetary conventions and golden tests (`CMP-1112-D2-02`) | Dev 2 | Dev 1 | Add edge-case fixtures and independently verify cents/sign/refund/transfer expectations. |
| CSV import and preview (`CMP-1112-D1-03`) | Dev 1 | Dev 3 | Verify imported-row identity is compatible with model evidence references and safe tool inputs. |
| Tool schemas and evidence IDs (`CMP-1112-D2-04`) | Dev 2 | Dev 4 | Implement and test the user-visible invalid-tool/evidence error state. |
| Training-data pipeline (`CMP-1114-D3-02`) | Dev 3 | Dev 2 | Audit financial examples, leakage boundaries, and deterministic tool-trace correctness. |
| Wrapped metric tests (`CMP-1119-D2-05`) | Dev 2 | Dev 1 | Add source-data and correction/recompute cases to the golden suite. |
| SFT/QLoRA run (`CMP-1119-D3-01`) | Dev 3 | Dev 2 | Verify reproducibility metadata and evaluate numeric-grounding cases independently. |
| Financial conversation regression (`CMP-1121-D2-03`) | Dev 2 | Dev 1 | Add evidence/provenance failure cases and inspect unsupported-claim blocks. |
| Adapter inference service (`CMP-1119-D4-01`) | Dev 4 | Dev 3 | Verify model identity, fixture-only responses, and safe handoff to constrained tools. |
| Tuned-versus-baseline evaluation (`CMP-1121-D4-01`) | Dev 4 | Dev 3 | Audit held-out split integrity and reproduce the paired failure examples. |
| Finance 100-case benchmark (`CMP-1126-D2-01`) | Dev 2 | Dev 4 | Automate the benchmark artifact view and verify a clean-machine run. |
| Final paired model benchmark (`CMP-1126-D3-01`) | Dev 3 | Dev 1 | Audit synthetic-data provenance, split integrity, and evidence artifacts. |
| Privacy/offline model test (`CMP-1126-D3-03`) | Dev 3 | Dev 2 | Verify no financial-data transmission and document the model-download exception. |
| Local quantization benchmark (`CMP-1126-D4-03`) | Dev 4 | Dev 3 | Reproduce the device measurement and check the model/config evidence. |
| Model release hardening (`CMP-1128-D4-01`) | Dev 4 | Dev 3 | Test offline recovery, adapter identity, and model-integration failure handling. |
| Final numerical audit (`CMP-1128-D2-03`) | Dev 2 | Dev 1 | Independently reconcile every displayed demo amount and chart axis to golden fixtures. |

**Lighter-work rule:** each developer may own at most one polish/stretch ticket at a time and must pair it with a P0/P1 correctness, safety, or integration contribution in the same gate. Polish work never begins while a paired risk ticket lacks passing evidence. This keeps mascot, transitions, visual refinement, and documentation work valuable without allowing it to crowd out hard engineering.

## Export, review, and create

From the repository root, generate a detailed, reviewable payload without changing GitHub:

```sh
python3 planning/scripts/markdown_to_github_issues.py \
  --output planning/generated/compass-issues.enriched.json \
  --markdown-output planning/generated/compass-issues.enriched.md \
  --developer-guides-dir planning/developers
```

The script validates that the plan has exactly 96 unique tickets. For each issue it exports the Dev 1–4 owner, deadline milestone derived from the CMP prefix, implementation scope, acceptance criteria, required evidence, source line, candidate requirement mappings, proposed priority/type/labels, estimate, code areas, reviewer role, safeguards, and dependencies to confirm at kickoff. Read `planning/generated/compass-issues.enriched.md` before creating anything.

Create and inspect a three-ticket pilot only after the labels and milestones exist:

```sh
cp planning/issue-assignees.example.json planning/issue-assignees.json
# Edit planning/issue-assignees.json with real GitHub handles and repository.
gh auth login

python3 planning/scripts/markdown_to_github_issues.py \
  --config planning/issue-assignees.json \
  --create --limit 3 \
  --confirm "CREATE COMPASS ISSUES"
```

For the full backlog, omit `--limit`. The exporter searches for the exact `[CMP-…]` title in the target repository and skips existing issues, making reruns safe against straightforward duplication. It never creates issues unless both `--create` and the exact confirmation phrase are supplied.

GitHub milestones carry the relevant meeting deadline. If the team needs an individual date in addition to the gate deadline, add a `Target date` date field to the Compass MVP Project and set it during the metadata-enrichment step. The exporter does not create labels, milestones, Projects, or parent/sub-issue links; those need to exist before the issue-creation run.
