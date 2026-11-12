# From the existing prototypes to Compass

## What we are building

One local application: a React/TypeScript interface calls a local FastAPI backend, which uses Python financial functions and SQLite. A fine-tuned local model selects approved tools and generates grounded conversation. Product requirements live in [PRODUCT_SPEC.md](../PRODUCT_SPEC.md#g2-proposed-technical-stack).

The Streamlit app and static browser demo are useful reference implementations. They are not two parallel MVP deliverables. Keep their existing checks working while the new application is introduced; do not delete them as part of documentation cleanup.

## Existing code to read and reuse

All paths below are relative to the project directory containing `app.py`.

| Work area | Existing files | How to use them |
| --- | --- | --- |
| Transaction rules | `compass/contracts.py` | Preserve source records, validation, and exact-cent conventions. |
| Import and review | `compass/importer.py`, `mapping.py`, `classification.py`, `db.py` within `compass/` | Extend existing parsing, persistence, and correction behavior; verify gaps against the spec. |
| Totals and evidence | `compass/analytics.py`, `compass/questions.py` | Reuse financial calculations and source references behind API handlers. |
| Conditional scenarios | `compass/scenarios.py` | Reuse deterministic math; label outputs as conditional. |
| Current model integration | `compass/ollama.py` | Inspect the existing router; it is not the fine-tuned conversation implementation. |
| Current Python interface | `app.py` | Read for working flows and service calls; move reusable logic out of UI handlers when needed. |
| Browser reference | `docs/` | Reference interactions and styling. Do not silently adopt its separate JS engine as a second financial authority. |
| Expected results | `fixtures/`, `tests/python/`, `tests/engine.test.js` | Check existing behavior and add targeted tests for new requirements. Historical test names do not indicate new ticket completion. |

## Proposed new code locations

These are planning conventions, not claims that scaffolding exists. Confirm exact files in the rewritten tickets before implementation.

| Proposed directory | Responsibility |
| --- | --- |
| `frontend/` | React/TypeScript app, feature components, API client, frontend tests |
| `api/` | FastAPI entry point, request/response schemas, routes calling `compass/` |
| `model/` | Synthetic dialogue preparation, training configuration, export instructions |
| `evaluation/` | Held-out model evaluation, reproducible comparisons, metric generation |

Continue using `compass/` for reusable Python application logic and `tests/python/` for Python regressions. Checkpoints and large model weights need a documented artifact location, not casual commits into source control.

## Build order and handoffs

| Order | Concrete deliverable | Required handoff / completion check |
| --- | --- | --- |
| 1. Establish the baseline | Run the current app and tests with fictional fixtures; list existing behavior and missing requirements. | Record commands and failures. Do not recreate functionality merely because an old ticket says “create.” |
| 2. Agree on the first API contract | Specify import/review, summary, evidence, and conversation payloads, including cents, dates, IDs, coverage, and errors. | Commit small request/response examples. Frontend and backend developers can work against the same fixtures. |
| 3. Add the local API and frontend shell | Create the proposed scaffolds; expose one existing Python summary through FastAPI and display it in React. | A documented command starts each service; displayed totals match the fixture. Name the integration owner in the ticket. |
| 4. Complete the first data journey | Upload → review/correct → recomputed summary → evidence breakdown. | Test the actual API and React app together. A fixture-only screen is an intermediate step, not completion. |
| 5. Integrate model conversation | Connect validated model tool requests to deterministic tools and return replies with evidence. | Test malformed calls, unavailable data, and unsupported claims. Baseline evaluation and synthetic training preparation can proceed in parallel after contracts are agreed. |
| 6. Build the story journey | Guess → reveal → Wrapped/awards → Confessional → What If? using the same financial tools. | Each feature owns its UI, behavior, tests, and explicit handoff; avoid duplicate screen ownership. |
| 7. Verify delivery | Export the tuned model, evaluate it, package the local app, and test offline use and deletion. | Reproduce the integrated experience and measured results on the target machines before freeze. |

This is dependency order, not a replacement calendar. Thursday/Saturday dates remain in the [engineering plan](COMPASS_ENGINEERING_PLAN.md). Packaging remains a decision to record; the product spec allows Tauri or a packaged local web app. Do not silently expand this into a separate mobile or hosted product.

## How revised tickets should use this guide

Every ticket must say whether it **reuses**, **extends**, or **creates** code. Give exact file paths, a small example, ordered steps, a named prerequisite, and a specific completion check. Label proposed files as new. A teammate should need only the ticket and its listed files, not the entire product specification.

For each developer, publish one weekly table with separate Thursday and Saturday deliverables. Assign feature implementation, review, integration, and report work explicitly. Balance total estimated effort and uncertainty rather than preserving 24 tickets per person. All four roles remain unassigned until that allocation is revised; having Codex is not a fifth responsibility.

## Documentation change record — November 11, 2026

- Kept the specified React/FastAPI/local-SLM target and existing prototype code unchanged.
- Removed the duplicated product proposal from the README; `PRODUCT_SPEC.md` is the product authority.
- Corrected links in navigation documents; left the product specification unchanged at the user’s request.
- Added the transition sequence and proposed code locations above.
- Did not reassign, close, regenerate, or publish the existing 96 tickets. Their workload and ownership revision is still pending.
