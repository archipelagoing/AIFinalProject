
# Compass: BNPL Opportunity Assessment

**Working concept:** A private, local-first financial assistant for understanding overlapping installment payments.

**Product tagline:** *See what you've already committed to before you commit to more.*

**Status:** Product hypothesis — not yet validated  
**Date:** November 2026  
**Project scope:** Four developers, two two-week sprints

---

## 1. Executive Summary

Compass was originally proposed as a local, privacy-preserving financial assistant that imports bank statements, organizes transactions, and uses a Small Language Model (SLM) to answer financial questions.

The original concept is technically feasible but commercially undifferentiated. Budgeting, conversational financial assistance, transaction categorization, and financial planning already exist in established products.

### Proposed Specialization

**Buy Now, Pay Later (BNPL) payment overlap and future financial commitments.**

Services such as Affirm, Klarna, Afterpay, and PayPal Pay in 4 allow consumers to divide purchases into smaller installments.

Although individual installments may appear affordable, users can accumulate multiple overlapping payment obligations across different providers.

The resulting problem is not necessarily overspending. It is **limited visibility into the combined timing and amount of future commitments**.

Compass could help users:

1. Identify existing installment obligations.
2. Reconstruct upcoming payment schedules.
3. Detect periods when multiple payments overlap.
4. Compare obligations against expected income and other bills.
5. Simulate the consequences of another installment purchase.
6. Understand the calculations through a conversational local SLM.

### Core Product Hypothesis

> Consumers using multiple installment-payment services may value a single private interface that reconstructs their future obligations and identifies potential cash-flow shortfalls before they occur.

This is a hypothesis requiring customer and technical validation.

---

## 2. The Financial Problem

### 2.1 Individual Affordability vs. Collective Affordability

BNPL checkout interfaces generally present the installment amount associated with a particular purchase.

However, the affordability of an individual installment does not establish whether the user's combined obligations are manageable.

Consider four hypothetical purchases:

| Purchase | Purchase Price | Installment |
|---|---:|---:|
| Sneakers | $120 | $30 |
| Concert tickets | $200 | $50 |
| Clothing | $160 | $40 |
| Headphones | $240 | $60 |
| **Total** | **$720** | **$180 per installment round** |

Each installment may appear relatively small.

If all four payments become due within the same period, the user could face $180 in combined installments before considering rent, subscriptions, transportation, or other obligations.

The central issue is **payment timing and accumulation**, not simply purchase price.

### 2.2 Loan Stacking

Loan stacking occurs when a borrower holds multiple installment obligations simultaneously.

A January 2025 Consumer Financial Protection Bureau report analyzing 2022 BNPL borrowing found:

- **63%** of BNPL borrowers had overlapping loans at some point during the year.
- **33%** had simultaneous loans across multiple BNPL providers.
- **20%** averaged more than one BNPL loan per month.

These are historical findings, not estimates of current 2026 prevalence.

Source: Consumer Financial Protection Bureau, *Consumer Use of Buy Now, Pay Later and Other Unsecured Debt* (January 2025).

Reference: https://www.consumerfinance.gov/data-research/research-reports/

Importantly, overlapping loans do not automatically indicate financial distress. The opportunity is to help consumers understand their obligations accurately.

### 2.3 The Specific User Question

The proposed product should be built around one primary question:

> **"If I buy this using Pay in 4, will my existing payments leave me enough money when the next installments are due?"**

This question is more specific and testable than:

> "How can AI help me manage my finances?"

---

## 3. Proposed Product: Compass Commitments

### 3.1 Product Definition

Compass Commitments is a proposed specialization of the original Compass application.

It is a local-first assistant that consolidates known installment obligations, reconstructs upcoming payment dates, identifies payment overlaps, and explains potential cash-flow problems.

The product does not issue loans, process payments, or automatically approve purchases.

### 3.2 Primary Features

#### A. Commitment Import

Users import supported sources such as:

- Bank statements in CSV or PDF format.
- BNPL payment schedules or confirmation documents.
- Manually entered installment plans.
- User-confirmed balances and upcoming income.

The application extracts and normalizes:

- Provider
- Purchase or agreement identifier
- Original amount
- Installment amount
- Payment dates
- Payment status
- Funding account
- Source document
- Confidence or verification status

**Important limitation:** A bank statement showing previous installments does not necessarily reveal all remaining obligations.

Compass must not infer a complete payment plan from insufficient evidence.

#### B. Payment Calendar

A unified timeline showing:

- Upcoming installments
- Other known recurring bills
- Expected income
- Projected cash balances
- Missing or unverified commitments

#### C. Payment Collision Detector

A deterministic engine identifies dates or periods when combined scheduled payments could create a shortfall.

Example:

**Potential shortfall: Saturday**

Three installments and one recurring bill may reduce the projected account balance below the user's specified minimum before the next expected deposit.

