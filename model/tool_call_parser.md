# Compass Tool-Call Parser

## Purpose

The model may suggest an approved tool, but it never executes tools or calculates money. Compass validates the model output and falls back to deterministic parsing when validation fails.

## Approved tools

Only these tools are allowed:

- `get_income`
- `get_expenses`
- `get_category_spending`
- `get_largest_expenses`
- `get_surplus`

## Argument schema

The validated model response must be an object with exactly these fields:

```json
{
  "tool": "get_income",
  "month": "2026-05",
  "category": null,
  "limit": 5
}
```

Validation rules:

- `tool` must be one of the five approved tools.
- `month` must use `YYYY-MM` format with a month from `01` through `12`.
- `category` must be a non-empty string or `null`.
- `limit` must be an integer from `1` through `20`.
- No extra fields are allowed.
- The model response must match the independently deterministic interpretation of the user’s question exactly.
- Category filters are only valid for `get_category_spending`.
- The model cannot change the month, category, limit, or intent selected by deterministic parsing.

## Retry policy

Compass does not retry invalid model tool calls by default. It immediately uses deterministic fallback parsing.

This is the chosen policy because deterministic parsing already identifies the user’s supported request. Retrying adds latency and could produce another unsafe or inconsistent response without improving correctness.

## Safe fallback behavior

The flow is:

```text
User question
  -> Deterministically parse and preserve the expected request
  -> Optionally ask the local model for routing advice
  -> Validate the complete model response
  -> Accept only an exact validated match
  -> Otherwise use the deterministic request
  -> Execute only the approved deterministic tool
```

If the local model is disabled, unavailable, too slow, remote, or fails validation, Compass returns the deterministic request with a fallback status. Exact financial calculations still come only from Compass’s deterministic tools.

## Invalid and unsafe output

The following must never execute a tool:

- Malformed JSON
- Unknown tools
- Missing required fields
- Extra fields
- Invalid dates, categories, or limits
- Changed filters or intent
- Incomplete model responses
- Remote/cloud model metadata
- Local connection failures or timeouts

For a supported question, Compass falls back to its deterministic request. For an unsupported or ambiguous question, deterministic parsing raises a clarification error instead of fabricating an answer.

## Evidence

The safety behavior is covered by `tests/python/test_phase3.py`. The current verification result is:

```text
Phase 3 tests: 70 passed
Full Python suite: 275 passed
```
