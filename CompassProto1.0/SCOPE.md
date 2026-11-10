# Compass Alpha 0.2 — Interactive audit scope and build contract

**Updated:** 2026-11-10. **State:** planned, building on completed Alpha 0.1. **Delivery window:** four relative weeks, two two-week sprints, four developers. [Weekly ownership and work packages](../DEVELOPMENT_PLAN.md) are the active delivery backlog. [Brand identity](../BRAND_IDENTITY.md) governs the new experience. The [old Alpha 0.1 scope](SCOPE_ALPHA_0_1.md) and phase reports preserve historical acceptance evidence.

“Audit” is the product name for a guided spending review. It is not a professional audit, bank-balance reconciliation, diagnosis, or certification of financial health.

## 1. Product outcome

A student or young adult can import a supported CSV, check its interpretation, guess a category total, reveal recorded spending, inspect every contributing row, supply context or skip, and voluntarily explore a small adjustment.

The required Alpha experience is **one complete guess → reveal → optional reaction → guided reflection → evidence/What If? loop**, presented as a short Money Wrapped. Financial tools remain directly accessible without playing. The local language model is optional at every stage.

## 2. Starting point: reuse completed work

The repo already implements CSV mapping and atomic import, source preservation, duplicate/overlap handling, SQLite persistence, effective classifications, six monthly summaries, five evidence-bearing tools, exact rent scenarios, confirmed deletion and a bounded local-only Ollama intent adapter. The recorded Alpha 0.1 baseline is 271 Python tests, 17 JavaScript tests, and browser/privacy release evidence in [PHASE5.md](PHASE5.md). These are previous release results, not proof of new features.

Extend Python/Streamlit and the existing SQLite database. Do not restart the financial foundation, replace the UI stack, duplicate arithmetic in components, or make parity with the separate Pages demo a release dependency. Database changes require forward migrations that preserve existing source rows and corrections.

Historical `ProtoToDo.md` phases 0–5 are completed checkpoints. References to “Phase 1” in the new direction mean the next Sprint 1/Weeks 1–2 feature work; the old Phase 1 importer is already done.

## 3. Scope tiers and cheap extensions

| Capability | Existing leverage | Alpha decision |
| --- | --- | --- |
| New identity and five coherent screen states | Existing app shell and evidence UI | Required in Week 1: tokens, lowercase wordmark, voice, readable responsive components |
| One category guessing game | `analytics.summarize_month` and category totals | Required in Week 1; exact amount/difference and receipts |
| Shared Insight objects | Existing transaction IDs, exclusions, month/category calculations | Required; one reusable contract for all new modes |
| Merchant grouping and detail | Preserved descriptions and source IDs | Required narrow rules plus reviewable aliases; unknown names remain raw; no fuzzy auto-merges |
| Recorded month comparisons | Existing month selectors and exact totals | Required narrow category comparison; expose coverage and reject incomparable filters |
| Money Wrapped | Reuse Insight objects and evidence renderer | Required, up to three eligible cards; fewer cards or a helpful empty state are valid |
| Guided Confessional | Existing question UI and session state | Required one bounded reflection; context optional and session-only by default |
| Reactions/tone controls | Templates and optional current router | Required neutral/off and reviewed Gentle/Direct; Roast gated by explicit opt-in and eligible subjects |
| Teach Me Why | Existing refund/transfer/surplus/scenario definitions | Required short reviewed explainers for those concepts; no general tutoring agent |
| Local model integration | Existing schema/timeout/fallback module | Timebox one real installed-model smoke test in Week 2; deterministic flow is the release path |
| Neutral Money Awards | Merchant/category facts already computed | Week 3 small extension: at most two templates; cut before the core loop |
| Saved scenario inputs | Existing pure calculator | Week 3 stretch, maximum eight combined delivery hours (four engine, four storage); store inputs and revision, recompute explicitly |
| One text-PDF layout | No current parser; CSV/source contract available | Week 2 gated stretch, maximum eight delivery hours total; no second layout or OCR |

Payments, exports, bank sync, automatic advice, encrypted multi-user hosting, goals with notifications, model training, predictive cash flow, learned ranking, automatic merchant entity resolution, extensive themes and persistent chat memory are deferred. The former Sprint 1 saved-goals proposal is deferred; optional saved scenario inputs are the bounded substitute. Former Sprint 2 plan monitoring and forecasting baselines remain later work. Preserve these deferrals rather than implying they shipped.

## 4. First supported journey