The warning must identify:

- Which payments contribute to the shortfall
- The dates and amounts
- The starting balance used
- Income assumptions
- Missing information
- The calculation producing the forecast

#### D. What If? Purchase Simulator

Users enter a hypothetical purchase and installment schedule.

Example:

> "What happens if I buy a $240 item in four $60 payments?"

Compass adds the proposed installments to the existing commitment calendar and recalculates projected balances.

The system should distinguish:

- Confirmed obligations
- Estimated recurring expenses
- Hypothetical purchases
- Uncertain future income

#### E. Conversational Explanation

A local SLM allows users to ask:

- "How much do I owe in installments next week?"
- "Which payments overlap?"
- "Why is Friday my lowest-balance day?"
- "What if I add another $40 installment?"
- "What happens if my paycheck arrives two days late?"
- "Which assumptions are you making?"

The SLM explains deterministic calculations rather than inventing financial figures.

---

## 4. Technical Architecture

The proposal preserves the original four-part local financial-assistant architecture.

```text
Financial Documents
CSV | PDF | Payment Schedules | Manual Entries
                    |
                    v
          Document Ingestion
        PDF Parsing / OCR / CSV
                    |
                    v
       Transaction Normalization
     Provider and Schedule Matching
                    |
                    v
           Local SQLite DB
       Transactions | Commitments
       Accounts | Sources | Status
                    |
          +---------+---------+
          |                   |
          v                   v
    Local SLM          Deterministic Engine
   Intent Routing       Payment Scheduling
   Tool Selection       Cash-Flow Projection
   Explanations         Collision Detection
          |                   |
          +---------+---------+
                    |
                    v
          Evidence Validator
                    |
                    v
             Compass UI
     Calendar | Chat | What If?
        Source Explanations
```

### Proposed Technology

| Component | Candidate Technology |
|---|---|
| Backend | Python, FastAPI |
| Data processing | pandas |
| Database | SQLite |
| PDF extraction | pdfplumber |
| OCR fallback | Tesseract |
| Local model | Quantized instruct SLM |
| Inference runtime | Ollama or llama.cpp |
| Frontend | React or Streamlit |
| Testing | pytest and labeled fixtures |

The exact model and frontend should be chosen after benchmarking target hardware.

### Critical Financial Rules

1. Never count an installment twice when it appears in both a payment schedule and a bank statement.
2. Never assume a past payment reveals the entire future schedule.
3. Never treat projected balances as guaranteed available funds.
4. Never assume an expected paycheck will arrive on time.
5. Distinguish payments already made from payments still due.
6. Preserve source references for every commitment.
7. Require confirmation when extracted amounts or dates are ambiguous.
8. Use deterministic code for financial arithmetic.
9. Abstain when insufficient information prevents a reliable answer.
10. Never automatically initiate financial transactions.

---

## 5. Investor Evaluation Rubric

### 5.1 General Compass Baseline

The following rubric evaluates the original general-purpose Compass concept as a standalone consumer fintech investment.

Scores are subjective concept-stage assessments, not empirical results.

| Criterion | Weight | Score / 10 | Weighted Points |
|---|---:|---:|---:|
| Market opportunity | 10% | 7 | 7.0 |
| Problem severity | 12% | 6 | 7.2 |
| Differentiation | 14% | 3 | 4.2 |
| Competitive defensibility | 12% | 2 | 2.4 |
| Customer acquisition | 10% | 3 | 3.0 |
| Retention potential | 10% | 4 | 4.0 |
| Monetization | 10% | 4 | 4.0 |
| Execution feasibility | 8% | 7 | 5.6 |
| Trust and risk | 8% | 5 | 4.0 |
| Evidence and traction | 6% | 0 | 0.0 |
| **Total** | **100%** | | **41.4 / 100** |

**Assessment:** Weak standalone venture investment at the concept stage.

The earlier approximate investor assessment was 39/100; the explicit weighted values above total 41.4/100.

### 5.2 BNPL-Specialized Compass

This is a proposed reassessment using the same weights.

| Criterion | Weight | Score / 10 | Weighted Points |
|---|---:|---:|---:|
| Market opportunity | 10% | 7 | 7.0 |
| Problem severity | 12% | 8 | 9.6 |
| Differentiation | 14% | 5 | 7.0 |
| Competitive defensibility | 12% | 3 | 3.6 |
| Customer acquisition | 10% | 5 | 5.0 |
| Retention potential | 10% | 5 | 5.0 |
| Monetization | 10% | 4 | 4.0 |
| Execution feasibility | 8% | 6 | 4.8 |
| Trust and risk | 8% | 5 | 4.0 |
| Evidence and traction | 6% | 0 | 0.0 |
| **Total** | **100%** | | **50.0 / 100** |

