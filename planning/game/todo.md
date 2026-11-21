# Dev 3 — Gate 1 Todo

This checklist covers Dev 3’s Gate 1 responsibilities: model feasibility, evaluation, safe tool use, and the first chat experience.

## Verification status — November 21, 2026

The repository baseline was checked after installing the development dependencies in `.venv`.

- [x] Fixture audit passed: 164 transactions and all monthly totals reconciled.
- [x] JavaScript test suite passed: 17 tests passed, 0 failed.
- [x] Python test suite passed: 272 tests passed, 0 failed.
- [x] Streamlit startup test passed on rerun; the earlier timeout was transient.
- [x] Planning-matrix validation passed after the validator was updated to resolve the repository’s `planning/` document location.

The planning validator change is in `scripts/audit_privacy.py`. It preserves compatibility with callers that pass the historical repository-root plan path while using the current `planning/COMPASS_ENGINEERING_PLAN.md` location. The Streamlit test passed without an application-code change.

Commands used:

```bash
python -m pytest -q
python scripts/audit_fixtures.py
npm test
```

Latest Python result:

```text
272 passed in 33.58s
```

## 1. Get familiar with the repository

- [ ] Run the existing Python tests:

  ```bash
  python -m pytest -q
  ```

- [ ] Run the fixture audit:

  ```bash
  python scripts/audit_fixtures.py
  ```

- [ ] Read `compass/ollama.py`.
- [ ] Read `compass/questions.py`.
- [ ] Read `compass/contracts.py`.
- [ ] Read `planning/developers/1.Dev3_README.md`.
- [ ] Review the relevant sections of `PRODUCT_SPEC.md`.

## 2. Make the hardware and model decision

- [ ] Record the available Colab GPU and VRAM.
- [x] Record the available Colab GPU and VRAM: NVIDIA L4, 23,034 MiB GPU memory.
- [x] In Colab, select **L4 GPU** as the default hardware for initial model testing.
- [x] Turn **High-RAM** on.
- [ ] Leave the runtime version on **Latest** for the first experiment; record the exact version shown by the runtime.
- [ ] Use an **A100 GPU** instead if fine-tuning requires more memory and the connected Google project has approved billing.
- [ ] Do not use a TPU for this GPU-oriented Qwen/Ollama workflow.
- [ ] Run `!nvidia-smi` in the first Colab cell and save the output.
- [x] Record Python and dependency versions: Python 3.13.16; NVIDIA driver 580.82.07; CUDA 13.0.
- [x] Record the Qwen model: `Qwen/Qwen3-1.7B`.
- [x] Record the model license: Apache-2.0, as listed on the Qwen model card.
- [x] Load the model successfully on the L4 using PyTorch `2.14.1+cu130` and Transformers `4.57.1`.
- [x] Run a synthetic smoke test: 7.268-second latency, 4.54 tokens/second, 3.22 GiB peak GPU memory, and 33 generated tokens.
- [ ] Test whether Qwen3-1.7B is practical across the full Compass benchmark.
- [ ] Assess whether a 4B model is feasible.
- [ ] Record expected inference speed and limitations.
- [ ] Write the recommendation and reasoning in `model/hardware_decision.md`.
- [ ] Include the commands or notebook steps needed to reproduce the decision.

Use synthetic Compass fixtures only in Colab. Do not upload real financial statements or user data.

### Why these choices

- **Colab:** Fast experiments without making cloud compute part of the product.
- **L4:** Enough for initial Qwen testing at lower cost than an A100.
- **High-RAM:** Reduces memory pressure when loading models and data.
- **A100:** Use only if fine-tuning needs more memory and billing is approved.
- **Latest runtime:** Easiest start; record the exact version for reproducibility.
- **No TPU:** The planned Qwen/Ollama tools are GPU-oriented.
- **Local runtime:** Keeps user financial data on-device.
- **Synthetic data only:** Prevents private data from leaving the user’s device.

