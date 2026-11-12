# Compass developer guides

Generated from the enriched 96-ticket backlog. Read the guide matching your assigned developer role. Each person owns a visible product slice, tests, integration evidence, and cross-domain risk work—not a narrow support-only function.

## Main contribution by developer

| Developer | Main contribution | Must also contribute |
| --- | --- | --- |
| Dev 1 | Import-to-insight: statement ingestion, provenance, correction/review, coverage, and evidence integrity. | Financial golden cases, model/data provenance review, frontend flows, and integration tests. |
| Dev 2 | Spending-to-decisions: exact financial rules, deterministic tools, X-Ray, insights, scenarios, and numerical audit. | Import/model data checks, UI delivery, reproducibility work, and cross-feature tests. |
| Dev 3 | Model-science-to-interaction: training, grounded conversation, evaluation, uncertainty, and meaningful model-driven interaction. | Import/evidence compatibility, financial claim checks, interaction design, and end-to-end integration. |
| Dev 4 | Runtime-to-reliable-journey: safe tool execution, adapter/runtime integration, consumer-device performance, and complete-flow reliability. | Frontend implementation, accessible interaction states, model/finance benchmark evidence, and release testing. |

## Saturday merge rubric — November 28, 2026

When all feature branches are merged into `main`, evaluate a **fresh checkout of `main`** using only synthetic fixtures. Record the result in the Gate 6 parent issue and attach commands, logs, screenshots, benchmark JSON, and remaining-defect links. This scores closeness to a release candidate; it does not replace individual ticket acceptance.

| Category | Points | What must be demonstrated |
| --- | ---: | --- |
| Financial and data correctness | 30 | Exact-cent golden suite; imports/corrections/refunds/transfers/unknowns reconcile; every shown total has inspectable evidence. |
| Complete user journey | 20 | Import → review/correct → Ask → X-Ray → Wrapped → Confessional → What If? → deletion works from a clean checkout. |
| Grounded model behavior and evaluation | 15 | Tool allowlist/schema blocks invalid calls; no unsupported numeric claim in release suite; base-vs-tuned evidence and local performance results are attached. |
| Privacy, resilience, and safety | 15 | Local-only/offline boundary tested, deletion verified, malformed input handled, no real financial data/telemetry, and no unresolved P0/P1 privacy or safety defect. |
| Accessibility and responsive quality | 10 | Keyboard, reduced motion, contrast, screen-reader alternatives, and supported mobile/desktop layouts pass documented checks. |
| Release evidence and reproducibility | 10 | Clean setup, CI, fixtures, model/config hashes, benchmark commands/results, known limitations, and demo evidence are present. |
| **Total** | **100** | **Score only from attached evidence, never from claimed completion.** |

### Hard gates

- **Not releasable regardless of score:** any P0 defect; fabricated/unsupported financial amount; privacy or deletion failure; broken clean-checkout core journey; or missing evidence for a claimed benchmark.
- **90–100:** release-candidate ready; only documented P2 issues remain.
- **75–89:** conditionally complete; merge is acceptable, but freeze requires an explicit owned repair list and rerun of affected evidence.
- **Below 75:** not ready for freeze; stop stretch/polish work and swarm the lowest-scoring category.

### Required Saturday evidence by developer

- **Dev 1:** import/provenance/privacy result, coverage checks, and source-data fixture evidence.
- **Dev 2:** financial golden-suite result, evidence/X-Ray audit, and scenario/chart verification.
- **Dev 3:** base-vs-tuned comparison, safety/grounding result, latency/RAM measurement, and model/config hash.
- **Dev 4:** full end-to-end recording/log, accessibility/responsive audit, usability/demo evidence, and known-issues list.

## Individual guides

- [Dev 1](Dev_1_README.md)
- [Dev 2](Dev_2_README.md)
- [Dev 3](Dev_3_README.md)
- [Dev 4](Dev_4_README.md)
