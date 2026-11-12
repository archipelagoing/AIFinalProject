Compass — Revised 96-Ticket Engineering and Evaluation Plan
Planning baseline: Thursday, November 12, 2026. No work is assumed shipped or verified.
Team: 4 developers × 24 tickets = 96 tickets. Code freeze: December 1, 2026 at 12:00 p.m. ET. ACL-style paper: December 1–3.
This is a proposed replacement backlog, not an audited edit of the original 96 ticket descriptions. The full original issue list was not supplied with this request; the six known ticket IDs are crosswalked below. Ticket names, dates and acceptance criteria here are proposed until the team reconciles them with GitHub. A ticket is not complete without passing evidence.

Product outcome and scope
A working localhost, local-first financial companion: supported CSV/text-PDF import; corrected transactions and provenance; deterministic financial calculations; evidence-backed X-Ray; local fine-tuned SLM; proactive feed of 3–5 meaningful insights; recurring/habit detection; guided conversational audit; contextual Teach Me Why; user-controlled insight preferences; seven-card narrative Wrapped with guessing, awards, charts and receipts; Confessional; What If?; privacy, deletion and offline verification.

Defer: live bank connections, production auth/billing, OCR, native apps, additional statement formats, elaborate mascot animation, excessive chart variations and extra model families. Preserve a simple branded pig mascot/chat identity if time allows.
Six vision upgrades — mandatory acceptance
Upgrade	Definition of done	Primary owners
Proactive discovery	Home shows 3–5 eligible, nonduplicative, evidence-linked insights ranked by surprise, relevance, confidence and diversity; prompts open follow-up	Dev 2 + Dev 4
Recurring behavior	Frequency, intervals, streaks, weekday concentration, recurring charges and trend shifts; uncertainty/coverage flags and tested false positives	Dev 1 + Dev 2
Guided financial audit	Finding → question → optional user explanation/consent → grounded follow-up → next discovery; 3+ turns	Dev 3 + Dev 4
Teach Me Why	One-click, context-specific plain-language explanation tied to actual calculations; uncertainty and no unsupported causal claims	Dev 3 + Dev 4
Insight preferences	More like this / Not interesting / Hide topic / Explore; local persistence and verified suppression	Dev 4 + Dev 2
Narrative Wrapped	Seven coherent cards: hook → surprising pattern → guess → habit reveal → award → explanation/receipts → personalized close; exact metrics locked by Nov 14	All four


Rebaseline: six meetings, outcomes and ticket counts
Meeting	Tickets due (each dev)	Acceptance gate
Nov 12 — Kickoff	5 (20 total)	Contracts, repository and tests established; no assumption that everything is coded
Nov 14 — Vertical slice	3 (12 total)	One import → correction → calculation → X-Ray → chat vertical slice
Nov 19 — Discovery alpha	5 (20 total)	Discovery engine, recurring patterns, tuned model and Wrapped alpha
Nov 21 — Integrated beta	3 (12 total)	Integrated seven-card Wrapped, guided audit, Confessional and What If? beta
Nov 26 — Evaluation and fixes (async permitted)	5 (20 total)	Benchmarks, privacy, user study and fixes; Thanksgiving async acceptable
Nov 28 — Release hardening	3 (12 total)	Regression, ablations, reproducibility and release hardening