**Assessment:** More focused and testable, but still unproven commercially.

The previously discussed 52/100 is an approximate directional assessment; the explicit rubric above yields 50/100.

### 5.3 Why Specialization Improves the Score

**Problem severity increases**

The application addresses a concrete financial decision with potentially immediate consequences.

**Differentiation improves**

The product focuses on cross-provider payment scheduling and future commitment visibility rather than general budgeting.

**Acquisition becomes more focused**

Potential customers can be described behaviorally: consumers who actively manage multiple installment plans.

**Research becomes measurable**

The team can evaluate schedule reconstruction, collision detection, and scenario calculations against known answers.

### 5.4 Why the Score Remains Limited

**Defensibility is weak**

Existing fintech companies could add overlapping-payment analysis.

**Retention is uncertain**

Users may only need the application when they have active installment obligations.

**Monetization is unproven**

The target audience may be especially unwilling to pay another recurring subscription.

**Data access is challenging**

Cross-provider schedules may not be available in consistent machine-readable formats.

**There is no demonstrated traction**

The concept currently has no validated customer demand, repeat usage, or paid conversion.

---

## 6. Competitive Positioning

### Existing Alternatives

| Alternative | Strength | Potential Compass Opportunity |
|---|---|---|
| Affirm | Visibility into its own payment plans | Combine obligations across providers |
| Klarna | Payment management within its ecosystem | Cross-provider commitment timeline |
| Afterpay | Installment tracking | Integrate obligations with other bills |
| PayPal Pay in 4 | PayPal plan visibility | Combine external installment schedules |
| Monarch Money | Broad financial aggregation and forecasting | Specialized BNPL schedule reconstruction |
| YNAB | Budget allocation and financial planning | Lower-setup conversational commitment analysis |
| Actual Budget | Local-first budgeting | Local conversational installment analysis |
| Spreadsheets | Flexible custom payment tracking | Automatic extraction and easier explanations |

**Competitive claim requiring validation:**

Users may value a dedicated cross-provider installment view more than managing each provider's payment calendar separately.

Compass should not claim that no existing product supports similar functionality without a systematic competitive audit.

---

## 7. Four-Week Development Proposal

### Sprint 1 — Weeks 1–2

**Objective:** Reconstruct and explain installment obligations from imported financial documents.

#### Week 1

| Developer | Deliverables |
|---|---|
| Dev 1 — Ingestion | CSV/PDF parser; synthetic BNPL fixtures; canonical transaction extraction |
| Dev 2 — Data | SQLite schema for accounts, transactions, commitments, installments, and source references |
| Dev 3 — SLM | Local inference setup; intent routing; approved financial-tool interfaces |
| Dev 4 — UI | Import screen, commitment table, calendar prototype, chat interface |

**Milestone:** Import a supported payment schedule and display its upcoming installments.

#### Week 2

| Developer | Deliverables |
|---|---|
| Dev 1 — Ingestion | Additional schedule format; source matching; review and correction |
| Dev 2 — Data | Installment reconciliation; paid/unpaid status; payment-calendar calculations |
| Dev 3 — SLM | Grounded Q&A; tool integration; evidence validation; missing-data handling |
| Dev 4 — UI | Complete import-review-calendar-chat workflow; source explanations |

**Sprint 1 acceptance:**

- Supported documents produce correct schedules.
- Users can correct extracted dates and amounts.
- Payments are not double-counted.
- The local SLM can answer questions using verified tools.
- Missing commitments are clearly identified.

### Sprint 2 — Weeks 3–4

**Objective:** Detect potential payment collisions and evaluate the product.

#### Week 3

| Developer | Deliverables |
|---|---|
| Dev 1 — Ingestion | Improve extraction reliability; multi-provider fixture testing; coverage checks |
| Dev 2 — Data | Cash-flow projection, collision detection, What If? scenario calculations |
| Dev 3 — SLM | Scenario-question handling; explanation quality; prompt-injection tests |
| Dev 4 — UI | Collision timeline, What If? purchase form, evidence and assumption panels |

**Milestone:** Simulate a new installment purchase and explain its projected cash-flow impact.

#### Week 4

| Developer | Deliverables |
|---|---|
| Dev 1 — Ingestion | Extraction benchmarks, regression testing, unsupported-format documentation |
| Dev 2 — Data | Calculation tests, reconciliation accuracy, shortfall-detection evaluation |
| Dev 3 — SLM | Model benchmarks, grounded-response accuracy, latency, hallucination testing |
| Dev 4 — UI | Usability testing, final polish, reproducible demo, installation instructions |

**Sprint 2 acceptance:**

- Users can import and verify multiple installment plans.
- The system produces an accurate commitment timeline on labeled fixtures.
- Payment collisions are computed deterministically.
- A hypothetical purchase updates projected balances correctly.
- The SLM explains results without fabricating figures.
- The team documents model limitations and privacy behavior.

