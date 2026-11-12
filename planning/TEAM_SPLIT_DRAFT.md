# Compass team split — draft for review

**Prepared November 11, 2026. Roles are unassigned.** This is a proposed allocation, not a claim that work is complete or a replacement for the published 96-ticket backlog yet. No GitHub issues are changed. The [product specification](../PRODUCT_SPEC.md) remains untouched. The next step after reviewing this draft is to write the individual developer guides and detailed tickets.

## 1. What the team is delivering

A local application in which someone imports a statement, corrects it, asks questions, explores Money Wrapped, inspects the underlying transactions, discusses their circumstances, and tries conditional What If? scenarios. A fine-tuned local model conducts the conversation; deterministic Python functions calculate the numbers.

The final project also needs reproducible evidence: data/finance tests, base-versus-tuned model results, local-device measurements, a small product-experience study, and an ACL-style report with a working demo. Software and research are both deliverables.

## 2. What exists and what still needs work

This inventory comes from reading the source, not a fresh test run. Existing behavior must be verified before counting it toward a checkpoint.

| Area | Existing starting point | Remaining work |
| --- | --- | --- |
| Import/storage | `compass/importer.py`, `mapping.py`, `contracts.py`, `db.py`; CSV parsing, identity, duplicate checks, SQLite | Public API, supported PDF, broader correction model, coverage, new UI and deletion integration |
| Corrections | `db.correct_classification()` changes type/category; original source fields are immutable | User-facing correction requests beyond type/category need an explicit override design; do not overwrite raw amounts/dates |
| Finance/evidence | `analytics.py`, `questions.py`, `scenarios.py`; summaries, five bounded question tools, source rows, rent scenarios | Merchant/period/recurring tools, Wrapped insights, awards, scenario extensions, claim validation |
| Model | `compass/ollama.py`; optional intent routing constrained by a deterministic parser | Synthetic dialogue pipeline, baseline, training, export, full multi-turn orchestration and evaluation |
| Interface | `app.py` Streamlit; separate static `docs/` demo | React/TypeScript application calling a local FastAPI API |
| Verification | Fixtures, Python/JS tests, audit scripts, existing smoke script | Tests of the new API/React journey, model benchmarks, packaged-device checks, comparative UX study |

Do not rebuild existing modules just because an old ticket says “create.” The static demo's JavaScript calculations are not a second authoritative financial engine for the new app. See the [repository guide](../REPOSITORY_GUIDE.md) and [transition guide](BUILD_TRANSITION.md).

## 3. The proposed four roles

| Role | Your responsibility in plain language | Your visible contribution | What you do not inherit |
| --- | --- | --- | --- |
| A — Data and app foundation | Get trustworthy records into the application and make the local app usable from the first screen | App shell/navigation, import/review, correction, coverage, privacy/deletion, local setup | Financial formulas, model training, model runtime, or repairing everyone else's feature bugs |
| B — Financial experience | Make every financial discovery correct, inspectable, and engaging | Financial tools, X-Ray, charts, Guess/Reveal, awards, What If?, and Wrapped pages | App-wide navigation, model training, conversation runtime, or packaging |
| C — Model research | Build, train and measure the specialized conversational model | Trained artifact, grounded dialogue examples, tone/context behavior, research results | React shell, mascot animation, packaging, or the full runtime orchestration service |
| D — Conversation runtime | Make the model, verified finance tools, and user conversation work safely together | Local inference service, tool validation/dispatch, chat, Confessional, opt-in memory, runtime tests | App shell, Wrapped pages, whole-product QA, packaging, or all integration repairs |

**Why these boundaries:** A and B can reuse substantial Python code, so they each own both behavior and the screens that expose it. C has a compute-dependent research workload, so unrelated visual tasks are removed. D owns one complete technical system—the conversation loop—rather than becoming the default owner for all application integration.

All four own tests and documentation for their work. C contributes interaction contracts and behavior tests rather than being forced to write unrelated frontend code merely to equalize participation. That is a proposed change to the old plan's “everyone writes frontend” rule, to accept or revise with this split.

