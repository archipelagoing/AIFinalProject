G7. Revised execution plan — 96 balanced tickets, November 10–December 3, 2026
This section replaces the earlier 91-ticket plan and the illustrative four-week schedule. Six meeting gates: Thursday/Saturday on November 12/14, 19/21, 26/28. Code freeze is Tuesday, December 1; December 1–3 is the dedicated ACL-style report and submission period. November 26 is US Thanksgiving; use an asynchronous review if needed. The project is a three-week accelerated MVP; no schedule can guarantee a flawless result. The definition of done is evidence-based.
Workload, ownership, and daily rules
- 96 tickets = 24 per developer: each developer gets 5 before each Thursday (15) and 3 before each Saturday (9). Each ticket should be one reviewable PR or a small coherent group of commits; tickets are not assumed equal in effort. Estimate hours at kickoff and rebalance by actual hours daily.
- All four developers write frontend code, and each also contributes tests, integration, data/model/backend work, and an evaluation artifact. Domain lead is accountable for the feature, not sole implementer.
- All four build Wrapped simultaneously November 16–21: Dev 1 owns coverage + calendar UI, Dev 2 guessing/awards/scenarios, Dev 3 SLM commentary and chat transitions, Dev 4 story navigation + mascot. Cross-owner PR review is mandatory.
- Every ticket requires: issue ID, clear scope, input/output contract, synthetic fixture, automated test or documented manual test, screenshot/log, reviewer, PR, acceptance pass/fail. A demo is not proof of all edge cases.
- Daily 7 PM ET async updates: completed ticket IDs, hours spent, test evidence, blockers, next day's plan. Meet Thursdays/Saturdays after tickets are submitted; review failed gates and rebalance workload.
- No real bank records in the training corpus or public demo. SLM performs conversation and constrained tool selection; exact numbers come from deterministic functions. All AI claims that contain numbers require evidence IDs.
- P0: financial misstatement, data leak, corrupted import, broken core flow. P1: essential feature nonfunctional, persistent tool hallucination, unhandled crash. No P0/P1 at freeze; P2 defects documented honestly.
Calendar and deliverables
Date	Individual daily action and team integration gate
Tue Nov 10	Create repository/branches/CI, assign 96 issues, estimate ticket hours, pin API contracts, check Colab GPU, agree synthetic fixture rules.
Wed Nov 11	Each developer completes at least 3 of 5 Nov 12 tickets; pair-review schemas and initial frontend contracts.
Thu Nov 12	Finish remaining 2 tickets before meeting; demonstrate CSV/PDF fixture, exact totals, base SLM and chat UI.
Fri Nov 13	Each developer completes 2 of 3 Nov 14 tickets, integrates against real APIs, posts PR evidence.
Sat Nov 14	Complete third ticket and demo import → correct → ask → inspect X-Ray. Lock tool and story schemas.
Sun Nov 15	Optional buffer; resolve blockers only, no unapproved new scope.
Mon Nov 16	All four begin Wrapped work in parallel; Dev 3 starts data/training preparation; merge chart and story contracts.
Tue Nov 17	Finish ~2 Nov 19 tickets per developer; run early integration tests and inspect first Colab training run.
Wed Nov 18	Finish ~2 more Nov 19 tickets; cross-review Wrapped cards, SLM tool outputs, evidence links.
Thu Nov 19	Finish fifth ticket before meeting; live shared Wrapped demo with model checkpoint and mascot prototype.
Fri Nov 20	Finish 2 of 3 Nov 21 tickets each; integrate all Wrapped parts and run E2E beta suite.
Sat Nov 21	Complete third ticket; demonstrate full import → chat → Wrapped → Confessional → What If → delete journey.
Sun Nov 22	Optional buffer for critical defects and checkpoint backups.
Mon Nov 23	Complete 2 Nov 26 tickets each; run finance, model and privacy benchmarks on frozen test sets.
Tue Nov 24	Complete 2 more Nov 26 tickets; conduct pilot and local inference measurements; triage P0/P1.
Wed Nov 25	Complete fifth Nov 26 ticket and rehearse full release-candidate demo.
Thu Nov 26	Meeting 5: benchmark review and feature-complete candidate; Thanksgiving async review permitted. Not code freeze.
Fri Nov 27	Complete 2 Nov 28 tickets each; patch failures; only add stretch work if all core P0/P1 cleared.
Sat Nov 28	Meeting 6: complete third ticket, code/benchmark demos, integration and stretch-feature decisions. Not a report-only meeting.
Sun Nov 29	Optional defect repair; prepare final measured artifacts.
Mon Nov 30	Full regression, reproducibility, performance, security and final release review; finalize figures/results JSON.
Tue Dec 1	12:00 PM ET code freeze: tag v1.0-rc; no feature work afterward. Begin ACL-style paper with assigned sections and actual measurements.
Wed Dec 2	All four write/review ACL sections, regenerate tables/figures, check citations, ethics, limitations, and reproducibility.
Thu Dec 3	Final ACL-style PDF, repository, benchmark artifacts and demo submission; verify receipt.


Weekly outcomes and meeting agendas (facilitator-ready)
Meeting operating rule: The Thursday and Saturday meetings are review and decision gates, not the time to start the tickets due that day. Each developer posts a 2–4 minute screen-recorded demo or reproducible evidence before the meeting. At the meeting, demonstrate the integrated app on the same synthetic fixture, inspect failing tests and benchmark changes, make decisions, and record an owner plus due date for each blocker. Suggested 60-minute format: 5 minutes goal/status, 20 minutes demos (5 per developer), 15 minutes integrated journey and QA, 15 minutes decisions/risks, 5 minutes assignments and written minutes. Meeting 5 may be asynchronous for Thanksgiving. The individual issue details and acceptance tests appear in the ticket backlog immediately below.
Week 1 — November 10–14: Trustworthy foundations and first financial conversation
Weekly outcome: A synthetic statement can be imported, normalized, calculated exactly, corrected or deleted, and queried through a visible chat flow with evidence links. The untuned SLM baseline and a held-out evaluation set exist before fine-tuning. Definition of success: the team can run import → preview → total → ask → X-Ray from a clean checkout without fabricated numbers.
Meeting 1 — Thursday, November 12: Contracts, data accuracy, and baseline
Before the meeting: 5 tickets per developer (CMP-1112-*)
Developer	Goal and demo required by Thursday
Dev 1	Repository/API contracts; two-persona synthetic fixture with golden totals; two-layout CSV importer; one text-PDF importer and unsupported-file warning; local provenance/deletion vertical slice. Demo both accepted and rejected files, plus deletion.
Dev 2	SQLite migrations and seed; cents/sign/refund/transfer rules; merchant/category/expense tools; Pydantic tool contracts with evidence IDs; real-data overview UI card. Demo a traceable merchant total and an invalid-argument rejection.
Dev 3	Colab GPU/model decision record; ≥150 held-out test cases with leakage rules; untuned Qwen3-1.7B benchmark; constrained tool-call parser; chat input/loading/error UI. Demo baseline results and an invalid model tool call being blocked.
Dev 4	Brand tokens and accessible components; navigation/import/review UI; chat visual language and tone selector; seven-card Wrapped storyboard; Playwright smoke harness. Demo keyboard navigation and the initial browser test.


