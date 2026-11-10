# compass. — Four-week developer delivery plan

**Planning baseline:** 2026-11-10, after completed Alpha 0.1 phases 0–5. **Next release:** Alpha 0.2, the interactive monthly audit. **Status:** all work packages below are planned, not implemented. Developer labels are **Dev 1–4**, as requested. Weeks are relative to team kickoff; no calendar availability has been assumed.

[Product README](README.md) · [Alpha build contract](CompassProto1.0/SCOPE.md) · [Brand identity](BRAND_IDENTITY.md) · [Existing release evidence](CompassProto1.0/PHASE5.md)

## 1. Delivery decision and capacity

The foundation already imports CSVs, preserves sources, classifies and corrects transactions, calculates exact totals, answers five question types, exposes evidence, models rent changes, persists records, and deletes local data. Reuse those capabilities. The new work is the participatory experience and its reusable insight layer.

**Sprint 1 / Weeks 1–2:** apply the new identity and complete one guess/reveal/receipts/reflection flow. **Sprint 2 / Weeks 3–4:** make it reliable across changes and repeat sessions, test with users, evaluate claims, and release.

**Capacity assumption:** 20 hours per developer per week, 80 team hours/week, 320 over four weeks. Each weekly row allocates **16 delivery hours**; the remaining **4 hours/person** cover reviews, integration and the weekly gate. Estimates are planning allowances, not commitments of actual availability. If capacity is lower, apply the cut rules before assigning extra work. Do not silently spend integration time twice.

Optional PDF and saved-input work occupy explicit slots inside those allowances. Unused stretch slots become regression/fix time. The core loop has priority over optional scope. No second frontend, second PDF layout, OCR, payments, export system, or predictive model enters this four-week critical path.

## 2. Stable ownership and review partners

| Developer | Primary ownership | Expected paths / interfaces | Review partner |
| --- | --- | --- | --- |
| **Dev 1** | Ingestion, SQLite/migrations, source/merchant metadata, privacy/deletion | Existing `compass/db.py`, `importer.py`, `mapping.py`; proposed `merchants.py` and preference persistence | Dev 2 for data/identity changes; Dev 3 for privacy/consent |
| **Dev 2** | Financial analytics, Insight contract, game math, comparisons, scenario correctness | Existing `analytics.py`, `contracts.py`, `scenarios.py`; proposed `insights.py` and game/story-selection functions | Dev 1 for evidence/coverage; Dev 3 for fact payloads |
| **Dev 3** | Reaction/reflection templates, optional local model, grounding/tone evaluation | Existing `questions.py`, `ollama.py`; proposed `narrative.py` and evaluation fixtures/scripts | Dev 2 for numeric claims; Dev 4 for voice and user choice |
| **Dev 4** | Product integration, brand application, navigation, accessible UI, usability/demo | `app.py`, `.streamlit/config.toml`, screen/component structure, brand guide and browser smoke | Dev 3 for tone; Dev 1 for privacy flows; Dev 2 for financial labels |

New filenames are proposed modules, not files claimed to exist today. Dev 4 owns shared UI composition to reduce conflicting `app.py` edits. Other developers deliver typed results/render contracts and tests; agree before editing shared UI. Dev 1 owns database migrations. Each owner writes tests and documentation for their changes; Dev 4 is not the team's sole tester.

The JavaScript `docs/` app is the existing public demo. Keep it working, but implement new features on Python/Streamlit first. Do not suggest both apps share a database or support identical new features.

## 3. Contracts agreed before implementation

On kickoff Day 1, all four developers review and freeze a version-1 contract within the shared review allowance:

1. **Insight:** metric definition, period/account/category/merchant filters, exact cents/counts, full evidence IDs, exclusions/refunds, coverage, data revision and presentation eligibility. Dev 2 drafts; Dev 1 validates provenance; Dev 3/4 consume it.
2. **Merchant metadata:** exact normalized-description aliases scoped by source/account, unchanged raw descriptions, no fuzzy auto-merging. Dev 1 drafts; Dev 2 consumes the mapping.
3. **Interaction state:** unrevealed/revealed/stale, exact-cent guess, optional reaction, optional context and skip. Dev 4 drafts; Dev 2 owns math; Dev 3 owns copy.
4. **Privacy state:** explicit tone preference, separate Roast opt-in, session-only context, deletion of every new persisted row. Dev 1/3 draft; Dev 4 exposes controls.
5. **Fact slots:** code renders amounts/counts/periods; templates or validated local wording cannot add financial facts. Dev 3 drafts; Dev 2 approves.

