# Gate 1 Hardware and Model Decision

## Decision

Use **Qwen3-1.7B** for initial Compass experiments and baseline evaluation. Run development experiments on an **NVIDIA L4** in Google Colab. Keep the customer-facing runtime local so financial data remains on-device.

## Observed environment

- GPU: NVIDIA L4
- GPU memory: 23,034 MiB
- NVIDIA driver: 580.82.07
- CUDA: 13.0
- Python: 3.13.16
- GPU processes at measurement time: none

## Rationale

- The L4 has enough memory for initial Qwen3-1.7B inference and small experiments.
- Qwen3-1.7B is the starting point because it is more likely to run locally on consumer hardware than a 4B model.
- An A100 is an optional escalation for fine-tuning if the L4 is insufficient and Google Cloud billing is approved.
- Colab is development infrastructure only; it is not the product runtime.
- Only synthetic Compass data may be used in Colab. Real financial statements must remain local.

## Remaining validation

- [ ] Confirm the exact Qwen3-1.7B revision and license.
- [ ] Install the pinned experiment dependencies.
- [ ] Measure model load time, inference latency, memory use, and invalid tool calls.
- [ ] Assess whether Qwen3-4B is feasible, without changing the initial 1.7B recommendation.
- [ ] Record the exact Colab runtime version for reproducibility.