Discussion agenda: (1) Agree on transaction signs, refunds, transfers, currencies and date boundaries; (2) approve the typed API and evidence-ID format; (3) review Colab VRAM, model feasibility and benchmark leakage policy; (4) approve the seven-card Wrapped storyboard and shared design tokens; (5) identify the most fragile import format and decide what is explicitly unsupported. Decisions to record: frozen v0 schemas, supported file formats, model candidate, baseline dataset version, reviewer for each integration PR. Gate: exact totals match golden fixtures, clean checkout works, and a baseline benchmark artifact is saved. If blocked: reduce supported PDF layouts before compromising arithmetic or provenance.
Meeting 2 — Saturday, November 14: First integrated vertical slice
Before the meeting: 3 tickets per developer (CMP-1114-*)
Developer	Goal and demo required by Saturday
Dev 1	Import correction/duplicate/coverage behavior integrated with review UI; demonstrate one corrected merchant and a re-import that does not double-count.
Dev 2	Month comparisons and source-backed X-Ray outputs connected to UI; demonstrate the exact rows behind a displayed amount.
Dev 3	SLM-to-tool orchestration and grounded reply path; demonstrate valid and invalid requests, uncertainty and abstention.
Dev 4	End-to-end import/chat/X-Ray interaction and browser regression; demonstrate complete vertical slice without manual database edits.


Discussion agenda: (1) Run the same import → correct → ask → receipts script together; (2) triage any discrepancy between UI and database; (3) lock Insight Object, Wrapped-card and conversation-response contracts; (4) approve training-data categories and human review rubric; (5) assign cross-owner Wrapped PR reviews. Decisions to record: v1 story schema, explicit P0/P1 defects, training set size and quality checks, Week 2 integration branches. Gate: the full vertical slice works on synthetic records; each numerical answer can be traced to transactions. If blocked: prioritize a working single-statement journey over additional file formats.
Week 2 — November 16–21: All-team Wrapped, specialized SLM, and conversational beta
Weekly outcome: All four developers build Wrapped in parallel, the fine-tuned SLM has a reproducible checkpoint, and the application supports import → chat → guess → reveal → receipts → Confessional → What If?. The flying ceramic pig is implemented as HTML/CSS/JS by Dev 4 with state signals from Dev 3; visual polish cannot block the core journey.
Meeting 3 — Thursday, November 19: Shared Wrapped alpha and first tuned checkpoint
Before the meeting: 5 tickets per developer (CMP-1119-*)
Developer	Goal and demo required by Thursday
Dev 1	Merchant aliases, source completeness and Wrapped calendar/heatmap frontend; show each day linked to included transactions and a missing-account warning.
Dev 2	Ranked insights, guessing-game arithmetic, awards and scenario tool/UI; demonstrate correct guess-versus-actual difference and conditional savings.
Dev 3	Synthetic SFT dataset and Colab QLoRA/LoRA run, saved adapter/checkpoint, tuned-model smoke comparison, SLM-generated grounded story and chat-state schema; show real outputs, not hand-authored copy.
Dev 4	Seven-card story shell, chart transitions, responsive chat/story navigation, first HTML/CSS/JS ceramic flying-pig implementation; show motion-reduction behavior and SLM state hookup.


Discussion agenda: (1) Each developer presents their own Wrapped card or interaction; (2) run one joined story from real synthetic fixture totals; (3) compare base versus tuned model on a small development set, not the locked final test set; (4) inspect tone and shame-risk examples; (5) choose what visual refinements can be deferred. Decisions to record: minimum story-card set, adapter version, allowed SLM animation states, integration blockers, targeted fixes for November 21. Gate: all four Wrapped contributions render together and the first tuned checkpoint is reproducible. If blocked: keep base model as a temporary diagnostic baseline, not a replacement for the fine-tuning deliverable; prioritize one working story over extra transitions.
Meeting 4 — Saturday, November 21: End-to-end beta and first model comparison
Before the meeting: 3 tickets per developer (CMP-1121-*)
Developer	Goal and demo required by Saturday
Dev 1	Complete coverage/correction and privacy integration through Wrapped; demonstrate reclassification changing both chart and explanation correctly.
Dev 2	Complete What If?, X-Ray and award-calculation integration; show deterministic numerical outputs across story and chat.
Dev 3	Connect tuned SLM to chat/Confessional and evaluate paired base-versus-tuned outputs on a fixed interim split; demonstrate no invented amount and controlled tool invocation.
Dev 4	Assemble chat, pig states, story transitions and responsive full-journey E2E test; demonstrate keyboard and reduced-motion flows.


Discussion agenda: (1) One teammate unfamiliar with the flow performs the complete beta journey; (2) examine exact calculation and grounding failures; (3) review base/tuned metrics, model latency and checkpoint backups; (4) inspect accessibility and mobile-width layout; (5) decide whether any feature is at risk of missing November 26. Decisions to record: beta acceptance result, prioritized P0/P1 list, benchmark owner and pilot participants, hardware target, features requiring hard scope limits. Gate: all major product experiences can be completed without developer intervention on supported fixtures. If blocked: fix broken core journeys before adding new features.
Week 3 — November 23–28: Reliability, investor evidence, and last coding meeting
Weekly outcome: Finish and test the README-defined research-grade MVP; gather honest investor-facing evidence for financial correctness, model specialization, privacy, latency, comprehension and user comfort. Meeting 6 remains an engineering meeting. Code freeze is not until December 1.
Meeting 5 — Thursday, November 26: Release candidate and benchmark review
Before the meeting: 5 tickets per developer (CMP-1126-*)
Developer	Goal and demo required by Thursday
Dev 1	Import edge cases, duplicate/transfer/refund and missing-account coverage, deletion/privacy checks and associated UI warnings; show extraction precision/recall.
Dev 2	Financial golden-suite, tool-argument/evidence validation, chart/award math, scenario tests and benchmark visualization; show exact accuracy and failure cases.
Dev 3	Locked-set base-versus-tuned evaluation, tool-selection/grounding/nonjudgment rubric, local model latency/RAM tests and reproducibility notes; show paired results with sample sizes.
Dev 4	Complete product QA, accessibility, mascot fallback, onboarding/usability pilot and demo packaging; show task completion and perceived-judgment feedback.