Day 2 consumers receive documented example objects for normal, empty, unknown, refund, missing-prior-month and stale states. Mocks are development fixtures, never hard-coded production answers. Contract changes need both producer and consumer review in the same work package.

## 4. Weekly goals at a glance

| Week | Shared outcome | Required end-of-week demo | Decision |
| --- | --- | --- | --- |
| **1 — First branded loop** | Brand applied to shell and one category guess/reveal with receipts | CSV demo → May Groceries guess → $299.78 reveal → evidence | If incomplete, carry the core loop and cancel the PDF spike |
| **2 — Functional interactive Alpha** | Up to three supported cards, guided reflection, basic comparison, choice/tone controls | Guess → reveal → optional reaction → context/skip → receipts → existing What If? | Freeze core contracts; admit only bounded Week 3 extensions |
| **3 — Repeat use and trust** | Corrections/imports invalidate stories; privacy/restart work; pilot feedback fixed | Edit/import → changed card → new reveal; tone off; delete/reload | Freeze features at week's end; cut unfinished stretch work |
| **4 — Evaluation and release** | Reproducible release with measured correctness/usability and disclosed limits | Fresh install → complete audit → evidence → adjustment → restart → deletion | Release only after required gates pass; unresolved blockers are explicit |

## 5. Week 1 — First branded guessing loop

**Goal:** make the product direction visible immediately while preserving the reliable financial foundation.

| Package / owner | Delivery allocation: 16h | Deliverable and handoff | Observable acceptance / reviewer |
| --- | --- | --- | --- |
| **W1-D1 · Dev 1** | 6h migration/metadata contract; 6h exact merchant normalization/alias API; 4h identity/source fixtures | Reusable exact grouping keys; migration approach for preferences/aliases; fixture cases and unchanged source access. Send contract + examples to Dev 2 by Day 2, storage adapter by Day 3. | Same-looking legitimate purchases survive; aliases preserve original descriptions and account scope; no source mutation. Dev 2 reviews. |
| **W1-D2 · Dev 2** | 6h Insight model/validation; 6h guess math/eligibility; 4h evidence and boundary tests | A category-net-spending Insight and game result from existing analytics. Contract/examples to Dev 3/4 by Day 2; working fixture result by Day 3. | May Groceries $299.78; $250.00 guess → −$49.78 signed / $49.78 absolute difference. Every contributing ID reconstructs the result. Empty/unknown/refund cases covered. Dev 1 reviews. |
| **W1-D3 · Dev 3** | 6h fact-slot/voice templates; 6h neutral prompt/reveal/skip/reflection copy; 4h safety and unsupported-input cases | Reviewed deterministic copy with no model dependency, initial tone policy and a supported-state matrix. Copy/slot contract to Dev 4 by Day 2. | Neutral complete path works with Ollama stopped; no generated amount/count or inferred motive; financial evidence/errors contain no humor. Dev 2/4 review. |
| **W1-D4 · Dev 4** | 5h tokens/wordmark/theme; 3h five annotated screen states; 8h shell + guess/reveal + receipts wiring | Apply Paper/Ink/Iris identity to the local shell and first game. Design welcome/import, review, home, Wrapped, Confessional/X-Ray states. Use contract examples before the engine is ready. | Real import → guess → reveal → receipts works; keyboard/focus and skip controls usable; initial 390px/desktop screenshots. Dev 3 reviews copy; Dev 2 verifies labels. |

**Week 1 integration sequence:** Day 1 contracts/ownership; Day 2 API fixtures and screen states; Day 3 first real engine/UI connection; Day 4 merge the full loop; Day 5 run the gate and record gaps. Do not wait until Friday to connect UI and engine.

**Gate:** the loop works from the actual bundled CSVs, not a precomputed story. Existing summaries/Q&A/rent/deletion regressions stay green. New brand implementation is distinguished from the unchanged Pages demo. If the loop fails, Week 2 starts with that blocker and no PDF work.

## 6. Week 2 — Functional interactive Alpha

**Goal:** complete the short Money Wrapped experience and bounded conversation using the shared facts.

