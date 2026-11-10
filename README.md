
# COMPASS
**Good with numbers. Good with people.**

*Your friendly, private personal financial assistant.*

## Run the local Python foundation

**Phase 0 is implemented:** a runnable Streamlit setup screen, local SQLite schema, exact-money and immutable-source contracts, fictional fixtures, and an independent fixture audit. Python CSV ingestion and the full assistant workflow are later phases. The separate [GitHub Pages prototype](https://archipelagoing.github.io/AIFinalProject/) remains available.

Requires **Python 3.11+**. Fresh-environment verification used Python 3.12.2, Streamlit 1.67.0, and pytest 9.2.0. Run these commands from the repository root.

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

The app binds to `127.0.0.1:8501`. It needs no cloud key or Ollama. Verification commands, after activating the virtual environment:

```sh
python -m pip check
python scripts/audit_fixtures.py
python -m pytest -q
```

The standalone audit uses only Python's standard library. Its `--json` option reports exact cents; a mismatch exits with status 1 and never rewrites expected values. Evaluation oracles are never read by the app.

See [Phase 0 implementation and verification](CompassProto1.0/PHASE0.md) for contracts, schema, fixtures, and remaining work. The product pitch below describes the broader planned application.

## A. What Is Compass?

Compass is a local-first, Small Language Model (SLM)-powered personal finance application that allows users to talk to their financial information like they would talk to a friendly, knowledgeable accountant.

Users can:
1. **Understand their money:** Import CSV/PDF bank statements, organize transactions, and identify spending patterns.
2. **Ask questions:** Use natural language to ask about income, expenses, subscriptions, and trends.
3. **Verify answers:** Inspect calculations, source transactions, assumptions, and missing information through Financial X-Ray.
4. **Explore decisions:** Use deterministic What If? simulations to understand hypothetical financial changes.
5. **Learn:** Receive approachable explanations of financial concepts through Teach Me Why.
6. **Reflect:** View optional, nonjudgmental monthly summaries through Compass Stories.

**Core identity:** A friendly personal accountant who explains without judgment and never pretends to know something it cannot verify.

### Technical Architecture

```text
CSV / PDF Bank Statements
          |
          v
Parsing + OCR Fallback
          |
          v
Normalization + Categorization
          |
          v
Local SQLite Database
          |
          +------------------------+
          |                        |
          v                        v
Local SLM (Ollama)      Deterministic Financial Tools
          |                        |
          +-----------+------------+
                      |
                      v
           Evidence + Validation
                      |
                      v
              Compass Interface
        Chat | X-Ray | What If?
          Stories | Teach Me Why
```

The SLM interprets questions, selects approved tools, and explains verified results. Python-based financial tools perform calculations.

**Accuracy principle:** Never fabricate financial figures. When data is incomplete or an answer cannot be verified, communicate that limitation.

---

## B. Why Is Compass Needed?

Managing personal finances can be confusing, intimidating, and emotionally uncomfortable.

### Problems

- **Financial anxiety:** People may avoid examining their spending because they anticipate judgment.
- **Fragmented information:** Financial records may be spread across multiple banks and statements.
- **Financial illiteracy:** Terms such as APR, compound interest, and cash flow can be difficult to understand.
- **Privacy concerns:** Users may not want to share financial data with cloud AI systems or third-party account aggregators.
- **Unreliable AI calculations:** General-purpose language models can produce plausible but incorrect financial answers.
- **Complicated interfaces:** Conventional budgeting tools may require extensive setup and ongoing maintenance.

### Proposed Solution

Compass combines conversational accessibility with private, evidence-backed financial analysis.

**Product philosophy: Facts without fear.**

Users should be able to understand their financial circumstances without feeling embarrassed, overwhelmed, or misled.

---

## C. Existing Market and Competitors

| Competitor | Existing strengths | Compass differentiation |
|---|---|---|
| Monarch Money | Account aggregation, budgeting, AI assistance, forecasting | Local-first statement analysis and verifiable on-device responses |
| YNAB | Budgeting methodology, education, planning | Conversational exploration without requiring a particular budgeting method |
| Actual Budget | Open-source, local-first budgeting | Friendly SLM-powered financial explanations |
| Rocket Money | Subscriptions, spending management, savings opportunities | Private statement-based analysis with source-level transparency |
| ChatGPT / Claude | Flexible conversational explanations and document analysis | Dedicated local financial tools and controlled calculations |
| Spreadsheets | Flexible, auditable financial calculations | Natural-language accessibility and guided explanations |

### Competitive Reality

Compass is not the first budgeting app, private finance tool, or financial AI assistant.

Its proposed differentiation is the combination of privacy, conversational accessibility, verifiable calculations, and nonjudgmental financial education.

This differentiation must be tested with users rather than assumed.

---

## D. What Specific Gap Does Compass Fill?

**Compass fills the proposed gap between traditional budgeting dashboards and general-purpose AI assistants.**

### Four Differentiators

**1. Privacy without financial isolation**

Users can combine financial statements from different institutions without providing banking credentials or requiring cloud inference.

**2. Financial X-Ray**

Every important numerical answer can reveal:
- Source transactions
- Calculation formulas
- Assumptions
- Data coverage
- Missing information

**3. Friendly, nonjudgmental conversation**

Compass explains financial information patiently and accurately without scolding users or making moral judgments about spending.

**4. Understanding and planning in one place**

Users can move through:

**What happened? → Why? → What could change?**

### Compass Stories

Optional monthly financial summaries that highlight meaningful patterns without embarrassing merchant rankings, arbitrary financial-health grades, or unsolicited criticism.

### Teach Me Why

Short financial explanations connected to the user's questions, with fictional examples available when personal data is unnecessary.

### Notifications

Quiet by default. Initial notifications are limited to in-app import confirmations, errors, and missing-data warnings.

---

## E. Business Model

### Primary: B2C / D2C

**Business-to-Consumer (B2C):** Compass sells software directly to individual consumers.

**Direct-to-Consumer (D2C):** Distribution occurs through a website or downloadable application.

### Secondary Opportunities

| Model | Application |
|---|---|
| B2C / D2C | Primary consumer software model |
| B2B | Institutional licensing to universities or employers |
| B2B2C | Organizations provide Compass to students or employees |
| C2C | Not applicable to the proposed product |
| Freemium | Free core application with optional paid features |
| SaaS | Possible for licensing/services, but cloud processing is not required |

### Target Customers

- Students and recent graduates
- Early-career professionals
- Privacy-conscious consumers
- People unfamiliar with financial terminology
- People who find conventional budgeting applications intimidating

### Revenue Principles

Compass should monetize software functionality, not financial data.

No sale of transaction histories, advertising based on purchases, or undisclosed financial-product commissions.

### Commercial Requirements

- Clear privacy policy
- Local data deletion and export
- Secure software updates
- Appropriate licensing
- Transparent limitations
- Legal review of financial-advice boundaries

Compass should not claim to replace a licensed accountant or financial adviser.

---

## F. Proposed Pricing

| Plan | Price | Features |
|---|---|---|
| Compass Free | $0 | Basic imports, financial overview, essential Q&A, calculations, corrections, source evidence |
| Decision Pass | $2.99 one-time | Saved scenario workspace, comparisons, sensitivity checks, exportable report |
| Compass Plus | $4.99/month | Unlimited saved scenarios, extended comparisons, Stories, detailed exports |
| Compass Plus Annual | $44.99/year | Annual alternative to monthly Plus |

*These are pricing hypotheses, not validated market prices.*

### Pricing Philosophy

**Never put accuracy, privacy, or verification behind a paywall.**

Paid features should provide convenience and advanced capabilities.

### Illustrative Revenue

Assume:
- 1,000 monthly active users
- 5% Plus conversion
- $4.99 monthly subscription

50 paying subscribers × $4.99 = **$249.50 monthly gross revenue**.

This excludes operating expenses, payment processing, support, taxes, and churn.

### Business Validation Needed

- Customer interviews
- Willingness-to-pay experiments
- Competitive comparisons
- Retention testing
- Support-cost estimates
- Subscription versus one-time purchase preference

A payment system is not required for the four-week academic prototype.

---

## G. Development Plan: 2 Sprints, 4 Weeks, 4 Developers

### Team Responsibilities

| Developer | Primary Responsibility |
|---|---|
| Dev 1 | Statement ingestion, PDF parsing, OCR, CSV, bank-format support |
| Dev 2 | SQLite, normalization, categorization, financial calculations |
| Dev 3 | Local SLM, tool routing, explanations, validation, model evaluation |
| Dev 4 | UI, onboarding, chat, Financial X-Ray, Stories, usability |

Each developer also contributes tests, documentation, and integration support.

### Sprint 1: Weeks 1–2

**Goal:** Complete the original local statement-chat workflow.

#### Week 1 — Foundation

| Developer | Deliverables |
|---|---|
| Dev 1 | Collect synthetic/consented statements; implement CSV and one text-PDF parser; preserve source references; produce canonical transaction records |
| Dev 2 | Define SQLite schema; implement account/transaction storage, duplicate detection, transfer flags, income/expense calculations |
| Dev 3 | Set up Ollama; benchmark two local models; define intent schema and approved tools; implement spending, category, and period-comparison intents |
| Dev 4 | Build application shell, import UI, transaction table, basic chat interface, backend integration |

**Shared:** Agree on API contracts, datasets, hardware requirements, privacy boundaries, and acceptance tests.

**Week 1 milestone:** Import a statement and answer at least one question with a correct, traceable calculation.

#### Week 2 — Functional Alpha

| Developer | Deliverables |
|---|---|
| Dev 1 | Add second text-PDF adapter; test OCR fallback; implement correction API; measure extraction accuracy |
| Dev 2 | Add recurring-payment detection, category editing, transfer exclusion, monthly comparison, evidence objects |
| Dev 3 | Connect SLM to financial tools; implement missing-data handling; validate numerical responses; benchmark intent accuracy and latency |
| Dev 4 | Complete import-review-chat workflow; add Financial X-Ray; implement friendly responses, error states, and demo flow |

**Shared:** Integration testing, privacy checks, arithmetic review, retrospective.

**Sprint 1 Acceptance Criteria**
- Local import-to-answer workflow works.
- CSV and two supported PDF layouts parse correctly on test fixtures.
- Duplicate and transfer handling passes benchmark tests.
- Numerical responses come from financial tools.
- Users can inspect source evidence.
- Unsupported questions produce clear limitations.

### Sprint 2: Weeks 3–4

**Goal:** Add product differentiation and rigorously evaluate the system.

#### Week 3 — Product Features and Reliability

| Developer | Deliverables |
|---|---|
| Dev 1 | Improve PDF reliability; test multi-bank imports; implement reconciliation and coverage checks |
| Dev 2 | Build deterministic What If? simulator; implement assumptions and sensitivity checks; prepare structured monthly insights |
| Dev 3 | Add Teach Me Why; evaluate misleading prompts and prompt injection; compare SLM-only and tool-grounded outputs |
| Dev 4 | Build What If? UI, three-card Stories, response-detail controls, privacy preferences; run usability sessions |

**Shared:** Financial-claim review, adversarial testing, competitor workflow comparison.

**Week 3 milestone:** A user can ask, verify, learn, and explore one hypothetical financial change.

#### Week 4 — Evaluation and Release

| Developer | Deliverables |
|---|---|
| Dev 1 | Freeze supported formats; complete parser regression tests; document unsupported inputs; test deletion |
| Dev 2 | Finalize calculation/scenario tests; cover refunds, transfers, irregular income, missing data; finalize benchmark results |
| Dev 3 | Finalize SLM selection; evaluate intent accuracy, grounding, hallucinations, latency, memory usage, prompt injection |
| Dev 4 | Polish onboarding and UI; add report export; test clean-machine installation; finalize usability fixes and demo |

**Shared:** Feature freeze, full regression testing, privacy/network tests, research report, presentation rehearsal.

**Sprint 2 Acceptance Criteria**
- Application works locally on target hardware.
- Financial benchmark has no known critical calculation failures.
- Missing information is handled correctly.
- SLM accuracy and latency are measured.
- Users can complete the core workflow independently.
- Demo includes chat, Financial X-Ray, and What If?.
- Results and limitations are reproducibly documented.

### Four-Week Milestones

| Week | Milestone |
|---|---|
| 1 | Import → SQLite → financial calculation → local Q&A |
| 2 | Complete grounded conversational finance workflow |
| 3 | What If?, Teach Me Why, optional Stories, usability |
| 4 | Validation, privacy testing, benchmarking, packaging, presentation |

### Priority Order

**P0 — Required**
- Local-first processing
- Supported statement imports
- Correct financial calculations
- Local SLM-powered Q&A
- Source evidence
- Missing-data handling

**P1 — High Value**
- Financial X-Ray
- What If? simulator
- Contextual financial explanations

**P2 — Optional**
- Compass Stories
- Advanced reports
- Additional PDF adapters
- Rich preferences

**Out of Scope**
- Live bank synchronization
- Automated investing
- Stock recommendations
- Full tax preparation
- Mobile push notifications
- Social financial sharing
- Autonomous financial decision-making

### Research Evaluation

| Research Question | Metric / Method |
|---|---|
| Can an SLM interpret financial questions? | Intent and tool-selection accuracy |
| Do deterministic tools reduce errors? | SLM-only versus SLM-plus-tools comparison |
| How accurate is statement extraction? | Precision, recall, amount/date accuracy |
| Is local inference practical? | Latency, RAM usage, model size |
| Do explanations improve understanding? | Comprehension and error-detection tasks |
| Does friendly language reduce judgment? | Controlled usability comparison |
| Does the app preserve privacy? | Network, storage, deletion, and injection tests |

Proposed benchmarks should include ordinary financial questions, incomplete data, refunds, transfers, irregular income, and adversarial requests.

Example targets:
- Zero known critical arithmetic errors on the fixed test suite.
- At least 95% correct tool selection on the agreed benchmark.

These are proposed targets, not achieved results.

---

## H. What's Missing?

### Product and Market

- [ ] Interview 10–15 prospective users.
- [ ] Validate the friendly accountant positioning.
- [ ] Compare Compass against existing apps and spreadsheets.
- [ ] Test whether users value local privacy enough to install software.
- [ ] Validate pricing and willingness to pay.

### Engineering

- [ ] Select target operating systems and hardware.
- [ ] Benchmark and select the SLM.
- [ ] Finalize supported PDF and CSV formats.
- [ ] Define transaction normalization rules.
- [ ] Establish financial calculation invariants.
- [ ] Create a privacy and security threat model.
- [ ] Define local storage, encryption, backups, and deletion behavior.
- [ ] Finalize integration contracts.

### Research

- [ ] Define labeled financial question datasets.
- [ ] Select model and system baselines.
- [ ] Establish evaluation thresholds.
- [ ] Test numerical grounding and hallucinations.
- [ ] Measure extraction reliability.
- [ ] Conduct usability and comprehension studies.
- [ ] Document failures and limitations.

### Business and Compliance

- [ ] Validate commercial differentiation.
- [ ] Evaluate distribution and support costs.
- [ ] Review model licenses.
- [ ] Review privacy and financial-advice boundaries.
- [ ] Establish realistic retention and conversion assumptions.

### Team

- [ ] Confirm Pranav's agreement with the evolved scope.
- [ ] Confirm developer assignments.
- [ ] Confirm course evaluation requirements.
- [ ] Agree on weekly milestones and acceptance criteria.
- [ ] Establish shared repository, code review, and testing rules.

### Three Biggest Risks

**1. Data reliability:** Incorrectly parsed statements can produce incorrect financial answers even when the arithmetic is flawless.

**2. Local model performance:** A model may be accurate on developer hardware but too slow or difficult to run on ordinary laptops.

**3. Market viability:** The combination of privacy, conversational AI, and explainability is promising but not yet proven commercially.

---

## Final Product Pitch

### compass.
**Good with numbers. Good with people.**

Managing money shouldn't require a finance degree, a complicated spreadsheet, or sharing your most private information with another company.

Compass is a friendly, local-first financial assistant powered by a small language model. It brings your bank statements together, answers questions in everyday language, explains exactly where the numbers come from, and helps you explore financial decisions without judgment.

Unlike a generic chatbot, Compass grounds its numerical answers in deterministic financial tools. Unlike a conventional budgeting dashboard, it starts with the conversation the user actually wants to have.

**Your money stays yours. Every answer has a reason.**

### Guiding Principle

**Compass makes it easier to talk about your money without making it easier to be misled about your money.**