Discussion agenda: (1) Review each metric's denominator, test set and evidence artifact; (2) inspect all P0/P1 bugs and privacy issues; (3) compare model quality and consumer-device performance; (4) review pilot feedback without presenting small-sample results as market proof; (5) select November 28 engineering priorities. Decisions to record: release-candidate status, defects assigned with due dates, whether one stretch feature is safe, final evaluation protocol, Thanksgiving attendance/asynchronous sign-offs. Gate: all essential flows are implemented and measured; no unowned critical bugs. If blocked: cancel stretch work and dedicate November 27–30 to reliability.
Meeting 6 — Saturday, November 28: Last coding and robustness review
Before the meeting: 3 tickets per developer (CMP-1128-*)
Developer	Goal and demo required by Saturday
Dev 1	Patch import/privacy regressions; rerun offline/deletion/coverage tests; optionally add one supported import enhancement only after all P0/P1 are cleared.
Dev 2	Fix financial/chart edge cases, run stress and property-based tests, validate all Wrapped statistics and export final metric tables.
Dev 3	Run model ablations and robustness cases, measure uncertainty/CI and failure categories, optimize local inference or adapter configuration.
Dev 4	Fix end-to-end UX and accessibility defects, refine pig/chat animations, test responsive performance, and optionally implement one low-risk stretch interaction.


Discussion agenda: (1) Run a fresh-checkout full demo with no hidden setup; (2) inspect automated test dashboard, performance and remaining defects; (3) review ablations and confidence intervals for credible paper/investor claims; (4) approve or reject any stretch feature based on risk; (5) assign November 29–30 final fixes and reproducibility tasks. Decisions to record: explicit go/no-go for December 1 freeze, exact remaining bugs with owners, final benchmark run command, version/tag owner, paper figures to regenerate after freeze. Gate: a complete release candidate exists with only documented low-severity issues. If blocked: all developers swarm P0/P1 defects; no cosmetic work until resolved.
Finalization — November 29–December 3: Freeze first, then ACL-style report
November 29–30 (engineering buffer): Each developer reruns their own test suite plus one other developer's integration tests, closes regressions, updates documentation and screenshots, and verifies clean setup. Dev 3 freezes the final model/config and benchmark scripts; Dev 2 regenerates numeric result tables; Dev 1 checks data provenance/privacy; Dev 4 checks end-to-end demo and accessibility. Do not change evaluation rules to improve scores after seeing results.

Tuesday, December 1, noon ET — code freeze: All four approve the release tag, dependency lockfiles, model adapter hash, fixture hash, benchmark outputs, screenshots, setup steps and known-limitations list. From this point, no planned feature coding; emergency fixes require all four to approve and record the change. Everyone's final-sprint deliverable includes an ACL-style paper contribution.

December 1–3 — ACL report work split: Dev 1 writes Dataset/Preprocessing/Privacy/Ethics; Dev 2 writes Financial Tools/Equations/Validation; Dev 3 writes Model/Fine-tuning/Experiments/Results; Dev 4 writes Introduction/Related Work/UX/Presentation and integrates ACL LaTeX. Each developer must contribute at least one figure/table, one limitations paragraph, a reproducibility note, and peer review of another section. All four approve abstract, conclusions and final claims. Thursday, December 3: submit PDF, repository, model/setup documentation, evaluation artifacts and demo before the actual course deadline.