| Package / owner | Delivery allocation: 16h | Deliverable and handoff | Observable acceptance / reviewer |
| --- | --- | --- | --- |
| **W2-D1 · Dev 1** | 4h coverage/account-scope metadata; 4h preferences/migration/deletion integration; 8h reserved PDF-or-hardening slot | Account/coverage metadata feeds comparison eligibility. Tone settings persist deliberately and clear atomically. Only after Week 1/core health is green, use the reserved slot for one text-PDF layout; otherwise importer/privacy regression fixes. | Old SQLite data/corrections survive migration/restart. New preference/alias rows clear with confirmed deletion. Any exposed PDF adapter meets CSV validation/provenance standards and rejects scans/other layouts. Dev 2/3 review. |
| **W2-D2 · Dev 2** | 6h category/merchant Insight variants; 4h recorded comparison; 6h deterministic card selection/tests | Up to three eligible cards, exact merchant expense-row counts, same-filter prior-period comparisons and safe unavailable states. Payloads to Dev 3/4 by Day 2; real selection service by Day 3. | Missing month ≠ zero; refunds/transfer/unknown rules explicit; zero/nonpositive prior denominator has no fabricated percent; comparisons retain coverage warnings. Dev 1 reviews. |
| **W2-D3 · Dev 3** | 6h guided Confessional; 4h tone/eligibility templates; 4h one local-model smoke timebox; 2h initial evaluation ledger | One optional context question with acknowledgement/skip/next action; Off/Gentle/Direct and separately consented eligible Roast. Test one already selected local instruct model if hardware/setup permits; keep deterministic fallback complete. | Context never changes money automatically; sensitive/custom/unknown categories stay neutral; unavailable/invalid/timeout model responses fall back. Record actual model/hardware/latency or an explicit unverified result. Dev 2/4 review. |
| **W2-D4 · Dev 4** | 4h Wrapped navigation/cards; 4h reflection/tone controls; 4h receipts/What If? handoff; 4h accessibility/error states | Integrate the full flow with original financial tools always reachable. Implement Off/skip/disagree, visible coverage, immediate/reduced-motion reveal and short Teach Me Why panels. | A new user completes one flow without a model; using What If? requires explicit confirmed inputs; reveal focus/announcement, loading/error and empty states work. Dev 3 reviews; Dev 2 validates labels. |

**Handoff:** Dev 1 coverage and Dev 2 comparison contracts are agreed before Day 2 UI binding. Dev 3 delivers the reflection state machine before Dev 4 builds its controls. Reserve Day 4 for the full journey and Day 5 for the Sprint 1 gate.

**PDF admission:** the eight-hour slot is the entire team delivery budget for this spike, not eight hours per developer. Scope exactly one declared synthetic text-PDF layout, row/page references and explicit rejection of unsupported files. If it cannot pass the standard import tests in that slot, ship CSV-only and record the limitation. Do not defer the core journey to add a parser.

**Sprint 1 gate:** complete guess/reveal/reaction/reflection/receipts/What If? journey; all baseline tests; no model requirement; tone Off default and separate Roast opt-in; truthful coverage; every new stored value included in deletion. Do not label a missing real-model run or unfinished PDF adapter complete.

## 7. Week 3 — Repeat use, integrity, and formative feedback

**Goal:** ensure new records/corrections change the story correctly and the experience remains respectful over more than one interaction.

| Package / owner | Delivery allocation: 16h | Deliverable and handoff | Observable acceptance / reviewer |
| --- | --- | --- | --- |
| **W3-D1 · Dev 1** | 4h alias/coverage edge cases; 4h privacy/restart regression; 4h supported-format freeze; 4h integration or optional saved-input schema support | Reliable metadata changes and deletion across new tables. Document exactly which formats exist. Provide persistence support only if the saved-input gate is met; otherwise improve failure/recovery coverage. | Alias edits preserve raw rows; same-file reimport remains idempotent; partial/missing accounts visible; migration and delete/restart pass. Dev 2/3 review. |
| **W3-D2 · Dev 2** | 4h at-most-two factual awards; 4h revision/invalidation tests; 4h reserved saved-input-or-hardening slot; 4h arithmetic boundaries | Stable selection/eligibility and stale-state behavior. Optional saved scenario inputs reuse the existing calculator and baseline revision; no cached authoritative result. Send award/stale payloads to Dev 4 by Day 2. | Edited classification/import/alias invalidates affected reveal. Saved inputs, if admitted, require explicit recomputation and delete cleanly. Suppress unsupported awards. Dev 1 reviews. |
| **W3-D3 · Dev 3** | 6h tone/consent/adversarial matrix; 4h negative and sensitive-topic cases; 2h context reset/skip behavior; 4h evaluation instrumentation | Test prompt-like merchant text, attempted numeric changes, Roast without consent, discomfort/skip and context-free operation. Measure local routing only where it actually runs. | No sensitive-target jokes or added financial facts in acceptance cases. Off/reset takes effect immediately. Observed failures enter the ledger rather than being hidden by averages. Dev 2/4 review. |
| **W3-D4 · Dev 4** | 4h 2–3 pilot sessions and synthesis; 6h highest-impact fixes; 4h keyboard/mobile/reduced-motion checks; 2h award presentation | Run short fictional-data pilot tasks and fix confusion in guess/reveal/receipts/skip. Add award UI only after the core states are stable. | Report task completion, misread definitions, comfort and observed blockers; publish redacted findings, screenshots and unresolved accessibility issues. Dev 3 reviews study/copy; Dev 1 reviews privacy. |