Capacity warning: 20-ticket Thursday gates on Nov 12 and Nov 19 are ambitious, particularly since nothing was delivered before Nov 12. Treat ticket counts as allocation, not proof of completion. At the Nov 12 kickoff, estimate hours and reassign or defer low-value work if capacity is insufficient; do not misreport incomplete tickets.
Proposed 96 tickets
Every ticket requires: a merged PR/commit, fixture or demonstration, test/acceptance result, evidence link, independent reviewer, and status (PASS, FAIL, BLOCKED, DEFERRED). A ticket without evidence is NOT VERIFIED.
Meeting 1: Nov 12 — Kickoff
Dev 1 — 5 tickets
- [ ] CMP-1112-D1-01 — Repository setup, reproducible local launch, environment sample. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D1-02 — Transaction schema: integer cents, dates, account and merchant IDs. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D1-03 — Synthetic personal-finance dataset with labeled truth and edge cases. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D1-04 — CSV import contract and first parser with row-level evidence. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D1-05 — Shared UI: import/upload and preview skeleton. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 5 tickets
- [ ] CMP-1112-D2-01 — Deterministic financial calculation APIs and cents-only rules. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D2-02 — Golden financial QA set: 150 independently computed cases. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D2-03 — Aggregation: merchant, category, monthly and date-range totals. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D2-04 — Tool schema for financial queries with evidence references. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D2-05 — Shared UI: first X-Ray breakdown view. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 5 tickets
- [ ] CMP-1112-D3-01 — Choose Qwen3-1.7B baseline and document local runtime constraints. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D3-02 — Define validated tool-call JSON schema and safe error behavior. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D3-03 — Build 100 labeled tool-choice/argument cases plus abstentions. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D3-04 — Base-model runner for tool selection, arguments and latency. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D3-05 — Seven-card narrative storyboard and evidence-safe commentary prompts. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 5 tickets
- [ ] CMP-1112-D4-01 — Compass brand tokens, responsive shell and accessibility baseline. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D4-02 — Navigation architecture: Home, Discover, Wrapped, Chat, X-Ray. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D4-03 — Local API/UI integration contract and error-state mock flows. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D4-04 — Usability protocol: dashboard vs reactive vs proactive Compass. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1112-D4-05 — Frontend: focus on import-to-first-insight path. Accept: merged artifact + reproducible passing test/demo + cross-review.
Meeting 2: Nov 14 — Vertical slice
Dev 1 — 3 tickets
- [ ] CMP-1114-D1-01 — CSV normalization, duplicate fingerprints, transfer/refund fixtures. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D1-02 — Text-PDF parser for one supported layout with coverage reporting. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D1-03 — Import → edit → persist → X-Ray integrated vertical slice. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 3 tickets
- [ ] CMP-1114-D2-01 — Refund/transfer/duplicate math tests and query integration. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D2-02 — Evidence-linked insight object schema and first three insight types. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D2-03 — Basic chart and merchant drill-down connected to actual totals. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 3 tickets
- [ ] CMP-1114-D3-01 — Training examples ≥500 with train/dev/test leakage checks. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D3-02 — QLoRA/LoRA training notebook, reproducible configs and checkpoint. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D3-03 — Guarded tool orchestrator with numeric-answer validator. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 3 tickets
- [ ] CMP-1114-D4-01 — Local runtime adapter, startup diagnostics and offline indicator. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D4-02 — First working responsive import → insight → chat journey. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1114-D4-03 — Automated browser E2E harness and smoke test. Accept: merged artifact + reproducible passing test/demo + cross-review.
Meeting 3: Nov 19 — Discovery alpha
Dev 1 — 5 tickets
- [ ] CMP-1119-D1-01 — Merchant normalization and alias mappings, tested. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D1-02 — Recurring-pattern feature data: interval/frequency/streak/weekday. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D1-03 — Corrections propagate through all dependent derived summaries. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D1-04 — Data completeness and partial-month coverage indicators. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D1-05 — Frontend: transaction review and evidence-link navigation. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 5 tickets
- [ ] CMP-1119-D2-01 — Proactive insight ranking: surprise, relevance, confidence, diversity. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D2-02 — Eligibility, coverage and suppression gates for insight feed. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D2-03 — Recurring behavior detector with confidence and explanations. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D2-04 — Seed 30 labeled discovery patterns and 100 recurring examples. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D2-05 — Frontend: 3–5 discovery cards with question prompts and receipts. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 5 tickets
- [ ] CMP-1119-D3-01 — First tuned checkpoint; base-vs-tuned paired evaluation. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D3-02 — Conversation state: follow-up resolution and user consent. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D3-03 — Guided audit: finding → reflection → follow-up → next discovery. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D3-04 — Gentle/Direct/Roast templates and anti-shaming tests. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D3-05 — Frontend: chat panel with evidence chips and uncertainty messages. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 5 tickets
- [ ] CMP-1119-D4-01 — Discovery home: 3–5 insights, prompts, receipts and empty states. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D4-02 — Insight controls: More like this, Not interesting, Hide, Explore. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D4-03 — Local preference persistence and topic suppression verification. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D4-04 — Seven-card Wrapped UI with deliberate narrative progression. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1119-D4-05 — Cross-feature navigation, keyboard and reduced-motion checks. Accept: merged artifact + reproducible passing test/demo + cross-review.
Meeting 4: Nov 21 — Integrated beta
Dev 1 — 3 tickets
- [ ] CMP-1121-D1-01 — Import QA: 10–15 labeled CSV/text-PDF fixtures, precision/recall. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D1-02 — Privacy controls: local export, clear data and restart persistence. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D1-03 — Wrapped integration: provenance for every story-card metric. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 3 tickets
- [ ] CMP-1121-D2-01 — Seven-card Wrapped metric contracts and deterministic ranking. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D2-02 — Guessing game scoring, awards and time/merchant patterns. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D2-03 — What If? scenario math, no-mutation test and evidence links. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 3 tickets
- [ ] CMP-1121-D3-01 — Wrapped commentary integrated with seven-card state. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D3-02 — Confessional consent, locally stored optional context, opt-out. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D3-03 — Teach Me Why explanations: averages, MoM, cash flow, correlation. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 3 tickets
- [ ] CMP-1121-D4-01 — Guided audit interaction, feedback and Teach Me Why UI. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D4-02 — Full Wrapped → X-Ray → Confessional → What If? E2E. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1121-D4-03 — Small internal beta, issues triaged by impact and severity. Accept: merged artifact + reproducible passing test/demo + cross-review.
Meeting 5: Nov 26 — Evaluation and fixes (async permitted)
Dev 1 — 5 tickets
- [ ] CMP-1126-D1-01 — Import benchmark runner and error taxonomy with artifact export. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D1-02 — Offline network isolation/egress monitoring and tests. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D1-03 — Recurring false-positive fixtures, uncertain-pattern flags. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D1-04 — Cross-review Dev 2 seeded discovery and financial math labels. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D1-05 — Fix P0/P1 import, deletion and provenance issues. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 5 tickets
- [ ] CMP-1126-D2-01 — Run 150 golden cases; fix every financial arithmetic mismatch. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D2-02 — Measure insight precision on 50 reviewed surfaced insights. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D2-03 — Measure seeded discovery recall and recurring precision/recall/F1. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D2-04 — Discovery ablation: ranking on/off, same data and rubric. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D2-05 — Cross-review Dev 3 numerical grounding and answer trace. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 5 tickets
- [ ] CMP-1126-D3-01 — ConvFinQA benchmark adapter and results for compatible subset. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D3-02 — FinQA benchmark adapter and results for compatible subset. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D3-03 — BFCL relevant-subset adapter or explicitly documented incompatibility. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D3-04 — 100 critical grounding checks; 30 multi-turn conversations. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D3-05 — Blind tone scoring, abstention analysis and cross-review Dev 2. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 5 tickets
- [ ] CMP-1126-D4-01 — 5–8-person discovery-yield study with counterbalanced conditions. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D4-02 — Time to first discovery, comprehension, usefulness and comfort. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D4-03 — Local latency p50/p95, peak RAM, tokens/sec on target device. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D4-04 — Run all 12 E2E journeys, mobile and accessibility checks. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1126-D4-05 — Cross-review Dev 1 offline/deletion and fix UX P0/P1. Accept: merged artifact + reproducible passing test/demo + cross-review.
Meeting 6: Nov 28 — Release hardening
Dev 1 — 3 tickets
- [ ] CMP-1128-D1-01 — Fresh-install and unsupported/malformed statement E2E tests. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D1-02 — Regression: corrections, duplicates, refunds and transfer cases. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D1-03 — Final dataset/privacy methodology, figures and limitations for paper. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 2 — 3 tickets
- [ ] CMP-1128-D2-01 — Freeze finance/insight fixtures, rerun reproducible benchmarks. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D2-02 — P0/P1 math, scenario and ranking fixes; cross-owner E2E. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D2-03 — Final financial equations, discovery results and figures for paper. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 3 — 3 tickets
- [ ] CMP-1128-D3-01 — Final paired base-vs-tuned test and 95% interval estimates. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D3-02 — Model runtime/guardrail failure fixes; benchmark reproducibility. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D3-03 — Final training, experiments, ablations, failure analysis for paper. Accept: merged artifact + reproducible passing test/demo + cross-review.
Dev 4 — 3 tickets
- [ ] CMP-1128-D4-01 — Final clean-checkout launch, demo fixture and screen recording. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D4-02 — Usability and E2E reruns; freeze launch documentation. Accept: merged artifact + reproducible passing test/demo + cross-review.
- [ ] CMP-1128-D4-03 — Final UX study, figures, threats to validity, ACL paper integration. Accept: merged artifact + reproducible passing test/demo + cross-review.
Existing-ticket crosswalk (from prior discussion)
Original ticket	Revised expectation
CMP-1119-D2-01 insight ranking	Proactive evidence-backed discovery with confidence, eligibility and diversity
CMP-1128-D2-02 recurring subscription stretch	Move required recurring-pattern implementation to CMP-1119-D2-03; Nov 28 becomes regression
CMP-1121-D3-03 conversation-to-Wrapped	Guided audit and evidence-linked follow-up
CMP-1128-D3-02 smarter follow-ups	Teach Me Why delivered Nov 21; Nov 28 is guardrail fixes
CMP-1119-D4-04 Confessional	Insight feedback and local preference persistence; Confessional integrated Nov 21
CMP-1112-D3-04 Wrapped storyboard	Seven-card narrative locked in kickoff; Dev 3 ticket numbering may differ after reconciliation