Meeting minutes template (copy for all six meetings): Date/time | attendees | gate passed? | four demos + PR links | benchmark snapshot (N/version) | P0/P1/P2 defects | decisions made | owner and deadline for each blocker | next meeting's exact demo | action items. Record metrics as measured, pending or failed—never as presumed success.
Meeting ticket backlog (each ticket has explicit build and acceptance)
Thursday, November 12 — Foundation and baseline
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1112-D1-01 — Repository and shared API contract. Implementation: Create monorepo, Python/TS formatting, CI, issue templates, typed transaction/import schemas and integration mock. Acceptance: Clean checkout installs; CI green; example request validated. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D1-02 — Synthetic two-persona dataset. Implementation: Generate two months per persona with refunds, transfers, merchant aliases, duplicate files, incomplete account and 100+ rows. Acceptance: Golden cents totals independently documented. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D1-03 — CSV import and preview endpoint. Implementation: Parse two explicit layouts, retain raw row IDs, handle dates and debit-credit sign conventions. Acceptance: Two fixtures import; bad rows are identified without silent loss. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D1-04 — PDF import and unsupported-file UX. Implementation: Support one text PDF format, error on scanned PDFs; wire frontend file-preview component. Acceptance: PDF fixture exact; unsupported format shows clear warning. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D1-05 — Privacy and deletion vertical slice. Implementation: Add local file-hash/provenance, no raw statement logs, delete-import endpoint and deletion confirmation UI. Acceptance: Deleted rows cannot be queried; privacy test passes. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1112-D2-01 — SQLite schema and seed. Implementation: Migrations for accounts/imports/transactions/aliases/corrections/conversations/insights/evidence. Acceptance: Seed command and foreign keys verified. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D2-02 — Monetary conventions and golden tests. Implementation: Define integer cents, income/refund/transfer handling, periods and currencies. Acceptance: Ten edge cases have expected outputs. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D2-03 — Core spending tool endpoints. Implementation: Implement merchant/category totals, count, average and net recorded cash flow. Acceptance: Exact cents match golden fixtures. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D2-04 — Tool schemas and evidence IDs. Implementation: Pydantic schemas for get_transactions, merchant_summary, category_summary, explain_total. Acceptance: Invalid tool arguments rejected; evidence references resolve. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D2-05 — Financial overview frontend card. Implementation: Build responsive spending summary and merchant table consuming real API. Acceptance: Displays totals and coverage, not mocked numbers. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1112-D3-01 — Colab hardware and training decision. Implementation: Record nvidia-smi, VRAM, dependencies, Qwen3-1.7B revision/license and 4B feasibility. Acceptance: Reproducible hardware notebook and model decision record. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D3-02 — Benchmark set and leakage policy. Implementation: Create held-out synthetic dialogue split by persona/scenario; label intents, tool calls, tone, grounding. Acceptance: At least 150 test cases; no train/test overlap. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D3-03 — Baseline SLM runtime. Implementation: Run original model on local or Colab benchmark; record latency, invalid calls, tool choice. Acceptance: Baseline JSONL outputs and reproducible script. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D3-04 — Constrained tool-call parser. Implementation: Implement model output schema, allowlist, argument validation, bounded retries and safe abstention. Acceptance: Malformed model outputs cannot execute tools. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D3-05 — Chat frontend first slice. Implementation: Build chat composer, message states, tool activity and evidence-link placeholders. Acceptance: User can submit a question and see response/loading/error. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1112-D4-01 — Compass design system. Implementation: Implement brand tokens, typography, spacing, dark/light contrast, accessible components. Acceptance: Tokens documented; contrast checked. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D4-02 — Navigation and import flow. Implementation: Build routes, home, import and transaction review shell with fixture-backed data. Acceptance: Keyboard accessible and responsive. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D4-03 — Chat visual language. Implementation: Create assistant/user messages, local-AI badge, evidence chips and tone selector. Acceptance: Chat shell supports mocked and real API states. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D4-04 — Wrapped story specification. Implementation: Wireframe seven-card journey, chart encodings, empty states, interaction choreography. Acceptance: Storyboard approved with each card tied to source metric. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1112-D4-05 — End-to-end smoke harness. Implementation: Set up Playwright or equivalent and screenshot baseline across import/home/chat. Acceptance: CI executes one navigable browser test. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Review merged PRs, live demo, benchmarks and blocked issues.
Saturday, November 14 — First integrated vertical slice
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1114-D1-01 — Transaction review and correction UI. Implementation: Implement editable merchant/category/date/amount preview and correction provenance. Acceptance: Corrected transaction changes aggregates after refresh. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D1-02 — Duplicate import detection. Implementation: Detect identical file hashes and repeated rows; distinguish duplicates from legitimate repeats. Acceptance: No double count; user sees decision. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D1-03 — Integration test: upload to chart. Implementation: Write browser/API test from CSV upload to merchant total display. Acceptance: Golden fixture visible on UI. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1114-D2-01 — Period comparison tools. Implementation: Add compare_periods and category trend tools with missing-period warnings. Acceptance: Correct month delta and zero-denominator behavior. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D2-02 — Financial X-Ray panel. Implementation: Implement evidence drilldown listing source transactions, exclusions and coverage. Acceptance: Every displayed total opens verifiable breakdown. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D2-03 — Tool-to-UI contract tests. Implementation: Generate typed client and contract fixtures for frontends. Acceptance: No schema mismatch in CI. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1114-D3-01 — End-to-end tool conversation. Implementation: Connect SLM -> approved tools -> grounded response -> chat UI. Acceptance: Three questions answered with correct tool calls. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D3-02 — Training data pipeline. Implementation: Build SFT JSONL with tool traces, empathetic responses, uncertainty and tone variants. Acceptance: 500+ reviewed/generated examples; schema and leakage checks. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D3-03 — Chat safety UX. Implementation: Implement invalid-tool, unavailable-data and uncertainty messages in frontend. Acceptance: UI does not fabricate answer when model fails. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1114-D4-01 — Home-to-Wrapped navigation. Implementation: Build Wrapped entry, story progress, resume and empty-state components. Acceptance: Accessible on mobile and desktop. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D4-02 — Chart primitives. Implementation: Implement reusable bar, heatmap, slope and guess-versus-actual components with accessible tables. Acceptance: Fixtures render correctly with no misleading axes. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1114-D4-03 — Cross-team integrated demo. Implementation: Own import -> correct -> chat -> X-Ray smoke run and defect list. Acceptance: All four flows demonstrated on one fixture. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Review merged PRs, live demo, benchmarks and blocked issues.
Thursday, November 19 — All-team Wrapped build and fine-tuning
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1119-D1-01 — Wrapped data provenance API. Implementation: Expose per-card evidence IDs, import coverage, filters and excluded transactions. Acceptance: Every story card can open source rows. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D1-02 — Merchant normalization and correction feedback. Implementation: Support alias overrides and recomputation of summaries. Acceptance: Alias change updates story and audit trail. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D1-03 — Spending calendar data + UI. Implementation: Implement daily buckets, refunds and calendar heatmap component. Acceptance: Correct date cells; screen-reader table available. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D1-04 — Data quality badges and coverage UX. Implementation: Add account/date completeness indicators and explain missing imports. Acceptance: Incomplete data never labeled complete. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D1-05 — Wrapped contribution integration test. Implementation: Add fixtures for top merchant and busiest day and browser test. Acceptance: Card values exactly match source data. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1119-D2-01 — Insight ranking and deduplication. Implementation: Implement normalized ranking, eligibility, evidence thresholds and diversity rules. Acceptance: No repeated same-merchant cards or unsupported claims. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D2-02 — Guess the Damage engine and UI. Implementation: Build estimate submission, absolute/relative error and animated reveal UI. Acceptance: $80 vs $143 yields $63; edge cases tested. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D2-03 — What If? tool and scenario widget. Implementation: Implement k*average scenario with assumptions, editable input and disclaimer. Acceptance: Conditional values exact and transparent. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D2-04 — Money Awards generator. Implementation: Implement deterministic award selection and award card UI. Acceptance: Award supported by named metrics and evidence. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D2-05 — Wrapped metrics tests. Implementation: Golden tests for MoM, share, streak, ranking, refunds and chart scale. Acceptance: 100% of golden arithmetic cases pass. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1119-D3-01 — SFT/QLoRA training run. Implementation: Train Qwen3-1.7B adapter in Colab with pinned config and checkpoints. Acceptance: Saved adapter, loss curve, GPU metadata, reproducible commands. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D3-02 — Tool and conversation specialization. Implementation: Train on tool traces, corrections, nonjudgmental dialogue and context use. Acceptance: Held-out examples never included in training. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D3-03 — Model adapter inference service. Implementation: Load tuned adapter and connect chat API, with explicit model identity. Acceptance: Model can answer on fixture and logs model version only. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D3-04 — SLM-generated Wrapped commentary. Implementation: Generate grounded card narration and suggested follow-up from structured insight objects. Acceptance: No fabricated numbers in scripted cards. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D3-05 — Model-driven chat tone UI. Implementation: Connect Gentle/Direct/Roast to constrained responses and frontend selection. Acceptance: Same facts in all tones; tone changes only style. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1119-D4-01 — Piggy bank HTML/CSS prototype. Implementation: Create literal ceramic piggy bank with large feather wings and coin slot, not cartoon mascot. Acceptance: Review against user reference; reduced-motion supported. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D4-02 — Pig state machine and chat integration. Implementation: Define idle/listening/thinking/reveal/supportive states and connect to chat lifecycle. Acceptance: No arbitrary model-generated code; states validated. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D4-03 — Wrapped seven-card flow. Implementation: Assemble shared components into story progression, skip/revisit and drilldowns. Acceptance: All cards load from real API. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D4-04 — Confessional screen and context controls. Implementation: Build optional user explanation input, consented memory control and follow-up UX. Acceptance: User can decline; explanation not treated as verified transaction fact. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1119-D4-05 — Cross-dev Wrapped integration. Implementation: Merge Dev1 heatmap, Dev2 awards/guess, Dev3 narration and Dev4 flow. Acceptance: Single story renders correctly end-to-end. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Review merged PRs, live demo, benchmarks and blocked issues.
Saturday, November 21 — Integrated beta
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1121-D1-01 — Statement formats and correction reliability. Implementation: Add second PDF fixture/layout or robust explicit unsupported notice; reconcile edited imports. Acceptance: Supported formats pass and unsupported formats fail clearly. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D1-02 — Wrapped data coverage tests. Implementation: Test missing months, duplicate rows, partial accounts and refunds across all cards. Acceptance: No false full-month claim. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D1-03 — Privacy settings UI contribution. Implementation: Build export/delete local records screen with confirmation and no telemetry default. Acceptance: Deletion and export demonstrable. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1121-D2-01 — Financial X-Ray for every Wrapped card. Implementation: Connect all cards and awards to drilldown, not just overview. Acceptance: Seven-card source inspection works. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D2-02 — Spending insights and trend charts. Implementation: Implement month-over-month slope and cumulative spend with correct scale. Acceptance: Comparisons handle missing baseline. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D2-03 — Financial conversation regression. Implementation: Test model calls against exact tool outputs and claim verifier. Acceptance: Unsupported numeric claims blocked. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1121-D3-01 — Tuned vs baseline interim evaluation. Implementation: Run identical held-out cases for base and tuned model. Acceptance: Preliminary paired metrics and failure examples saved. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D3-02 — Confessional contextual memory. Implementation: Use opt-in local user statements, separate from factual transaction data; support forgetting. Acceptance: No fabricated motives; opt-out honored. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D3-03 — Conversation-to-Wrapped integration. Implementation: Enable SLM follow-up from story cards, clarifications and What If? tools. Acceptance: User can switch between card and chat without losing context. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1121-D4-01 — Pig integration and accessibility. Implementation: Mount coded pig on chatbot, use semantic labels and static reduced-motion fallback. Acceptance: Works across viewport and state transitions. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D4-02 — Full Wrapped UI beta. Implementation: Polish guessing, charts, awards, receipts and chat handoff. Acceptance: First-time user completes seven-card story. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1121-D4-03 — End-to-end beta test and triage. Implementation: Run scripted upload -> correction -> chat -> Wrapped -> Confessional -> What If -> delete. Acceptance: Failures filed with severity and owner. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Review merged PRs, live demo, benchmarks and blocked issues.
Thursday, November 26 — Full-feature validation (Thanksgiving; async allowed)
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1126-D1-01 — Import and privacy robustness. Implementation: Fuzz malformed CSV/PDF, malicious filenames, file size, duplicate detection and local logs. Acceptance: Security/privacy regression documented. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D1-02 — Data export and deletion verification. Implementation: Ensure database, imports, conversation memory and caches obey delete behavior. Acceptance: No recoverable app-level records after deletion on test. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D1-03 — Cross-device setup and data UI. Implementation: Document and test clean install; build import-format helper in UI. Acceptance: Supported laptop demo works without developer fixes. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D1-04 — Wrapped coverage/error handling. Implementation: Test and fix all incomplete-period and bad merchant scenarios. Acceptance: No misleading chart or false confidence. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D1-05 — Data quality benchmark and artifact. Implementation: Compute parse accuracy, coverage, correction success on labeled synthetic corpus. Acceptance: Machine-readable benchmark and UI chart exported. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1126-D2-01 — Finance 100-case benchmark. Implementation: Run exact money tests incl refunds/transfers/rounding and record results. Acceptance: Reproducible pass/fail table. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D2-02 — Grounding validator and claims UI. Implementation: Show evidence for amounts and safe abstention for unsupported claims. Acceptance: Zero unsupported numeric claims in release suite. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D2-03 — Insights ranking ablation. Implementation: Compare ranking with/without diversity and user relevance; generate charts. Acceptance: Document ranking sensitivity and limitations. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D2-04 — Scenario/award bug fixes. Implementation: Fix edge cases and integrate missing source links. Acceptance: No P0/P1 finance issues. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D2-05 — Investor metrics dashboard component. Implementation: Build small local demo page for benchmark scorecards and caveats. Acceptance: All numbers pulled from result JSON, not hardcoded. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1126-D3-01 — Final paired model benchmark. Implementation: Run base vs tuned on fixed held-out cases; report tool exact match, groundedness, tone. Acceptance: JSONL, confidence intervals and error taxonomy. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D3-02 — Local quantization benchmark. Implementation: Measure quantized model on actual available consumer device; memory, p50/p95 latency. Acceptance: Hardware specified and results reproducible. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D3-03 — Privacy/offline network test. Implementation: Test no outbound inference or raw statement telemetry; document model-download exception. Acceptance: Offline after install works on target machine. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D3-04 — Failure repair and regression. Implementation: Fix invalid tools, context overflow, hallucination and unsafe humor. Acceptance: No P0/P1 model issues. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D3-05 — SLM explanation UI improvement. Implementation: Build model status, local-processing disclosure and uncertainty indicators. Acceptance: Users can tell when AI vs deterministic tool acts. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1126-D4-01 — Complete user-journey E2E tests. Implementation: Automate import, correction, chat, Wrapped, X-Ray, What If, settings, deletion. Acceptance: Green on clean supported machine. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D4-02 — Accessible charts and responsive audit. Implementation: Keyboard, labels, contrast, reduced motion, screen-reader alternatives. Acceptance: Documented WCAG-oriented checks. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D4-03 — Usability pilot. Implementation: Run 3-5 consented fictional-data sessions and collect task, comfort, comprehension. Acceptance: Anonymized data and limitations. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D4-04 — Pig refinement and fallback. Implementation: Refine realistic ceramic design, ensure it does not block chat. Acceptance: Approved appearance or neutral fallback. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1126-D4-05 — Product performance and onboarding. Implementation: Optimize load, navigation, install, first-run demo; add helpful empty states. Acceptance: 10-minute scripted demo succeeds. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Full feature validation, but code remains open until Dec 1.
Saturday, November 28 — Coding, benchmarks, stretch improvements
Dev 1 — Data integrity + frontend analytics
- [ ] CMP-1128-D1-01 — Import stretch: additional CSV format. Implementation: Add a third supported mapping and UI format selector if P0/P1 cleared. Acceptance: Fixture import passes or ticket explicitly descoped. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D1-02 — Privacy adversarial check. Implementation: Attempt logs/export/deletion and malicious import failures; patch defects. Acceptance: Signed privacy checklist and fixes. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D1-03 — Wrapped integration polish. Implementation: Fix heatmap labels, receipts navigation and source coverage regressions. Acceptance: No P0/P1 in owned cards. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 2 — Financial intelligence + interactive charts
- [ ] CMP-1128-D2-01 — Benchmark robustness and CIs. Implementation: Compute bootstrap CIs and confusion matrices for finance/tool metrics. Acceptance: Scripts and raw outputs reproducible. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D2-02 — Stretch: recurring subscription story. Implementation: Add recurring merchant frequency story card and UI if core green. Acceptance: Card sourced and inspectable or descoped. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D2-03 — Final numerical audit. Implementation: Audit every demo dollar and chart axis, patch defects. Acceptance: All demo values match golden fixtures. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 3 — SLM training + conversational UI
- [ ] CMP-1128-D3-01 — Model ablation and uncertainty. Implementation: Compare base/tuned and prompt-only baseline if time; error analysis and CI. Acceptance: Honest table with N and limitations. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D3-02 — Stretch: smarter follow-up suggestions. Implementation: Add safe evidence-grounded next-question suggestions in chat. Acceptance: Suggestions execute valid tools only. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D3-03 — Model release hardening. Implementation: Freeze adapter revision, test offline, error handling, and recoverability. Acceptance: No P0/P1 in model integration. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Dev 4 — Experience orchestration + mascot + QA
- [ ] CMP-1128-D4-01 — Stretch: polished story transitions. Implementation: Add restrained transitions and keyboard/reduced-motion parity. Acceptance: No accessibility regressions. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D4-02 — Pilot and UX benchmark finalization. Implementation: Run additional short fictional-data user sessions or complete pilot analysis. Acceptance: Task outcomes and judgment survey recorded. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
- [ ] CMP-1128-D4-03 — Cross-platform smoke and mascot fallback. Implementation: Fix responsive, browser and pig animation issues; rehearse complete flow. Acceptance: Supported device demo passes. Required evidence: PR + test result + screenshot/JSON artifact + reviewer sign-off.
Meeting gate: Review merged PRs, live demo, benchmarks and blocked issues.
December 1–3: ACL-style paper — required for all four developers
These are final-sprint obligations in addition to the 96 engineering tickets (not squeezed into Meeting 6):
Developer	Dec 1 (after freeze)	Dec 2	Dec 3 submission responsibility
Dev 1	Draft Data, preprocessing, provenance, privacy and ethics	Reproduce dataset tables, source coverage and limitations	Verify dataset and reproducibility appendix
Dev 2	Draft financial tool methods, equations, evidence and ranking	Reproduce exact arithmetic and grounding tables/figures	Verify formulas and reported numbers
Dev 3	Draft SLM model, QLoRA, baselines, experimental design	Reproduce paired model results, CIs, errors, hardware and limitations	Verify model/revision/config appendix
Dev 4	Draft abstract, introduction, UX methodology, user study, related work	Assemble ACL LaTeX, screenshots, figures, references and discussion	Produce final PDF, demo package and submission checklist