### Current Colab evidence

```json
{
  "model_id": "Qwen/Qwen3-1.7B",
  "license": "Apache-2.0",
  "gpu": "NVIDIA L4",
  "gpu_memory_gib": 22.03,
  "python": "3.13.16",
  "torch": "2.14.1+cu130",
  "transformers": "4.57.1",
  "note": "Synthetic smoke prompt only; this model did not calculate a financial amount."
}
```

The model loaded successfully on the L4. The smoke test produced a refusal rather than a Compass tool call, so runtime feasibility is confirmed but Compass-specific behavior still needs benchmark testing. Transformers also warned that `temperature`, `top_p`, and `top_k` were ignored; this did not prevent generation.

Smoke-test result:

```text
Latency: 7.268 seconds
Generated tokens: 33
Tokens/second: 4.54
Peak GPU memory: 3.22 GiB
Result: model ran successfully but refused the synthetic financial question
```

## 3. Create the synthetic conversation benchmark

- [x] Create at least 150 fictional conversation examples: 160 created.
- [x] Include spending, merchant, monthly comparison, and follow-up questions.
- [x] Include ambiguous and unsupported questions.
- [x] Include gentle, direct, and playful tone examples.
- [x] Include cases where Compass must ask for clarification or admit missing data.
- [x] Label each example with persona and scenario.
- [x] Label expected intent and approved tool.
- [x] Label whether evidence is required.
- [x] Split the examples into training and held-out test sets: 80 train / 80 test.
- [x] Verify that no identical examples or scenarios leak between the splits.
- [x] Keep all examples synthetic; do not use real bank statements or user data.

Generated benchmark files:

- `model/benchmark_train.jsonl`
- `model/benchmark_test.jsonl`
- `model/benchmark_report.json`
- `model/build_benchmark.py`

Validation report: 160 total examples, 0 duplicate questions, 0 scenario leakage, and all examples marked synthetic. The held-out set includes both supported tool scenarios and unsupported/clarification scenarios so baseline tool selection and safe abstention are both measured.

Example record:

```json
{
  "question": "How much did I spend on restaurants in May?",
  "expected_intent": "category_total",
  "expected_tool": "category_summary",
  "expected_tone": "gentle",
  "requires_evidence": true,
  "persona": "college_student",
  "scenario": "high_delivery_spending"
}
```

## 4. Establish the baseline model performance

- [x] Run the original, untrained model against the held-out benchmark: 80 cases.
- [x] Record the model response for every test case.
- [x] Record whether the tool choice was correct.
- [x] Record whether tool arguments were valid.
- [x] Check for invented financial numbers: 0 possible numeric inventions.
- [x] Record response latency: 0.954 seconds mean.
- [x] Record whether the model correctly refused or requested clarification.
- [x] Save the results as JSONL in `model/baseline_results (2).jsonl`.
- [x] Create a reproducible notebook: `model/baseline_evaluation_qwen3_1_7b.ipynb`.

Baseline report (`model/baseline_report (2).json`):

- Tool-match rate: **50%**
- Valid-tool rate: **100%**
- Valid-argument rate: **7.5%**
- Appropriate-clarification rate: **25%**
- Possible numeric inventions: **0**
- Mean latency: **0.954 seconds**

Interpretation: the base model can select some approved tools, but it frequently produces invalid arguments and routes unsupported merchant/comparison questions to tools. The runtime must validate and reject these outputs before execution; the model is not safe to dispatch directly.

## 5. Verify safe tool use

- [ ] Keep the model limited to approved tools.
- [ ] Validate every tool name and argument against a schema.
- [ ] Do not let the model calculate financial totals.
- [ ] Do not let the model execute arbitrary code or access the network.
- [ ] Reject malformed JSON or unknown tools.
- [ ] Reject model output that changes the user’s filters or intent unexpectedly.
- [ ] Fall back to deterministic parsing when the model fails validation.
- [ ] Show a clear error or clarification request when safe fallback is not possible.
- [ ] Confirm that exact numbers come from deterministic Compass functions.