1. Open the local app with a clear fictional-demo option and the new identity.
2. Import checking and savings CSVs using existing mapping/validation; review unknowns.
3. Choose a month; see observed date range, imported accounts, unresolved value and incomplete-coverage warning.
4. Choose an eligible category, enter a nonnegative exact-cent guess, and submit. No answer amount appears inside the unrevealed card or its accessible text.
5. Reveal recorded net spending and the signed/absolute guess difference. Existing summary tools may still be opened independently; this is a voluntary game, not concealment of user data.
6. Open receipts: filters, expenses/refunds, excluded unknowns/transfers, account labels, immutable source IDs/rows and calculation agree with the card.
7. Optionally enable an eligible reaction. Add context, disagree, choose a suggested reflection or skip.
8. Explore an existing What If? input with confirmation. Nothing inferred from a comment silently changes a financial assumption.
9. Correct a source classification or import more activity; affected insights/reveals invalidate and recompute from current records.
10. Restart to retain financial records and explicitly saved preferences. Clear local data to remove new persisted preferences/aliases and any optional saved inputs, as well as existing financial records.

## 5. Financial and insight contract

### Immutable evidence

Keep the existing signed-cents convention, ISO dates, account/source identity, raw source JSON, original row ordinals, import hashes and separate predicted/override fields. Types remain `income|expense|refund|transfer|unknown`; category is separate. Existing ground truth and expected JSON remain test/audit-only.

New merchant aliases are explicit derived metadata, never replacements for original descriptions. Default grouping uses trimmed/case-normalized description text, without stripping meaningful digits or fuzzy merging. A reviewed alias maps an exact normalized description to a display merchant within a source/account scope. Alias changes have a revision and clear evidence. Merchant frequency counts included expense rows; label them purchases or transactions, not visits without separate visit evidence. Two legitimate identical-looking transactions still count twice.

### Shared Insight object

| Field | Meaning |
| --- | --- |
| `insight_id`, `schema_version` | Stable definition identity and version |
| `insight_type`, `metric_definition` | Category net spending, merchant purchase total/count, or recorded comparison; explicit calculation semantics |
| `period_start`, `period_end`, `filters` | Inclusive calendar interval; category/merchant/account scope |
| `amount_cents`, `purchase_count` | Exact financial result and separately defined expense-row count, where applicable |
| `included_transaction_ids` | Every contributing internal ID; never a truncated example presented as full evidence |
| `excluded_transaction_ids`, `exclusion_reasons` | Relevant unknowns/transfers and any scope exclusions |
| `refund_cents` | Explicit included refund offset for net-spending metrics |
| `comparison` | Optional prior period, amount, contributing IDs, dollar delta and denominator status |
| `coverage`, `warnings` | Observed dates, unresolved amounts, imported-account scope and unverified completeness |
| `data_revision` | Fingerprint/revision covering contributing financial labels, imports and aliases; invalidates stale displays |
| `eligibility`, `eligibility_reason` | Whether guessing, comparison, award and playful reaction are permitted |

The engine validates the object before rendering. Narrative text receives an approved fact payload, not unrestricted raw statements. For Alpha, money/count/date slots are rendered by code into reviewed templates. If model-generated wording is attempted, reject unknown numeric claims, entities or changed filters and use the template. The model cannot create an Insight, change its evidence or calculate totals. User context stays outside the financial fact object.

### Arithmetic definitions

```text
net_expenses = sum(expense outflow magnitudes) − sum(included refund inflows)
verified_surplus = classified_income − net_expenses
guess_delta = guess_cents − actual_recorded_cents
absolute_guess_error = abs(guess_delta)
recorded_change = current_net_spending − prior_net_spending
replace_rent_delta = new_rent − confirmed_existing_rent
additional_rent_delta = new_rent
projected_surplus = baseline_surplus + income_adjustment − added_spending − rent_delta
six_month_static_change = 6 × projected_surplus
```

Zero guess delta means equal; negative means underestimated; positive means overestimated. A percentage guess error is defined only for positive actual spending. A percentage month change is defined only with a positive prior denominator and comparable filters. Show the dollar change and a denominator explanation otherwise; never render infinity or a fabricated percentage.

Category guessing uses **net** expenses including category refunds and excluding transfers/unknowns. Merchant purchase-count/total cards use expense rows only and must say so; do not reuse that total as net spending. Merchant refund netting requires an explicit reviewed merchant match; unresolved matches remain visible. Do not infer a visit count from aggregated statement descriptions.