All four co-review Abstract, Conclusion, Limitations and Ethics. No invented empirical claims. Paper structure: Abstract, Introduction, Related Work, System, Dataset, Model Training, Experiments, Results, Ablations, Ethics, Limitations, Conclusion, References, Appendix. Use official ACL template if required by course; GitHub README equations use $...$ and $$...$$.
Traceability: complete product journeys and test owners
README requirement	Owners (primary + integration)	Acceptance evidence
Local CSV/PDF import, corrections, duplicates	D1 + D4 + D2	Golden fixtures, E2E import/edit and no double count
Local SQLite, coverage, privacy, deletion	D1 + D2 + D4	Migrations, no raw logging, delete test, offline check
Specialized fine-tuned SLM and tool selection	D3 + D2 + D4	Adapter checkpoint, baseline/tuned paired evaluation, tool schema tests
Chat, contextual follow-ups, tones, Confessional	D3 + D4 + D1	Multi-turn E2E, memory opt-out, tone and no-shame review
X-Ray and deterministic financial calculations	D2 + D1 + D4	All monetary claims link to source rows, 100-case tests
Money Wrapped: guessing, awards, four charts	D1 + D2 + D3 + D4	Seven-card story, evidence, accessible chart alternatives
What If? and Teach Me Why	D2 + D3 + D4	Assumption-based tool response; financial concept Q&A benchmark
Flying ceramic piggy bank chatbot character	D4 + D3	HTML/CSS/JS animation states, reduced-motion fallback
Consumer-local model, setup, speed	D3 + D4 + D1	Quantized local inference, offline test, p50/p95 latency, RAM
Evaluation, investor evidence, paper	All four	Reproducible JSON metrics, CIs, UX study, ACL-style report


