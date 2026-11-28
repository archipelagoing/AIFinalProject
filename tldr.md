# Dev 3 — Gate 1 TL;DR

---------------------

1. `CMP-1112-D3-01` — Colab hardware and training decision

- Selected Google Colab with an NVIDIA L4 for initial model experiments.
- Recorded NVIDIA L4 hardware with 23,034 MiB GPU memory, CUDA 13.0, driver 580.82.07, and Python 3.13.16.
- Selected Qwen3-1.7B as the starting model and recorded its Apache-2.0 license.
- Confirmed that Qwen3-1.7B loads successfully on the L4.
- Smoke test measured 7.268 seconds latency, 4.54 tokens/second, and 3.22 GiB peak GPU memory.
- Finding: Colab is useful for development evidence, but the customer-facing product should run locally so financial data stays on-device.
- Remaining: assess whether Qwen3-4B is feasible and record the exact Colab runtime version if required.

---------------------

2. `CMP-1112-D3-02` — Benchmark set and leakage policy

- Created 160 fictional conversation examples.
- Split the dataset into 80 training examples and 80 held-out test examples.
- Included supported spending questions, merchant questions, monthly comparisons, follow-ups, ambiguous requests, unsupported requests, and clarification cases.
- Labeled persona, scenario, expected intent, expected tool, tone, arguments, and evidence requirements.
- Verified zero duplicate questions and zero scenario leakage between train and test splits.
- Finding: the held-out set measures both correct tool use and safe refusal/clarification.
- Files: `model/benchmark_train.jsonl`, `model/benchmark_test.jsonl`, `model/benchmark_report.json`, and `model/build_benchmark.py`.

---------------------

3. `CMP-1112-D3-03` — Baseline SLM runtime

- Ran the untrained Qwen3-1.7B model against 80 held-out synthetic cases.
- Recorded responses, selected tools, argument validity, clarification behavior, possible numeric invention, and latency.
- Findings: 50% tool-match rate, 100% approved-tool rate, 7.5% valid-argument rate, 25% appropriate-clarification rate, zero possible numeric inventions, and 0.954 seconds mean latency.
- Main finding: the model can select approved tools but frequently produces invalid arguments and routes unsupported merchant/comparison questions to tools.
- Safety implication: raw model output must never be dispatched directly; schema validation and deterministic fallback are required.
- Files: `model/baseline_results (2).jsonl`, `model/baseline_report (2).json`, and `model/baseline_evaluation_qwen3_1_7b.ipynb`.

---------------------

4. `CMP-1112-D3-04` — Constrained tool-call parser / Wrapped story specification

- Verified the existing loopback-only router in `compass/ollama.py`.
- Added safety tests for approved calls, unknown tools, missing and extra arguments, invalid months/categories/limits, malformed JSON, changed filters, unsupported questions, timeouts, and local failures.
- Confirmed that routing never executes financial tools directly.
- Documented the approved tools, schema, validation rules, immediate deterministic fallback, and safe-abstention behavior in `model/tool_call_parser.md`.
- Phase 3 safety tests pass: 70 passed. Full Python suite passes: 275 passed.
- Decision: do not retry invalid tool calls by default; deterministic parsing already knows the supported request and avoids extra latency and unsafe variation.
- Remaining: confirm with the team whether D3-04 officially means the parser or the Wrapped story specification, attach evidence, commit/push the latest files, and obtain cross-owner review.
- If D3-04 means Wrapped story specification, choose one of the four options in `todo.md` and create the approved seven-card storyboard.

---------------------

5. `CMP-1112-D3-05` — Chat frontend first slice

- Used the existing Streamlit app as the first chat experience.
- Tested the question: `What was my surplus in May 2026?`
- The app displayed deterministic routing, the `get_surplus` tool, the verified result `$747.06`, the query period, the calculation formula, included-row count, evidence, and a coverage warning.
- Finding: the current app demonstrates a safe request-to-response flow using synthetic data and deterministic calculations.
- Remaining: document or capture a loading state, save the chat screenshot, attach the test/evidence artifacts, commit/push the final changes, and obtain cross-owner review.

---------------------

6. TL;DR squared — the whole Gate 1 review