## 4. File boundaries and handoffs

Paths are relative to the project root. **New paths below are proposals, not existing scaffolding.**

| Role | Existing files to start with | Proposed new locations |
| --- | --- | --- |
| A | `app.py`; `compass/importer.py`, `mapping.py`, `classification.py`, `contracts.py`, `db.py`; `fixtures/`; `scripts/` | `api/main.py`, `api/routes/imports.py`, `api/routes/privacy.py`; `frontend/src/app/`, `features/import/`, `privacy/`, `coverage/`; local setup documentation |
| B | `compass/analytics.py`, `questions.py`, `scenarios.py`; `tests/python/` | `api/routes/finance.py`; `compass/insights.py`, `compass/claims.py`; `frontend/src/features/finance/`, `features/wrapped/`; finance evaluation scripts |
| C | `fixtures/`; `compass/ollama.py` as a reference, not a training pipeline | `model/` for dataset/training/export configuration; `evaluation/model/`; dialogue fixtures and behavior specifications |
| D | `compass/ollama.py` for local transport constraints; `app.py`, `docs/` as interaction references | `api/routes/chat.py`; `compass/conversation.py`; `frontend/src/features/chat/`, `features/confessional/`; conversation-runtime tests |

A initializes the app/API skeleton once; B and D add their own route modules and feature components. A owns database migrations for import/data features. D specifies and owns the lifecycle of user-approved conversation state, while A reviews storage changes for local-data/privacy consistency. B owns tool definitions and financial claim checks. C owns model artifacts/prompts and their evaluation. D owns loading/invocation, constrained dispatch, retries, context orchestration, and chat/Confessional failure states.

A database change or shared schema change is reviewed by its consumer before merging. Do not have two people independently change the same shared contract.

### Required shared examples

Before parallel implementation, commit small synthetic examples for these interfaces. These are contract requirements, not finalized JSON schemas.

| Producer → consumer | What must be agreed |
| --- | --- |
| A → B/D | Transaction ID, immutable source reference, effective corrected fields, account/date scope, coverage and invalid-row errors |
| B → C/D | Tool name, argument schema, exact-cent output, included/excluded IDs, formula, coverage, unsupported-request response |
| C → D | Model/adapter revision, loading/export instructions, prompt/tool format, sample response, context limit, behavior examples |
| B/C → D | Story facts and evidence from B; narrative behavior from C; explicit separation between facts and generated commentary |
| D → A | Runtime startup requirements and the location/lifecycle of conversation state |

While waiting on an implementation, work against agreed fixture payloads. Fixture-backed UI is an intermediate deliverable and must not be represented as integrated completion.

## 5. Weekly delivery plan

Thursday and Saturday are **review deadlines**, not start dates. Each cell lists actions in intended order and the result to show. Estimates in section 6 include both checkpoints together.

### Week 1 — November 11–14: contracts and the first connected journey

**Reality check:** November 12 is tomorrow. The old plan expected substantial work starting November 10. This draft proposes a smaller November 12 contract/baseline checkpoint, not an implausible claim that every foundation can be built in a day. Confirm this gate adjustment as part of adopting the draft.

| Role | Thursday, Nov 12 — show this | Saturday, Nov 14 — show this |
| --- | --- | --- |
| A | Run existing fixture import; document supported CSV fields, identity and correction limits; create the minimal app shell/navigation and supply transaction/error examples | Expose CSV preview/import, classification correction and coverage through API routes; connect an import/review component; show a correction reflected in a refreshed summary |
| B | Verify a known fixture total and source rows; define shared tool/evidence examples and sign/refund rules | Wrap existing supported tools in API routes; deliver summary and X-Ray component; demonstrate an exact total and its included/excluded records |
| C | Confirm available training hardware/model candidate; define train/dev/test separation and evaluation rubric | Save reproducible untuned baseline outputs and initial reviewed synthetic training examples; give D model/tool response examples and run instructions |
| D | Define chat request/response shape with B/C and create the conversation route/service skeleton | Deliver basic chat with validated supported-tool dispatch, loading and failure states; integrate the B tool contract into the conversation loop |