Important: The new numbering is a proposed complete backlog, not a guarantee of one-to-one preservation of all original issue IDs. Reconcile before bulk-importing into GitHub.
CompassBench v1 — 12 internal benchmarks
#	Metric	Dataset	Proposed threshold	Owner	First run	Final run
1	Financial arithmetic	150 independently computed cases	100% on release-critical cases	Dev 2	Nov 14	Nov 30
2	Statement import	10–15 labeled supported CSV/text-PDF fixtures	≥98% precision and recall	Dev 1	Nov 14	Nov 30
3	Tool selection	100 labeled prompts	≥90%	Dev 3	Nov 14	Nov 28
4	Tool arguments	Same prompts; exact schema/arguments	≥85%	Dev 3	Nov 14	Nov 28
5	Numerical grounding	100 claims checked against tool evidence	100% on critical suite	Dev 3	Nov 21	Nov 30
6	Multi-turn completion	30 conversations, 3–5 turns	≥80%	Dev 3	Nov 21	Nov 28
7	Insight precision	50 independently reviewed insights	≥95%	Dev 2	Nov 19	Nov 28
8	Pattern discovery recall	30 seeded eligible patterns	≥80%	Dev 2	Nov 19	Nov 28
9	Recurring detection F1	100 labeled positive/negative patterns	≥0.85	Dev 2	Nov 19	Nov 28
10	Local runtime	30 queries on target hardware	Report p50/p95, peak RAM, tokens/s; no invented pass target	Dev 4	Nov 21	Nov 30
11	Privacy and offline	Offline E2E and monitored egress	Zero unauthorized sensitive-data egress	Dev 1	Nov 21	Nov 30
12	Discovery yield	5–8-person exploratory dashboard/reactive/proactive comparison	Report validated discoveries per 5 min; +1/user aspirational	Dev 4	Nov 26	Nov 28