Comparisons use the same metric, effective category definition and account scope in each period. Missing prior data produces an unavailable state, not zero. Recorded-month comparisons retain both coverage warnings and never assert complete bank reconciliation or causal behavioral change. Nonpositive net-spending categories use a neutral refund/no-spend card rather than a guessing/roast target.

Any ratio or average used for a display is calculated outside the model with exact decimal/rational arithmetic. Proposed display rounding is two monetary decimals with an explicit policy; original amounts are never rounded or rewritten. Prefer existing exact What If? inputs over a new purchase-reduction simulator. A later simulator must label average-based amounts conditional and define rounding before implementation.

## 6. Story selection and conversation

Use deterministic, inspectable selection: selected category total, a supported repeated-merchant fact, and a comparable prior-period fact when available. Stable ties use a documented key; no invented confidence score or arbitrary weighted “financial health” ranking. Never force three cards when the data supports only one.

The Confessional has a bounded question, optional context, acknowledgement and optional next action. Tone off is the default. Gentle/Direct are selected by the user; Roast requires separate opt-in. Only reviewed discretionary categories/templates are eligible. Sensitive/custom/unknown categories receive neutral language. Do not infer motives or treat user context as a transaction correction. Context is session-only in the required scope; persistent personalization requires explicit separate design and deletion coverage.

At most two awards describe measured patterns without moral judgment, such as a clearly defined most-frequent eligible merchant. Suppress award/roast generation when eligibility, coverage or count evidence is insufficient. No joke in financial errors, X-Ray, hardship, healthcare, housing or debt-distress content. The ordinary tools and skip/off controls remain accessible.

## 7. Local state and privacy

Persist only necessary financial records, explicit alias edits and user-selected preferences. New tables need a migration, restart test and atomic inclusion in **Clear all local data**. Default tone stays off until set; do not treat opening a story as consent to Roast. Optional scenario persistence stores inputs plus baseline revision, not an authoritative cached financial answer.

No analytics, financial uploads, remote font/CDN dependency, cloud inference, or external account access. Usability research uses fictional data and separately consented, minimal notes. No raw statements/context in logs or published artifacts. Installing dependencies/models is a separate network action. The existing local-only/unencrypted/unauthenticated and logical-deletion limitations still apply.

## 8. Stretch admission and cut rules

The Week 2 PDF spike starts only after the Week 1 loop and core regression checks are green and Dev 1 has capacity. It supports one declared text layout with synthetic fixtures, row/page provenance and explicit rejection of scanned/unsupported documents. If it does not meet the same import contract within eight combined delivery hours, leave CSV as the supported input and record the spike; do not expose a partial parser. No second format or OCR enters this plan.

The Week 3 saved-input spike starts only after correction invalidation, preference deletion and the complete core flow pass. Stop after eight combined delivery hours if schema/deletion/revision handling is not ready. Optional awards and animations are cut before evidence or core integration. Unfinished model wording always falls back to reviewed templates.

## 9. Alpha 0.2 release gate

| Required evidence | Observable pass |
| --- | --- |
| Brand and journey | Five coherent screen states implemented at least for the core path; keyboard, contrast states, reduced-motion and 390px/desktop checks recorded |
| Exact reveal | May Groceries recorded net spending is **$299.78**; a **$250.00** guess yields **−$49.78** signed delta and **$49.78** absolute error, with source rows |
| Existing regressions | May income $3,700.00/net expenses $2,952.94/surplus $747.06; rent replace $522.06/additional −$752.94; June $80 unknown remains visible |
| Grounded cards | Amounts/counts/periods reconstruct from every included ID; refunds, missing prior month, zero denominator and duplicate-looking transactions have tests |
| Freshness | Import/edit/alias changes invalidate affected cards; stale reveals do not remain definitive |
| Choice and tone | Off default; separate Roast opt-in; sensitive topics neutral; skip/disagree/context-empty paths complete |
| Privacy/deletion | No external processing in default flow; all new persisted state survives restart and is removed by confirmed deletion |
| Robust fallback | Complete journey works with no model installed or with Ollama stopped/invalid/timeout responses |
| Release evidence | Updated browser smoke, clean-machine instructions, formative findings, known limits and a new fictional audit demo |

No new checkbox becomes complete from planning alone. Weekly acceptance and evidence ownership are defined in [DEVELOPMENT_PLAN.md](../DEVELOPMENT_PLAN.md).
