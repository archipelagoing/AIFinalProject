# Phase 3 — Snapshot and deterministic Ask Compass

Implemented on 2026-11-10 in the root Python/Streamlit app. All six P0 checklist items and the optional local router are covered by automated acceptance tests. Run `streamlit run app.py` after installing `requirements.txt`; load both fictional statements and open **Ask Compass**. The separate JavaScript GitHub Pages prototype remains available; GitHub Pages does not run this Python server.

## Snapshot and data quality

The month selector, classified income, expenses net of refunds, verified surplus, category table, and source rows use the same integer-cent analytics as question answers. All six fixture months reconcile with the unchanged supplied expected JSON in tests. Evaluation files are never read by production code.

Each snapshot and answer shows reviewed/unreviewed classification counts, unknown absolute value and separate inflow/outflow values, observed activity dates, and incomplete-coverage warnings. A reviewed row means a saved category/type override, including a deliberately confirmed unchanged classification. Restoring rule classification clears that review indication. This is a classification-review count, not an audit or bank-balance reconciliation. Unknown inflows and outflows cannot cancel out of the quality notice. The June ATM remains an excluded $80 outflow until corrected.

## Five tools and supported questions

`compass/questions.py` provides `get_income`, `get_expenses`, `get_category_spending`, `get_largest_expenses`, and `get_surplus`. Each returns exact cents, the inclusive calendar query period, observed coverage, included transactions, exclusions, and a calculation description. Tools read effective labels; category refunds offset spending. Largest expenses ranks expense outflows only, defaults to five rows, and accepts 1–20. Ties resolve by amount, date, then stable local record ID. Its answer amount is the sum of the listed rows, rather than total monthly spending.

Supported examples:

- `What was my income in May 2026?`
- `What were my expenses in May 2026?`
- `How much did I spend on Groceries in April 2026?`
- `Show my top 3 expenses in May 2026`
- `What was my surplus in June 2026?`
- `income for 2026-05`
- `largest expenses`

Omitting the month follows the selected snapshot month. An explicit question month stays fixed when the snapshot selector changes. A month name without a year is accepted only if exactly one imported year contains that month. Category names must match an effective category in that month's table, ignoring case; ambiguous case collisions require clarification. Missing months, unknown categories, multiple questions/months, account filters, date ranges, comparisons, balances, and forecasts receive clarification/examples without an answer figure. This is a bounded grammar, not unrestricted natural-language understanding.

Answers show the tool/month/all-account filters, category or ranking count, calendar period versus observed activity coverage, calculation, and evidence tables. Included rows expose source IDs, row ordinals, filenames, import hashes, and stable local IDs. Month-wide excluded transfers and unknowns appear separately; they are not confused with other categories or expense rows outside a ranking. Original values remain inspectable in the source-row viewer.

The session stores the submitted question, not a financial answer. Every rerun reads SQLite again and recalculates using current classifications. Saving/restoring classifications, importing more activity, changing an implicit month, and reopening the app cannot reuse stale totals. Explicit-month questions retain their own filters. Imports retain the existing duplicate protections.

## Optional local Ollama router

The default app does not contact Ollama. To opt in, first disable cloud inference in the **Ollama server process** and restart it. For example, start a server with `OLLAMA_NO_CLOUD=1 ollama serve` on macOS/Linux, or set `$env:OLLAMA_NO_CLOUD="1"` then run `ollama serve` in PowerShell. A separately running desktop/service process must receive its own configuration; setting an environment variable only for Streamlit does not configure that server. See the official [Ollama FAQ](https://docs.ollama.com/faq) and [chat API](https://docs.ollama.com/api/chat).

In **Optional local Ollama routing**, enable routing, enter an already installed local model name, and confirm cloud features are disabled. Compass does not download models. This prototype requires local GGUF metadata from `/api/show`, rejects remote-model metadata and cloud model names, and uses only `127.0.0.1:11434` with no environment proxy or redirect following.

The model receives only the bounded question and independently validated intent, never the transaction dataset or calculated totals. `/api/chat` uses a five-tool allowlist, JSON Schema structured output, `stream=false`, bounded generation/context, a shared four-second request deadline, and a 64 KiB response ceiling. `jsonschema` validates the returned object, rejects extra keys and invalid values, and domain checks require exactly the independently parsed tool/month/category/count. No model text becomes SQL, executable code, or an answer amount. Model routing is advisory and intentionally cannot broaden supported syntax or override deterministic filters. All arithmetic stays in Python tools.

Disabled/stopped services, missing models, timeouts, invalid/incomplete JSON, schema failures, unexpected metadata, and changed filters fall back to deterministic routing. Unsupported or ambiguous input is clarified before contacting the model. Cold model starts may exceed the deadline and fall back; the app remains usable.

## Verification and limits

Verification passed: **215 Python tests**, **17 JavaScript tests**, independent fixture audit, and dependency check. Run `python -m pytest -q`, `python scripts/audit_fixtures.py`, `python -m pip check`, and `npm test` from the root with the virtual environment active. Phase 3 tests cover all six fixture months and five tools; exact source-row arithmetic; refund offsets; fixed questions; ambiguous years, unsupported filters and missing data; counts and boundaries; unknown value without net cancellation; correction evidence; local schema/allowlist/filter safeguards; stopped-service fallback; loopback transport limits and cleanup; and Streamlit answers after edits, new imports, duplicate imports, month changes, and fresh sessions.

Ollama protocol and failure tests use simulated responses/connections. A real installed-model inference smoke test and native-browser walkthrough have not been performed for this phase. Streamlit AppTest verifies rendered controls and real handlers. Phase 4 What If? integration, account-balance reconciliation, PDF/OCR, arbitrary date/account filters, and broader natural-language interpretation remain outside this phase.