Metric definitions: accuracy = correct / evaluated; precision = valid predicted / all predicted; recall = valid detected / all eligible; F1 = 2PR/(P+R); discovery yield = independently validated meaningful discoveries / participants; p95 latency = 95th percentile end-to-end response time. Add ≥20 abstention cases (incomplete data, ambiguous merchant, unsupported query) and score correct abstention separately. Log denominator, confidence interval where feasible, fixture version and failure examples.
Established benchmarks (separate from CompassBench)
| Dataset | What it demonstrates | Implementation | Date |
|---|---|---|
| ConvFinQA | Multi-turn numerical reasoning on corporate financial reports | Run compatible held-out subset with base and tuned model; document adaptation, exclusions and exact-match/math metrics | Adapter Nov 26; final Nov 28 |
| FinQA | Financial report numerical reasoning | Run held-out compatible subset; report score and whether calculator/tools allowed | Adapter Nov 26; final Nov 28 |
| BFCL | Function selection and argument generation | Use an appropriate published subset if compatible with Compass runtime; otherwise explicitly label a BFCL-inspired internal tool benchmark, not an official BFCL score | Compatibility Nov 14; final Nov 28 |
| FinanceBench (optional) | Evidence-grounded corporate-report Q&A | Include only if time and document-QA scope permit; otherwise defer | Decision Nov 19 |

