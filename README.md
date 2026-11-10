# compass.

**Most financial apps show you what you spent. Compass makes you want to find out.**

Good with numbers. Good with people.

Your bank statement has receipts. Compass has commentary.

Compass is evolving from a private financial assistant into an interactive monthly money audit for students and young adults. Guess what you spent, reveal the recorded amount, inspect the receipts, explain the context, and explore a change if you want to.

**Current repo:** the local Alpha 0.1 financial foundation is implemented. **Next build:** Alpha 0.2, the branded interactive audit described below, is planned. Guess the Damage, Money Wrapped, awards, roast controls, and Confessional are not yet implemented. The current app still uses its earlier visual identity.

[Run the app](#run-the-local-python-foundation) · [Alpha scope](CompassProto1.0/SCOPE.md) · [Four-week developer plan](DEVELOPMENT_PLAN.md) · [Brand identity](BRAND_IDENTITY.md) · [Recorded foundation demo](CompassProto1.0/demo/README.md) · [Previous README](ReadmeOld.md)

## A. What is Compass?

Compass is a local-first personal finance app that makes reviewing financial records participatory. Its first audience is students and young adults beginning to manage their money independently.

Imagine a fictional interaction:

> “Before I tell you, what do you think you spent on takeout last month?”
>
> You guess $80. The recorded total is $143 across 11 purchases.
>
> “You and takeout are getting pretty serious.”

You open the transactions, recognize the late-class routine, and decide whether three fewer visits would be realistic. The joke invites attention; the evidence supports the amount; the user supplies the explanation. These example amounts are illustrative, not results from the bundled fixtures.

Two complementary experiences share one engine:

| Experience | Character | Purpose |
| --- | --- | --- |
| Your financial assistant | Calm, precise, trustworthy | Ask, inspect transactions, check calculations, explore What If? |
| Your financial reality show | Playful, surprising, personal | Guess, reveal, react, reflect, and return next month |

The proposed signature experiences are:

| Experience | Alpha 0.2 commitment |
| --- | --- |
| **Guess the Damage** | One category-spending guess, a recorded-total reveal, and exact guess difference |
| **Money Wrapped** | A short monthly sequence of up to three eligible story cards using the same verified insight objects |
| **The Money Awards** | At most two neutral, factual award templates after the core loop works |
| **Reality Check** | Off by default; optional Gentle/Direct copy, with Roast requiring separate opt-in and safe eligible subjects |
| **The Confessional** | One guided reflection with optional context and a voluntary next step; deterministic follow-ups remain available |

Financial X-Ray means the existing source rows, filters, formulas, classifications and exclusions remain available from every new story. What If? reuses the existing calculator. Teach Me Why begins with short reviewed explanations of concepts already used by the app; a general financial tutor is outside this Alpha.

**Target journey:** import → review → choose month → guess → reveal → inspect evidence → add context or skip → optionally explore an adjustment. Users can skip the game and open the ordinary financial tools.

## B. Why is Compass needed?

Access to a bank statement does not automatically make someone want to read it. Reviewing spending can feel tedious, intimidating, or judgmental. A transaction list also cannot explain whether an expense reflected convenience, social plans, an essential need, or a deliberate priority.

Our hypothesis is that curiosity, surprise, and optional humor can encourage useful financial reflection. The app should ask about context before interpreting behavior and make its calculations inspectable throughout.

We will measure engagement, understanding, comfort, and willingness to repeat the import. Improved financial habits and monthly retention are research questions, not demonstrated outcomes.

## C. What already exists?

Compass enters an established product category. Account aggregators, budgeting systems, subscription managers, local finance tools, and general AI assistants already address parts of this problem.

Our competitive research shortlist includes Monarch Money, YNAB, Rocket Money, Actual Budget, and general AI assistants. A dated review of their current workflows is a Week 4 research task; this README does not claim an exclusive feature advantage.

The proposed distinction is a recurring, participatory financial audit supported by a local dataset and inspectable calculations. Financial analysis, AI conversation, and spending recaps themselves are not new inventions.

## D. The gap, experience, and brand

The product loop is **curiosity → reveal → recognition → conversation → voluntary adjustment**. A difference between a guess and recorded spending is an invitation to investigate, not proof of irresponsibility.

### Brand direction

The wordmark is **compass.**, always lowercase with a period. The visual direction is **neo-editorial pop**: confident magazine-like headlines, a paper-and-ink foundation, precise numbers, expressive story cards, and a small compass-needle commentator.

| Token | Color | Role |
| --- | --- | --- |
| Paper | `#F5F1E8` | Everyday canvas |
| Ink | `#17171B` | Body text, evidence and numerals |
| Voltage | `#D9FF43` | Selective interaction and reveal emphasis |
| Iris | `#8755E8` | Recognizable brand accent |
| Pool | `#82DDE5` | Supporting story backgrounds |
| Guava | `#FF806D` | Playful story emphasis |

**Everyday Compass** is calm and readable. **Money Wrapped** uses bolder composition and color. **Financial X-Ray** is orderly and literal, with no jokes inside evidence or error messages. The [brand guide](BRAND_IDENTITY.md) defines permitted text/background pairs, typography, motion, voice and component states. These are implementation targets; the new identity is not yet applied to either frontend.

Humor targets an optional discretionary pattern, never hardship, debt distress, essential spending, healthcare, housing insecurity, or personal identity. No invented merchant visits, inferred motivations, diagnoses, or moral scores. Off, skip, disagree, and “show the receipts” are first-class controls. We will not monetize accuracy, corrections, evidence, or privacy controls.

## E. Business model and go-to-market hypothesis

The initial model is B2C with direct distribution through the website, campus communities, creators and referrals. University or employer sponsorship is a later B2B2C possibility, with no institutional access to individuals' records implied. Institutional licensing and payments are outside the four-week build.

A short guessing/reveal interaction could make the product easier to explain. Repeat use still depends on meaningful new insights and willingness to import another statement. Sharing personal financial data is not required for acquisition; exports, social publishing and referral mechanics are deferred.

## F. Pricing hypotheses

| Proposed offer | Illustrative price | Hypothesis to test |
| --- | ---: | --- |
| Free | $0 | Imports, essential Q&A, X-Ray, corrections, privacy and a limited monthly story establish trust |
| Story Pass | $2.99 once | An expanded themed audit could support a one-time purchase |
| Compass Plus | $4.99/month; possible $44.99/year | Longer history, saved goals and deeper comparisons could support repeat value |

These are unvalidated research concepts, not available offers. No paywall, billing, payment SDK, or locked financial correctness is planned for Alpha 0.2.

Illustrative subscription arithmetic: `10,000 active users × 5% conversion × $4.99 = $2,495/month gross`. This excludes all costs, taxes, refunds and churn and is not a forecast.

## The technology behind Compass

**Deterministic software owns financial facts. A local model may help route or phrase an interaction.**

```text
CSV import + review → SQLite source records and separate corrections
                              ↓
              Exact financial tools + data-quality checks
                              ↓
                Validated Insight objects [planned]
                              ↓
          Guess / Wrapped / awards / reaction / reflection [planned]
                              ↘ source evidence + existing What If?
```

The new modes reuse one Insight contract containing period, metric definition, integer-cent amount, count definition, every contributing transaction ID, exclusions, coverage and data revision. A category card never changes its financial definition to fit a punchline. Corrections and new imports invalidate affected cards and reveals. The [Alpha contract](CompassProto1.0/SCOPE.md) specifies grouping, refunds, comparison eligibility, privacy and arithmetic.

The four-week implementation extends the **Python/Streamlit app**. The existing JavaScript [GitHub Pages prototype](https://archipelagoing.github.io/AIFinalProject/) remains a separate demonstration; it does not run Python or share the local SQLite database. Parallel feature implementation on both frontends is outside the required plan.

### What already works

The completed Alpha 0.1 baseline includes CSV import/mapping, account-scoped duplicate handling, local SQLite persistence, transparent classification and corrections, six-month summaries, five deterministic question tools, source evidence, exact rent scenarios, confirmed local-data deletion, and an optional bounded Ollama intent adapter.

Recorded release evidence is **271 Python tests**, **17 JavaScript tests**, fixture/privacy audits, Chromium desktop/mobile smoke tests, and a [73-second fictional-data demo](CompassProto1.0/demo/README.md). Those results describe the existing baseline, not the unimplemented interactive audit. Real installed-model inference remains unverified. See [Phase 5](CompassProto1.0/PHASE5.md).

## G. Four developers, two sprints, four weeks

The plan builds on that foundation. Brand application and the first guessing loop begin in Week 1.

| Week | Shared goal | Friday acceptance |
| --- | --- | --- |
| 1 | Establish the brand and first complete guessing interaction | Fictional CSV → category guess → exact reveal → source rows works without Ollama |
| 2 | Complete the functional interactive Alpha | Up to three monthly cards, one comparison where eligible, guided reflection, tone controls, and existing Q&A/What If? form one flow |
| 3 | Improve repeat use and test trust | Corrections/imports refresh stories; eligible awards and privacy controls work; formative user testing produces fixes |
| 4 | Freeze, evaluate, and hand off | A fresh user can finish the core journey; regression/privacy checks, research results and a reproducible demo accompany the release |

Ownership: **Dev 1 — ingestion/storage/privacy; Dev 2 — financial/insight engine; Dev 3 — conversation/tone/evaluation; Dev 4 — product/brand/UI.** Dev 1–4 are the team labels used throughout this plan. The separate [development plan](DEVELOPMENT_PLAN.md) contains each developer's weekly work packages, estimated capacity, review partners, handoffs, dependencies, weekly gates, and cut rules.

Low-effort extensions promoted into the Alpha include merchant summaries with reviewed aliases, structured insights, basic month comparisons, guided context, template-based reactions, and short explanations. One narrowly supported text-PDF adapter is a gated stretch task. OCR, multiple PDF formats, bank sync, a frontend rewrite, learned insight ranking, elaborate animation, exports and billing are deferred.

## H. What still needs proving?

| Question | Planned evidence |
| --- | --- |
| Does guessing improve engagement or understanding? | A small within-person comparison of ordinary summary versus interactive review, with order balanced |
| Does humor feel useful and respectful? | Explicit comfort/judgment feedback, skip/off controls, reviewed sensitive-category cases |
| Will users return after the first surprise? | Repeat-use intention and, where scheduling permits, a second session; no retention claim from one session |
| Can a local model improve the interaction reliably? | One on-device model smoke test with tool/grounding/latency results and deterministic fallback |
| Is the brand readable and appealing? | Keyboard/reduced-motion/contrast checks plus target-user feedback |
| Is willingness to pay real? | Exploratory interview questions; no revenue or conversion claim from the prototype |

The Week 4 study is formative, with a target of 5–8 consenting participants if available. A 10–15-person discovery study and a three-condition controlled experiment remain later research goals. Synthetic data is the default for testing; study notes should not capture bank statements or raw financial details.

The immediate implementation contract is [SCOPE.md](CompassProto1.0/SCOPE.md). The [historical phase checklist](CompassProto1.0/ProtoToDo.md) preserves completed Alpha 0.1 evidence. The [old README](ReadmeOld.md) preserves the previous pitch and run documentation.

## Run the local Python foundation

Requires **Python 3.11+**. Run from the repository root. No cloud key or model is required.

macOS / Linux:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Windows PowerShell:

```powershell
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Open `http://127.0.0.1:8501`. Load the fictional checking and savings statements. May 2026 has **$3,700.00 income**, **$2,952.94 net expenses**, and **$747.06 verified surplus**. Replacing $1,275 rent with $1,500 yields **$522.06**; adding $1,500 rent yields **−$752.94**. June's $80 ATM withdrawal remains unknown and excluded until reviewed. No game/reveal screens are available yet.

```sh
python -m pip check
python scripts/audit_fixtures.py
python scripts/audit_privacy.py
python -m pytest -q
npm test
```

### Storage, deletion, and privacy boundary

The default database is `.local/compass.db`; `COMPASS_DB_PATH` selects another local workspace. `imports` stores filenames/hashes/timestamps; `import_settings` stores source identity/mapping; `transactions` stores immutable original fields and separate overrides; `transaction_details` exposes effective labels. Money uses signed integer cents. Fractional-cent input is rejected rather than silently rounded.

To delete imports, open **Privacy and local data**, acknowledge deletion, type **DELETE**, and click **Clear all local data**. Records, overrides and this session's uploader/questions/scenarios are reset. The schema and fictional fixtures remain. Original files elsewhere are untouched; close/reload other sessions. This is logical deletion, with no promise of erasure from backups, snapshots, old journals or memory.

Financial processing is local to the browser/loopback server and SQLite. Usage telemetry is disabled. Optional Ollama uses `127.0.0.1:11434`; cloud features must be disabled in its server. Installation/model downloads are a separate network boundary. No authentication, encryption at rest, PDF support, bank-balance reconciliation or financial forecasting is provided. See [current privacy and limitations](CompassProto1.0/PHASE5.md) and [Ollama setup](CompassProto1.0/PHASE3.md).

### Release smoke and recorded demo

[Watch the current foundation demo](CompassProto1.0/demo/README.md). Optional browser tooling uses its own temporary database and profile:

```sh
python -m pip install -r requirements-dev.txt
PLAYWRIGHT_BROWSERS_PATH=.local/playwright python -m playwright install chromium
python scripts/release_smoke.py
```

For PowerShell, set `$env:PLAYWRIGHT_BROWSERS_PATH="$PWD/.local/playwright"`, then run `python -m playwright install chromium` and `python scripts/release_smoke.py` after installing the same dev requirements. Add `--record` for a roughly 72-second WebM. Generated artifacts are ignored. This smoke records the existing foundation; the new audit journey will need new acceptance coverage.

**Your money has a story. Let's talk about it.**
