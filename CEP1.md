# Compass engineering execution plan — 96 issues and verification

**Companion to [`README.md`](README.md).** This is the authoritative delivery plan, **not a second product specification**. The README controls product scope, formulas, user promises, design, architecture, and the proposed $0 / $8.88 monthly / $88.88 annual / $1.50 Story Pass pricing. The plan controls the 96 tickets, meeting goals, deadlines, evidence requirements, and release verification. Any mismatch requires a reviewed cross-file correction.

**Status:** All requirements and test mappings are planned until supported by code, independently reviewed CI evidence and release artifacts. No ticket is marked passed by this document alone.

**Importing into GitHub:** Each `CMP-...` checklist item below is one issue. Preserve the identifier in the issue title, keep implementation and acceptance text in its body, add owner, milestone, requirement IDs, test IDs, dependencies, estimate, reviewer and evidence links from the issue template. Do not interpret checklist formatting as proof of completion.

**Six meetings:** Nov 12, 14, 19, 21, 26, 28. **All-team Wrapped:** Nov 16–21. **Coding and benchmarks continue:** Nov 28. **Freeze:** Dec 1 at noon ET. **ACL report:** Dec 1–3.

**Coverage matrix:** [`COMPASS_COVERAGE_MATRIX.csv`](COMPASS_COVERAGE_MATRIX.csv) contains candidate links only. Some rows in the previous source summarized additional candidates as “+N”; those are deliberately not invented here. A reviewer must complete the mapping against all 96 issue bodies and add real test IDs before claiming full traceability.

## G7. Revised execution plan — 96 balanced tickets, November 10–December 3, 2026

**This section replaces the earlier 91-ticket plan and the illustrative four-week schedule.** Six meeting gates: Thursday/Saturday on November 12/14, 19/21, 26/28. **Code freeze is Tuesday, December 1**; December 1–3 is the dedicated ACL-style report and submission period. November 26 is US Thanksgiving; use an asynchronous review if needed. The project is a three-week accelerated MVP; no schedule can guarantee a flawless result. The definition of done is evidence-based.

### Workload, ownership, and daily rules

- **96 tickets = 24 per developer**: each developer gets 5 before each Thursday (15) and 3 before each Saturday (9). Each ticket should be one reviewable PR or a small coherent group of commits; tickets are not assumed equal in effort. Estimate hours at kickoff and rebalance by actual hours daily.
- **All four developers write frontend code**, and each also contributes tests, integration, data/model/backend work, and an evaluation artifact. Domain lead is accountable for the feature, not sole implementer.
- **All four build Wrapped simultaneously November 16–21:** Dev 1 owns coverage + calendar UI, Dev 2 guessing/awards/scenarios, Dev 3 SLM commentary and chat transitions, Dev 4 story navigation + mascot. Cross-owner PR review is mandatory.
- Every ticket requires: issue ID, clear scope, input/output contract, synthetic fixture, automated test or documented manual test, screenshot/log, reviewer, PR, acceptance pass/fail. A demo is not proof of all edge cases.
- Daily 7 PM ET async updates: completed ticket IDs, hours spent, test evidence, blockers, next day's plan. Meet Thursdays/Saturdays after tickets are submitted; review failed gates and rebalance workload.
- No real bank records in the training corpus or public demo. SLM performs conversation and constrained tool selection; exact numbers come from deterministic functions. All AI claims that contain numbers require evidence IDs.
- **P0:** financial misstatement, data leak, corrupted import, broken core flow. **P1:** essential feature nonfunctional, persistent tool hallucination, unhandled crash. No P0/P1 at freeze; P2 defects documented honestly.

### Calendar and deliverables

| Date | Individual daily action and team integration gate |
|---|---|
| Tue Nov 10 | Create repository/branches/CI, assign 96 issues, estimate ticket hours, pin API contracts, check Colab GPU, agree synthetic fixture rules. |
| Wed Nov 11 | Each developer completes at least 3 of 5 Nov 12 tickets; pair-review schemas and initial frontend contracts. |
| Thu Nov 12 | Finish remaining 2 tickets before meeting; demonstrate CSV/PDF fixture, exact totals, base SLM and chat UI. |
| Fri Nov 13 | Each developer completes 2 of 3 Nov 14 tickets, integrates against real APIs, posts PR evidence. |
| Sat Nov 14 | Complete third ticket and demo import → correct → ask → inspect X-Ray. Lock tool and story schemas. |
| Sun Nov 15 | Optional buffer; resolve blockers only, no unapproved new scope. |
| Mon Nov 16 | All four begin Wrapped work in parallel; Dev 3 starts data/training preparation; merge chart and story contracts. |
| Tue Nov 17 | Finish ~2 Nov 19 tickets per developer; run early integration tests and inspect first Colab training run. |
| Wed Nov 18 | Finish ~2 more Nov 19 tickets; cross-review Wrapped cards, SLM tool outputs, evidence links. |
| Thu Nov 19 | Finish fifth ticket before meeting; live shared Wrapped demo with model checkpoint and mascot prototype. |
| Fri Nov 20 | Finish 2 of 3 Nov 21 tickets each; integrate all Wrapped parts and run E2E beta suite. |
| Sat Nov 21 | Complete third ticket; demonstrate full import → chat → Wrapped → Confessional → What If → delete journey. |
| Sun Nov 22 | Optional buffer for critical defects and checkpoint backups. |
| Mon Nov 23 | Complete 2 Nov 26 tickets each; run finance, model and privacy benchmarks on frozen test sets. |
| Tue Nov 24 | Complete 2 more Nov 26 tickets; conduct pilot and local inference measurements; triage P0/P1. |
| Wed Nov 25 | Complete fifth Nov 26 ticket and rehearse full release-candidate demo. |
| Thu Nov 26 | Meeting 5: benchmark review and feature-complete candidate; Thanksgiving async review permitted. **Not code freeze.** |
| Fri Nov 27 | Complete 2 Nov 28 tickets each; patch failures; only add stretch work if all core P0/P1 cleared. |
| Sat Nov 28 | Meeting 6: complete third ticket, code/benchmark demos, integration and stretch-feature decisions. **Not a report-only meeting.** |
| Sun Nov 29 | Optional defect repair; prepare final measured artifacts. |
| Mon Nov 30 | Full regression, reproducibility, performance, security and final release review; finalize figures/results JSON. |
| Tue Dec 1 | **12:00 PM ET code freeze:** tag `v1.0-rc`; no feature work afterward. Begin ACL-style paper with assigned sections and actual measurements. |
| Wed Dec 2 | All four write/review ACL sections, regenerate tables/figures, check citations, ethics, limitations, and reproducibility. |
| Thu Dec 3 | Final ACL-style PDF, repository, benchmark artifacts and demo submission; verify receipt. |

### Weekly outcomes and meeting agendas (facilitator-ready)

**Meeting operating rule:** The Thursday and Saturday meetings are **review and decision gates**, not the time to start the tickets due that day. Each developer posts a 2–4 minute screen-recorded demo or reproducible evidence before the meeting. At the meeting, demonstrate the integrated app on the same synthetic fixture, inspect failing tests and benchmark changes, make decisions, and record an owner plus due date for each blocker. Suggested 60-minute format: 5 minutes goal/status, 20 minutes demos (5 per developer), 15 minutes integrated journey and QA, 15 minutes decisions/risks, 5 minutes assignments and written minutes. Meeting 5 may be asynchronous for Thanksgiving. The individual issue details and acceptance tests appear in the ticket backlog immediately below.

#### Week 1 — November 10–14: Trustworthy foundations and first financial conversation

**Weekly outcome:** A synthetic statement can be imported, normalized, calculated exactly, corrected or deleted, and queried through a visible chat flow with evidence links. The untuned SLM baseline and a held-out evaluation set exist before fine-tuning. **Definition of success:** the team can run `import → preview → total → ask → X-Ray` from a clean checkout without fabricated numbers.

