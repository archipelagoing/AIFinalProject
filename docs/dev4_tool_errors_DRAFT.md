# Tool error contract — DRAFT hand-off to Dev 4

Ticket: **CMP-1112-D2-04** (tool schemas and evidence IDs, Gate 1) · Owner: Dev 2 · Status: **ready for Dev 4 review**.
Dev 1 confirmed on 11/25 that errors use the guide's JSON format (Q4), and that evidence IDs reuse the existing transaction IDs with `result_id` added on top (Q5).
Tools are plain Python functions (Q3). The app calls `compass/tools.py`: a typed function raises `ToolError`, and the envelope is in `e.envelope`. The model loop calls `tools.handle_tool_call()`, which returns the envelope as a dict instead of raising.

## How this file relates to the repo

| Item | Location in `git_repo` |
|---|---|
| This document | `docs/dev4_tool_errors_DRAFT.md` (new) |
| Where errors are built | `compass/tool_contracts.py`: `error_envelope()`, `validate_call()` |
| Where `evidence_not_found` comes from | `compass/evidence.py`: `resolve_evidence()` |
| Every example below, machine-readable | `tests/python/fixtures/tool_error_cases.json` |
| Test that keeps code and examples in sync | `tests/python/test_tool_error_cases.py` |

If the code changes an error, that test fails until the fixture is updated. The fixture then becomes the new contract, so a change can't reach you silently.

## The one error shape

Each failed tool call returns this object in place of a result:

```json
{
  "error":   "invalid_tool_arguments",
  "tool":    "get_transactions",
  "message": "Arguments for get_transactions failed validation (1 problem).",
  "details": [
    {"loc": ["limit"], "msg": "Input should be a valid integer", "input": 5.0}
  ]
}
```

| Key | Type | Meaning | How the UI should use it |
|---|---|---|---|
| `error` | string | Machine-readable code (see below) | **Branch on this.** |
| `tool` | string | The tool name the model asked for | Show it in debug views |
| `message` | string | One human sentence | Safe to show as-is |
| `details` | list | One entry per problem; `[]` when there's no field detail | Highlight fields |
| `details[].loc` | list | Path to the bad field: `["limit"]`, `["period","start"]`; `[]` = whole input | Use it to find the field |
| `details[].msg` | string | Human text (from Pydantic for argument errors) | Show it; **don't parse it**. The wording may change on a library upgrade |
| `details[].input` | any JSON | What the model actually sent for that field | Show it next to the message |

Tell an error from a result by checking for the `"error"` key. The Python helper for this is `is_error()`.

## Error codes (starting set)

| Code | When | Typical cause | Suggested UI |
|---|---|---|---|
| `unknown_tool` | Tool name isn't one of the 4 | The model made up a tool | "Compass couldn't answer that"; log it for model tuning |
| `invalid_tool_arguments` | Tool exists, but its args break a rule (also covers broken JSON) | Bad or reversed dates, extra field, float or text where an int is needed, value out of range | Same user message; show `details` in the debug or X-Ray panel |
| `evidence_not_found` | `explain_total` got a well-formed `result_id` with no saved evidence | The ID was made up, or it came from an empty result (known draft limitation) | "No receipts found for that number" |

## Rules every tool argument follows

- **Period** `{"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}`: the end date is *not* included, and end must be after start. The period can be at most 366 days.
- **Unknown fields are rejected** at every level, including inside `period`.
- **No type guessing:** `5.0`, `true` and `"5"` are all rejected where an int is required.
- **Limits:** `get_transactions.limit` must be 1–500 (default 100). `top_n` must be 1–50 (default 10). Names must be 1–80 characters.
- **`result_id`** must match `^res_[0-9a-f]{12}$`.

## Sample bad calls

Each row below is one case in the fixture, which holds the full expected envelope.

| Case | Tool | Model sent | `error` | `loc` | `msg` |
|---|---|---|---|---|---|
| unknown_tool | get_balance | `{"account":"checking"}` | unknown_tool | — | — |
| malformed_json | category_summary | `{"period": {"start": "2026-10-01"` | invalid_tool_arguments | `[]` | Invalid JSON: EOF while parsing… |
| missing_period | category_summary | `{}` | invalid_tool_arguments | `["period"]` | Field required |
| reversed_dates | category_summary | start 2026-11-01, end 2026-10-01 | invalid_tool_arguments | `["period"]` | Value error, end must be after start (end is exclusive) |
| empty_period | merchant_summary | start = end = 2026-10-01 | invalid_tool_arguments | `["period"]` | same as above |
| range_too_long | get_transactions | 2025-01-01 → 2026-06-01 | invalid_tool_arguments | `["period"]` | Value error, period is longer than 366 days |
| impossible_date | get_transactions | start 2026-02-30 | invalid_tool_arguments | `["period","start"]` | …day value is outside expected range |
| non_iso_date | get_transactions | start 10/01/2026 | invalid_tool_arguments | `["period","start"]` | …invalid character in year |
| extra_field | category_summary | `"currency": "EUR"` | invalid_tool_arguments | `["currency"]` | Extra inputs are not permitted |
| limit_float | get_transactions | `"limit": 5.0` | invalid_tool_arguments | `["limit"]` | Input should be a valid integer |
| limit_bool | get_transactions | `"limit": true` | invalid_tool_arguments | `["limit"]` | Input should be a valid integer |
| limit_string | get_transactions | `"limit": "5"` | invalid_tool_arguments | `["limit"]` | Input should be a valid integer |
| limit_too_big | get_transactions | `"limit": 501` | invalid_tool_arguments | `["limit"]` | Input should be less than or equal to 500 |
| empty_category | category_summary | `"category": ""` | invalid_tool_arguments | `["category"]` | String should have at least 1 character |
| two_problems | get_transactions | `"limit": 0, "sort": "desc"` | invalid_tool_arguments | `["limit"]`, `["sort"]` | both problems are reported |
| bad_result_id | explain_total | `"result_id": "res_XYZ"` | invalid_tool_arguments | `["result_id"]` | String should match pattern… |
| evidence_not_found | explain_total | `"result_id": "res_000000000000"` | evidence_not_found | `["result_id"]` | no evidence rows for this result_id |

## Settled by Dev 1 (11/25)

- **Error style (Q4):** the guide's coded JSON envelope shown above.
- **IDs (Q5):** evidence IDs are the existing transaction IDs (`T1`…), unchanged. Each result adds `result_id` = `res_` + 12 hex characters.

## Still open

1. **More codes later:** the guide adds data codes (`no_data_for_period`, `partial_period`, `mixed_currency`) in ticket 6, evidence codes in ticket 7, and `unsupported_claim` in Gate 4. Today partial data is a *result* with `coverage.complete = false`, not an error.
2. **Empty results:** a result with zero rows saves no evidence, so `explain_total` on it returns `evidence_not_found`. Should that be a different code, or should an empty-evidence marker be stored?

Please reply with a sign-off or requested changes on the PR comment for CMP-1112-D2-04.