**Saved-input admission:** W3-D2's four-hour implementation slot may use at most the already reserved four-hour W3-D1 schema-support slot: eight combined delivery hours total. It does not add capacity. If migration/deletion/revision handling is incomplete, drop persistence and keep existing session-only scenarios. Persistent goals and automated plan monitoring remain deferred.

**Gate:** a demonstrated classification correction and additional import refresh all affected cards/answers; old reveals are visibly stale or cleared. Tone can be turned off; context can be skipped; restart/deletion cover all new persisted data. End the week with feature freeze. Keep a known-issues list and cut unfinished awards, saved inputs, PDF work or animation instead of carrying unstable optional features into Week 4.

## 8. Week 4 — Evaluate, package, and release

**Goal:** prove the bounded experience works for a fresh user and make every accuracy/privacy/product claim traceable.

| Package / owner | Delivery allocation: 16h | Deliverable and handoff | Observable acceptance / reviewer |
| --- | --- | --- | --- |
| **W4-D1 · Dev 1** | 4h import/migration regressions; 4h clean-workspace/restart/delete tests; 4h format/setup docs; 4h privacy inspection | Frozen supported-input matrix, migration/deletion evidence, clean setup steps and scoped network/logging report. | No new raw data in logs/artifacts; no external financial-data attempts in default smoke; private artifacts ignored; new/old databases load and clear. Dev 3 reviews. |
| **W4-D2 · Dev 2** | 6h reference results and claim reconstruction; 6h financial/insight regression; 4h benchmark package | Reproducible fixture totals, all new Insight definitions, full contributing-ID checks, guess/compare/award/scenario edge cases. | Zero known incorrect monetary/count/period claims in release cases. Ground truth remains evaluation-only; no dropped genuine duplicates. Dev 1 reviews independently. |
| **W4-D3 · Dev 3** | 8h fixed-set evaluation; 4h tone/grounding review; 4h model/evaluation report | Freeze 40 cases: 20 supported (five existing tools × four variants), 10 unsupported/ambiguous, 10 malformed/adversarial. Add narrative fact/tone cases separately. If a local model is available, compare matched tool-grounded/model-only offline fictional cases; otherwise report deterministic results and the unrun comparison. | Report tool accuracy denominator, abstention, supported numeric-claim count, timeout/fallback rate and latency. Never present fallback success as model accuracy or a missed run as a benchmark. Dev 2 reviews. |
| **W4-D4 · Dev 4** | 6h remaining user sessions/synthesis; 4h blocker fixes; 3h new 60–90s audit demo; 3h release/presentation | Complete the target 5–8 total formative participants where available, release walkthrough and new branded demo with evidence, context/skip and voluntary adjustment. Update README/status only after verified gates. | Fresh participant can complete the core flow without coaching; record help needed and discomfort. Release assets contain only fictional data. No unimplemented feature appears as shipped. Dev 3/1 review. |

All developers help recruit through separately agreed, consented arrangements and may facilitate sessions within the shared integration allowance. Do not collect real statements, record private screen content, or promise a participant count before recruitment. If fewer than five are available, report the smaller sample and its limits; do not replace missing participants with invented observations.

**Release sequence:** Day 1 freeze fixtures/evaluation cases and supported features; Days 2–3 run studies/regressions and fix blockers; Day 4 clean install, privacy smoke and new recording; Day 5 independent cross-review, report and handoff. Re-run checks affected by fixes, rather than repeatedly rerunning everything without a change.