##### Meeting 1 — Thursday, November 12: Contracts, data accuracy, and baseline

**Before the meeting: 5 tickets per developer (CMP-1112-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Repository/API contracts; two-persona synthetic fixture with golden totals; two-layout CSV importer; one text-PDF importer and unsupported-file warning; local provenance/deletion vertical slice. Demo both accepted and rejected files, plus deletion. |
| **Dev 2** | SQLite migrations and seed; cents/sign/refund/transfer rules; merchant/category/expense tools; Pydantic tool contracts with evidence IDs; real-data overview UI card. Demo a traceable merchant total and an invalid-argument rejection. |
| **Dev 3** | Colab GPU/model decision record; ≥150 held-out test cases with leakage rules; untuned Qwen3-1.7B benchmark; constrained tool-call parser; chat input/loading/error UI. Demo baseline results and an invalid model tool call being blocked. |
| **Dev 4** | Brand tokens and accessible components; navigation/import/review UI; chat visual language and tone selector; seven-card Wrapped storyboard; Playwright smoke harness. Demo keyboard navigation and the initial browser test. |

**Discussion agenda:** (1) Agree on transaction signs, refunds, transfers, currencies and date boundaries; (2) approve the typed API and evidence-ID format; (3) review Colab VRAM, model feasibility and benchmark leakage policy; (4) approve the seven-card Wrapped storyboard and shared design tokens; (5) identify the most fragile import format and decide what is explicitly unsupported. **Decisions to record:** frozen v0 schemas, supported file formats, model candidate, baseline dataset version, reviewer for each integration PR. **Gate:** exact totals match golden fixtures, clean checkout works, and a baseline benchmark artifact is saved. **If blocked:** reduce supported PDF layouts before compromising arithmetic or provenance.

##### Meeting 2 — Saturday, November 14: First integrated vertical slice

**Before the meeting: 3 tickets per developer (CMP-1114-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Import correction/duplicate/coverage behavior integrated with review UI; demonstrate one corrected merchant and a re-import that does not double-count. |
| **Dev 2** | Month comparisons and source-backed X-Ray outputs connected to UI; demonstrate the exact rows behind a displayed amount. |
| **Dev 3** | SLM-to-tool orchestration and grounded reply path; demonstrate valid and invalid requests, uncertainty and abstention. |
| **Dev 4** | End-to-end import/chat/X-Ray interaction and browser regression; demonstrate complete vertical slice without manual database edits. |

**Discussion agenda:** (1) Run the same `import → correct → ask → receipts` script together; (2) triage any discrepancy between UI and database; (3) lock Insight Object, Wrapped-card and conversation-response contracts; (4) approve training-data categories and human review rubric; (5) assign cross-owner Wrapped PR reviews. **Decisions to record:** v1 story schema, explicit P0/P1 defects, training set size and quality checks, Week 2 integration branches. **Gate:** the full vertical slice works on synthetic records; each numerical answer can be traced to transactions. **If blocked:** prioritize a working single-statement journey over additional file formats.

#### Week 2 — November 16–21: All-team Wrapped, specialized SLM, and conversational beta

**Weekly outcome:** All four developers build Wrapped in parallel, the fine-tuned SLM has a reproducible checkpoint, and the application supports `import → chat → guess → reveal → receipts → Confessional → What If?`. The flying ceramic pig is implemented as HTML/CSS/JS by Dev 4 with state signals from Dev 3; visual polish cannot block the core journey.

##### Meeting 3 — Thursday, November 19: Shared Wrapped alpha and first tuned checkpoint

**Before the meeting: 5 tickets per developer (CMP-1119-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Merchant aliases, source completeness and Wrapped calendar/heatmap frontend; show each day linked to included transactions and a missing-account warning. |
| **Dev 2** | Ranked insights, guessing-game arithmetic, awards and scenario tool/UI; demonstrate correct guess-versus-actual difference and conditional savings. |
| **Dev 3** | Synthetic SFT dataset and Colab QLoRA/LoRA run, saved adapter/checkpoint, tuned-model smoke comparison, SLM-generated grounded story and chat-state schema; show real outputs, not hand-authored copy. |
| **Dev 4** | Seven-card story shell, chart transitions, responsive chat/story navigation, first HTML/CSS/JS ceramic flying-pig implementation; show motion-reduction behavior and SLM state hookup. |

**Discussion agenda:** (1) Each developer presents their own Wrapped card or interaction; (2) run one joined story from real synthetic fixture totals; (3) compare base versus tuned model on a *small development set*, not the locked final test set; (4) inspect tone and shame-risk examples; (5) choose what visual refinements can be deferred. **Decisions to record:** minimum story-card set, adapter version, allowed SLM animation states, integration blockers, targeted fixes for November 21. **Gate:** all four Wrapped contributions render together and the first tuned checkpoint is reproducible. **If blocked:** keep base model as a temporary diagnostic baseline, not a replacement for the fine-tuning deliverable; prioritize one working story over extra transitions.

##### Meeting 4 — Saturday, November 21: End-to-end beta and first model comparison

**Before the meeting: 3 tickets per developer (CMP-1121-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Complete coverage/correction and privacy integration through Wrapped; demonstrate reclassification changing both chart and explanation correctly. |
| **Dev 2** | Complete What If?, X-Ray and award-calculation integration; show deterministic numerical outputs across story and chat. |
| **Dev 3** | Connect tuned SLM to chat/Confessional and evaluate paired base-versus-tuned outputs on a fixed interim split; demonstrate no invented amount and controlled tool invocation. |
| **Dev 4** | Assemble chat, pig states, story transitions and responsive full-journey E2E test; demonstrate keyboard and reduced-motion flows. |

**Discussion agenda:** (1) One teammate unfamiliar with the flow performs the complete beta journey; (2) examine exact calculation and grounding failures; (3) review base/tuned metrics, model latency and checkpoint backups; (4) inspect accessibility and mobile-width layout; (5) decide whether any feature is at risk of missing November 26. **Decisions to record:** beta acceptance result, prioritized P0/P1 list, benchmark owner and pilot participants, hardware target, features requiring hard scope limits. **Gate:** all major product experiences can be completed without developer intervention on supported fixtures. **If blocked:** fix broken core journeys before adding new features.

#### Week 3 — November 23–28: Reliability, investor evidence, and last coding meeting

**Weekly outcome:** Finish and test the README-defined research-grade MVP; gather honest investor-facing evidence for financial correctness, model specialization, privacy, latency, comprehension and user comfort. Meeting 6 remains an engineering meeting. **Code freeze is not until December 1.**

##### Meeting 5 — Thursday, November 26: Release candidate and benchmark review

**Before the meeting: 5 tickets per developer (CMP-1126-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Import edge cases, duplicate/transfer/refund and missing-account coverage, deletion/privacy checks and associated UI warnings; show extraction precision/recall. |
| **Dev 2** | Financial golden-suite, tool-argument/evidence validation, chart/award math, scenario tests and benchmark visualization; show exact accuracy and failure cases. |
| **Dev 3** | Locked-set base-versus-tuned evaluation, tool-selection/grounding/nonjudgment rubric, local model latency/RAM tests and reproducibility notes; show paired results with sample sizes. |
| **Dev 4** | Complete product QA, accessibility, mascot fallback, onboarding/usability pilot and demo packaging; show task completion and perceived-judgment feedback. |

**Discussion agenda:** (1) Review each metric's denominator, test set and evidence artifact; (2) inspect all P0/P1 bugs and privacy issues; (3) compare model quality and consumer-device performance; (4) review pilot feedback without presenting small-sample results as market proof; (5) select November 28 engineering priorities. **Decisions to record:** release-candidate status, defects assigned with due dates, whether one stretch feature is safe, final evaluation protocol, Thanksgiving attendance/asynchronous sign-offs. **Gate:** all essential flows are implemented and measured; no unowned critical bugs. **If blocked:** cancel stretch work and dedicate November 27–30 to reliability.

##### Meeting 6 — Saturday, November 28: Last coding and robustness review

**Before the meeting: 3 tickets per developer (CMP-1128-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Patch import/privacy regressions; rerun offline/deletion/coverage tests; optionally add one supported import enhancement only after all P0/P1 are cleared. |
| **Dev 2** | Fix financial/chart edge cases, run stress and property-based tests, validate all Wrapped statistics and export final metric tables. |
| **Dev 3** | Run model ablations and robustness cases, measure uncertainty/CI and failure categories, optimize local inference or adapter configuration. |
| **Dev 4** | Fix end-to-end UX and accessibility defects, refine pig/chat animations, test responsive performance, and optionally implement one low-risk stretch interaction. |

**Discussion agenda:** (1) Run a fresh-checkout full demo with no hidden setup; (2) inspect automated test dashboard, performance and remaining defects; (3) review ablations and confidence intervals for credible paper/investor claims; (4) approve or reject any stretch feature based on risk; (5) assign November 29–30 final fixes and reproducibility tasks. **Decisions to record:** explicit go/no-go for December 1 freeze, exact remaining bugs with owners, final benchmark run command, version/tag owner, paper figures to regenerate after freeze. **Gate:** a complete release candidate exists with only documented low-severity issues. **If blocked:** all developers swarm P0/P1 defects; no cosmetic work until resolved.

#### Finalization — November 29–December 3: Freeze first, then ACL-style report

**November 29–30 (engineering buffer):** Each developer reruns their own test suite plus one other developer's integration tests, closes regressions, updates documentation and screenshots, and verifies clean setup. Dev 3 freezes the final model/config and benchmark scripts; Dev 2 regenerates numeric result tables; Dev 1 checks data provenance/privacy; Dev 4 checks end-to-end demo and accessibility. Do not change evaluation rules to improve scores after seeing results.

**Tuesday, December 1, noon ET — code freeze:** All four approve the release tag, dependency lockfiles, model adapter hash, fixture hash, benchmark outputs, screenshots, setup steps and known-limitations list. From this point, no planned feature coding; emergency fixes require all four to approve and record the change. **Everyone's final-sprint deliverable includes an ACL-style paper contribution.**

**December 1–3 — ACL report work split:** Dev 1 writes Dataset/Preprocessing/Privacy/Ethics; Dev 2 writes Financial Tools/Equations/Validation; Dev 3 writes Model/Fine-tuning/Experiments/Results; Dev 4 writes Introduction/Related Work/UX/Presentation and integrates ACL LaTeX. Each developer must contribute at least one figure/table, one limitations paragraph, a reproducibility note, and peer review of another section. All four approve abstract, conclusions and final claims. **Thursday, December 3:** submit PDF, repository, model/setup documentation, evaluation artifacts and demo before the actual course deadline.

**Meeting minutes template (copy for all six meetings):** `Date/time | attendees | gate passed? | four demos + PR links | benchmark snapshot (N/version) | P0/P1/P2 defects | decisions made | owner and deadline for each blocker | next meeting's exact demo | action items`. Record metrics as measured, pending or failed—never as presumed success.

### Meeting ticket backlog (each ticket has explicit build and acceptance)

#### Thursday, November 12 — Foundation and baseline

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1112-D1-01 — Repository and shared API contract.** **Implementation:** Create monorepo, Python/TS formatting, CI, issue templates, typed transaction/import schemas and integration mock. **Acceptance:** Clean checkout installs; CI green; example request validated. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-02 — Synthetic two-persona dataset.** **Implementation:** Generate two months per persona with refunds, transfers, merchant aliases, duplicate files, incomplete account and 100+ rows. **Acceptance:** Golden cents totals independently documented. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-03 — CSV import and preview endpoint.** **Implementation:** Parse two explicit layouts, retain raw row IDs, handle dates and debit-credit sign conventions. **Acceptance:** Two fixtures import; bad rows are identified without silent loss. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-04 — PDF import and unsupported-file UX.** **Implementation:** Support one text PDF format, error on scanned PDFs; wire frontend file-preview component. **Acceptance:** PDF fixture exact; unsupported format shows clear warning. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-05 — Privacy and deletion vertical slice.** **Implementation:** Add local file-hash/provenance, no raw statement logs, delete-import endpoint and deletion confirmation UI. **Acceptance:** Deleted rows cannot be queried; privacy test passes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1112-D2-01 — SQLite schema and seed.** **Implementation:** Migrations for accounts/imports/transactions/aliases/corrections/conversations/insights/evidence. **Acceptance:** Seed command and foreign keys verified. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-02 — Monetary conventions and golden tests.** **Implementation:** Define integer cents, income/refund/transfer handling, periods and currencies. **Acceptance:** Ten edge cases have expected outputs. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-03 — Core spending tool endpoints.** **Implementation:** Implement merchant/category totals, count, average and net recorded cash flow. **Acceptance:** Exact cents match golden fixtures. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-04 — Tool schemas and evidence IDs.** **Implementation:** Pydantic schemas for get_transactions, merchant_summary, category_summary, explain_total. **Acceptance:** Invalid tool arguments rejected; evidence references resolve. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-05 — Financial overview frontend card.** **Implementation:** Build responsive spending summary and merchant table consuming real API. **Acceptance:** Displays totals and coverage, not mocked numbers. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1112-D3-01 — Colab hardware and training decision.** **Implementation:** Record nvidia-smi, VRAM, dependencies, Qwen3-1.7B revision/license and 4B feasibility. **Acceptance:** Reproducible hardware notebook and model decision record. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-02 — Benchmark set and leakage policy.** **Implementation:** Create held-out synthetic dialogue split by persona/scenario; label intents, tool calls, tone, grounding. **Acceptance:** At least 150 test cases; no train/test overlap. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-03 — Baseline SLM runtime.** **Implementation:** Run original model on local or Colab benchmark; record latency, invalid calls, tool choice. **Acceptance:** Baseline JSONL outputs and reproducible script. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-04 — Constrained tool-call parser.** **Implementation:** Implement model output schema, allowlist, argument validation, bounded retries and safe abstention. **Acceptance:** Malformed model outputs cannot execute tools. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-05 — Chat frontend first slice.** **Implementation:** Build chat composer, message states, tool activity and evidence-link placeholders. **Acceptance:** User can submit a question and see response/loading/error. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1112-D4-01 — Compass design system.** **Implementation:** Implement brand tokens, typography, spacing, dark/light contrast, accessible components. **Acceptance:** Tokens documented; contrast checked. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-02 — Navigation and import flow.** **Implementation:** Build routes, home, import and transaction review shell with fixture-backed data. **Acceptance:** Keyboard accessible and responsive. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-03 — Chat visual language.** **Implementation:** Create assistant/user messages, local-AI badge, evidence chips and tone selector. **Acceptance:** Chat shell supports mocked and real API states. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-04 — Wrapped story specification.** **Implementation:** Wireframe seven-card journey, chart encodings, empty states, interaction choreography. **Acceptance:** Storyboard approved with each card tied to source metric. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-05 — End-to-end smoke harness.** **Implementation:** Set up Playwright or equivalent and screenshot baseline across import/home/chat. **Acceptance:** CI executes one navigable browser test. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Saturday, November 14 — First integrated vertical slice

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1114-D1-01 — Transaction review and correction UI.** **Implementation:** Implement editable merchant/category/date/amount preview and correction provenance. **Acceptance:** Corrected transaction changes aggregates after refresh. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D1-02 — Duplicate import detection.** **Implementation:** Detect identical file hashes and repeated rows; distinguish duplicates from legitimate repeats. **Acceptance:** No double count; user sees decision. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D1-03 — Integration test: upload to chart.** **Implementation:** Write browser/API test from CSV upload to merchant total display. **Acceptance:** Golden fixture visible on UI. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1114-D2-01 — Period comparison tools.** **Implementation:** Add compare_periods and category trend tools with missing-period warnings. **Acceptance:** Correct month delta and zero-denominator behavior. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D2-02 — Financial X-Ray panel.** **Implementation:** Implement evidence drilldown listing source transactions, exclusions and coverage. **Acceptance:** Every displayed total opens verifiable breakdown. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D2-03 — Tool-to-UI contract tests.** **Implementation:** Generate typed client and contract fixtures for frontends. **Acceptance:** No schema mismatch in CI. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1114-D3-01 — End-to-end tool conversation.** **Implementation:** Connect SLM -> approved tools -> grounded response -> chat UI. **Acceptance:** Three questions answered with correct tool calls. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D3-02 — Training data pipeline.** **Implementation:** Build SFT JSONL with tool traces, empathetic responses, uncertainty and tone variants. **Acceptance:** 500+ reviewed/generated examples; schema and leakage checks. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D3-03 — Chat safety UX.** **Implementation:** Implement invalid-tool, unavailable-data and uncertainty messages in frontend. **Acceptance:** UI does not fabricate answer when model fails. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1114-D4-01 — Home-to-Wrapped navigation.** **Implementation:** Build Wrapped entry, story progress, resume and empty-state components. **Acceptance:** Accessible on mobile and desktop. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D4-02 — Chart primitives.** **Implementation:** Implement reusable bar, heatmap, slope and guess-versus-actual components with accessible tables. **Acceptance:** Fixtures render correctly with no misleading axes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D4-03 — Cross-team integrated demo.** **Implementation:** Own import -> correct -> chat -> X-Ray smoke run and defect list. **Acceptance:** All four flows demonstrated on one fixture. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Thursday, November 19 — All-team Wrapped build and fine-tuning

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1119-D1-01 — Wrapped data provenance API.** **Implementation:** Expose per-card evidence IDs, import coverage, filters and excluded transactions. **Acceptance:** Every story card can open source rows. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-02 — Merchant normalization and correction feedback.** **Implementation:** Support alias overrides and recomputation of summaries. **Acceptance:** Alias change updates story and audit trail. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-03 — Spending calendar data + UI.** **Implementation:** Implement daily buckets, refunds and calendar heatmap component. **Acceptance:** Correct date cells; screen-reader table available. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-04 — Data quality badges and coverage UX.** **Implementation:** Add account/date completeness indicators and explain missing imports. **Acceptance:** Incomplete data never labeled complete. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-05 — Wrapped contribution integration test.** **Implementation:** Add fixtures for top merchant and busiest day and browser test. **Acceptance:** Card values exactly match source data. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1119-D2-01 — Insight ranking and deduplication.** **Implementation:** Implement normalized ranking, eligibility, evidence thresholds and diversity rules. **Acceptance:** No repeated same-merchant cards or unsupported claims. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-02 — Guess the Damage engine and UI.** **Implementation:** Build estimate submission, absolute/relative error and animated reveal UI. **Acceptance:** $80 vs $143 yields $63; edge cases tested. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-03 — What If? tool and scenario widget.** **Implementation:** Implement k*average scenario with assumptions, editable input and disclaimer. **Acceptance:** Conditional values exact and transparent. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-04 — Money Awards generator.** **Implementation:** Implement deterministic award selection and award card UI. **Acceptance:** Award supported by named metrics and evidence. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-05 — Wrapped metrics tests.** **Implementation:** Golden tests for MoM, share, streak, ranking, refunds and chart scale. **Acceptance:** 100% of golden arithmetic cases pass. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1119-D3-01 — SFT/QLoRA training run.** **Implementation:** Train Qwen3-1.7B adapter in Colab with pinned config and checkpoints. **Acceptance:** Saved adapter, loss curve, GPU metadata, reproducible commands. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-02 — Tool and conversation specialization.** **Implementation:** Train on tool traces, corrections, nonjudgmental dialogue and context use. **Acceptance:** Held-out examples never included in training. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-03 — Model adapter inference service.** **Implementation:** Load tuned adapter and connect chat API, with explicit model identity. **Acceptance:** Model can answer on fixture and logs model version only. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-04 — SLM-generated Wrapped commentary.** **Implementation:** Generate grounded card narration and suggested follow-up from structured insight objects. **Acceptance:** No fabricated numbers in scripted cards. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-05 — Model-driven chat tone UI.** **Implementation:** Connect Gentle/Direct/Roast to constrained responses and frontend selection. **Acceptance:** Same facts in all tones; tone changes only style. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1119-D4-01 — Piggy bank HTML/CSS prototype.** **Implementation:** Create literal ceramic piggy bank with large feather wings and coin slot, not cartoon mascot. **Acceptance:** Review against user reference; reduced-motion supported. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-02 — Pig state machine and chat integration.** **Implementation:** Define idle/listening/thinking/reveal/supportive states and connect to chat lifecycle. **Acceptance:** No arbitrary model-generated code; states validated. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-03 — Wrapped seven-card flow.** **Implementation:** Assemble shared components into story progression, skip/revisit and drilldowns. **Acceptance:** All cards load from real API. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-04 — Confessional screen and context controls.** **Implementation:** Build optional user explanation input, consented memory control and follow-up UX. **Acceptance:** User can decline; explanation not treated as verified transaction fact. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-05 — Cross-dev Wrapped integration.** **Implementation:** Merge Dev1 heatmap, Dev2 awards/guess, Dev3 narration and Dev4 flow. **Acceptance:** Single story renders correctly end-to-end. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Saturday, November 21 — Integrated beta

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1121-D1-01 — Statement formats and correction reliability.** **Implementation:** Add second PDF fixture/layout or robust explicit unsupported notice; reconcile edited imports. **Acceptance:** Supported formats pass and unsupported formats fail clearly. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D1-02 — Wrapped data coverage tests.** **Implementation:** Test missing months, duplicate rows, partial accounts and refunds across all cards. **Acceptance:** No false full-month claim. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D1-03 — Privacy settings UI contribution.** **Implementation:** Build export/delete local records screen with confirmation and no telemetry default. **Acceptance:** Deletion and export demonstrable. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1121-D2-01 — Financial X-Ray for every Wrapped card.** **Implementation:** Connect all cards and awards to drilldown, not just overview. **Acceptance:** Seven-card source inspection works. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D2-02 — Spending insights and trend charts.** **Implementation:** Implement month-over-month slope and cumulative spend with correct scale. **Acceptance:** Comparisons handle missing baseline. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D2-03 — Financial conversation regression.** **Implementation:** Test model calls against exact tool outputs and claim verifier. **Acceptance:** Unsupported numeric claims blocked. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1121-D3-01 — Tuned vs baseline interim evaluation.** **Implementation:** Run identical held-out cases for base and tuned model. **Acceptance:** Preliminary paired metrics and failure examples saved. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D3-02 — Confessional contextual memory.** **Implementation:** Use opt-in local user statements, separate from factual transaction data; support forgetting. **Acceptance:** No fabricated motives; opt-out honored. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D3-03 — Conversation-to-Wrapped integration.** **Implementation:** Enable SLM follow-up from story cards, clarifications and What If? tools. **Acceptance:** User can switch between card and chat without losing context. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1121-D4-01 — Pig integration and accessibility.** **Implementation:** Mount coded pig on chatbot, use semantic labels and static reduced-motion fallback. **Acceptance:** Works across viewport and state transitions. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D4-02 — Full Wrapped UI beta.** **Implementation:** Polish guessing, charts, awards, receipts and chat handoff. **Acceptance:** First-time user completes seven-card story. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D4-03 — End-to-end beta test and triage.** **Implementation:** Run scripted upload -> correction -> chat -> Wrapped -> Confessional -> What If -> delete. **Acceptance:** Failures filed with severity and owner. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Thursday, November 26 — Full-feature validation (Thanksgiving; async allowed)

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1126-D1-01 — Import and privacy robustness.** **Implementation:** Fuzz malformed CSV/PDF, malicious filenames, file size, duplicate detection and local logs. **Acceptance:** Security/privacy regression documented. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-02 — Data export and deletion verification.** **Implementation:** Ensure database, imports, conversation memory and caches obey delete behavior. **Acceptance:** No recoverable app-level records after deletion on test. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-03 — Cross-device setup and data UI.** **Implementation:** Document and test clean install; build import-format helper in UI. **Acceptance:** Supported laptop demo works without developer fixes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-04 — Wrapped coverage/error handling.** **Implementation:** Test and fix all incomplete-period and bad merchant scenarios. **Acceptance:** No misleading chart or false confidence. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-05 — Data quality benchmark and artifact.** **Implementation:** Compute parse accuracy, coverage, correction success on labeled synthetic corpus. **Acceptance:** Machine-readable benchmark and UI chart exported. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1126-D2-01 — Finance 100-case benchmark.** **Implementation:** Run exact money tests incl refunds/transfers/rounding and record results. **Acceptance:** Reproducible pass/fail table. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-02 — Grounding validator and claims UI.** **Implementation:** Show evidence for amounts and safe abstention for unsupported claims. **Acceptance:** Zero unsupported numeric claims in release suite. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-03 — Insights ranking ablation.** **Implementation:** Compare ranking with/without diversity and user relevance; generate charts. **Acceptance:** Document ranking sensitivity and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-04 — Scenario/award bug fixes.** **Implementation:** Fix edge cases and integrate missing source links. **Acceptance:** No P0/P1 finance issues. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-05 — Investor metrics dashboard component.** **Implementation:** Build small local demo page for benchmark scorecards and caveats. **Acceptance:** All numbers pulled from result JSON, not hardcoded. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1126-D3-01 — Final paired model benchmark.** **Implementation:** Run base vs tuned on fixed held-out cases; report tool exact match, groundedness, tone. **Acceptance:** JSONL, confidence intervals and error taxonomy. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-02 — Local quantization benchmark.** **Implementation:** Measure quantized model on actual available consumer device; memory, p50/p95 latency. **Acceptance:** Hardware specified and results reproducible. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-03 — Privacy/offline network test.** **Implementation:** Test no outbound inference or raw statement telemetry; document model-download exception. **Acceptance:** Offline after install works on target machine. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-04 — Failure repair and regression.** **Implementation:** Fix invalid tools, context overflow, hallucination and unsafe humor. **Acceptance:** No P0/P1 model issues. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-05 — SLM explanation UI improvement.** **Implementation:** Build model status, local-processing disclosure and uncertainty indicators. **Acceptance:** Users can tell when AI vs deterministic tool acts. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1126-D4-01 — Complete user-journey E2E tests.** **Implementation:** Automate import, correction, chat, Wrapped, X-Ray, What If, settings, deletion. **Acceptance:** Green on clean supported machine. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-02 — Accessible charts and responsive audit.** **Implementation:** Keyboard, labels, contrast, reduced motion, screen-reader alternatives. **Acceptance:** Documented WCAG-oriented checks. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-03 — Usability pilot.** **Implementation:** Run 3-5 consented fictional-data sessions and collect task, comfort, comprehension. **Acceptance:** Anonymized data and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-04 — Pig refinement and fallback.** **Implementation:** Refine realistic ceramic design, ensure it does not block chat. **Acceptance:** Approved appearance or neutral fallback. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-05 — Product performance and onboarding.** **Implementation:** Optimize load, navigation, install, first-run demo; add helpful empty states. **Acceptance:** 10-minute scripted demo succeeds. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Full feature validation, but code remains open until Dec 1.

#### Saturday, November 28 — Coding, benchmarks, stretch improvements

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1128-D1-01 — Import stretch: additional CSV format.** **Implementation:** Add a third supported mapping and UI format selector if P0/P1 cleared. **Acceptance:** Fixture import passes or ticket explicitly descoped. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D1-02 — Privacy adversarial check.** **Implementation:** Attempt logs/export/deletion and malicious import failures; patch defects. **Acceptance:** Signed privacy checklist and fixes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D1-03 — Wrapped integration polish.** **Implementation:** Fix heatmap labels, receipts navigation and source coverage regressions. **Acceptance:** No P0/P1 in owned cards. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1128-D2-01 — Benchmark robustness and CIs.** **Implementation:** Compute bootstrap CIs and confusion matrices for finance/tool metrics. **Acceptance:** Scripts and raw outputs reproducible. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D2-02 — Stretch: recurring subscription story.** **Implementation:** Add recurring merchant frequency story card and UI if core green. **Acceptance:** Card sourced and inspectable or descoped. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D2-03 — Final numerical audit.** **Implementation:** Audit every demo dollar and chart axis, patch defects. **Acceptance:** All demo values match golden fixtures. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1128-D3-01 — Model ablation and uncertainty.** **Implementation:** Compare base/tuned and prompt-only baseline if time; error analysis and CI. **Acceptance:** Honest table with N and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D3-02 — Stretch: smarter follow-up suggestions.** **Implementation:** Add safe evidence-grounded next-question suggestions in chat. **Acceptance:** Suggestions execute valid tools only. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D3-03 — Model release hardening.** **Implementation:** Freeze adapter revision, test offline, error handling, and recoverability. **Acceptance:** No P0/P1 in model integration. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1128-D4-01 — Stretch: polished story transitions.** **Implementation:** Add restrained transitions and keyboard/reduced-motion parity. **Acceptance:** No accessibility regressions. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D4-02 — Pilot and UX benchmark finalization.** **Implementation:** Run additional short fictional-data user sessions or complete pilot analysis. **Acceptance:** Task outcomes and judgment survey recorded. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D4-03 — Cross-platform smoke and mascot fallback.** **Implementation:** Fix responsive, browser and pig animation issues; rehearse complete flow. **Acceptance:** Supported device demo passes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

### December 1–3: ACL-style paper — required for all four developers

These are **final-sprint obligations in addition to the 96 engineering tickets** (not squeezed into Meeting 6):

| Developer | Dec 1 (after freeze) | Dec 2 | Dec 3 submission responsibility |
|---|---|---|---|
| Dev 1 | Draft Data, preprocessing, provenance, privacy and ethics | Reproduce dataset tables, source coverage and limitations | Verify dataset and reproducibility appendix |
| Dev 2 | Draft financial tool methods, equations, evidence and ranking | Reproduce exact arithmetic and grounding tables/figures | Verify formulas and reported numbers |
| Dev 3 | Draft SLM model, QLoRA, baselines, experimental design | Reproduce paired model results, CIs, errors, hardware and limitations | Verify model/revision/config appendix |
| Dev 4 | Draft abstract, introduction, UX methodology, user study, related work | Assemble ACL LaTeX, screenshots, figures, references and discussion | Produce final PDF, demo package and submission checklist |

All four co-review Abstract, Conclusion, Limitations and Ethics. No invented empirical claims. Paper structure: Abstract, Introduction, Related Work, System, Dataset, Model Training, Experiments, Results, Ablations, Ethics, Limitations, Conclusion, References, Appendix. Use official ACL template if required by course; GitHub README equations use `$...$` and `$$...$$`.

### Traceability: complete product journeys and test owners

| README requirement | Owners (primary + integration) | Acceptance evidence |
|---|---|---|
| Local CSV/PDF import, corrections, duplicates | D1 + D4 + D2 | Golden fixtures, E2E import/edit and no double count |
| Local SQLite, coverage, privacy, deletion | D1 + D2 + D4 | Migrations, no raw logging, delete test, offline check |
| Specialized fine-tuned SLM and tool selection | D3 + D2 + D4 | Adapter checkpoint, baseline/tuned paired evaluation, tool schema tests |
| Chat, contextual follow-ups, tones, Confessional | D3 + D4 + D1 | Multi-turn E2E, memory opt-out, tone and no-shame review |
| X-Ray and deterministic financial calculations | D2 + D1 + D4 | All monetary claims link to source rows, 100-case tests |
| Money Wrapped: guessing, awards, four charts | **D1 + D2 + D3 + D4** | Seven-card story, evidence, accessible chart alternatives |
| What If? and Teach Me Why | D2 + D3 + D4 | Assumption-based tool response; financial concept Q&A benchmark |
| Flying ceramic piggy bank chatbot character | D4 + D3 | HTML/CSS/JS animation states, reduced-motion fallback |
| Consumer-local model, setup, speed | D3 + D4 + D1 | Quantized local inference, offline test, p50/p95 latency, RAM |
| Evaluation, investor evidence, paper | **All four** | Reproducible JSON metrics, CIs, UX study, ACL-style report |

**Explicit scope guard:** This is a functional research-grade local desktop/browser-on-localhost MVP, not a commercially certified bank app. Automatic bank sync, real SMS, native mobile deployment, commercial billing, voice, and full-scale consumer security review remain post-MVP. Do not claim an unimplemented stretch goal is complete.

### Benchmark calendar and investor-ready metrics

**Nov 11–12: baseline.** Lock held-out synthetic benchmark and run untuned Qwen3-1.7B; label tool calls, grounded claims, conversation behavior and response times. Publish model revision and N. **Nov 19:** preliminary tuned checkpoint and smoke metrics. **Nov 21:** paired interim model and complete journey beta. **Nov 23–26:** final fixed-set tests, local hardware profiling, privacy, import and human UX pilot. **Nov 28:** robustness/ablation, confidence intervals, follow-up user testing, no data leakage. **Nov 30:** regenerate final reproducible benchmark report. **Dec 1–3:** freeze and write measured results.

| Metric | Definition and reporting | Investor significance | Suggested gate (not a claim) |
|---|---|---|---|
| Exact financial arithmetic | `correct golden cases / total golden cases`; 100+ cases | Trust | 100% |
| Tool selection accuracy | Correct tool / labeled query, with tool-argument exact match separately | Model utility | ≥90% tool; ≥85% arguments |
| Grounded numerical claims | Supported numeric claims / all numeric claims; also count critical invented amounts | Safety | 100% in release suite; zero critical fabricated amounts |
| Nonjudgmental response rate | Blind human rubric, 2+ raters, N, mean and inter-rater agreement | Emotional differentiation | ≥90% acceptable; report agreement |
| Multi-turn task success | Completed user goals / labeled multi-turn scenarios | Conversation usefulness | ≥80% |
| Import precision/recall | Correctly extracted rows and required fields vs labeled fixtures; coverage separate | Reliability | ≥98% on supported fixtures |
| Offline/local privacy | Network egress audit and deletion verification on test machine | Privacy claim | Zero inference payload egress; deletion pass |
| Device performance | Cold start, peak RAM, median/p95 first-token latency, tokens/s, model disk size | Consumer viability | Measure, then set supported-device target |
| UX comprehension | Correct responses to questions after dashboard vs static Wrapped vs interactive Compass | Product advantage | Report group sizes, effect and CI, no assumed lift |
| Perceived judgment | 1–5 user questionnaire and comments, comparative where possible | Nonjudgmental positioning | Report raw distribution, not just average |
| Activation / completion | Users reaching first evidenced insight and completing Wrapped / starters | Product engagement | Report measured funnel; avoid investor forecasts |
| Willingness to pay | Actual choices or stated intent clearly distinguished | Pricing validation | No revenue claims without real test |

**Model comparisons:** A) base Qwen3-1.7B with same tools/prompts; B) tuned Qwen3-1.7B with same tools/prompts; optional C) prompt-engineered base model; optional D) Qwen3-4B if hardware permits. Keep test set, inference settings, prompts and tool access matched. For binary paired outcomes use paired bootstrap 95% CI (and McNemar when appropriate); for UX outcomes report N, descriptive stats, uncertainty and limitations. Avoid statistical significance claims from a tiny convenience sample.

**Benchmark sources:** Primarily **CompassBench**, an explicitly named *team-created synthetic benchmark*, not a published standard. Supplement with publicly licensed financial QA datasets (e.g. FinQA for arithmetic/reasoning, ConvFinQA for conversational finance) only as out-of-domain checks: they emphasize financial-report reasoning, not bank-statement conversations. Evaluate licensing, leakage and task mismatch before use. For tool calling, consider BFCL-style methodology as an external reference, not as proof that the full benchmark applies to Compass. Document exact benchmark versions, sources and sample sizes.

### Quality-control audit of the previous 91 tickets

The previous file contained exactly **91** tickets: 20/12/20/11/20/8 across the six meetings. Its strengths were synthetic-data privacy, deterministic money calculations, SLM tool schemas, fine-tuning, and end-to-end acceptance. Its weaknesses were Dev 4 frontend bottleneck, no even Saturday workload, late all-team Wrapped integration, Nov 26 premature feature freeze, Nov 28 report-only work, and large non-atomic tasks such as “finish all core user journeys.” This revised 96-ticket schedule fixes allocation and traceability, but **cannot prove correctness before implementation**. Check correctness with unit/contract/E2E tests, benchmark artifacts, cross-owner code reviews, accessibility checks, privacy/offline checks and an explicit pass/fail release checklist. Count is a planning metric, not a quality metric.



## G12. Completeness assurance and release evidence ledger

**Status as of November 10, 2026: PLANNED / NOT YET VERIFIED.** This section is an acceptance framework, not a claim that the application has been built or tested. It supplements G7 and G9; where older G7a or generic four-week language conflicts with G7, the dated G7 schedule governs. Every proposed result below is a target until a real CI run, reviewer, and timestamped artifact establish it.

### G12.1 Scope contract: what constitutes a complete Compass MVP

**In scope:** a localhost-accessible, local-first research MVP with supported CSV and text-based PDF import; normalized editable transaction records; deterministic source-backed financial tools; specialized tuned SLM with guarded tool calls; everyday chat; seven-card Money Wrapped with guessing, awards, charts, receipts and Confessional; conditional What If?; financial education; accessible responsive interface; privacy/deletion/offline validation; reproducible comparative benchmarks; ACL-style paper. A feature counts only when the user can complete its journey on a fresh checkout using documented fixtures, without manual database edits or mock-only responses.

**Out of scope:** live bank connections, production authentication/billing, native mobile, SMS/RCS, financial advice or money movement, OCR for scanned PDFs unless explicitly supported, commercial certification, statistically established market traction. An excluded capability must not appear as an implemented promise in demo, paper, or pitch.

**Definition of complete:** (1) all P0 requirements pass their specified automated and manual checks; (2) all supported journeys pass end to end; (3) all numerical outputs have deterministic provenance; (4) tuned model and evaluation artifacts are reproducible; (5) privacy and deletion claims pass observable tests; (6) no open P0/P1 issues; (7) all 96 tickets are closed with evidence or formally marked deferred with an explicit resulting scope reduction; (8) every claim in README/demo/paper is classified as implemented, measured, proposed, or excluded. Ticket closure alone is insufficient.

### G12.2 Requirement-to-ticket coverage index

This index links existing ticket titles to requirements using a **keyword-based candidate mapping**, not a reviewed assertion that each ticket fully implements that requirement. The feature owner must inspect implementation and fill in `verified PR / test ID / result / reviewer` before changing a requirement to PASS. A ticket can contribute to several requirements, but cannot substitute for missing integration evidence.

| ID | Product requirement | Candidate existing ticket IDs | Verification status |
|---|---|---|---|
| REQ-01 | Supported CSV/PDF import and rejection | `CMP-1112-D1-03`, `CMP-1112-D1-04`, `CMP-1112-D4-02`, `CMP-1114-D1-02`, `CMP-1126-D1-01`, `CMP-1128-D1-01` | NOT VERIFIED |
| REQ-02 | Transaction correctness and editing | `CMP-1112-D2-01`, `CMP-1114-D1-01`, `CMP-1114-D1-02`, `CMP-1119-D1-02`, `CMP-1119-D1-04`, `CMP-1121-D1-01`, `CMP-1121-D1-02`, `CMP-1126-D1-04` | NOT VERIFIED |
| REQ-03 | Privacy, local operation and deletion | `CMP-1112-D1-05`, `CMP-1121-D1-03`, `CMP-1126-D1-01`, `CMP-1126-D1-02`, `CMP-1126-D3-02`, `CMP-1126-D3-03`, `CMP-1128-D1-02` | NOT VERIFIED |
| REQ-04 | Financial tools and source-backed X-Ray | `CMP-1112-D2-03`, `CMP-1112-D2-04`, `CMP-1112-D2-05`, `CMP-1112-D3-04`, `CMP-1114-D2-01`, `CMP-1114-D2-02`, `CMP-1114-D2-03`, `CMP-1114-D3-01`, `CMP-1119-D1-01`, `CMP-1119-D2-03`, `CMP-1119-D3-02`, `CMP-1121-D2-01` (+1 additional candidates) | NOT VERIFIED |
| REQ-05 | SLM specialization and constrained orchestration | `CMP-1112-D2-03`, `CMP-1112-D2-04`, `CMP-1112-D3-01`, `CMP-1112-D3-03`, `CMP-1112-D3-04`, `CMP-1114-D2-01`, `CMP-1114-D2-03`, `CMP-1114-D3-01`, `CMP-1114-D3-02`, `CMP-1119-D2-03`, `CMP-1119-D3-01`, `CMP-1119-D3-02` (+7 additional candidates) | NOT VERIFIED |
| REQ-06 | Everyday conversational experience | `CMP-1112-D3-05`, `CMP-1112-D4-03`, `CMP-1114-D3-01`, `CMP-1114-D3-03`, `CMP-1119-D3-02`, `CMP-1119-D3-05`, `CMP-1119-D4-02`, `CMP-1119-D4-04`, `CMP-1121-D2-03`, `CMP-1121-D3-02`, `CMP-1121-D3-03`, `CMP-1126-D2-02` | NOT VERIFIED |
| REQ-07 | Money Wrapped story and guessing | `CMP-1112-D2-05`, `CMP-1112-D4-04`, `CMP-1114-D4-01`, `CMP-1119-D1-01`, `CMP-1119-D1-05`, `CMP-1119-D2-02`, `CMP-1119-D2-05`, `CMP-1119-D3-04`, `CMP-1119-D4-03`, `CMP-1119-D4-05`, `CMP-1121-D1-02`, `CMP-1121-D2-01` (+6 additional candidates) | NOT VERIFIED |
| REQ-08 | Awards, charts and insight ranking | `CMP-1114-D1-03`, `CMP-1114-D4-02`, `CMP-1119-D1-03`, `CMP-1119-D2-01`, `CMP-1119-D2-04`, `CMP-1119-D2-05`, `CMP-1121-D2-02`, `CMP-1126-D2-03`, `CMP-1126-D2-04`, `CMP-1126-D2-05`, `CMP-1126-D4-02` | NOT VERIFIED |
| REQ-09 | What If? and financial education | `CMP-1119-D2-03`, `CMP-1126-D2-04` | NOT VERIFIED |
| REQ-10 | Accessible, distinctive interface | `CMP-1112-D2-05`, `CMP-1112-D3-05`, `CMP-1112-D4-01`, `CMP-1112-D4-02`, `CMP-1114-D1-01`, `CMP-1114-D2-03`, `CMP-1114-D4-01`, `CMP-1119-D1-03`, `CMP-1119-D2-02`, `CMP-1119-D3-05`, `CMP-1119-D4-01`, `CMP-1119-D4-02` (+8 additional candidates) | NOT VERIFIED |
| REQ-11 | End-to-end reliability and release | `CMP-1112-D2-02`, `CMP-1112-D2-05`, `CMP-1112-D3-01`, `CMP-1112-D3-02`, `CMP-1112-D4-04`, `CMP-1114-D1-03`, `CMP-1114-D2-02`, `CMP-1114-D2-03`, `CMP-1119-D1-05`, `CMP-1119-D2-05`, `CMP-1119-D3-02`, `CMP-1119-D4-02` (+18 additional candidates) | NOT VERIFIED |
| REQ-12 | Evaluation and ACL evidence | `CMP-1112-D3-02`, `CMP-1121-D3-01`, `CMP-1126-D1-05`, `CMP-1126-D2-01`, `CMP-1126-D2-03`, `CMP-1126-D3-01`, `CMP-1126-D3-02`, `CMP-1126-D4-03`, `CMP-1128-D2-01`, `CMP-1128-D3-01`, `CMP-1128-D4-02` | NOT VERIFIED |

**Mandatory review of candidate links:** the lead and a different developer must read each referenced ticket's implementation and acceptance, not merely its title. Replace candidates with exact requirement-to-PR-to-test links in the live tracker. If a requirement lacks a passing test, it is uncovered even if its candidate list is long.

### G12.3 Contract-level acceptance matrix: proof needed, not just ticket completion

| Requirement | Required deterministic / automated proof | Required user-level or adversarial proof | Release decision |
|---|---|---|---|
| REQ-01 | Golden CSV and supported text-PDF row/field oracle; unsupported format error test; source row IDs | Import two layouts and one rejected PDF; no silent row drops | P0 if incorrect totals or silent corruption |
| REQ-02 | Golden cents/refund/transfer/dedup/correction tests; idempotent reimport; migration roundtrip | Correct a category and see every downstream number update | P0 if duplicate-count or corrupted money |
| REQ-03 | Offline network egress capture, local data location, deletion/restart test, log secret scan | Disconnect network, ask a question, delete data, restart, verify absence | P0 if unexpected sensitive egress or retained deleted records |
| REQ-04 | Decimal/integer-cent oracle, invalid arguments, evidence-ID integrity, zero denominator | Click a numerical claim and reconcile all displayed source transactions | P0 if fabricated amount or inconsistent sums |
| REQ-05 | Pinned model/adapter hash, training manifest, held-out split audit, base-vs-tuned paired run | Ambiguous and malicious prompts must not bypass tool allowlist | P1 if tuned model missing; P0 if fabricated money reaches user |
| REQ-06 | Multi-turn state, abstention, tone boundaries, context reset, errors | Ask follow-up after a correction; switch tone without changing amounts | P1 if core chat cannot finish |
| REQ-07 | Seven-card schema validation, deterministic guess delta, evidence-linked story cards | Full guess → reveal → receipts → Confessional flow on fresh fixture | P1 if core story cannot finish |
| REQ-08 | Chart totals reconcile to underlying tool outputs; rank ties and sparse data | Compare charts/awards against receipts; accessible text equivalents | P1 for false visual numbers |
| REQ-09 | Scenario input validation, transparent assumptions, no real-world action execution | Compare baseline vs hypothetical, then return to unchanged actuals | P1 if scenarios mutate records |
| REQ-10 | Keyboard/axe-style audit, reduced-motion check, mobile-width browser suite | Screen-reader labels, tab sequence, responsive and animation-off walkthrough | P1 for blocked essential journey |
| REQ-11 | CI green from clean checkout; pinned dependencies; integration and smoke suites | Two reviewers independently run documented install and demo | P1 if clean install fails |
| REQ-12 | Locked split, benchmark JSON, denominators, CIs, reproducibility commands | Independent rerun and paper-to-artifact number check | P1 if results cannot be reproduced |

### G12.4 Mandatory cross-feature integration journeys

These are **additional release-level acceptance tests** to be implemented within the existing 96 tickets, not fictitious completed tickets. Name each Playwright/pytest test and link it to its CI artifact.

| Journey ID | Exact flow | Invariants / pass condition | Primary / independent reviewer |
|---|---|---|---|
| E2E-01 | Fresh install → import CSV → review → ask merchant total → X-Ray | Display, DB and evidence rows agree to the cent | D1 / D2 |
| E2E-02 | Import PDF → correct category → Wrapped → chart → chat | Correction propagates to every view; no stale cache | D1 / D4 |
| E2E-03 | Reimport same statement → refund/transfer → month comparison | No duplicate, transfer counted as configured, correct signs | D2 / D1 |
| E2E-04 | Missing month/account → Wrapped → ask comparison | Explicit coverage warning; no unsupported conclusion | D1 / D3 |
| E2E-05 | Guess → reveal → award → receipts → Confessional | Same deterministic numbers and source IDs across cards/chat | D2 / D3 |
| E2E-06 | Confessional → What If? → return to actuals | Hypothetical is labeled and cannot mutate actual records | D3 / D2 |
| E2E-07 | Gentle → Direct → Roast → opt out → restart | Style changes; evidence unchanged; opt-out respected | D3 / D4 |
| E2E-08 | Offline session → chat → delete all → restart | No sensitive payload egress; no recoverable app records in documented scope | D1 / D4 |
| E2E-09 | Keyboard-only → mobile width → reduced motion | All core controls usable, chart alternatives and pig fallback | D4 / D1 |
| E2E-10 | Base model vs tuned model → same held-out cases | Same tools/prompts/test cases; differences and errors saved | D3 / D2 |
| E2E-11 | Empty/partial data → unsupported PDF → malformed tool call | Graceful error/abstention; never invented transactions | D3 / D1 |
| E2E-12 | Clean clone → install → fixture → full demo → benchmark rerun | No private setup, missing file, hidden service or hard-coded demo response | D4 / D3 |

### G12.5 Ticket-level evidence manifest and enforcement

Every one of the 96 issue descriptions must contain these fields before the corresponding meeting: `Requirement IDs`, `Owner`, `Independent reviewer`, `Estimated hours`, `Actual hours`, `Dependency IDs`, `User-visible behavior`, `Input/output schema`, `Supported and unsupported cases`, `Fixture ID`, `Automated test ID`, `Manual/E2E test ID`, `PR/commit`, `CI run URL`, `Screenshot/log`, `Result (PASS/FAIL/BLOCKED/DEFERRED)`, `Last verified timestamp`, `Known limitations`. **No evidence link = NOT VERIFIED, not PASS.**

**PR gate:** tests pass; independent reviewer verifies at least one adversarial case; API/schema change is reflected in contracts; source IDs are preserved; no real financial data or secrets in logs; frontend states include loading/empty/error; documentation updated. For a model-only ticket, substitute saved eval outputs and a reproducible command for screenshots. For a UI-only ticket, require browser screenshots and a keyboard check.

**Effort fairness:** 24 tickets per developer is count parity, not workload parity. At kickoff assign estimates and dependency risk (1–3); report estimated and actual hours per developer at every meeting; rebalance implementation or pair reviews when projected hours differ by more than 15%, without silently changing acceptance criteria. Every developer must show frontend, non-frontend, test and integration contributions in the final contribution ledger.

### G12.6 Gate-by-gate completeness scorecard (fill with actual evidence)

| Gate | Must be demonstrable | Evidence to attach | Default status |
|---|---|---|---|
| Nov 12 / Meeting 1 | Contracts, supported import, exact totals, base SLM and chat shell | CI, golden fixture, baseline dataset/hash | PENDING |
| Nov 14 / Meeting 2 | Import → correct → ask → X-Ray | E2E-01 and E2E-03, source-ID audit | PENDING |
| Nov 19 / Meeting 3 | All four Wrapped contributions plus tuned checkpoint | Story integration PRs, adapter hash, dev-set comparison | PENDING |
| Nov 21 / Meeting 4 | Complete interactive beta and corrections reflected everywhere | E2E-02, 04–07 and browser videos | PENDING |
| Nov 26 / Meeting 5 | Feature-complete candidate and locked-set metrics | Benchmark JSON, privacy run, pilot notes, defect register | PENDING |
| Nov 28 / Meeting 6 | Coding/robustness fixes, ablations, full release candidate | E2E-08–12, stress logs, ablation tables | PENDING |
| Nov 30 | Clean-checkout independent regression and paper-ready artifacts | CI run, tagged candidate, frozen metrics manifest | PENDING |
| Dec 1 noon ET | Unanimous code-freeze approval; no open P0/P1 | Signed release checklist, hashes, defect report | PENDING |
| Dec 1–3 | ACL report with figures matching frozen outputs | PDF, paper-source links, reproducibility appendix | PENDING |

### G12.7 Quantitative coverage and honest claims

Report separately: `ticket completion = evidenced PASS tickets / 96`; `requirement coverage = requirements with mapped passing tests / 12`; `journey success = passing E2E journeys / 12`; `critical issue count = open P0 + P1`; `numerical correctness = passing supported golden cases / tested supported cases`; `grounding = verified numerical claims / checked numerical claims`; `model comparison = paired tuned minus baseline metric with uncertainty`; `privacy = named egress/deletion checks passed / attempted`; `cross-functional contribution = developers with frontend + backend/data/model + test evidence / 4`. Never combine these into an unexplained single “product completeness” percentage. Report denominators and exclusions.

**Release rules:** Any open P0/P1 or failed mandatory journey means NO-GO for a claim of complete MVP. A deferred core requirement requires an explicit narrower MVP statement and an updated pitch/demo/paper; it does not count as passed. Stretch features cannot compensate for missing core behavior. Small user pilots establish usability signals, not retention, product-market fit, willingness to pay, or investor traction. Proposed thresholds in G9 are hypotheses; if they are missed, report the actual result rather than changing the test after the fact.

### G12.8 Completeness audit procedure for December 1

1. Export all 96 issues and confirm 24 per developer, 20/12/20/12/20/12 per meeting, no duplicates and no unowned issues.
2. Inspect each ticket's actual code/test evidence and independently verify requirement mapping; candidate keyword links above are not accepted without review.
3. Execute all 12 E2E journeys on a clean checkout; save pass/fail, run time, fixture hash and screenshot/log.
4. Reconcile every numerical UI claim and chart against the deterministic transaction oracle; inspect refunds, transfers, missing periods and corrections.
5. Independently rerun base/tuned evaluation on the frozen holdout and confirm model/data hashes, denominators, uncertainty and failure categories.
6. Run offline, deletion, sensitive-log and malformed-input tests on documented target hardware; record limitations.
7. Confirm all four developers contributed code across frontend and non-frontend surfaces and peer-reviewed another domain.
8. Match every demo/pitch/README/paper feature claim to one of `IMPLEMENTED + VERIFIED`, `IMPLEMENTED + UNVERIFIED`, `PROPOSED`, or `OUT OF SCOPE`; only the first may be presented as working.
9. Obtain four sign-offs for the release ledger, tag commit/model/fixtures, and freeze at noon ET December 1; use December 1–3 for the ACL report.

**Known residual risk:** The backlog cannot guarantee all real-world statement formats, consumer-device configurations, security threats, or user outcomes. Evidence-based completeness is bounded by explicitly supported formats, fixtures, target devices and tests.


## GitHub issue template (apply to each of the 96 tickets)

```markdown
## Product contract
- README feature / section:
- Requirement IDs:
- User-visible behavior:
- In scope / out of scope:

## Execution
- Owner / independent reviewer:
- Meeting milestone / due date:
- Estimate / actual hours:
- Dependencies / interface contracts:
- Implementation tasks:

## Verification
- Acceptance criteria (given / when / then):
- Golden fixture / test data:
- Automated test IDs / E2E journey IDs:
- Negative, empty, privacy and accessibility cases as applicable:
- PR / commit / CI URL:
- Screenshots, logs or model evaluation artifact:
- Result: NOT VERIFIED / PASS / FAIL / BLOCKED / DEFERRED
- Last verified / known limitations:
```

**Issue closure rule:** Only independent review plus linked passing evidence qualifies as PASS. A closed GitHub issue without that evidence remains NOT VERIFIED for release reporting.