**Team demo:** import → correct classification → summary → question → evidence on one fixture. If model execution is blocked, a labeled stub can prove wiring, but the model part of the checkpoint remains blocked. Existing deterministic routing is not evidence of the required trained conversational model.

**Critical dependency:** D's skeleton and the shared examples must be available before A/B finish UI/API wiring. C's baseline work can proceed independently on synthetic fixtures. Review Saturday feasibility immediately after Thursday's baseline check.

### Week 2 — November 16–21: specialized model and full product loop

| Role | Thursday, Nov 19 — show this | Saturday, Nov 21 — show this |
| --- | --- | --- |
| A | Add one supported text-PDF format with clear unsupported/scanned-file errors; implement correction overrides/merchant aliases without changing raw records; supply coverage/calendar component | Finish import/coverage regressions, privacy screen, and app navigation; prove confirmed deletion includes A-owned app state |
| B | Add merchant/period/recurring-candidate calculations, ranked insights and award facts; deliver Guess/Reveal, conditional scenario, and first Wrapped pages | Connect X-Ray to all story facts, charts and awards; add claim validation and invalid-evidence cases; verify $80 vs $143 gives $63 and three purchases at $13 gives conditional $39 |
| C | Validate synthetic training set and complete first checkpointed LoRA/QLoRA run; supply versioned artifact plus narration/tone examples | Compare base/tuned with the same protocol; inspect sensitive-context and uncertainty failures; hand D export/loading instructions and reproducible examples |
| D | Load the model artifact when available; connect chat, approved tools and grounded narration | Complete Confessional opt-in/forget behavior, story-to-chat context, tone control, safe failure states, and conversation-runtime tests |

**Team demo:** import → review → Wrapped guess/reveal/awards → receipts → discussion → What If? → delete. Coverage warnings must survive the entire journey. The first tuned checkpoint is due November 19; delayed GPU access must be recorded, not disguised as completion with a base model.

**Critical dependency:** B's story/tool schemas must stabilize before C trains tool traces and D connects narration. C supplies the artifact; D owns app runtime integration. D defines conversation-state lifecycle and consent behavior; A reviews the storage change and deletes it through the privacy flow.

### Week 3 — November 23–28: verification and release candidate

| Role | Thursday, Nov 26 — show this | Saturday, Nov 28 — show this |
| --- | --- | --- |
| A | Run malformed import, provenance, export and deletion checks; test app navigation/setup; record data-quality results | Verify clean setup and A-owned screens on two available representative machines; repair owned failures and publish setup/privacy evidence |
| B | Produce the 100+ case financial result table and audit all displayed claims; implement result-table generation and Wrapped checks; run ranking sensitivity checks | Independently reconcile demo amounts and chart scales; finalize financial/grounding artifacts, Wrapped pages, and the product-study analysis |
| C | Run fixed-set base/tuned comparisons and blinded tone review with a second teammate; export/quantize and measure local latency/memory | Complete error analysis, reproducibility metadata and feasible ablations; finalize model artifact/version and report limitations without changing test rules after seeing results |
| D | Run conversation-runtime tests: invalid tools, context limits, memory consent, timeouts, and evidence handoff | Repair runtime regressions, rehearse the conversation portion of the demo, and attach defects with specific feature owners |

November 26 may use asynchronous evidence review for Thanksgiving. B owns the pilot protocol/session coordination; A and D each facilitate a session or rate a bounded batch, included in their time budget. C owns the model study; B supplies independent blinded ratings and analysis support. Small pilot findings must not be presented as proof of long-term behavior change.

**Team demo:** a fresh setup completes the entire product journey, with reproducible finance/model results and a clear known-issues list. Cosmetic polish does not take priority over incorrect amounts, privacy failures, or a broken core journey. A failing feature goes back to its owner, not automatically to D or the person with Codex.

### Finalization — November 29–December 3