Explicit scope guard: This is a functional research-grade local desktop/browser-on-localhost MVP, not a commercially certified bank app. Automatic bank sync, real SMS, native mobile deployment, commercial billing, voice, and full-scale consumer security review remain post-MVP. Do not claim an unimplemented stretch goal is complete.
Benchmark calendar and investor-ready metrics
Nov 11–12: baseline. Lock held-out synthetic benchmark and run untuned Qwen3-1.7B; label tool calls, grounded claims, conversation behavior and response times. Publish model revision and N. Nov 19: preliminary tuned checkpoint and smoke metrics. Nov 21: paired interim model and complete journey beta. Nov 23–26: final fixed-set tests, local hardware profiling, privacy, import and human UX pilot. Nov 28: robustness/ablation, confidence intervals, follow-up user testing, no data leakage. Nov 30: regenerate final reproducible benchmark report. Dec 1–3: freeze and write measured results.
Metric	Definition and reporting	Investor significance	Suggested gate (not a claim)
Exact financial arithmetic	correct golden cases / total golden cases; 100+ cases	Trust	100%
Tool selection accuracy	Correct tool / labeled query, with tool-argument exact match separately	Model utility	≥90% tool; ≥85% arguments
Grounded numerical claims	Supported numeric claims / all numeric claims; also count critical invented amounts	Safety	100% in release suite; zero critical fabricated amounts
Nonjudgmental response rate	Blind human rubric, 2+ raters, N, mean and inter-rater agreement	Emotional differentiation	≥90% acceptable; report agreement
Multi-turn task success	Completed user goals / labeled multi-turn scenarios	Conversation usefulness	≥80%
Import precision/recall	Correctly extracted rows and required fields vs labeled fixtures; coverage separate	Reliability	≥98% on supported fixtures
Offline/local privacy	Network egress audit and deletion verification on test machine	Privacy claim	Zero inference payload egress; deletion pass
Device performance	Cold start, peak RAM, median/p95 first-token latency, tokens/s, model disk size	Consumer viability	Measure, then set supported-device target
UX comprehension	Correct responses to questions after dashboard vs static Wrapped vs interactive Compass	Product advantage	Report group sizes, effect and CI, no assumed lift
Perceived judgment	1–5 user questionnaire and comments, comparative where possible	Nonjudgmental positioning	Report raw distribution, not just average
Activation / completion	Users reaching first evidenced insight and completing Wrapped / starters	Product engagement	Report measured funnel; avoid investor forecasts
Willingness to pay	Actual choices or stated intent clearly distinguished	Pricing validation	No revenue claims without real test