Validity warning: FinQA, ConvFinQA and FinanceBench are corporate-document tasks, not personal-bank-statement tests. Never present their results as proof of Compass transaction accuracy. Respect published scoring, licenses, splits, prompt formats and tool conditions; clearly distinguish adapted subsets from official leaderboard scores.

Benchmark references: FinQA, ConvFinQA, BFCL, FinanceBench.
Three paper experiments
1. Fine-tuning: base Qwen3-1.7B versus QLoRA-tuned checkpoint with identical prompts, tools and decoding; compare tool selection, arguments, abstention, grounding and latency. Report paired differences and uncertainty.
2. Discovery ablation: conventional dashboard versus reactive Compass versus proactive Compass; counterbalance order and use equivalent synthetic histories. Primary outcome = correctly explained, independently validated discoveries in five minutes; secondary = time to first insight, comprehension, usefulness and comfort. With 5–8 participants, this is formative, not proof of population-wide superiority.
3. End-to-end reliability: independently computed ground truth versus import → deterministic tool → model answer → evidence; compare exact amounts, traceability, correction propagation and failure behavior.
Evaluation calendar
Date	Work
Nov 12	Define benchmark schemas, assign owners, document zero-delivery baseline; create base-model smoke runner if ready
Nov 14	Version CompassBench v1, lock test split, initial import/arithmetic/tool baseline and first vertical slice
Nov 19	First discovery/recurring measurements, base-vs-tuned checkpoint and narrative alpha
Nov 21	Integrated beta, 30 multi-turn cases, grounding and first full Wrapped E2E
Nov 22–26	Formal internal metrics, established-benchmark compatible subsets, pilot study, privacy and runtime
Nov 28	Ablations, cross-review, error analysis, fix failures, publish benchmark artifact bundle
Nov 29–30	Independent clean-checkout rerun, 12 E2E journeys, freeze evidence and paper tables
Dec 1 noon ET	Code/model freeze; exceptions only for documented release blockers
Dec 1–3	ACL-style paper, figures, demo, limitations and reproducibility instructions


Release acceptance and go/no-go
- A new user can install locally and finish: import → correct → discover → explore receipts → Wrapped → guided chat → Teach Me Why → What If? → delete.
- All seven Wrapped cards use actual evidence-backed values; missing/partial data produce honest fallbacks.
- Golden arithmetic and critical numerical grounding have no known incorrect financial claims; any P0/P1 failure blocks release or is transparently scoped out.
- All 12 mandatory E2E journeys are recorded with PASS/FAIL and logs; zero undocumented privacy egress.
- Base/tuned benchmark scores and discovery study results are measured, never invented. If targets are missed, report misses and failure modes.
- Paper contains methodology, data provenance, train/dev/test splits, baselines, comparisons, ablations, limitations and reproducible scripts.
Paper responsibility split
Dev	Paper sections
1	Datasets, ingestion, provenance, privacy, supported formats and limitations
2	Financial engine, equations, discovery ranking, recurring detection and numerical validation
3	SLM setup, training, FinQA/ConvFinQA/BFCL methods, model comparisons and failures
4	Product/UX, comparative study, interface, accessibility, paper integration and release reproducibility


Evidence folder contract
Store versioned benchmarks/compassbench_v1/ fixtures and locked held-out cases, eval/results/<run-id>/ JSON/CSV scores, model/config hashes, machine specs, test logs, E2E traces and anonymized study summaries. Never include real bank statements or personally identifying financial data in the repository.
Risks and explicit fallbacks
- Time: 96 tickets in 19 days is high risk from a zero-delivery start. Re-estimate Nov 12; prioritize one complete path over breadth.
- Training feasibility: If QLoRA checkpoint cannot run on target hardware, keep the baseline+guarded tools working, report tuning as incomplete, and avoid claiming fine-tuned offline deployment.
- External benchmarks: If adapters require too much time, prioritize CompassBench + one compatible established benchmark; disclose omitted ones.
- User study: If 5–8 participants are unavailable, report a smaller formative pilot and do not infer statistical superiority.
- Scope: Simplify animation, format breadth and visual polish before dropping evidence, privacy or core discovery.