| Role | Nov 29–Dec 1 noon ET: verify and freeze | Dec 1–3: report and submission contribution |
| --- | --- | --- |
| A | Re-run import, correction, deletion, navigation and clean setup | Dataset/preprocessing/privacy/ethics section, dataset table, setup appendix; verify submitted repository instructions |
| B | Re-run financial audit and regenerate frozen result tables | Financial methods/equations/validation/results and Wrapped/product-study results; assemble report source and verify table/figure values |
| C | Freeze model/data/config identifiers and reproduce benchmark outputs | Model/training/experimental protocol/model results/error analysis; verify model artifact instructions and citations |
| D | Re-run the conversation loop and runtime failure states | Conversation-system section; produce chat/Confessional screenshots and review demo/runtime claims |

Each person writes their own limitations and reproducibility notes. Report review ring: A reviews B, B reviews C, C reviews D, D reviews A. B assembles the report from supplied sections; B is not responsible for writing missing sections. All four review the abstract, conclusion and final claims. Nominate one submitter when names are assigned; submission is a checklist task, not a separate engineering role.

**Freeze remains December 1 at noon Eastern.** Report/submission period remains December 1–3; the actual course submission time needs confirmation. After freeze, use the existing engineering plan's recorded emergency-change rule.

## 6. Workload estimate and fairness check

These are rough active-person-hour estimates for this draft, not measured estimates or confirmed availability. They include implementation, focused tests, one cross-review per checkpoint, integration, and evidence. GPU waiting is not active work, but can delay dependencies. The ranges assume working familiarity with Python and the ability to learn basic React; learning time could increase them substantially.

| Role | Week 1, remaining Nov 11–14 | Week 2 | Week 3 | Finalization/report | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| A | 14–20 h | 20–28 h | 16–22 h | 10–14 h | 60–84 h |
| B | 12–18 h | 22–30 h | 18–24 h | 12–16 h | 64–88 h |
| C | 14–20 h | 20–30 h | 18–26 h | 10–14 h | 62–90 h |
| D | 12–18 h | 18–26 h | 14–20 h | 8–12 h | 52–76 h |

**This is comparable, not perfectly equal.** B and C carry the highest central estimates; C also has the largest compute uncertainty. D is intentionally lighter because conversation runtime depends on upstream contracts and artifacts. Week 2 is heavy for everyone. If teammates only have 8–10 hours/week, this draft is not feasible as written; changing ticket wording cannot fix that. Confirm capacity before making these dates commitments.

Bounded rebalancing options, without changing product requirements:

- If A is overloaded, D takes a bounded navigation/error-state component and A keeps import/privacy correctness. Broad OCR and extra formats are already stretch; do not quietly remove the required known text-PDF path.
- If B is overloaded, A takes one fixture/edge-case batch, and D takes a bounded chat-to-Wrapped handoff component. B keeps financial rules and evidence contracts.
- If C is overloaded, transfer reviewed synthetic-example batches and analysis scripts to B, using C's schema and rubric. C keeps split integrity and training ownership.
- If D is under-loaded after contracts stabilize, take a named conversation-related test or UI state from B or A. Do not assign general cleanup work.

Each checkpoint's integration coordinator gets a planned 1–2 hour coordination block inside their estimate: A on Nov 12/14, B on Nov 19/21, C on Nov 26, D on Nov 28. This person runs the checklist and records blockers; feature owners fix their own failures. No person becomes the default cleanup engineer because they have Codex.

## 7. How the split contributes to the final project

| Deliverable | Accountable role | Essential contributions from others |
| --- | --- | --- |
| Trustworthy imported records and app foundation | A | B checks sign/refund conventions; D consumes records through approved contracts; C uses only approved synthetic examples |
| Exact, inspectable financial discoveries and Wrapped | B | A provides records and app shell; D uses approved tool/evidence results; C verbalizes tool-backed facts |
| Fine-tuned model and research comparison | C | B validates numerical examples/ratings; D integrates inference; A verifies local deployment boundary |
| Safe conversational system | D | A supplies record/privacy contracts; B supplies finance/evidence tools; C supplies model artifacts and behavior |
| Local delivery and privacy evidence | A | D supplies runtime requirements; C supplies model requirements; B supplies known-result verification |
| Product-experience study | B | A/D assist sessions; C helps interpret dialogue failures without overstating results |
| ACL report and demonstration | All four; B assembles report | Each role supplies its own section, figure/table, limitations and reproducibility evidence |