Model comparisons: A) base Qwen3-1.7B with same tools/prompts; B) tuned Qwen3-1.7B with same tools/prompts; optional C) prompt-engineered base model; optional D) Qwen3-4B if hardware permits. Keep test set, inference settings, prompts and tool access matched. For binary paired outcomes use paired bootstrap 95% CI (and McNemar when appropriate); for UX outcomes report N, descriptive stats, uncertainty and limitations. Avoid statistical significance claims from a tiny convenience sample.

Benchmark sources: Primarily CompassBench, an explicitly named team-created synthetic benchmark, not a published standard. Supplement with publicly licensed financial QA datasets (e.g. FinQA for arithmetic/reasoning, ConvFinQA for conversational finance) only as out-of-domain checks: they emphasize financial-report reasoning, not bank-statement conversations. Evaluate licensing, leakage and task mismatch before use. For tool calling, consider BFCL-style methodology as an external reference, not as proof that the full benchmark applies to Compass. Document exact benchmark versions, sources and sample sizes.
Quality-control audit of the previous 91 tickets
The previous file contained exactly 91 tickets: 20/12/20/11/20/8 across the six meetings. Its strengths were synthetic-data privacy, deterministic money calculations, SLM tool schemas, fine-tuning, and end-to-end acceptance. Its weaknesses were Dev 4 frontend bottleneck, no even Saturday workload, late all-team Wrapped integration, Nov 26 premature feature freeze, Nov 28 report-only work, and large non-atomic tasks such as “finish all core user journeys.” This revised 96-ticket schedule fixes allocation and traceability, but cannot prove correctness before implementation. Check correctness with unit/contract/E2E tests, benchmark artifacts, cross-owner code reviews, accessibility checks, privacy/offline checks and an explicit pass/fail release checklist. Count is a planning metric, not a quality metric.
G7a. Original four-week plan (superseded)
The earlier illustrative four-week plan is superseded by the date-specific 96-ticket schedule above. Use the schedule above as the single source of truth for deadlines, developer ownership, and release gates.
G8. Academic evaluation — two complementary studies
Study 1: Does fine-tuning improve the SLM?
Compare untuned Qwen3-1.7B vs Compass-tuned Qwen3-1.7B on held-out scenarios, same tools, same hardware and decoding settings. Optionally include Qwen3-4B as a capacity reference. Report tool-call accuracy, numerical grounding, unsupported-claim rate, conversational coherence, nonjudgmental human ratings, agency preservation, and latency/memory. Human raters should score blinded responses and record inter-rater agreement.

A proposed nonjudgmental score for human review is:
\[
J=0.30R+0.25A+0.20E+0.15U+0.10T
\]
where R = respectful language, A = autonomy preservation, E = contextual empathy, U = avoidance of unsupported assumptions, and T = appropriate tone; each is scaled 0–1. These weights are a starting rubric, not validated science. Keep factual correctness separate and mandatory.
Study 2: Does the experience improve financial understanding?
Compare (1) conventional dashboard, (2) static Wrapped, (3) interactive Wrapped + tuned SLM, using equivalent synthetic financial data. Measure comprehension, delayed recall if feasible, engagement, judgment, intent to return, and spending-estimate calibration. Avoid claiming improved long-term financial behavior from a short usability study.

Guess error:
\[
G=|\widehat S-S|,\qquad G_{\%}=100\frac{|\widehat S-S|}{S}\quad(S>0)
\]
For repeated sessions, track whether normalized guess error decreases, controlling for changes in category and data difficulty. Use actual participant data only with informed consent and appropriate privacy procedures.
G9. Explicit benchmark protocol and success gates
Benchmark is not a single leaderboard. Compass needs an SLM benchmark, a financial reliability benchmark, a consumer-device benchmark, and a product-experience study. All figures below are proposed MVP targets, not achieved results or industry standards.
Evaluation	Baseline / comparator	Dataset / method	Proposed pass criterion
SLM specialization	Untuned Qwen3-1.7B vs Compass LoRA-tuned 1.7B; optional 4B reference	200+ held-out synthetic, multi-turn conversations, separated by fictional user/profile and merchant pattern	Clear improvement in blinded nonjudgmental ratings without degrading grounding/tool use
Tool selection	Gold tool-call labels and arguments	100+ intent cases, ambiguous cases included	≥90% correct tool choice on supported intents; report argument exact match separately
Financial arithmetic	Deterministic Python Decimal / integer-cent oracle	100+ unit fixtures plus edge cases: refunds, transfers, missing accounts, zero denominators	100% exact arithmetic on supported fixtures
Numerical grounding	Verified transaction provenance	100+ generated answers, every numerical claim checked	≥99% grounded numerical claims; zero fabricated transactions in demo
Nonjudgmental dialogue	Blinded human evaluation, 2+ raters	50+ scenarios including debt, shame, essentials and opt-outs	Mean ≥4/5; report inter-rater agreement and failure examples
Local feasibility	Quantized tuned model on actual target laptops	Cold start, warm latency, peak RAM, tokens/sec, offline test	Define hardware-specific target after Week 1 measurements; no untested universal speed claim
Product engagement	Dashboard vs static Wrapped vs interactive Compass	Same synthetic financial records, counterbalanced tasks	Report completion, comprehension, recall, perceived judgment, and confidence intervals; no guaranteed uplift