Baseline evidence makes this the next priority: the untrained model selected the correct tool only 50% of the time and produced valid arguments only 7.5% of the time. Do not dispatch its raw output.

Safety test coverage added in `tests/python/test_phase3.py` covers approved calls, unknown/missing/extra arguments, invalid months/categories/limits, malformed JSON, changed filters, unsupported merchant/comparison questions, timeouts, local failures, and the guarantee that routing itself never executes a financial tool. Phase 3 tests pass: **70 passed**. Full Python suite: **275 passed**.

The intended flow is:

```text
User question
    -> Model suggests an approved tool
    -> Schema validates the tool and arguments
    -> Deterministic Compass function calculates the answer
    -> Model explains the verified result
```

## 6. Build the first chat experience

- [ ] Add a text box for the user’s question.
- [ ] Add a loading state.
- [ ] Display the assistant response.
- [ ] Display tool activity, such as “Checking your May transactions…”.
- [ ] Display an error state when the model or local runtime fails.
- [ ] Add placeholders for evidence links or source transactions.
- [ ] Use the existing synthetic fixtures for the demo.
- [ ] Verify that a user can submit one question and see the complete flow.

The Gate 1 chat does not need to be visually complete. It needs to demonstrate a safe, understandable request-to-response flow.

## 7. Resolve the planning mismatch

- [ ] Confirm with the team whether Dev 3’s fourth Gate 1 task is the wrapped-story specification or the constrained tool-call parser.
- [ ] **Next recommended implementation:** prioritize the constrained tool-call parser because the baseline model currently produces unsafe/invalid tool outputs.
- [ ] If the parser is assigned, document its schema, allowlist, validation, retry limit, and safe-abstention behavior.
- [ ] If the wrapped-story specification is assigned, document the seven-card journey, chart encodings, empty states, and interaction choreography.

### D3-04 remaining work

If D3-04 is the **constrained tool-call parser**:

- [x] Document the parser schema and approved-tool allowlist in `model/tool_call_parser.md`.
- [x] Document the retry policy: no retry by default; use immediate deterministic fallback.
- [x] Document safe-abstention behavior for malformed, unsupported, or unsafe model output.
- [ ] Attach the parser test output and baseline evidence to the ticket.
- [ ] Commit and push the latest parser tests and baseline files.
- [ ] Obtain cross-owner review and record the acceptance result.

If D3-04 is the **Wrapped story specification** instead:

- [ ] Define the seven-card journey.
- [ ] Define chart encodings and interaction choreography.
- [ ] Define loading, empty, error, and incomplete-data states.
- [ ] Tie every card and displayed metric to a verified source metric.
- [ ] Obtain storyboard approval and record cross-owner review.

## 8. Collect completion evidence

- [ ] Save the hardware/model decision.
- [ ] Save the benchmark dataset and leakage-check result.
- [ ] Save the baseline JSONL output.
- [ ] Capture a screenshot of the first chat flow.
- [ ] Run the Python tests:

  ```bash
  python -m pytest -q
  ```

- [ ] Run the JavaScript tests:

  ```bash
  npm test
  ```

- [ ] Link the PR, test output, screenshots, and JSON artifacts.
- [ ] Request cross-owner review.
- [ ] Record reviewer feedback and whether each acceptance criterion passed.

## Gate 1 completion check

- [ ] A reproducible model/hardware decision exists.
- [ ] The benchmark contains at least 150 held-out synthetic cases.
- [ ] No train/test leakage was found.
- [ ] Baseline model results are saved and reproducible.
- [ ] Unsafe model outputs cannot execute tools.
- [ ] A user can submit a question and see response, loading, error, tool, and evidence states.
- [ ] Tests pass and evidence is attached to the PR.