A makes trustworthy records and a usable local foundation. B makes the financial story correct and usable. C supplies and measures the project's AI contribution. D makes the model and verified tools into a safe conversation. Removing any one leaves an incomplete final project.

## 8. Team rules

These are working agreements, not a scoring system. They exist to keep integration from turning into invisible extra work for one person.

1. **Own the result, not just the code.** A feature owner delivers the implementation, its tests, a short setup note, and evidence that the stated behavior works.
2. **Hand off a contract, not a vague request.** Before another person depends on your work, provide a versioned example payload or artifact, expected result, and known limits. “It should work” is not a handoff.
3. **The defect goes back to the subsystem that caused it.** The person running a demo records a failure; the feature owner fixes it. An integration coordinator is not the default repair person.
4. **Freeze shared contracts before parallel work.** A, B, C, and D use the examples in section 4. Changing a shared schema requires notifying its consumers and updating the fixture/example in the same change.
5. **Use fixtures for parallel work, label them honestly.** A screen can use agreed fixture data while an API is unfinished, but it is not complete until it works against the real integration.
6. **Protect correctness and privacy first.** Incorrect money, fabricated evidence, loss of records, or a deletion/privacy failure stops polish and stretch work until fixed.
7. **Integration time is planned work.** Every checkpoint includes a 1–2 hour coordination/review block. It counts toward workload; nobody is expected to absorb unlimited integration because they are faster or have Codex.
8. **Model work has a stable boundary.** C owns model quality, training, and reproducibility. D owns runtime behavior. B owns financial truth and evidence. A owns local records and privacy. Do not silently move a failure across those boundaries.
9. **Use measured evidence in the report.** Do not turn a demo, an unverified ticket, or a small pilot into a stronger claim than the recorded tests support.
10. **Rebalance named work, not anxiety.** If someone is overloaded, transfer a specific task with a clear outcome, estimate, and new owner. Do not assign “help with whatever is needed.”

## 9. How this becomes clear tickets

After agreement, create a developer guide for each role and small numbered task files. One canonical ticket body; guides link to it. Keep old CMP IDs in a mapping rather than losing coverage when consolidating the old backlog.

Every ticket must include: one plain-language outcome; reuse/extend/create label; exact files to read/change; ordered steps; example input/output; prerequisite and producing owner; test command or manual steps with expected results; what to submit; and a copy-ready ChatGPT prompt listing only the relevant context files. New verification commands must be implemented with the task, not presented as already available.

Existing baseline commands, from the project root, are `python -m pytest -q`, `python scripts/audit_fixtures.py`, `python scripts/audit_privacy.py`, and `npm test`. These do not prove the future React/FastAPI/model paths work.

Example task outcome: “Upload a supported synthetic CSV through the import screen, show row-level validation errors, confirm import, and display its coverage.” Its prerequisite is the agreed import API contract and app shell. It is complete only when the real API path works—not when a screenshot renders fixture data. The detailed ticket will name the exact functions, files, and verification steps after scaffolding decisions are finalized.

## 10. Decisions needed before adopting this draft

- Assign names based on experience and preference, not AI subscription access.
- Confirm weekly availability and local/Colab hardware access; revise estimates accordingly.
- Accept or revise the smaller November 12 checkpoint and the role-boundary change described above.
- Confirm the proposed directories, shared contract examples, and local setup ownership (A, with D's runtime requirements and C's model requirements).
- Map every old ticket/requirement to a new task, existing verified behavior, or an explicitly reviewed scope decision. This draft groups work; it does not claim exhaustive ticket-level coverage yet.

The historical developer guides and generated issue files retain their old assignments until this draft is accepted and translated. No requirement is marked complete or silently removed by this document.