Data leakage controls: train/dev/test split by fictional persona and underlying transaction scenario, not merely by paraphrase. Record model ID/revision, dataset version, LoRA configuration, seed, quantization, hardware, runtime, inference settings and evaluation scripts. Publish anonymized or synthetic examples only.

Training schedule: Week 1 baseline and hardware test; Week 2 synthetic data and evaluation harness; Sprint 2 Week 3 Colab QLoRA fine-tuning of Qwen3-1.7B and optional Qwen3-4B baseline; Week 4 evaluate, quantize, deploy and test. Free Colab GPU availability is variable; scope runs to checkpoint frequently. DPO is optional after a reliable SFT baseline, not a critical-path dependency.
G10. Money Wrapped — chart and metric design system
Rule: one chart = one human question = one surprising verified fact = one optional conversation. Do not create decorative analytics for their own sake. Use accessible labels, plain-language captions, transaction counts, coverage warnings and Financial X-Ray links. Every graph is generated from deterministic calculations; the SLM writes the narrative and asks follow-ups.
Visual	Human question	Core metric	Interactive reveal
Ranked horizontal bars	Where did my money actually go?	Merchant/category spend and share	Guess the top merchant before the bars reorder
Calendar heatmap	Which days got expensive?	Daily spend, purchase count	Tap a bright day to reveal purchases and context
Slope chart	What changed since last month?	Absolute and % category change	Drag a prediction for October, then reveal the actual line
Cumulative line	When did spending accelerate?	Running monthly total vs prior comparable period	Scrub through the month to find the turning point
100% stacked bar	What was my spending mix?	Category share of eligible expenses	Reveal a category's share and the underlying merchants
Dot / lollipop plot	Which habits are frequent vs expensive?	Purchase frequency and average ticket	Contrast '11 small visits' with '2 large purchases'
Small multiples	Did my patterns change across months?	Per-month normalized category or merchant spend	Flip between three months, highlighting one story at a time
Guess vs actual dumbbell	How well do I know my spending?	Estimate, actual and absolute error	The user places the first dot; actual appears afterward


Prefer horizontal bars, heatmaps, slopes and dumbbells over pie charts, 3D graphics, gauges, or dense Sankey diagrams. Use percentages only with meaningful denominators; display dollars and number of purchases alongside ratios. Avoid shame-coded red/green for moral judgments. Reduced-motion and screen-reader equivalents are required.
Wrapped metrics that are both useful and memorable
Metric	Formula / operational definition	Possible story title	Caveat
Top merchant	argmax_v spend(v, month)	Your most loyal relationship	Exclude transfers; normalize aliases
Visit frequency	count(eligible transactions at merchant)	You went back HOW many times?	Purchases ≠ visits when split transactions
Average ticket	merchant_spend / merchant_count	Your usual order	Only if count > 0
Category share	category_spend / total_eligible_expenses	Where the plot thickened	Warn on incomplete accounts
Month-on-month delta	current - prior	Biggest plot twist	Comparable coverage needed
Percent change	100 * (current-prior)/prior	The comeback / the escalation	Undefined when prior = 0
Most expensive day	argmax_day daily_eligible_spend	The day that did the most	Could reflect rent/essentials; don't roast
Small-purchase accumulation	Sum/count of eligible purchases below user-defined threshold	The little things added up	Threshold is user-controlled, not universal
Recurring merchant cadence	Repeated merchant charges at similar intervals	The recurring character	Detect patterns; don't assume subscription
Guessing accuracy	abs(guess-actual) and 100*abs(guess-actual)/actual	You were off by…	Relative error undefined at actual=0
Spending concentration	top_3_merchant_spend / total_eligible_spend	Three names, one plot	Merchants may represent necessities
Spending variability	std(daily_spend) with zero-spend days included	Calm month or rollercoaster?	Contextualize with pay/rent dates
Conditional scenario	avoided_count * observed_avg_ticket	What if you skipped three?	A hypothetical, not promised savings


Narrative sequencing: (1) prediction → (2) dramatic reveal → (3) comparison → (4) contextual question → (5) receipt drawer → (6) user chooses interpretation → (7) optional What If? → (8) takeaway card. The SLM must not invent motives or tell the user which spending was 'bad'.

Example, fictional data: 11 Taco Bell transactions total $143; user guesses $80. Reveal $63 underestimation and an average of $13.00 per transaction. Ask whether this spending felt worthwhile; show the 11 dated receipts. A conditional scenario of three fewer similar purchases is $39.00, not a guarantee. Offer 'Keep it', 'Explore alternatives', and 'Not enough context' as equally legitimate choices.

Story ranking: retain the existing evidence-aware score, but use diversity constraints (no repeated merchant in consecutive cards), sensitivity filters (no joking about medical, debt hardship or essentials), and user-goal relevance. Score emotional interest from surprise and contrast, never from inferred moral failure.
G11. Relationship to Pranav's original model
Pranav's Idea 1 was a bank-hosted assistant with a hosted LLM; Idea 2 was a privacy-first local statement-chat application using PDF/OCR ingestion, normalization, SQLite, a local model (Ollama/llama.cpp), natural-language queries, deterministic Python/SQL calculations and a simple UI. Compass is an evolution of Idea 2, not a wholly separate architecture.
Dimension	Pranav Idea 2	Compass refinement
Privacy	Local processing and storage	Retained, with explicit offline tests and threat model
Data	Multi-bank PDFs, OCR and normalization	Retained; CSV-first MVP with supported PDFs and provenance
Database	SQLite	Retained; corrections, coverage and evidence IDs added
AI	Local model for statement Q&A	Fine-tuned domain-specific SLM is the central conversation orchestrator
Calculations	Python/SQL tools	Retained; exact arithmetic and evidence validator
UI	Functional statement-chat UI	Distinctive neo-editorial product, Wrapped, awards, guessing, Confessional
Evaluation	Accuracy and basic utility	Added SLM fine-tuning study, nonjudgmental ratings, consumer hardware and engagement study
Commercialization	Project prototype	Free/Story Pass/Plus, differentiated positioning, pricing validation


Similarity estimate: Roughly 80–90% of the original technical foundation is retained as a qualitative architecture comparison, not a measured code-overlap percentage. The major new contribution is specialized model training plus interaction design and research evaluation. Credit the original proposal explicitly in the team README.