- **D3-01: Hardware/model decision.** I tested Compass in Colab on an NVIDIA L4, recorded the environment, selected Qwen3-1.7B, and measured a successful smoke test. What did not work: the base model initially refused a Compass financial-routing prompt, and Qwen3-4B has not been assessed yet. Remaining: record the exact Colab runtime version if required and decide whether 4B testing is worth doing.
- **D3-02: Benchmark and leakage policy.** I created 160 fictional examples, split them 80/80, and verified no duplicate questions or scenario leakage. What did not work: the first test split contained only unsupported questions, so it could not measure supported tool selection. I corrected the split and reran the benchmark.
- **D3-03: Baseline SLM runtime.** I evaluated Qwen3-1.7B on 80 held-out cases. The model matched the expected tool 50% of the time, produced valid arguments only 7.5% of the time, had a mean latency of 0.954 seconds, and invented no financial numbers. Finding: the model is fast enough to test but unsafe to dispatch directly.
- **D3-04: Parser/story scope.** I verified and tested the constrained router, documented the schema, allowlist, fallback, and no-retry policy, and reached 70 passing Phase 3 tests. What remains: the team must confirm whether D3-04 officially means the parser or the Wrapped storyboard. If it means the parser, the remaining work is evidence attachment, commit/push, and cross-owner approval. If it means Wrapped, a seven-card storyboard must be approved.
- **D3-05: Chat frontend.** I demonstrated the existing chat flow with a synthetic statement. Compass returned the correct May surplus of $747.06, showed deterministic routing, the selected tool, formula, evidence count, and a coverage warning. What remains: capture the screenshot, document a loading state, attach evidence, and get review.
- **What passed overall.** The Python suite passed with 275 tests, the JavaScript suite passed with 17 tests, and the fixture audit passed with 164 transactions and reconciled monthly totals.
- **What did not work or is incomplete.** The base model is unreliable at argument formatting and unsupported-request handling; the first benchmark split was incomplete; the Colab smoke prompt produced a refusal; the exact runtime version and Qwen3-4B feasibility are not recorded; and the final screenshot/review package is unfinished.
- **Next steps.** First, commit and push the parser tests, parser documentation, baseline artifacts, updated todo, and chat evidence. Second, confirm the D3-04 scope with the team. Third, save the chat screenshot and document loading/error behavior. Fourth, attach the test output and JSON evidence to the tickets. Finally, get cross-owner review and record approval.

---------------------

7. Wrapped Story options to pitch to the team

### Option 1 — Guess the Damage

- Welcome and coverage
- Guess a category total
- Reveal the verified amount
- Show the receipts
- Explain the spending pattern
- Ask what was happening
- Try a What If? change
- Pitch: the most playful and distinctive Spotify Wrapped-style experience.

### Option 2 — Your Month in Receipts

- Month overview
- Income and expenses
- Biggest spending category
- Largest individual purchases
- Transaction receipts
- Missing or uncertain data
- Suggested follow-up question
- Pitch: the clearest option for trust, transparency, and financial correctness.

### Option 3 — The Spending Story ***Pranav Preference

- What kind of month was this?
- Where most money went
- The biggest surprise
- A meaningful spending pattern
- Evidence behind the pattern
- User explains the context
- Decide whether anything should change
- Pitch: the strongest option for a conversational and emotionally intelligent product.

### Option 4 — Choose Your Own Money Adventure ***Pranav Evidence

- Welcome and coverage
- Pick a category or merchant
- Guess or inspect the total
- Reveal the evidence
- Compare with another month
- Explore a What If? scenario
- Save a takeaway or ask Compass another question
- Pitch: the most flexible option, but it requires the most interaction design.

* Pranav: Spending patterns, where the curstomer could have spent less & saved more money
* Mandar: First say you're doing good but criticize what you're doing wrong
* Should give ideas to the customer based on their spending:
    - Wrapped should be able to 
* STAR method: Situation, task, action, reason
        * taco bell $83- 143, -> Spend less on Taco Bell --> Alert customer about repeated transaction (ex: twice a week) ---> customer will be thoughtful of spending more. 
        * If he's spending more than 20% on groceries, give an alert about how much he should be saving
        * --> say that he has to spend more on savings next month
        * ---> final alert that spending too much: what is a good consequence? a terrrible roast? 
        * --Maybe a funny version, a roast version, an encouragement mode
        * ----> saving: give a congrati. Reward
* Om: Lets try to gamify it like duolingo, how can the user be rewarded and have the game
### Recommended pitch

Start with **Option 1 — Guess the Damage**. It makes financial review participatory, memorable, and clearly different from a normal dashboard while keeping every number tied to deterministic evidence.