---

## 8. Research Evaluation

### Research Question

> Can a constrained, locally deployed small language model, combined with deterministic financial tools, help users reconstruct and understand overlapping installment obligations accurately and privately?

### Proposed Experiments

| Experiment | Evaluation |
|---|---|
| Document extraction | Installment amount/date precision and recall |
| Schedule reconstruction | Correct upcoming payments and due dates |
| Reconciliation | Duplicate and paid-installment detection |
| Collision detection | Precision and recall against labeled scenarios |
| SLM intent routing | Correct financial tool selection |
| Numerical grounding | Unsupported or incorrect numerical claims |
| Local performance | Response latency and memory usage |
| User comprehension | Ability to identify upcoming payment conflicts |
| Usability | Task completion, time, errors, perceived clarity |
| Privacy | Network activity, local data storage, deletion behavior |

### Suggested Baselines

1. Manual spreadsheet tracking.
2. Deterministic payment-calendar interface without conversational AI.
3. Ungrounded SLM responding directly to financial questions.
4. SLM using deterministic financial tools and evidence validation.

### Success Criteria to Define Before Testing

- Correct schedule reconstruction on supported document fixtures.
- No known critical arithmetic errors on the fixed benchmark.
- High tool-selection accuracy.
- Accurate identification of synthetic payment collisions.
- Clear handling of incomplete or ambiguous financial data.
- Usability improvements over at least one relevant baseline.

---

## 9. Commercial Model Hypotheses

### Possible Pricing

| Plan | Proposed Price | Value |
|---|---:|---|
| Free | $0 | Import and view commitments, verify payment schedules, basic collision detection |
| Decision Pass | $2.99 one-time | Saved What If? scenarios and comparison report |
| Plus | $4.99/month | Extended history, multiple saved plans, advanced comparisons |

**Pricing remains unvalidated.**

A one-time purchase may be more appropriate than a subscription for users who need occasional purchase decisions.

Core financial accuracy, source verification, and essential payment warnings should remain free.

### Possible Go-to-Market

- Students and early-career consumers
- Financial education communities
- Privacy-conscious budgeting users
- People managing multiple installment providers
- Campus financial wellness programs

Distribution effectiveness and acquisition costs must be measured.

---

## 10. Risks and Open Questions

### Product Risks

- Users may already be satisfied with provider-specific payment reminders.
- The application may require too much manual data entry.
- Users may not trust cash-flow projections.
- BNPL usage may not generate frequent enough engagement.
- People may prefer a free spreadsheet.

### Technical Risks

- Bank statements may not contain complete future payment schedules.
- Providers may use different installment structures.
- OCR may misread amounts or dates.
- Payments may be rescheduled, refunded, or partially paid.
- Transfers and installment transactions may be double-counted.
- Expected income may be uncertain.
- Local SLM performance may be insufficient on ordinary hardware.

### Business Risks

- Low willingness to pay.
- Weak retention.
- Limited competitive moat.
- Customer acquisition costs exceeding revenue.
- Regulatory or compliance complications from financial guidance.

### Questions Requiring Validation

- [ ] How many prospective users actively maintain multiple BNPL plans?
- [ ] How do they currently track upcoming payments?
- [ ] How often do unexpected installment overlaps occur?
- [ ] Do they consider these overlaps a serious problem?
- [ ] Can Compass reconstruct schedules from real supported documents?
- [ ] Will users complete the import and correction process?
- [ ] Does Compass improve payment-timing comprehension?
- [ ] Do users return for another financial decision?
- [ ] Would users pay for planning features?
- [ ] Can an incumbent reproduce the same experience easily?

---

## 11. Recommendation

### Short-Term: Specialize in BNPL

Build the first version around:

**Import → Reconstruct → Detect Overlap → Simulate → Explain**

This is specific enough for a four-week technical project and supports objective evaluation.

### Long-Term: Expand to Financial Commitments

BNPL should be the initial use case, not necessarily the permanent limit of the product.

A broader commitment assistant could eventually cover:

- Installment payments
- Subscriptions
- Credit card minimum payments
- Loan repayments
- Rent and utilities
- Other scheduled obligations

This expansion should follow user validation rather than precede it.

### Investment Decision

**General Compass:** Weakly differentiated concept.

**BNPL Compass:** Stronger problem definition and more measurable technical value, but still requires validation.

**Current recommendation:** Proceed with a focused prototype and customer-discovery experiment, not a full commercial launch.

---

## Final Positioning

# Compass

**See what you've already committed to before you commit to more.**

A private financial assistant that helps users understand when their installment payments are due, where their obligations overlap, and how another purchase could affect their future cash flow.

**The product's central promise is not to tell users what they should buy. It is to make the commitments behind their decisions visible, understandable, and verifiable.**