**Gate:** the [Alpha release contract](CompassProto1.0/SCOPE.md#9-alpha-02-release-gate) passes on declared hardware and fixtures; zero unresolved critical accuracy/data-loss/privacy defects; documented exceptions for optional/unrun work; a complete reproducible demo and named evidence owners.

## 9. Integration rhythm and definition of done

Each developer's weekly **4 shared hours** are reserved for 1h contract/planning review, 2h pairing/PR review/integration, and 1h gate/demo/retrospective. Producer/consumer pairs join the same session, so count the time against both people's capacity. Keep remaining delivery estimates honest when availability changes.

Use a short branch and reviewable PR for each package (`W1-D1`, etc.). Include the package ID, concrete behavior, dependencies, relevant tests, screenshots for UI, and remaining limitations. Integrate the real path by midweek; do not merge four isolated systems on Friday. A direct `main` push is not a substitute for the team's agreed review process.

A package is done when its producer contract, consumer integration, normal/empty/error states, relevant tests, privacy impact and documentation are reviewed. A pure engine function alone is not a completed user journey. Optional features that miss their gate are documented as deferred and absent from release claims.

For new persisted state, require migration/restart/deletion tests. For financial claims, require exact cents/counts and full source reconstruction. For UI, require actual rendered desktop/narrow checks and keyboard/reduced-motion review. For model work, record actual model/version/hardware/prompt/schema and measured outcomes; simulated protocol tests alone do not establish inference quality.

## 10. Product and AI evaluation protocol

Use a small within-person formative comparison: ordinary summary and interactive review on equivalent fictional datasets, with order balanced across participants. Use matched but different periods/categories to reduce answer memorization. Do not call this a statistically powered controlled trial. A separate 10–15-person discovery study and dashboard/static/interactive three-arm experiment are future work.

Record completion without help, time to find the correct spending/evidence, recall/definition errors, estimate error before reveal, perceived comfort/judgment, skipped humor, preferred tone and stated willingness to return. A second-session estimate comparison is useful only if actually scheduled; disclose missing follow-up. Willingness to return/pay is stated preference, not observed retention/revenue.

Engine correctness has a separate oracle-based benchmark. Numeric grounding is supported numeric claims divided by all numeric claims actually emitted; abstentions have their own metric. Report both failures and the size/scope of the case set. No generated confidence percentage or overall “financial health” score enters the product.

## 11. Risk ownership and cut order

| Risk / trigger | Owner | Response |
| --- | --- | --- |
| Incorrect money/count/provenance or lost rows | Dev 2 + Dev 1 | Stop release; fix and add regression before any narrative/UI polish |
| Revealed story survives a contributing edit | Dev 2 + Dev 4 | Invalidate by revision, clear stale result, require new reveal |
| Humor feels judgmental or targets a sensitive category | Dev 3 + Dev 4 | Disable that template/tone; use neutral facts; preserve skip/off |
| Model setup/inference fails or exceeds bounds | Dev 3 | Keep deterministic path; document hardware/result; cut generative wording |
| Streamlit customization becomes a framework rewrite | Dev 4 | Apply achievable theme/components; cut elaborate motion; keep one frontend |
| PDF spike misses eight-hour contract | Dev 1 | Keep CSV-only; document unsupported files; no second layout/OCR |
| New stored preference/alias/input survives deletion | Dev 1 | Release blocker; migrate deletion atomically and test restart |
| Recruitment is smaller than target | Dev 4 | Report real sample and limitations; do not claim retention or statistical effect |

**Protect:** import integrity, exact facts, evidence, incomplete-data handling, consent/deletion, one complete branded loop and existing What If?. **Cut first:** elaborate motion/theme variants → extra awards → saved inputs → PDF → model-generated wording. No cut may hide a regression, invented amount or missing source evidence.

## 12. First kickoff checklist

- [ ] Confirm actual weekly availability against the 20h/person assumption and choose kickoff dates.
- [ ] Dev 1–4 accept the ownership/review map; record handles when available.
- [ ] Freeze v1 Insight/merchant/state/consent contracts and synthetic examples.
- [ ] Dev 4 publishes five annotated states using the brand guide.
- [ ] Select one target model/hardware only for the timeboxed optional smoke.
- [ ] Create package issues with the weekly acceptance criteria; do not mark planned work complete from this document.

The existing [phase checklist](CompassProto1.0/ProtoToDo.md) remains historical evidence of Alpha 0.1. This document is the current Alpha 0.2 delivery plan; weekly package evidence belongs in implementation PRs and an updated status section when work actually lands.
