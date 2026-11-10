# compass.

> **Delivery plan revised November 10, 2026:** 96 balanced engineering tickets, all-team Wrapped build November 16–21, continued coding and benchmarking November 28, code freeze December 1, ACL-style report December 1–3, and December 3 submission. See [G7 revised execution plan](#g7-revised-execution-plan--96-balanced-tickets-november-10december-3-2026).

> **GitHub README math:** Equations use GitHub-supported `$...$` (inline) and `$$...$$` (display) LaTeX delimiters. Render this file in GitHub Markdown, not a plain-text preview.


Comprehensive README · Product proposal A–H · SLM fine-tuning strategy · Brand system · Four-week implementation

# Good with numbers. Good with people.

Your bank statement has receipts. Compass has commentary.

## Executive summary

Compass is a privacy-first, nonjudgmental conversational financial companion powered by a specialized, fine-tuned small language model (SLM). It transforms locally processed bank statements into evidence-backed dialogue, interactive financial stories, and practical insights. The model is the core of the product, not an optional chatbot attached to a dashboard.

We're building it for students and young adults who want to be better with money but don't particularly enjoy budgeting, examining bank statements, or confronting their own spending habits.

Our core insight is that financial awareness is not simply a data problem. It's also an engagement problem.

People may already suspect they spend too much on delivery, impulse purchases, subscriptions, or little everyday luxuries. The information is sitting in their bank statements. But looking at it can be boring, uncomfortable, or embarrassing.

Compass changes how that information is experienced.

Imagine a personal financial audit that feels like Spotify Wrapped crossed with a candid, funny conversation. You guess how much you spent. Compass reveals the actual number, shows you the receipts, makes a memorable observation, asks what happened, and helps you explore a change if you want one.

Underneath that playful experience is a serious technical foundation: a **fine-tuned local SLM as the conversational orchestrator**, local statement processing, a structured financial database, deterministic financial tools, and verifiable evidence. The SLM decides what to ask and which approved tools to call; it does not invent amounts or replace exact arithmetic.

THE INVESTMENT THESIS

## Make financial self-awareness something people choose to experience, rather than something they avoid.

The opportunity is not another dashboard or another chatbot. It's a distinctive consumer experience that makes personal financial information engaging, conversational, and actionable—without sacrificing accuracy or privacy.

### Product at a glance

| Dimension                  | Compass proposal                                                               |
| -------------------------- | ------------------------------------------------------------------------------ |
| Primary audience           | Students and young adults, approximately 18–30                                 |
| Main problem               | Avoidance of financial information and difficulty interpreting spending habits |
| Signature experience       | Interactive Money Wrapped and conversational financial audit                   |
| Core technology            | Fine-tuned Qwen-class SLM + local inference + deterministic tools + SQLite      |
| Data ingestion             | CSV and supported PDF statements                                               |
| Differentiation hypothesis | Participatory financial storytelling with source-backed AI conversation        |
| Business model             | B2C freemium, optional one-time purchase and subscription                      |
| Longer-term distribution   | B2B2C through universities and employers                                       |
| MVP timeline               | Four weeks, two two-week sprints                                               |
| Team                       | Four developers                                                                |
| Research focus             | Fine-tuning gains, grounded tool use, nonjudgmental dialogue, local feasibility |

# A. What is Compass?

## A1. The product

Compass is a local-first financial companion that helps users understand their financial behavior through conversation and interactive storytelling. Its three non-negotiable pillars are **privacy-first operation, conversational intelligence, and nonjudgmental support**. Its fine-tuned SLM is the primary interaction engine: it understands intent, chooses verified financial tools, asks clarifying questions, maintains user-controlled context, and explains results without shame.

It has two complementary modes.

Everyday Compass is the practical assistant. Users import statements, review transactions, ask questions, understand financial terminology, and explore financial scenarios.

Compass Money Wrapped is the signature experience. It turns verified transaction patterns into guesses, reveals, awards, humorous observations, and conversations about spending.

The two modes are powered by the **same specialized SLM and deterministic financial engine**, so the entertaining version never needs to invent or reinterpret numbers independently. Fine-tuning should specialize financial dialogue and tool selection, not memorize private bank statements.

## A1a. Product commitments and boundaries

**Privacy first.** In the intended consumer product, raw statements, transaction records, embeddings/memory, and inference stay on-device by default. No bank passwords are required. No real personal statements are uploaded to Colab for training. Local-first is a design target to verify through network, logging, storage, and deletion tests—not an automatic guarantee from using an SLM.

**Conversational.** The model conducts multi-turn investigations: interpret question → select approved tool → inspect evidence → respond → invite correction or context → update only user-approved memory. It may ask why an expense mattered, but may not claim to know the reason.

**Nonjudgmental.** Financial facts are not moral verdicts. Gentle, Direct, and Roast change style only; none may shame poverty, debt, essential spending, identity, or personal circumstances. Users can disable humor and decline suggestions.

**Truthful.** The model must say when accounts or periods are missing, distinguish estimates from recorded facts, and link numerical claims to transaction evidence. Deterministic tools calculate money in integer cents or Decimal.

**User autonomy.** Compass offers trade-offs, not unilateral instructions or financial decisions. The user may conclude that a purchase was worthwhile.

## A2. The five signature experiences

1\. Guess the Damage

Before seeing a spending total, users estimate how much they spent on a category or merchant.

The difference between their estimate and the actual amount becomes the reveal.

“You guessed $80. The receipts say $143.”

2\. Money Wrapped

A personalized monthly story featuring spending changes, favorite merchants, recurring patterns, unusual expenses, and improvements.

The user moves through short editorial cards instead of navigating an ordinary financial report.

3\. The Money Awards

Data-backed, humorous recognitions such as Most Loyal Merchant, Biggest Plot Twist, Most Frequent Small Purchase, and Best Comeback.

Awards make patterns memorable without turning spending into a moral score.

4\. Reality Check

Playful, direct commentary on verified spending patterns. Users select Gentle, Direct, or Roast.

“Eleven Taco Bell trips. At this point, you should be on the holiday card list.”

Humor targets the spending pattern, not the user's identity, income, or circumstances.

5\. The Confessional

After the reveal, users explain the circumstances behind their spending.

Compass asks contextual questions, respects user priorities, and calculates realistic alternatives if the user wants to change something.

## A3. Supporting financial features

These remain essential parts of the original Compass vision.

| Feature            | Purpose                                            | Example                                      |
| ------------------ | -------------------------------------------------- | -------------------------------------------- |
| Financial X-Ray    | Explain where a number came from                   | Show the 11 transactions totaling $143       |
| What If?           | Explore conditional financial changes              | What if I reduced three purchases?           |
| Teach Me Why       | Explain financial concepts in plain language       | What's the difference between APR and APY?   |
| Statement Chat     | Answer supported questions about financial records | Why did October cost more than September?    |
| Transaction Review | Let users correct imported records                 | Reclassify a transfer or mislabeled merchant |
| Coverage Warnings  | Identify incomplete or outdated information        | October only includes one bank account       |

The critical product principle is that a user should always be able to move from a funny story to a serious explanation. The SLM carries context across the transition; the deterministic evidence stays unchanged. **The Plot Twist** is an additional narrative pattern, not a sixth independent product: Compass compares the user’s initial belief with the verified data and their own revised interpretation, without claiming that a changed belief is necessarily a mistake.

## A4. Example user experience

A fictional user, Alice, imports her October statements.

Compass finds 11 Taco Bell transactions totaling $143, compared with $92 in September.

Rather than immediately showing the amount, it asks Alice to guess.

# compass.

Illustrative demo

OCTOBER MONEY WRAPPED

# How much do you think you spent at Taco Bell?

# $80

Show me the receipts

Fictional data. In the actual product, every displayed amount must come from verified transactions.

## A5. What Compass is not

Compass is not a bank, a lender, a payment processor, an investment adviser, or an autonomous financial agent.

It does not move money, approve purchases, automatically take out loans, or decide which expenses a user is allowed to make.

It provides financial information, education, and conditional calculations. Users remain responsible for their decisions.

# B. Why is Compass needed?

## B1. The behavioral problem

Many people do not need another tool to record spending. Their banks already do that.

They need a reason to look closely enough to understand their spending.

There are several plausible barriers:

- Avoidance: Looking at spending can produce discomfort or regret.
- Information overload: Hundreds of transactions are difficult to interpret individually.
- Lack of context: A statement says what happened, but not why.
- Low engagement: Traditional budgeting reports can feel repetitive.
- Financial intimidation: Users may hesitate to ask basic questions or acknowledge habits they want to change.

These are research hypotheses for our target population, not claims that every young adult experiences all five.

## B2. The problem with ordinary financial summaries

Imagine a user sees:

“Dining: $286.”

That number may be accurate, but it provides little context.

Compass could instead ask:

“You spent $286 dining out this month. How much did you think it was?”

The user guesses $160.

The reveal is $126 higher than expected.

Compass can then show whether the difference came from more purchases, larger purchases, or both.

This makes the information personally relevant rather than merely numerical.

## B3. Why entertainment might help

Our hypothesis is that curiosity and humor can lower the friction of beginning an uncomfortable task.

The experience should be designed to create recognition, not humiliation.

A useful distinction:

Discretionary spending refers to spending that may be adjustable.

Wasteful spending is a value judgment that depends on the user's needs, circumstances, and preferences.

Compass can detect frequent restaurant purchases. It cannot automatically know that those purchases were stupid.

It can ask, make a playful observation, and help the user decide whether the pattern is worth changing.

## B4. The desired outcome

The goal is not to make users spend as little as possible.

It is to help them become more aware of their behavior, understand trade-offs, and make intentional choices.

A successful interaction might end with a spending adjustment.

It might also end with the user deciding that an expense is worthwhile.

Both outcomes can represent better understanding.

# C. What already exists in the market?

## C1. Competitive landscape

Compass competes for attention with budgeting applications, financial education content, general-purpose AI assistants, and existing banking tools.

| Product                       | Primary strength                                                    | What we would test against it                                       |
| ----------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Monarch Money                 | Consolidated financial management, budgeting, forecasting, insights | Does interactive storytelling create greater engagement?            |
| YNAB                          | Structured budgeting and educational methodology                    | Can Compass deliver useful insight with less setup?                 |
| Rocket Money                  | Subscription tracking, bill management                              | Is conversational reflection a compelling additional value?         |
| Actual Budget                 | Local-first privacy and user control                                | Can Compass make local finance software more approachable?          |
| General-purpose AI assistants | Flexible natural-language interaction                               | Can dedicated tools and transaction provenance improve reliability? |
| Banking applications          | Direct access to current balances and transactions                  | Can Compass explain cross-merchant patterns more engagingly?        |

We should not claim that competitors lack AI, insights, recaps, or financial education.

Our advantage must be demonstrated through the complete experience.

## C2. Competitive positioning — feature-by-feature and price-by-price

Compass combines **personal finance** (accurate records and calculations), **entertainment** (memorable stories), **conversational AI** (contextual reflection), and **privacy software** (local processing and user control). This combination is a positioning hypothesis, **not an established moat**.

### C2.1. Head-to-head capability matrix

**Legend:** ✅ = established core/advertised capability; ❌ = not a core advertised capability; ◐ = partial, plan-dependent, integration-dependent, or not clearly established; 🛠️ = proposed Compass feature, not yet shipped. A ❌ is **not** proof that no adjacent feature exists. The table compares product emphasis, not independent laboratory testing.

| Capability | Compass (planned) | Rocket Money | YNAB | Monarch | ChatGPT Finances | Actual Budget |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| Track and categorize transactions | 🛠️ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Connected bank-account synchronization | ❌ | ✅ | ✅ | ✅ | ✅ | ◐ |
| Conversational questions about spending | 🛠️ | ✅¹ | ◐ | ✅ | ✅ | ❌ |
| Text-message financial AI | ❌² | ✅¹ | ❌ | ❌ | ❌ | ❌ |
| Fine-tuned *small* financial conversation model | 🛠️ | ◐ | ◐ | ◐ | ❌ | ❌ |
| Local/on-device AI inference by default | 🛠️ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Local-first financial records | 🛠️ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Structured budgeting and goal planning | ◐ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Interactive guessing / reveal game | 🛠️ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Story-led Money Wrapped with awards | 🛠️ | ◐ | ◐ | ◐ | ◐ | ❌ |
| Explicit source-backed numerical explanations | 🛠️ | ◐ | ◐ | ◐ | ◐ | ◐ |
| Explicitly evaluated nonjudgmental dialogue | 🛠️ | ◐ | ◐ | ◐ | ◐ | ❌ |
| Subscription cancellation / bill negotiation | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

¹ Rocket Money's **Rowan** is included in **Premium+** and supports financial questions through phone messaging (subject to eligibility). ² Compass SMS/RCS texting is a **post-MVP stretch goal**, not a currently promised feature. Some competitors may offer recaps, summaries, conversational features, or source evidence in forms not captured by a binary table; verify before making public marketing claims. The fine-tuned SLM row means a **disclosed, product-specific small local model**, not simply any proprietary AI.

### C2.2. Head-to-head pricing (USD, checked November 2026)

| Product | Free entry | Paid monthly | Annual price / equivalent | What the price buys |
|---|---|---|---|---|
| **Compass — proposed** | **$0** | **$8.88 Plus** | **$88.88/year (~$7.41/mo)** | Private specialized conversation, deeper stories, comparisons, saved reflections |
| **Compass Story Pass — proposed** | — | **$1.50 one-time** | Not a subscription | One expanded themed Wrapped/audit |
| Rocket Money | Yes | Premium sliding scale, typically **$7–$14**; **Premium+ $15** | Varies by plan/platform | Premium+ includes Rowan text assistant and bill negotiation |
| YNAB | Trial (34 days) | **$14.99** | **$109/year (~$9.08/mo)** | Structured budgeting methodology |
| Monarch Money Core | Trial (7 days) | **$14.99** | **$99.99/year (~$8.33/mo)** | Full-featured budgeting, account aggregation and reports |
| Monarch Money Plus | Trial | Verify current monthly option | **$199.99/year (~$16.67/mo)** | Advanced financial planning/reporting |
| ChatGPT Finances | Available to eligible **Free** users | **No separate Finances fee established**; ChatGPT Plus **$20** | Depends on ChatGPT plan | Broad hosted financial conversations; account connections where eligible |
| Actual Budget | **Free, open source** | Optional hosting, e.g. ~$2/mo on a third-party host | Hosting-dependent | Local-first envelope budgeting |

**Source links:** [Rocket Money pricing](https://help.rocketmoney.com/en/articles/2217739-how-much-does-rocket-money-cost) · [Rowan](https://help.rocketmoney.com/en/articles/16760933-what-is-rowan) · [YNAB](https://www.ynab.com/pricing) · [Monarch](https://www.monarch.com/pricing) · [Monarch monthly](https://help.monarch.com/hc/en-us/articles/44815447567636-Updating-Your-Subscription) · [ChatGPT Finances](https://openai.com/index/personal-finance-chatgpt/) · [ChatGPT Plus](https://help.openai.com/en/articles/6950777) · [Actual Budget](https://github.com/actualbudget/actual). Prices and entitlements can change; recheck before publication.

### C2.3. Head-to-head strategic conclusions

- **Against Rocket Money:** Rocket wins on bank connections, subscription management and its existing text assistant. Compass must win on genuinely local AI and user-controlled reflection—not claim to invent texting.
- **Against YNAB:** YNAB wins on structured proactive budgeting. Compass targets people who want to understand what happened before adopting a budget.
- **Against Monarch:** Monarch wins on breadth, aggregation and mature reporting. Compass targets a lighter, specialized and privacy-first conversational experience.
- **Against ChatGPT Finances:** ChatGPT wins on general reasoning breadth and integrations. Compass must test whether a specialized small model can provide a *better-fit* emotional experience for narrow tasks with private on-device inference; do not claim superior raw intelligence.
- **Against Actual Budget:** Actual already owns a strong local-first story. Compass must demonstrate that conversation, interaction design and memorable reflection add value beyond privacy.

**Defensible positioning hypothesis:** *Most finance products help people track, budget or optimize money. Compass helps people talk about it—privately, accurately and without judgment.* This is a hypothesis to test, not proof of superiority.

### C2.4. What must be benchmarked, not asserted

Measure the same tasks and equivalent synthetic data across (a) a conventional dashboard, (b) static Wrapped and (c) Compass conversational Wrapped. Separately compare the base SLM with the fine-tuned SLM using identical tools, prompts, decoding settings and held-out cases. We cannot assume any competitor's real-world performance without controlled access and comparable conditions.

## C3. What we need to prove

Investors will ask whether people find Compass substantially more valuable than existing alternatives.

We should compare equivalent tasks across products and measure:

- Task completion and numerical correctness.
- Time required to understand a spending pattern.
- Recall of the insight after a delay.
- Perceived usefulness and judgment.
- Willingness to repeat the experience.
- Willingness to pay.

A strong product demonstration is useful. Comparative evidence is more convincing.

# D. What specific gap does Compass fill?

## D1. The proposed market gap

Compass addresses a potential gap between having financial information and wanting to engage with it.

Its primary interaction is not “build a budget.”

It is “discover something about your money.”

That distinction affects the onboarding, content, navigation, visual design, and AI behavior.

## D2. Our core product loop

Import and verify financial data

Identify meaningful spending patterns

Guess → Reveal → React

Discuss → Decide → Explore alternatives

Return with new financial data

## D3. Financial X-Ray as the trust mechanism

Every numerical insight should have an inspectable source.

If Compass says a user spent $143 at Taco Bell, the user should be able to see:

- The period analyzed.
- The transactions included.
- The merchant-normalization rules.
- The total and calculation method.
- Any refunds or excluded transactions.
- Whether all relevant accounts were imported.

The application must not present incomplete records as a complete financial picture.

## D3a. Why a fine-tuned SLM is the differentiation hypothesis

A generic LLM can discuss money; a spreadsheet can calculate totals. Compass tests whether a **small, locally deployable, domain-specialized conversational model** can combine financial tool orchestration, grounded explanations, contextual follow-ups, and nonjudgmental interaction better than an equivalently sized untuned baseline. This is a hypothesis requiring evaluation, not a proven moat. Training is centralized during development; inference is local for consumers.

## D4. Compass's distinct brand identity

The design should be memorable enough that users recognize it without seeing the logo.

### Brand positioning

Neo-editorial pop: Independent magazine art direction meets a precise financial tool.

The design combines expressive typography, asymmetrical layouts, playful graphic elements, and clean financial evidence displays.

It should avoid generic fintech dashboards, excessive gradients, stock illustrations, and decorative AI imagery without a purpose.

### Color palette

Paper

\#F5F1E8Warm background

Ink

\#17171BTypography

Voltage

\#D9FF43Highlights

Iris

\#8755E8Signature accent

Pool

\#82DDE5Secondary stories

Guava

\#FF806DEditorial emphasis

The palette is a design proposal. Exact text/background pairings require contrast testing before implementation.

### Typography

- Display: bold, expressive grotesk typography for story headlines.
- Body: clean sans-serif typography for navigation and explanations.
- Numbers: tabular or monospaced numerals for totals, calculations, and comparisons.

### Brand mascot

**Primary mascot: a tiny flying piggy bank.** The pig should feel like a charming, slightly cheeky editorial character, not a generic cartoon banking logo. Its silhouette combines a rounded ceramic piggy-bank body, small wings, a coin slot, expressive eyes, and a minimal compass-star accent that ties it to the product name. An alternate static piggy-bank form works for compact UI placements.

**Mascot role:** The pig acts as a companion and guide—celebrating discoveries, reacting to surprising patterns, introducing Money Wrapped awards, and making difficult financial conversations feel less intimidating. It must never mock debt, poverty, income, or essential purchases. Its expression should change with the user's selected Gentle/Direct/Roast tone without changing factual content.

**Visual rules:** Distinctive simple silhouette, legible at favicon size, accessible contrast, no excessive infantilization, no clutter over financial charts. Use the Iris/Guava/Voltage palette selectively; avoid implying the pig itself is an AI entity with independent financial authority.

**Brand meaning:** A piggy bank represents personal money; wings represent freedom and perspective. The abundance symbolism in the $8.88 and $88.88 prices is a playful brand motif, not a promise of wealth.

### Motion design

Motion should communicate the story.

A guessing-game reveal can use a dramatic number transition. An award can appear like an editorial title card. Financial X-Ray should expand smoothly without unnecessary animation.

Reduced-motion preferences must be respected.

### Page architecture

| Page     | Design direction            | Purpose                                   |
| -------- | --------------------------- | ----------------------------------------- |
| Landing  | Bold editorial storytelling | Communicate the concept immediately       |
| Import   | Minimal and reassuring      | Upload and verify statements              |
| Home     | Warm, personal, organized   | Access the latest audit and ask questions |
| Wrapped  | Full-color story experience | Interactive financial discoveries         |
| Chat     | Calm conversational layout  | Discuss habits and questions              |
| Insights | Precise, information-rich   | Examine calculations and source records   |
| Settings | Clear and transparent       | Control privacy, data, and personality    |

The design principle is simple:

The storytelling can be theatrical. The evidence should never be theatrical.

# E. Business model, audience, distribution, and growth

## E1. Our initial customer

Our primary audience is people aged approximately 18–30 who are becoming financially independent.

That includes college students, graduate students, people entering the workforce, young renters, and people managing credit cards or multiple accounts for the first time.

They don't necessarily need to be in debt or struggling financially. Someone can have a stable income and still be surprised by how much they spend on everyday conveniences.

### Three initial customer personas

Alice — The busy student

She has limited time, unpredictable expenses, and no interest in maintaining a detailed budget. Compass helps her notice where small purchases accumulate without criticizing necessary spending.

Jordan — The first-job professional

Jordan earns a regular paycheck but doesn't understand why savings aren't growing. Compass identifies recurring spending patterns and compares months.

Sam — The reluctant budgeter

Sam has tried traditional budgeting apps and stopped using them. A five-minute monthly Wrapped feels more approachable than another spreadsheet.

These are design personas, not research-validated customer segments.

## E2. Business model categories

| Model    | Meaning                                  | Compass application                                                          |
| -------- | ---------------------------------------- | ---------------------------------------------------------------------------- |
| B2C      | Business to consumer                     | Our main business: individuals use Compass and may purchase premium features |
| D2C      | Direct to consumer                       | We reach users directly through our website and marketing                    |
| B2B      | Business to business                     | Potential licensing to financial education organizations                     |
| B2B2C    | Business to business to consumer         | Universities or employers sponsor access for their students or employees     |
| C2C      | Consumer to consumer                     | Not part of the core product                                                 |
| Freemium | Free core product with paid enhancements | Reduces adoption friction and allows users to experience value before paying |

## E3. Customer acquisition strategy

Our most promising acquisition asset is the product demonstration itself.

A conventional finance app might advertise a spending chart. Compass can show a short interaction:

“How much did you spend at your favorite restaurant?”

The user guesses.

The number appears.

Compass delivers a witty, personalized observation.

The viewer immediately understands what the product does.

We would test four initial acquisition channels: campus organizations and financial-literacy workshops; short-form creator demonstrations; student ambassadors and referrals; and privacy-focused or budgeting communities.

The initial landing page should demonstrate the product with fictional data before asking visitors to import financial records.

## E4. Activation funnel

We should measure the steps from discovery to first meaningful value.

1. Visitor: Arrives at the Compass website.
2. Interested user: Tries a fictional-data demonstration.
3. Activated user: Imports a statement and reviews the transactions.
4. Engaged user: Completes a personalized financial reveal.
5. Reflective user: Opens the evidence or participates in a follow-up conversation.
6. Returning user: Imports a later statement or completes another audit.
7. Paying user: Purchases an optional premium experience.

Activation should not mean merely creating an account. It should mean reaching the first useful, trustworthy financial insight.

## E5. Retention strategy

The monthly financial audit creates a potential recurring habit.

However, entertainment alone may not sustain retention. Compass should give users meaningful comparisons across time.

Examples include whether a merchant became more frequent, whether an expense category increased, whether a goal was maintained, and whether the user's spending estimates became more accurate.

A returning user might see:

“Last month you underestimated your takeout spending by $63. Want to see how close your guess is this month?”

That is both an entertaining callback and a measurable form of improved financial awareness.

The main retention obstacle is manual statement importing. We should evaluate whether the privacy benefit is worth that recurring effort to users.

## E6. Privacy as part of the business model

Our intended consumer architecture uses local storage and local inference. Users should not need to provide their bank passwords. **Google Colab is for training on synthetic or appropriately licensed non-sensitive examples only; consumer financial records must not be sent there.** Packaging, local model download, filesystem permissions, telemetry, and optional sync need explicit security review.

We should not sell transaction data, create advertising profiles from purchases, or monetize by steering users toward loans and credit products.

Institutional sponsors must not receive identifiable spending histories.

A local-first design reduces some external data exposure, but it still requires secure storage, careful logging, document handling, and deletion controls.

## E7. Unit economics and business viability

Subscription revenue alone is not enough to evaluate a business.

We also need customer acquisition costs, retention, support costs, and gross margins.

A simplified customer acquisition cost is:

$$
CAC=\frac{\text{Acquisition spending}}{\text{New paying customers}}
$$

Monthly subscription churn:

$$
c=\frac{\text{Subscribers lost during month}}{\text{Subscribers at start}}
$$

For an illustrative stable subscription business, expected customer lifetime in months can be approximated as:

$$
L\approx\frac{1}{c}
$$

This assumes approximately constant monthly churn and is not reliable for every subscription cohort.

A simplified subscription lifetime gross profit is:

$$
LTV\approx\frac{P\times g}{c}
$$

Where $P$ is monthly price and $g$ is gross margin.

We should not present an LTV/CAC ratio until we have real acquisition, churn, and margin data.

# F. Proposed pricing and monetization

## F1. Pricing philosophy and recommended tiers

**Recommendation (hypothesis, not validated willingness-to-pay):** Keep an actually useful free conversational product, lower the impulse-priced one-time story, and test **$8.88/month** for recurring value. Do not charge for correctness, provenance, privacy controls or basic conversations. Because inference is local, cloud-token cost need not scale with every conversation, but customer support, distribution, app updates, payment fees and optional texting still cost money.

| Plan | Proposed price | Included | Why it exists |
|---|---:|---|---|
| **Compass Free** | **$0** | Local statement import, transaction corrections, basic SLM conversation, essential X-Ray, one basic Wrapped/month, complete evidence and deletion controls | Build trust; compete with free ChatGPT Finances and Actual Budget |
| **Story Pass** | **$1.50 once** | One expanded themed Wrapped, additional awards, alternate story layouts and shareable *redacted* export | Low-risk impulse purchase, not a recurring commitment |
| **Compass Plus** | **$8.88/month** | Unlimited eligible story runs within local hardware limits, longer local history, cross-month comparisons, personalized reflections, saved goals, custom story themes, advanced What If? | Subscription must earn recurring use beyond one monthly reveal |
| **Compass Plus Annual** | **$88.88/year** | Same Plus benefits; about **$7.41/month** equivalent | Lower price for committed users; ~16.6% below 12 monthly payments |

**Why not $4.99?** It may underprice a distinctive recurring experience, but price is not a proxy for value. **Why not $15?** Rocket Money already bundles real messaging and automation at $15; Compass initially has fewer mature financial-management features. **Why $8.88?** The repeating 8s reference the angel number 888, associated symbolically with financial abundance. This is a memorable branding choice—not a promise of prosperity or proof of willingness to pay. The price is below many premium monthly finance plans, but its value must be tested. **Important:** ChatGPT Finances is accessible to eligible Free users, so conversation itself is not a defensible premium feature.

**Value ladder:** Free = understand the facts; Story Pass = one special experience; Plus = richer recurring conversations, long-term comparisons and personalization. No manipulative lock-in or paid access to deleting records. Real SMS/RCS texting, automated imports, mobile deployment and cross-device sync are **stretch goals**, not promised Plus launch features.

**Pricing experiments:** randomized price-page tests at $6.99/$8.88/$10.99; actual checkout intent or preorders where appropriate; one-time $0.99/$1.50/$2.49; segment by student vs first-job user; measure activation, conversion, 30-day retention and refund rates. Avoid claiming validated willingness to pay from hypothetical surveys alone.

## F2. What should never be paywalled

The following should be included in the free experience: accurate supported calculations, source evidence, correction of imported transactions, missing-data warnings, privacy controls, and deletion of personal financial data.

## F3. Revenue formulas

Monthly subscription gross revenue:

$$
MRR=N_{\text{paid}}\times P
$$

Total monthly gross revenue including one-time purchases:

$$
R_{\text{gross}}=(N_{\text{paid}}\times P)+(N_{\text{passes}}\times P_{\text{pass}})
$$

For example, suppose Compass has 10,000 monthly active users, 500 Plus subscribers, and 200 Story Pass purchases in one month.

$$
R_{\text{gross}}=500(8.88)+200(1.50)
$$

$$
R_{\text{gross}}=\$4{,}740
$$

This is an illustrative revenue scenario, not a prediction. It excludes refunds, taxes, processing costs, and operating expenses.

## F4. What we must validate

We need to determine whether users prefer paying once for a special audit or subscribing for recurring financial reflection.

We also need to test whether the paid features are valuable enough to support their prices without making the free version feel deliberately incomplete.

A strong early experiment would offer prospective users a real choice between a free audit, a $1.50 expanded audit, and a $8.88 recurring plan—rather than asking only whether they say they would pay.

# G. Technical implementation, formulas, and four-week sprint plan

## G0. AI transparency — what is AI and what is not

Compass should explain its AI clearly in the interface, README, and investor pitch. **The specialized fine-tuned small language model is the central conversational agent**, but it does not calculate or independently verify money totals.

| Product behavior | AI-driven? | Mechanism and trust boundary |
|---|---|---|
| Understanding user questions and follow-ups | **Yes** | Fine-tuned on-device SLM interprets intent and conversational context |
| Choosing approved financial tools | **Yes, constrained** | SLM proposes a structured tool call; schema validation and permission checks decide whether to execute it |
| Adding expenses, counting transactions, computing changes | **No** | Deterministic, tested Python functions over SQLite records using exact decimal/integer-cent arithmetic |
| Parsing supported structured CSV rows | **Generally no** | Deterministic import rules; ambiguous rows are flagged for review |
| Explaining spending patterns and asking thoughtful questions | **Yes** | SLM verbalizes tool-backed facts, with user-selected tone |
| Ranking candidate Wrapped insights | **Hybrid** | Deterministic scoring and evidence filters; SLM sequences the story and writes captions |
| Guess-versus-actual reveal | **Hybrid** | User supplies guess; deterministic engine computes difference; SLM provides commentary |
| Financial X-Ray evidence and missing-data warnings | **No for underlying facts** | Transaction provenance and coverage checks; SLM may explain the result |
| Inferring motives, emotional states, or moral worth | **Not permitted as fact** | Ask users rather than assume; no hidden psychological profiling |
| Training the Compass model | **Yes, during development** | Synthetic financial dialogue and reviewed preference data; Colab GPU for fine-tuning, never required by end users |
| Running Compass after installation | **Yes, locally** | Quantized model on supported consumer hardware; actual device compatibility must be benchmarked |

**Model disclosure:** Document the base model and version, fine-tuning method, training-data provenance, evaluation results, hardware requirements, and known failure modes. Label generated commentary as AI-generated; distinguish facts from hypotheses and hypothetical scenarios. Never claim that local inference alone guarantees complete privacy: verify logs, network calls, storage, exports, and deletion.

## G1. SLM-native system architecture

**Central principle: the fine-tuned SLM is the conversational brain; deterministic tools are the financial source of truth.** The SLM is not optional to the product's core research contribution.

```text
User (question / estimate / context / correction)
        ↓
Fine-tuned local SLM (intent, tool choice, dialogue, tone)
        ↕                       ↕
Approved financial tools    Local user-controlled memory
        ↕                       ↕
SQLite + provenance + verified transaction records
        ↓
Claim validator / coverage checks / safety rules
        ↓
Conversational reply + evidence + Wrapped / Confessional UI
```

The model can choose an approved tool, interpret structured results, request clarification, generate contextual explanations and narrative cards, and use opted-in conversational memory. It **cannot** invent a transaction, directly rewrite imported records, calculate authoritative totals in free text, make investment decisions, or send personal financial data to remote services.

### Tool contract (initial)

| Tool | Inputs | Outputs / constraints |
| --- | --- | --- |
| `get_spending` | account scope, date range, category/merchant | integer-cent total, transaction IDs, coverage |
| `compare_periods` | matched scopes and periods | amounts, absolute and conditional percent change |
| `get_transactions` | filters, pagination | redacted structured records and provenance |
| `get_recurring` | scope, time window | recurring candidates, evidence and uncertainty |
| `simulate_change` | baseline, proposed frequency/amount | explicitly conditional savings estimates |
| `get_import_coverage` | account IDs, date range | included/missing data and warnings |
| `request_correction` | transaction ID, proposed correction | **user confirmation required** before mutation |

All tool calls use validated schemas, scoped queries, limits, and auditable outputs. Treat bank statement descriptions as untrusted input; they must not become instructions to the model.

## G2. Proposed technical stack

| Layer | Preferred implementation | Notes |
| --- | --- | --- |
| Frontend | React + TypeScript, custom design tokens | Neo-editorial, accessible, responsive |
| Desktop delivery | Tauri or packaged local web app (decision pending) | Verify ordinary-user installation |
| Local backend | Python + FastAPI for MVP | Production packaging may change |
| Storage | SQLite, local-only by default | Secure file handling, deletion, no raw-data telemetry |
| Import | CSV, one known text-PDF format; `pdfplumber` | OCR and broad PDF coverage stretch goals |
| Base model | **Qwen3-1.7B** initial candidate | Compare Qwen3-4B if compute permits; no assumed winner |
| Alternative baseline | SmolLM3-3B or another compact instruct model | Only if evaluation budget allows |
| Training | Google Colab free GPU + Transformers + PEFT + TRL | QLoRA/LoRA subject to GPU memory and compatibility |
| Local inference | llama.cpp / Ollama with quantized model | Benchmark on CPU and Apple Silicon |
| Finance engine | Python `Decimal` or integer cents | Deterministic, tested |
| Validation | Pydantic, provenance validator, pytest | Fail closed on unsupported financial claims |

### G2a. Fine-tuning strategy

**Research hypothesis.** A domain-specialized SLM will outperform the same base model on grounded personal-finance dialogue, appropriate tool selection, and nonjudgmental responses, while remaining usable on ordinary consumer hardware.

**Training and consumer inference are different.** A free Colab NVIDIA GPU may train LoRA adapters; users should not need Colab, NVIDIA hardware, or a cloud account. The resulting adapter can be merged where supported, quantized, and shipped with or downloaded by the local application. Model/license and redistribution terms must be checked before release.

**Candidate selection.** Benchmark untuned Qwen3-1.7B first. Challenge it with Qwen3-4B if GPU VRAM and consumer latency permit. Choose on observed quality, memory, throughput, and model licensing—not parameter count alone.

**Data design (planning targets, not validated requirements):**

| Synthetic SFT category | Target examples |
| --- | ---: |
| Financial education and explanations | 500 |
| Tool selection, grounded tool results, evidence | 500 |
| Nonjudgmental and sensitive financial dialogue | 600 |
| Multi-turn contextual clarification | 400 |
| Missing data, correction, uncertainty and refusal | 300 |
| Tone variation, humor and narrative | 200 |
| **Total** | **2,500** |

Use synthetic user profiles, simulated statements, diverse income/circumstance cases, validated numerical ground truth, and carefully reviewed examples. Partition by **profile and scenario family** so test conversations are not near-duplicates of training cases. Do not include real private statements in training by default. Maintain a dataset manifest with provenance, generation prompts, review status, and license.

**Training steps:** (1) establish base-model baseline; (2) create and validate SFT dataset; (3) run a small smoke-test LoRA/QLoRA job; (4) train the adapter with checkpointing; (5) compare on held-out tests; (6) optionally construct 300–500 reviewed preference pairs for DPO **only if time permits**; (7) export, quantize, and test local inference. Preference training is a stretch goal, not a prerequisite for a successful MVP.

**Colab setup check:** select an available GPU runtime and run `!nvidia-smi` plus `torch.cuda.get_device_properties(0)`. GPU type, VRAM, quota, and session lifetime are not guaranteed. Store **non-sensitive** checkpoints and adapter weights in a controlled Drive location; never upload personal transaction files.

**Core evaluation:** base vs fine-tuned model on identical held-out questions. Report intent/tool selection accuracy, grounded numerical claim rate, hallucination rate, evidence coverage, multi-turn consistency, perceived judgment (human-rated), preference/agency respect, response latency, peak memory, and quantized local usability. Financial correctness and privacy are hard gates, not dimensions that humor can compensate for. Compare with a deterministic dashboard/template baseline for product-level comprehension.

### G2b. Local consumer distribution decision

- **MVP:** local-first desktop prototype with packaged backend and quantized model; avoid requiring a developer to start a server manually for the final usability test.
- **Potential later:** browser-local inference on supported devices, or mobile-specific smaller variants, after compatibility testing.
- **No mandatory hosted inference:** a cloud fallback must be an explicit opt-in, clearly disclosed, and never silently transmit financial data.
- **Acceptance:** test installation, offline operation after setup, no unexpected network calls, deletion, response speed, and memory on at least two representative consumer machines.

## G3. Core data model

At minimum, we need structured representations for accounts, imports, transactions, categories, insights, conversations, and scenarios.

A transaction should preserve the original description, normalized merchant, amount, date, account, source import, and correction status.

An Insight Object should preserve the calculation result, relevant transaction references, confidence or coverage indicators, and the rules used to select the insight.

The SLM must not modify a financial fact simply to make a joke funnier.

## G4. Core financial formulas

### Recorded expenses

$$
E_m=\sum_{i\in m}e_i
$$

Where $e_i$ represents an eligible expense in month $m$.

Transfers between a user's own accounts should not be double-counted as expenses. Refunds should be handled explicitly.

### Net recorded cash flow

$$
NCF_m=I_m-E_m
$$

Where $I_m$ is recorded income.

This is not necessarily a complete measure of financial health, especially if accounts are missing.

### Merchant spending

$$
S_{v,m}=\sum_{i\in m}e_i\mathbf{1}(merchant_i=v)
$$

Where $v$ identifies a normalized merchant.

### Merchant frequency

$$
N_{v,m}=\sum_{i\in m}\mathbf{1}(merchant_i=v)
$$

### Average transaction amount

$$
\overline e_{v,m}=\frac{S_{v,m}}{N_{v,m}}
$$

Defined when $N_{v,m}>0$.

### Month-over-month spending change

$$
\Delta S=S_{v,m}-S_{v,m-1}
$$

$$
\%\Delta S= \frac{S_{v,m}-S_{v,m-1}}{S_{v,m-1}}\times100
$$

If the previous period is zero, the percentage change is undefined. Compass should show the absolute change instead.

### Guessing-game error

$$
G=|\widehat S-S|
$$

Where $\widehat S$ is the user's estimate and $S$ is actual recorded spending.

Normalized error:

$$
G_{\%}=\frac{|\widehat S-S|}{S}\times100
$$

For positive $S$.

### Scenario savings

$$
M=k\overline e
$$

Where $k$ is the number of avoided purchases and $\overline e$ is the assumed average cost.

Annualized:

$$
A=12M
$$

These are conditional estimates, not guaranteed savings.

## G5. Insight-ranking algorithm

We need a method to choose which insights deserve to appear in Wrapped.

An initial scoring formula could be:

$$
Q_j=0.30U_j+0.25F_j+0.20M_j+0.15C_j+0.10R_j
$$

All components are normalized to $[0,1]$.

| Variable  | Interpretation                                            |
| --------- | --------------------------------------------------------- |
| $U_j$ | How unusual the pattern is relative to the user's history |
| $F_j$ | Frequency or repetition                                   |
| $M_j$ | Financial magnitude                                       |
| $C_j$ | Confidence in the data and classification                 |
| $R_j$ | Relevance to a user-selected interest or goal             |

These are proposed weights, not empirically established values.

Before ranking, the system should exclude insights that lack sufficient evidence or involve categories unsuitable for humor.

The final story selection should also avoid redundancy. Five cards about the same restaurant would make a weak Wrapped experience even if all five score highly.

## G6. Conversational personality

Compass supports three tones.

Compass personality preview

GentleDirectRoast

compass.

Eleven Taco Bell visits and $143. That's a pretty consistent habit. Want to look at it?

The financial facts remain identical. Only the wording changes.

The SLM should receive structured facts and approved tone instructions.

It should never invent transactions, claim to know a user's motivations, mock essential expenses, or imply that financial hardship is a personal failure.

## G7. Revised execution plan — 96 balanced tickets, November 10–December 3, 2026

**This section replaces the earlier 91-ticket plan and the illustrative four-week schedule.** Six meeting gates: Thursday/Saturday on November 12/14, 19/21, 26/28. **Code freeze is Tuesday, December 1**; December 1–3 is the dedicated ACL-style report and submission period. November 26 is US Thanksgiving; use an asynchronous review if needed. The project is a three-week accelerated MVP; no schedule can guarantee a flawless result. The definition of done is evidence-based.

### Workload, ownership, and daily rules

- **96 tickets = 24 per developer**: each developer gets 5 before each Thursday (15) and 3 before each Saturday (9). Each ticket should be one reviewable PR or a small coherent group of commits; tickets are not assumed equal in effort. Estimate hours at kickoff and rebalance by actual hours daily.
- **All four developers write frontend code**, and each also contributes tests, integration, data/model/backend work, and an evaluation artifact. Domain lead is accountable for the feature, not sole implementer.
- **All four build Wrapped simultaneously November 16–21:** Dev 1 owns coverage + calendar UI, Dev 2 guessing/awards/scenarios, Dev 3 SLM commentary and chat transitions, Dev 4 story navigation + mascot. Cross-owner PR review is mandatory.
- Every ticket requires: issue ID, clear scope, input/output contract, synthetic fixture, automated test or documented manual test, screenshot/log, reviewer, PR, acceptance pass/fail. A demo is not proof of all edge cases.
- Daily 7 PM ET async updates: completed ticket IDs, hours spent, test evidence, blockers, next day's plan. Meet Thursdays/Saturdays after tickets are submitted; review failed gates and rebalance workload.
- No real bank records in the training corpus or public demo. SLM performs conversation and constrained tool selection; exact numbers come from deterministic functions. All AI claims that contain numbers require evidence IDs.
- **P0:** financial misstatement, data leak, corrupted import, broken core flow. **P1:** essential feature nonfunctional, persistent tool hallucination, unhandled crash. No P0/P1 at freeze; P2 defects documented honestly.

### Calendar and deliverables

| Date | Individual daily action and team integration gate |
|---|---|
| Tue Nov 10 | Create repository/branches/CI, assign 96 issues, estimate ticket hours, pin API contracts, check Colab GPU, agree synthetic fixture rules. |
| Wed Nov 11 | Each developer completes at least 3 of 5 Nov 12 tickets; pair-review schemas and initial frontend contracts. |
| Thu Nov 12 | Finish remaining 2 tickets before meeting; demonstrate CSV/PDF fixture, exact totals, base SLM and chat UI. |
| Fri Nov 13 | Each developer completes 2 of 3 Nov 14 tickets, integrates against real APIs, posts PR evidence. |
| Sat Nov 14 | Complete third ticket and demo import → correct → ask → inspect X-Ray. Lock tool and story schemas. |
| Sun Nov 15 | Optional buffer; resolve blockers only, no unapproved new scope. |
| Mon Nov 16 | All four begin Wrapped work in parallel; Dev 3 starts data/training preparation; merge chart and story contracts. |
| Tue Nov 17 | Finish ~2 Nov 19 tickets per developer; run early integration tests and inspect first Colab training run. |
| Wed Nov 18 | Finish ~2 more Nov 19 tickets; cross-review Wrapped cards, SLM tool outputs, evidence links. |
| Thu Nov 19 | Finish fifth ticket before meeting; live shared Wrapped demo with model checkpoint and mascot prototype. |
| Fri Nov 20 | Finish 2 of 3 Nov 21 tickets each; integrate all Wrapped parts and run E2E beta suite. |
| Sat Nov 21 | Complete third ticket; demonstrate full import → chat → Wrapped → Confessional → What If → delete journey. |
| Sun Nov 22 | Optional buffer for critical defects and checkpoint backups. |
| Mon Nov 23 | Complete 2 Nov 26 tickets each; run finance, model and privacy benchmarks on frozen test sets. |
| Tue Nov 24 | Complete 2 more Nov 26 tickets; conduct pilot and local inference measurements; triage P0/P1. |
| Wed Nov 25 | Complete fifth Nov 26 ticket and rehearse full release-candidate demo. |
| Thu Nov 26 | Meeting 5: benchmark review and feature-complete candidate; Thanksgiving async review permitted. **Not code freeze.** |
| Fri Nov 27 | Complete 2 Nov 28 tickets each; patch failures; only add stretch work if all core P0/P1 cleared. |
| Sat Nov 28 | Meeting 6: complete third ticket, code/benchmark demos, integration and stretch-feature decisions. **Not a report-only meeting.** |
| Sun Nov 29 | Optional defect repair; prepare final measured artifacts. |
| Mon Nov 30 | Full regression, reproducibility, performance, security and final release review; finalize figures/results JSON. |
| Tue Dec 1 | **12:00 PM ET code freeze:** tag `v1.0-rc`; no feature work afterward. Begin ACL-style paper with assigned sections and actual measurements. |
| Wed Dec 2 | All four write/review ACL sections, regenerate tables/figures, check citations, ethics, limitations, and reproducibility. |
| Thu Dec 3 | Final ACL-style PDF, repository, benchmark artifacts and demo submission; verify receipt. |

### Weekly outcomes and meeting agendas (facilitator-ready)

**Meeting operating rule:** The Thursday and Saturday meetings are **review and decision gates**, not the time to start the tickets due that day. Each developer posts a 2–4 minute screen-recorded demo or reproducible evidence before the meeting. At the meeting, demonstrate the integrated app on the same synthetic fixture, inspect failing tests and benchmark changes, make decisions, and record an owner plus due date for each blocker. Suggested 60-minute format: 5 minutes goal/status, 20 minutes demos (5 per developer), 15 minutes integrated journey and QA, 15 minutes decisions/risks, 5 minutes assignments and written minutes. Meeting 5 may be asynchronous for Thanksgiving. The individual issue details and acceptance tests appear in the ticket backlog immediately below.

#### Week 1 — November 10–14: Trustworthy foundations and first financial conversation

**Weekly outcome:** A synthetic statement can be imported, normalized, calculated exactly, corrected or deleted, and queried through a visible chat flow with evidence links. The untuned SLM baseline and a held-out evaluation set exist before fine-tuning. **Definition of success:** the team can run `import → preview → total → ask → X-Ray` from a clean checkout without fabricated numbers.

##### Meeting 1 — Thursday, November 12: Contracts, data accuracy, and baseline

**Before the meeting: 5 tickets per developer (CMP-1112-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Repository/API contracts; two-persona synthetic fixture with golden totals; two-layout CSV importer; one text-PDF importer and unsupported-file warning; local provenance/deletion vertical slice. Demo both accepted and rejected files, plus deletion. |
| **Dev 2** | SQLite migrations and seed; cents/sign/refund/transfer rules; merchant/category/expense tools; Pydantic tool contracts with evidence IDs; real-data overview UI card. Demo a traceable merchant total and an invalid-argument rejection. |
| **Dev 3** | Colab GPU/model decision record; ≥150 held-out test cases with leakage rules; untuned Qwen3-1.7B benchmark; constrained tool-call parser; chat input/loading/error UI. Demo baseline results and an invalid model tool call being blocked. |
| **Dev 4** | Brand tokens and accessible components; navigation/import/review UI; chat visual language and tone selector; seven-card Wrapped storyboard; Playwright smoke harness. Demo keyboard navigation and the initial browser test. |

**Discussion agenda:** (1) Agree on transaction signs, refunds, transfers, currencies and date boundaries; (2) approve the typed API and evidence-ID format; (3) review Colab VRAM, model feasibility and benchmark leakage policy; (4) approve the seven-card Wrapped storyboard and shared design tokens; (5) identify the most fragile import format and decide what is explicitly unsupported. **Decisions to record:** frozen v0 schemas, supported file formats, model candidate, baseline dataset version, reviewer for each integration PR. **Gate:** exact totals match golden fixtures, clean checkout works, and a baseline benchmark artifact is saved. **If blocked:** reduce supported PDF layouts before compromising arithmetic or provenance.

##### Meeting 2 — Saturday, November 14: First integrated vertical slice

**Before the meeting: 3 tickets per developer (CMP-1114-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Import correction/duplicate/coverage behavior integrated with review UI; demonstrate one corrected merchant and a re-import that does not double-count. |
| **Dev 2** | Month comparisons and source-backed X-Ray outputs connected to UI; demonstrate the exact rows behind a displayed amount. |
| **Dev 3** | SLM-to-tool orchestration and grounded reply path; demonstrate valid and invalid requests, uncertainty and abstention. |
| **Dev 4** | End-to-end import/chat/X-Ray interaction and browser regression; demonstrate complete vertical slice without manual database edits. |

**Discussion agenda:** (1) Run the same `import → correct → ask → receipts` script together; (2) triage any discrepancy between UI and database; (3) lock Insight Object, Wrapped-card and conversation-response contracts; (4) approve training-data categories and human review rubric; (5) assign cross-owner Wrapped PR reviews. **Decisions to record:** v1 story schema, explicit P0/P1 defects, training set size and quality checks, Week 2 integration branches. **Gate:** the full vertical slice works on synthetic records; each numerical answer can be traced to transactions. **If blocked:** prioritize a working single-statement journey over additional file formats.

#### Week 2 — November 16–21: All-team Wrapped, specialized SLM, and conversational beta

**Weekly outcome:** All four developers build Wrapped in parallel, the fine-tuned SLM has a reproducible checkpoint, and the application supports `import → chat → guess → reveal → receipts → Confessional → What If?`. The flying ceramic pig is implemented as HTML/CSS/JS by Dev 4 with state signals from Dev 3; visual polish cannot block the core journey.

##### Meeting 3 — Thursday, November 19: Shared Wrapped alpha and first tuned checkpoint

**Before the meeting: 5 tickets per developer (CMP-1119-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Merchant aliases, source completeness and Wrapped calendar/heatmap frontend; show each day linked to included transactions and a missing-account warning. |
| **Dev 2** | Ranked insights, guessing-game arithmetic, awards and scenario tool/UI; demonstrate correct guess-versus-actual difference and conditional savings. |
| **Dev 3** | Synthetic SFT dataset and Colab QLoRA/LoRA run, saved adapter/checkpoint, tuned-model smoke comparison, SLM-generated grounded story and chat-state schema; show real outputs, not hand-authored copy. |
| **Dev 4** | Seven-card story shell, chart transitions, responsive chat/story navigation, first HTML/CSS/JS ceramic flying-pig implementation; show motion-reduction behavior and SLM state hookup. |

**Discussion agenda:** (1) Each developer presents their own Wrapped card or interaction; (2) run one joined story from real synthetic fixture totals; (3) compare base versus tuned model on a *small development set*, not the locked final test set; (4) inspect tone and shame-risk examples; (5) choose what visual refinements can be deferred. **Decisions to record:** minimum story-card set, adapter version, allowed SLM animation states, integration blockers, targeted fixes for November 21. **Gate:** all four Wrapped contributions render together and the first tuned checkpoint is reproducible. **If blocked:** keep base model as a temporary diagnostic baseline, not a replacement for the fine-tuning deliverable; prioritize one working story over extra transitions.

##### Meeting 4 — Saturday, November 21: End-to-end beta and first model comparison

**Before the meeting: 3 tickets per developer (CMP-1121-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Complete coverage/correction and privacy integration through Wrapped; demonstrate reclassification changing both chart and explanation correctly. |
| **Dev 2** | Complete What If?, X-Ray and award-calculation integration; show deterministic numerical outputs across story and chat. |
| **Dev 3** | Connect tuned SLM to chat/Confessional and evaluate paired base-versus-tuned outputs on a fixed interim split; demonstrate no invented amount and controlled tool invocation. |
| **Dev 4** | Assemble chat, pig states, story transitions and responsive full-journey E2E test; demonstrate keyboard and reduced-motion flows. |

**Discussion agenda:** (1) One teammate unfamiliar with the flow performs the complete beta journey; (2) examine exact calculation and grounding failures; (3) review base/tuned metrics, model latency and checkpoint backups; (4) inspect accessibility and mobile-width layout; (5) decide whether any feature is at risk of missing November 26. **Decisions to record:** beta acceptance result, prioritized P0/P1 list, benchmark owner and pilot participants, hardware target, features requiring hard scope limits. **Gate:** all major product experiences can be completed without developer intervention on supported fixtures. **If blocked:** fix broken core journeys before adding new features.

#### Week 3 — November 23–28: Reliability, investor evidence, and last coding meeting

**Weekly outcome:** Finish and test the README-defined research-grade MVP; gather honest investor-facing evidence for financial correctness, model specialization, privacy, latency, comprehension and user comfort. Meeting 6 remains an engineering meeting. **Code freeze is not until December 1.**

##### Meeting 5 — Thursday, November 26: Release candidate and benchmark review

**Before the meeting: 5 tickets per developer (CMP-1126-*)**

| Developer | Goal and demo required by Thursday |
|---|---|
| **Dev 1** | Import edge cases, duplicate/transfer/refund and missing-account coverage, deletion/privacy checks and associated UI warnings; show extraction precision/recall. |
| **Dev 2** | Financial golden-suite, tool-argument/evidence validation, chart/award math, scenario tests and benchmark visualization; show exact accuracy and failure cases. |
| **Dev 3** | Locked-set base-versus-tuned evaluation, tool-selection/grounding/nonjudgment rubric, local model latency/RAM tests and reproducibility notes; show paired results with sample sizes. |
| **Dev 4** | Complete product QA, accessibility, mascot fallback, onboarding/usability pilot and demo packaging; show task completion and perceived-judgment feedback. |

**Discussion agenda:** (1) Review each metric's denominator, test set and evidence artifact; (2) inspect all P0/P1 bugs and privacy issues; (3) compare model quality and consumer-device performance; (4) review pilot feedback without presenting small-sample results as market proof; (5) select November 28 engineering priorities. **Decisions to record:** release-candidate status, defects assigned with due dates, whether one stretch feature is safe, final evaluation protocol, Thanksgiving attendance/asynchronous sign-offs. **Gate:** all essential flows are implemented and measured; no unowned critical bugs. **If blocked:** cancel stretch work and dedicate November 27–30 to reliability.

##### Meeting 6 — Saturday, November 28: Last coding and robustness review

**Before the meeting: 3 tickets per developer (CMP-1128-*)**

| Developer | Goal and demo required by Saturday |
|---|---|
| **Dev 1** | Patch import/privacy regressions; rerun offline/deletion/coverage tests; optionally add one supported import enhancement only after all P0/P1 are cleared. |
| **Dev 2** | Fix financial/chart edge cases, run stress and property-based tests, validate all Wrapped statistics and export final metric tables. |
| **Dev 3** | Run model ablations and robustness cases, measure uncertainty/CI and failure categories, optimize local inference or adapter configuration. |
| **Dev 4** | Fix end-to-end UX and accessibility defects, refine pig/chat animations, test responsive performance, and optionally implement one low-risk stretch interaction. |

**Discussion agenda:** (1) Run a fresh-checkout full demo with no hidden setup; (2) inspect automated test dashboard, performance and remaining defects; (3) review ablations and confidence intervals for credible paper/investor claims; (4) approve or reject any stretch feature based on risk; (5) assign November 29–30 final fixes and reproducibility tasks. **Decisions to record:** explicit go/no-go for December 1 freeze, exact remaining bugs with owners, final benchmark run command, version/tag owner, paper figures to regenerate after freeze. **Gate:** a complete release candidate exists with only documented low-severity issues. **If blocked:** all developers swarm P0/P1 defects; no cosmetic work until resolved.

#### Finalization — November 29–December 3: Freeze first, then ACL-style report

**November 29–30 (engineering buffer):** Each developer reruns their own test suite plus one other developer's integration tests, closes regressions, updates documentation and screenshots, and verifies clean setup. Dev 3 freezes the final model/config and benchmark scripts; Dev 2 regenerates numeric result tables; Dev 1 checks data provenance/privacy; Dev 4 checks end-to-end demo and accessibility. Do not change evaluation rules to improve scores after seeing results.

**Tuesday, December 1, noon ET — code freeze:** All four approve the release tag, dependency lockfiles, model adapter hash, fixture hash, benchmark outputs, screenshots, setup steps and known-limitations list. From this point, no planned feature coding; emergency fixes require all four to approve and record the change. **Everyone's final-sprint deliverable includes an ACL-style paper contribution.**

**December 1–3 — ACL report work split:** Dev 1 writes Dataset/Preprocessing/Privacy/Ethics; Dev 2 writes Financial Tools/Equations/Validation; Dev 3 writes Model/Fine-tuning/Experiments/Results; Dev 4 writes Introduction/Related Work/UX/Presentation and integrates ACL LaTeX. Each developer must contribute at least one figure/table, one limitations paragraph, a reproducibility note, and peer review of another section. All four approve abstract, conclusions and final claims. **Thursday, December 3:** submit PDF, repository, model/setup documentation, evaluation artifacts and demo before the actual course deadline.

**Meeting minutes template (copy for all six meetings):** `Date/time | attendees | gate passed? | four demos + PR links | benchmark snapshot (N/version) | P0/P1/P2 defects | decisions made | owner and deadline for each blocker | next meeting's exact demo | action items`. Record metrics as measured, pending or failed—never as presumed success.

### Meeting ticket backlog (each ticket has explicit build and acceptance)

#### Thursday, November 12 — Foundation and baseline

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1112-D1-01 — Repository and shared API contract.** **Implementation:** Create monorepo, Python/TS formatting, CI, issue templates, typed transaction/import schemas and integration mock. **Acceptance:** Clean checkout installs; CI green; example request validated. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-02 — Synthetic two-persona dataset.** **Implementation:** Generate two months per persona with refunds, transfers, merchant aliases, duplicate files, incomplete account and 100+ rows. **Acceptance:** Golden cents totals independently documented. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-03 — CSV import and preview endpoint.** **Implementation:** Parse two explicit layouts, retain raw row IDs, handle dates and debit-credit sign conventions. **Acceptance:** Two fixtures import; bad rows are identified without silent loss. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-04 — PDF import and unsupported-file UX.** **Implementation:** Support one text PDF format, error on scanned PDFs; wire frontend file-preview component. **Acceptance:** PDF fixture exact; unsupported format shows clear warning. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D1-05 — Privacy and deletion vertical slice.** **Implementation:** Add local file-hash/provenance, no raw statement logs, delete-import endpoint and deletion confirmation UI. **Acceptance:** Deleted rows cannot be queried; privacy test passes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1112-D2-01 — SQLite schema and seed.** **Implementation:** Migrations for accounts/imports/transactions/aliases/corrections/conversations/insights/evidence. **Acceptance:** Seed command and foreign keys verified. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-02 — Monetary conventions and golden tests.** **Implementation:** Define integer cents, income/refund/transfer handling, periods and currencies. **Acceptance:** Ten edge cases have expected outputs. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-03 — Core spending tool endpoints.** **Implementation:** Implement merchant/category totals, count, average and net recorded cash flow. **Acceptance:** Exact cents match golden fixtures. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-04 — Tool schemas and evidence IDs.** **Implementation:** Pydantic schemas for get_transactions, merchant_summary, category_summary, explain_total. **Acceptance:** Invalid tool arguments rejected; evidence references resolve. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D2-05 — Financial overview frontend card.** **Implementation:** Build responsive spending summary and merchant table consuming real API. **Acceptance:** Displays totals and coverage, not mocked numbers. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1112-D3-01 — Colab hardware and training decision.** **Implementation:** Record nvidia-smi, VRAM, dependencies, Qwen3-1.7B revision/license and 4B feasibility. **Acceptance:** Reproducible hardware notebook and model decision record. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-02 — Benchmark set and leakage policy.** **Implementation:** Create held-out synthetic dialogue split by persona/scenario; label intents, tool calls, tone, grounding. **Acceptance:** At least 150 test cases; no train/test overlap. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-03 — Baseline SLM runtime.** **Implementation:** Run original model on local or Colab benchmark; record latency, invalid calls, tool choice. **Acceptance:** Baseline JSONL outputs and reproducible script. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-04 — Constrained tool-call parser.** **Implementation:** Implement model output schema, allowlist, argument validation, bounded retries and safe abstention. **Acceptance:** Malformed model outputs cannot execute tools. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D3-05 — Chat frontend first slice.** **Implementation:** Build chat composer, message states, tool activity and evidence-link placeholders. **Acceptance:** User can submit a question and see response/loading/error. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1112-D4-01 — Compass design system.** **Implementation:** Implement brand tokens, typography, spacing, dark/light contrast, accessible components. **Acceptance:** Tokens documented; contrast checked. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-02 — Navigation and import flow.** **Implementation:** Build routes, home, import and transaction review shell with fixture-backed data. **Acceptance:** Keyboard accessible and responsive. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-03 — Chat visual language.** **Implementation:** Create assistant/user messages, local-AI badge, evidence chips and tone selector. **Acceptance:** Chat shell supports mocked and real API states. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-04 — Wrapped story specification.** **Implementation:** Wireframe seven-card journey, chart encodings, empty states, interaction choreography. **Acceptance:** Storyboard approved with each card tied to source metric. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1112-D4-05 — End-to-end smoke harness.** **Implementation:** Set up Playwright or equivalent and screenshot baseline across import/home/chat. **Acceptance:** CI executes one navigable browser test. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Saturday, November 14 — First integrated vertical slice

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1114-D1-01 — Transaction review and correction UI.** **Implementation:** Implement editable merchant/category/date/amount preview and correction provenance. **Acceptance:** Corrected transaction changes aggregates after refresh. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D1-02 — Duplicate import detection.** **Implementation:** Detect identical file hashes and repeated rows; distinguish duplicates from legitimate repeats. **Acceptance:** No double count; user sees decision. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D1-03 — Integration test: upload to chart.** **Implementation:** Write browser/API test from CSV upload to merchant total display. **Acceptance:** Golden fixture visible on UI. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1114-D2-01 — Period comparison tools.** **Implementation:** Add compare_periods and category trend tools with missing-period warnings. **Acceptance:** Correct month delta and zero-denominator behavior. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D2-02 — Financial X-Ray panel.** **Implementation:** Implement evidence drilldown listing source transactions, exclusions and coverage. **Acceptance:** Every displayed total opens verifiable breakdown. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D2-03 — Tool-to-UI contract tests.** **Implementation:** Generate typed client and contract fixtures for frontends. **Acceptance:** No schema mismatch in CI. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1114-D3-01 — End-to-end tool conversation.** **Implementation:** Connect SLM -> approved tools -> grounded response -> chat UI. **Acceptance:** Three questions answered with correct tool calls. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D3-02 — Training data pipeline.** **Implementation:** Build SFT JSONL with tool traces, empathetic responses, uncertainty and tone variants. **Acceptance:** 500+ reviewed/generated examples; schema and leakage checks. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D3-03 — Chat safety UX.** **Implementation:** Implement invalid-tool, unavailable-data and uncertainty messages in frontend. **Acceptance:** UI does not fabricate answer when model fails. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1114-D4-01 — Home-to-Wrapped navigation.** **Implementation:** Build Wrapped entry, story progress, resume and empty-state components. **Acceptance:** Accessible on mobile and desktop. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D4-02 — Chart primitives.** **Implementation:** Implement reusable bar, heatmap, slope and guess-versus-actual components with accessible tables. **Acceptance:** Fixtures render correctly with no misleading axes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1114-D4-03 — Cross-team integrated demo.** **Implementation:** Own import -> correct -> chat -> X-Ray smoke run and defect list. **Acceptance:** All four flows demonstrated on one fixture. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Thursday, November 19 — All-team Wrapped build and fine-tuning

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1119-D1-01 — Wrapped data provenance API.** **Implementation:** Expose per-card evidence IDs, import coverage, filters and excluded transactions. **Acceptance:** Every story card can open source rows. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-02 — Merchant normalization and correction feedback.** **Implementation:** Support alias overrides and recomputation of summaries. **Acceptance:** Alias change updates story and audit trail. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-03 — Spending calendar data + UI.** **Implementation:** Implement daily buckets, refunds and calendar heatmap component. **Acceptance:** Correct date cells; screen-reader table available. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-04 — Data quality badges and coverage UX.** **Implementation:** Add account/date completeness indicators and explain missing imports. **Acceptance:** Incomplete data never labeled complete. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D1-05 — Wrapped contribution integration test.** **Implementation:** Add fixtures for top merchant and busiest day and browser test. **Acceptance:** Card values exactly match source data. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1119-D2-01 — Insight ranking and deduplication.** **Implementation:** Implement normalized ranking, eligibility, evidence thresholds and diversity rules. **Acceptance:** No repeated same-merchant cards or unsupported claims. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-02 — Guess the Damage engine and UI.** **Implementation:** Build estimate submission, absolute/relative error and animated reveal UI. **Acceptance:** $80 vs $143 yields $63; edge cases tested. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-03 — What If? tool and scenario widget.** **Implementation:** Implement k*average scenario with assumptions, editable input and disclaimer. **Acceptance:** Conditional values exact and transparent. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-04 — Money Awards generator.** **Implementation:** Implement deterministic award selection and award card UI. **Acceptance:** Award supported by named metrics and evidence. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D2-05 — Wrapped metrics tests.** **Implementation:** Golden tests for MoM, share, streak, ranking, refunds and chart scale. **Acceptance:** 100% of golden arithmetic cases pass. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1119-D3-01 — SFT/QLoRA training run.** **Implementation:** Train Qwen3-1.7B adapter in Colab with pinned config and checkpoints. **Acceptance:** Saved adapter, loss curve, GPU metadata, reproducible commands. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-02 — Tool and conversation specialization.** **Implementation:** Train on tool traces, corrections, nonjudgmental dialogue and context use. **Acceptance:** Held-out examples never included in training. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-03 — Model adapter inference service.** **Implementation:** Load tuned adapter and connect chat API, with explicit model identity. **Acceptance:** Model can answer on fixture and logs model version only. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-04 — SLM-generated Wrapped commentary.** **Implementation:** Generate grounded card narration and suggested follow-up from structured insight objects. **Acceptance:** No fabricated numbers in scripted cards. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D3-05 — Model-driven chat tone UI.** **Implementation:** Connect Gentle/Direct/Roast to constrained responses and frontend selection. **Acceptance:** Same facts in all tones; tone changes only style. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1119-D4-01 — Piggy bank HTML/CSS prototype.** **Implementation:** Create literal ceramic piggy bank with large feather wings and coin slot, not cartoon mascot. **Acceptance:** Review against user reference; reduced-motion supported. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-02 — Pig state machine and chat integration.** **Implementation:** Define idle/listening/thinking/reveal/supportive states and connect to chat lifecycle. **Acceptance:** No arbitrary model-generated code; states validated. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-03 — Wrapped seven-card flow.** **Implementation:** Assemble shared components into story progression, skip/revisit and drilldowns. **Acceptance:** All cards load from real API. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-04 — Confessional screen and context controls.** **Implementation:** Build optional user explanation input, consented memory control and follow-up UX. **Acceptance:** User can decline; explanation not treated as verified transaction fact. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1119-D4-05 — Cross-dev Wrapped integration.** **Implementation:** Merge Dev1 heatmap, Dev2 awards/guess, Dev3 narration and Dev4 flow. **Acceptance:** Single story renders correctly end-to-end. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Saturday, November 21 — Integrated beta

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1121-D1-01 — Statement formats and correction reliability.** **Implementation:** Add second PDF fixture/layout or robust explicit unsupported notice; reconcile edited imports. **Acceptance:** Supported formats pass and unsupported formats fail clearly. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D1-02 — Wrapped data coverage tests.** **Implementation:** Test missing months, duplicate rows, partial accounts and refunds across all cards. **Acceptance:** No false full-month claim. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D1-03 — Privacy settings UI contribution.** **Implementation:** Build export/delete local records screen with confirmation and no telemetry default. **Acceptance:** Deletion and export demonstrable. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1121-D2-01 — Financial X-Ray for every Wrapped card.** **Implementation:** Connect all cards and awards to drilldown, not just overview. **Acceptance:** Seven-card source inspection works. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D2-02 — Spending insights and trend charts.** **Implementation:** Implement month-over-month slope and cumulative spend with correct scale. **Acceptance:** Comparisons handle missing baseline. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D2-03 — Financial conversation regression.** **Implementation:** Test model calls against exact tool outputs and claim verifier. **Acceptance:** Unsupported numeric claims blocked. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1121-D3-01 — Tuned vs baseline interim evaluation.** **Implementation:** Run identical held-out cases for base and tuned model. **Acceptance:** Preliminary paired metrics and failure examples saved. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D3-02 — Confessional contextual memory.** **Implementation:** Use opt-in local user statements, separate from factual transaction data; support forgetting. **Acceptance:** No fabricated motives; opt-out honored. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D3-03 — Conversation-to-Wrapped integration.** **Implementation:** Enable SLM follow-up from story cards, clarifications and What If? tools. **Acceptance:** User can switch between card and chat without losing context. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1121-D4-01 — Pig integration and accessibility.** **Implementation:** Mount coded pig on chatbot, use semantic labels and static reduced-motion fallback. **Acceptance:** Works across viewport and state transitions. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D4-02 — Full Wrapped UI beta.** **Implementation:** Polish guessing, charts, awards, receipts and chat handoff. **Acceptance:** First-time user completes seven-card story. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1121-D4-03 — End-to-end beta test and triage.** **Implementation:** Run scripted upload -> correction -> chat -> Wrapped -> Confessional -> What If -> delete. **Acceptance:** Failures filed with severity and owner. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

#### Thursday, November 26 — Full-feature validation (Thanksgiving; async allowed)

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1126-D1-01 — Import and privacy robustness.** **Implementation:** Fuzz malformed CSV/PDF, malicious filenames, file size, duplicate detection and local logs. **Acceptance:** Security/privacy regression documented. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-02 — Data export and deletion verification.** **Implementation:** Ensure database, imports, conversation memory and caches obey delete behavior. **Acceptance:** No recoverable app-level records after deletion on test. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-03 — Cross-device setup and data UI.** **Implementation:** Document and test clean install; build import-format helper in UI. **Acceptance:** Supported laptop demo works without developer fixes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-04 — Wrapped coverage/error handling.** **Implementation:** Test and fix all incomplete-period and bad merchant scenarios. **Acceptance:** No misleading chart or false confidence. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D1-05 — Data quality benchmark and artifact.** **Implementation:** Compute parse accuracy, coverage, correction success on labeled synthetic corpus. **Acceptance:** Machine-readable benchmark and UI chart exported. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1126-D2-01 — Finance 100-case benchmark.** **Implementation:** Run exact money tests incl refunds/transfers/rounding and record results. **Acceptance:** Reproducible pass/fail table. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-02 — Grounding validator and claims UI.** **Implementation:** Show evidence for amounts and safe abstention for unsupported claims. **Acceptance:** Zero unsupported numeric claims in release suite. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-03 — Insights ranking ablation.** **Implementation:** Compare ranking with/without diversity and user relevance; generate charts. **Acceptance:** Document ranking sensitivity and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-04 — Scenario/award bug fixes.** **Implementation:** Fix edge cases and integrate missing source links. **Acceptance:** No P0/P1 finance issues. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D2-05 — Investor metrics dashboard component.** **Implementation:** Build small local demo page for benchmark scorecards and caveats. **Acceptance:** All numbers pulled from result JSON, not hardcoded. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1126-D3-01 — Final paired model benchmark.** **Implementation:** Run base vs tuned on fixed held-out cases; report tool exact match, groundedness, tone. **Acceptance:** JSONL, confidence intervals and error taxonomy. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-02 — Local quantization benchmark.** **Implementation:** Measure quantized model on actual available consumer device; memory, p50/p95 latency. **Acceptance:** Hardware specified and results reproducible. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-03 — Privacy/offline network test.** **Implementation:** Test no outbound inference or raw statement telemetry; document model-download exception. **Acceptance:** Offline after install works on target machine. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-04 — Failure repair and regression.** **Implementation:** Fix invalid tools, context overflow, hallucination and unsafe humor. **Acceptance:** No P0/P1 model issues. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D3-05 — SLM explanation UI improvement.** **Implementation:** Build model status, local-processing disclosure and uncertainty indicators. **Acceptance:** Users can tell when AI vs deterministic tool acts. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1126-D4-01 — Complete user-journey E2E tests.** **Implementation:** Automate import, correction, chat, Wrapped, X-Ray, What If, settings, deletion. **Acceptance:** Green on clean supported machine. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-02 — Accessible charts and responsive audit.** **Implementation:** Keyboard, labels, contrast, reduced motion, screen-reader alternatives. **Acceptance:** Documented WCAG-oriented checks. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-03 — Usability pilot.** **Implementation:** Run 3-5 consented fictional-data sessions and collect task, comfort, comprehension. **Acceptance:** Anonymized data and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-04 — Pig refinement and fallback.** **Implementation:** Refine realistic ceramic design, ensure it does not block chat. **Acceptance:** Approved appearance or neutral fallback. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1126-D4-05 — Product performance and onboarding.** **Implementation:** Optimize load, navigation, install, first-run demo; add helpful empty states. **Acceptance:** 10-minute scripted demo succeeds. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Full feature validation, but code remains open until Dec 1.

#### Saturday, November 28 — Coding, benchmarks, stretch improvements

##### Dev 1 — Data integrity + frontend analytics

- [ ] **CMP-1128-D1-01 — Import stretch: additional CSV format.** **Implementation:** Add a third supported mapping and UI format selector if P0/P1 cleared. **Acceptance:** Fixture import passes or ticket explicitly descoped. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D1-02 — Privacy adversarial check.** **Implementation:** Attempt logs/export/deletion and malicious import failures; patch defects. **Acceptance:** Signed privacy checklist and fixes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D1-03 — Wrapped integration polish.** **Implementation:** Fix heatmap labels, receipts navigation and source coverage regressions. **Acceptance:** No P0/P1 in owned cards. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 2 — Financial intelligence + interactive charts

- [ ] **CMP-1128-D2-01 — Benchmark robustness and CIs.** **Implementation:** Compute bootstrap CIs and confusion matrices for finance/tool metrics. **Acceptance:** Scripts and raw outputs reproducible. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D2-02 — Stretch: recurring subscription story.** **Implementation:** Add recurring merchant frequency story card and UI if core green. **Acceptance:** Card sourced and inspectable or descoped. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D2-03 — Final numerical audit.** **Implementation:** Audit every demo dollar and chart axis, patch defects. **Acceptance:** All demo values match golden fixtures. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 3 — SLM training + conversational UI

- [ ] **CMP-1128-D3-01 — Model ablation and uncertainty.** **Implementation:** Compare base/tuned and prompt-only baseline if time; error analysis and CI. **Acceptance:** Honest table with N and limitations. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D3-02 — Stretch: smarter follow-up suggestions.** **Implementation:** Add safe evidence-grounded next-question suggestions in chat. **Acceptance:** Suggestions execute valid tools only. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D3-03 — Model release hardening.** **Implementation:** Freeze adapter revision, test offline, error handling, and recoverability. **Acceptance:** No P0/P1 in model integration. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

##### Dev 4 — Experience orchestration + mascot + QA

- [ ] **CMP-1128-D4-01 — Stretch: polished story transitions.** **Implementation:** Add restrained transitions and keyboard/reduced-motion parity. **Acceptance:** No accessibility regressions. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D4-02 — Pilot and UX benchmark finalization.** **Implementation:** Run additional short fictional-data user sessions or complete pilot analysis. **Acceptance:** Task outcomes and judgment survey recorded. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

- [ ] **CMP-1128-D4-03 — Cross-platform smoke and mascot fallback.** **Implementation:** Fix responsive, browser and pig animation issues; rehearse complete flow. **Acceptance:** Supported device demo passes. **Required evidence:** PR + test result + screenshot/JSON artifact + reviewer sign-off.

**Meeting gate:** Review merged PRs, live demo, benchmarks and blocked issues.

### December 1–3: ACL-style paper — required for all four developers

These are **final-sprint obligations in addition to the 96 engineering tickets** (not squeezed into Meeting 6):

| Developer | Dec 1 (after freeze) | Dec 2 | Dec 3 submission responsibility |
|---|---|---|---|
| Dev 1 | Draft Data, preprocessing, provenance, privacy and ethics | Reproduce dataset tables, source coverage and limitations | Verify dataset and reproducibility appendix |
| Dev 2 | Draft financial tool methods, equations, evidence and ranking | Reproduce exact arithmetic and grounding tables/figures | Verify formulas and reported numbers |
| Dev 3 | Draft SLM model, QLoRA, baselines, experimental design | Reproduce paired model results, CIs, errors, hardware and limitations | Verify model/revision/config appendix |
| Dev 4 | Draft abstract, introduction, UX methodology, user study, related work | Assemble ACL LaTeX, screenshots, figures, references and discussion | Produce final PDF, demo package and submission checklist |

All four co-review Abstract, Conclusion, Limitations and Ethics. No invented empirical claims. Paper structure: Abstract, Introduction, Related Work, System, Dataset, Model Training, Experiments, Results, Ablations, Ethics, Limitations, Conclusion, References, Appendix. Use official ACL template if required by course; GitHub README equations use `$...$` and `$$...$$`.

### Traceability: complete product journeys and test owners

| README requirement | Owners (primary + integration) | Acceptance evidence |
|---|---|---|
| Local CSV/PDF import, corrections, duplicates | D1 + D4 + D2 | Golden fixtures, E2E import/edit and no double count |
| Local SQLite, coverage, privacy, deletion | D1 + D2 + D4 | Migrations, no raw logging, delete test, offline check |
| Specialized fine-tuned SLM and tool selection | D3 + D2 + D4 | Adapter checkpoint, baseline/tuned paired evaluation, tool schema tests |
| Chat, contextual follow-ups, tones, Confessional | D3 + D4 + D1 | Multi-turn E2E, memory opt-out, tone and no-shame review |
| X-Ray and deterministic financial calculations | D2 + D1 + D4 | All monetary claims link to source rows, 100-case tests |
| Money Wrapped: guessing, awards, four charts | **D1 + D2 + D3 + D4** | Seven-card story, evidence, accessible chart alternatives |
| What If? and Teach Me Why | D2 + D3 + D4 | Assumption-based tool response; financial concept Q&A benchmark |
| Flying ceramic piggy bank chatbot character | D4 + D3 | HTML/CSS/JS animation states, reduced-motion fallback |
| Consumer-local model, setup, speed | D3 + D4 + D1 | Quantized local inference, offline test, p50/p95 latency, RAM |
| Evaluation, investor evidence, paper | **All four** | Reproducible JSON metrics, CIs, UX study, ACL-style report |

**Explicit scope guard:** This is a functional research-grade local desktop/browser-on-localhost MVP, not a commercially certified bank app. Automatic bank sync, real SMS, native mobile deployment, commercial billing, voice, and full-scale consumer security review remain post-MVP. Do not claim an unimplemented stretch goal is complete.

### Benchmark calendar and investor-ready metrics

**Nov 11–12: baseline.** Lock held-out synthetic benchmark and run untuned Qwen3-1.7B; label tool calls, grounded claims, conversation behavior and response times. Publish model revision and N. **Nov 19:** preliminary tuned checkpoint and smoke metrics. **Nov 21:** paired interim model and complete journey beta. **Nov 23–26:** final fixed-set tests, local hardware profiling, privacy, import and human UX pilot. **Nov 28:** robustness/ablation, confidence intervals, follow-up user testing, no data leakage. **Nov 30:** regenerate final reproducible benchmark report. **Dec 1–3:** freeze and write measured results.

| Metric | Definition and reporting | Investor significance | Suggested gate (not a claim) |
|---|---|---|---|
| Exact financial arithmetic | `correct golden cases / total golden cases`; 100+ cases | Trust | 100% |
| Tool selection accuracy | Correct tool / labeled query, with tool-argument exact match separately | Model utility | ≥90% tool; ≥85% arguments |
| Grounded numerical claims | Supported numeric claims / all numeric claims; also count critical invented amounts | Safety | 100% in release suite; zero critical fabricated amounts |
| Nonjudgmental response rate | Blind human rubric, 2+ raters, N, mean and inter-rater agreement | Emotional differentiation | ≥90% acceptable; report agreement |
| Multi-turn task success | Completed user goals / labeled multi-turn scenarios | Conversation usefulness | ≥80% |
| Import precision/recall | Correctly extracted rows and required fields vs labeled fixtures; coverage separate | Reliability | ≥98% on supported fixtures |
| Offline/local privacy | Network egress audit and deletion verification on test machine | Privacy claim | Zero inference payload egress; deletion pass |
| Device performance | Cold start, peak RAM, median/p95 first-token latency, tokens/s, model disk size | Consumer viability | Measure, then set supported-device target |
| UX comprehension | Correct responses to questions after dashboard vs static Wrapped vs interactive Compass | Product advantage | Report group sizes, effect and CI, no assumed lift |
| Perceived judgment | 1–5 user questionnaire and comments, comparative where possible | Nonjudgmental positioning | Report raw distribution, not just average |
| Activation / completion | Users reaching first evidenced insight and completing Wrapped / starters | Product engagement | Report measured funnel; avoid investor forecasts |
| Willingness to pay | Actual choices or stated intent clearly distinguished | Pricing validation | No revenue claims without real test |

**Model comparisons:** A) base Qwen3-1.7B with same tools/prompts; B) tuned Qwen3-1.7B with same tools/prompts; optional C) prompt-engineered base model; optional D) Qwen3-4B if hardware permits. Keep test set, inference settings, prompts and tool access matched. For binary paired outcomes use paired bootstrap 95% CI (and McNemar when appropriate); for UX outcomes report N, descriptive stats, uncertainty and limitations. Avoid statistical significance claims from a tiny convenience sample.

**Benchmark sources:** Primarily **CompassBench**, an explicitly named *team-created synthetic benchmark*, not a published standard. Supplement with publicly licensed financial QA datasets (e.g. FinQA for arithmetic/reasoning, ConvFinQA for conversational finance) only as out-of-domain checks: they emphasize financial-report reasoning, not bank-statement conversations. Evaluate licensing, leakage and task mismatch before use. For tool calling, consider BFCL-style methodology as an external reference, not as proof that the full benchmark applies to Compass. Document exact benchmark versions, sources and sample sizes.

### Quality-control audit of the previous 91 tickets

The previous file contained exactly **91** tickets: 20/12/20/11/20/8 across the six meetings. Its strengths were synthetic-data privacy, deterministic money calculations, SLM tool schemas, fine-tuning, and end-to-end acceptance. Its weaknesses were Dev 4 frontend bottleneck, no even Saturday workload, late all-team Wrapped integration, Nov 26 premature feature freeze, Nov 28 report-only work, and large non-atomic tasks such as “finish all core user journeys.” This revised 96-ticket schedule fixes allocation and traceability, but **cannot prove correctness before implementation**. Check correctness with unit/contract/E2E tests, benchmark artifacts, cross-owner code reviews, accessibility checks, privacy/offline checks and an explicit pass/fail release checklist. Count is a planning metric, not a quality metric.



## G12. Completeness assurance and release evidence ledger (authoritative supplement)

**Status as of November 10, 2026: PLANNED / NOT YET VERIFIED.** This section is an acceptance framework, not a claim that the application has been built or tested. It supplements G7 and G9; where older G7a or generic four-week language conflicts with G7, the dated G7 schedule governs. Every proposed result below is a target until a real CI run, reviewer, and timestamped artifact establish it.

### G12.1 Scope contract: what constitutes a complete Compass MVP

**In scope:** a localhost-accessible, local-first research MVP with supported CSV and text-based PDF import; normalized editable transaction records; deterministic source-backed financial tools; specialized tuned SLM with guarded tool calls; everyday chat; seven-card Money Wrapped with guessing, awards, charts, receipts and Confessional; conditional What If?; financial education; accessible responsive interface; privacy/deletion/offline validation; reproducible comparative benchmarks; ACL-style paper. A feature counts only when the user can complete its journey on a fresh checkout using documented fixtures, without manual database edits or mock-only responses.

**Out of scope:** live bank connections, production authentication/billing, native mobile, SMS/RCS, financial advice or money movement, OCR for scanned PDFs unless explicitly supported, commercial certification, statistically established market traction. An excluded capability must not appear as an implemented promise in demo, paper, or pitch.

**Definition of complete:** (1) all P0 requirements pass their specified automated and manual checks; (2) all supported journeys pass end to end; (3) all numerical outputs have deterministic provenance; (4) tuned model and evaluation artifacts are reproducible; (5) privacy and deletion claims pass observable tests; (6) no open P0/P1 issues; (7) all 96 tickets are closed with evidence or formally marked deferred with an explicit resulting scope reduction; (8) every claim in README/demo/paper is classified as implemented, measured, proposed, or excluded. Ticket closure alone is insufficient.

### G12.2 Requirement-to-ticket coverage index

This index links existing ticket titles to requirements using a **keyword-based candidate mapping**, not a reviewed assertion that each ticket fully implements that requirement. The feature owner must inspect implementation and fill in `verified PR / test ID / result / reviewer` before changing a requirement to PASS. A ticket can contribute to several requirements, but cannot substitute for missing integration evidence.

| ID | Product requirement | Candidate existing ticket IDs | Verification status |
|---|---|---|---|
| REQ-01 | Supported CSV/PDF import and rejection | `CMP-1112-D1-03`, `CMP-1112-D1-04`, `CMP-1112-D4-02`, `CMP-1114-D1-02`, `CMP-1126-D1-01`, `CMP-1128-D1-01` | NOT VERIFIED |
| REQ-02 | Transaction correctness and editing | `CMP-1112-D2-01`, `CMP-1114-D1-01`, `CMP-1114-D1-02`, `CMP-1119-D1-02`, `CMP-1119-D1-04`, `CMP-1121-D1-01`, `CMP-1121-D1-02`, `CMP-1126-D1-04` | NOT VERIFIED |
| REQ-03 | Privacy, local operation and deletion | `CMP-1112-D1-05`, `CMP-1121-D1-03`, `CMP-1126-D1-01`, `CMP-1126-D1-02`, `CMP-1126-D3-02`, `CMP-1126-D3-03`, `CMP-1128-D1-02` | NOT VERIFIED |
| REQ-04 | Financial tools and source-backed X-Ray | `CMP-1112-D2-03`, `CMP-1112-D2-04`, `CMP-1112-D2-05`, `CMP-1112-D3-04`, `CMP-1114-D2-01`, `CMP-1114-D2-02`, `CMP-1114-D2-03`, `CMP-1114-D3-01`, `CMP-1119-D1-01`, `CMP-1119-D2-03`, `CMP-1119-D3-02`, `CMP-1121-D2-01` (+1 additional candidates) | NOT VERIFIED |
| REQ-05 | SLM specialization and constrained orchestration | `CMP-1112-D2-03`, `CMP-1112-D2-04`, `CMP-1112-D3-01`, `CMP-1112-D3-03`, `CMP-1112-D3-04`, `CMP-1114-D2-01`, `CMP-1114-D2-03`, `CMP-1114-D3-01`, `CMP-1114-D3-02`, `CMP-1119-D2-03`, `CMP-1119-D3-01`, `CMP-1119-D3-02` (+7 additional candidates) | NOT VERIFIED |
| REQ-06 | Everyday conversational experience | `CMP-1112-D3-05`, `CMP-1112-D4-03`, `CMP-1114-D3-01`, `CMP-1114-D3-03`, `CMP-1119-D3-02`, `CMP-1119-D3-05`, `CMP-1119-D4-02`, `CMP-1119-D4-04`, `CMP-1121-D2-03`, `CMP-1121-D3-02`, `CMP-1121-D3-03`, `CMP-1126-D2-02` | NOT VERIFIED |
| REQ-07 | Money Wrapped story and guessing | `CMP-1112-D2-05`, `CMP-1112-D4-04`, `CMP-1114-D4-01`, `CMP-1119-D1-01`, `CMP-1119-D1-05`, `CMP-1119-D2-02`, `CMP-1119-D2-05`, `CMP-1119-D3-04`, `CMP-1119-D4-03`, `CMP-1119-D4-05`, `CMP-1121-D1-02`, `CMP-1121-D2-01` (+6 additional candidates) | NOT VERIFIED |
| REQ-08 | Awards, charts and insight ranking | `CMP-1114-D1-03`, `CMP-1114-D4-02`, `CMP-1119-D1-03`, `CMP-1119-D2-01`, `CMP-1119-D2-04`, `CMP-1119-D2-05`, `CMP-1121-D2-02`, `CMP-1126-D2-03`, `CMP-1126-D2-04`, `CMP-1126-D2-05`, `CMP-1126-D4-02` | NOT VERIFIED |
| REQ-09 | What If? and financial education | `CMP-1119-D2-03`, `CMP-1126-D2-04` | NOT VERIFIED |
| REQ-10 | Accessible, distinctive interface | `CMP-1112-D2-05`, `CMP-1112-D3-05`, `CMP-1112-D4-01`, `CMP-1112-D4-02`, `CMP-1114-D1-01`, `CMP-1114-D2-03`, `CMP-1114-D4-01`, `CMP-1119-D1-03`, `CMP-1119-D2-02`, `CMP-1119-D3-05`, `CMP-1119-D4-01`, `CMP-1119-D4-02` (+8 additional candidates) | NOT VERIFIED |
| REQ-11 | End-to-end reliability and release | `CMP-1112-D2-02`, `CMP-1112-D2-05`, `CMP-1112-D3-01`, `CMP-1112-D3-02`, `CMP-1112-D4-04`, `CMP-1114-D1-03`, `CMP-1114-D2-02`, `CMP-1114-D2-03`, `CMP-1119-D1-05`, `CMP-1119-D2-05`, `CMP-1119-D3-02`, `CMP-1119-D4-02` (+18 additional candidates) | NOT VERIFIED |
| REQ-12 | Evaluation and ACL evidence | `CMP-1112-D3-02`, `CMP-1121-D3-01`, `CMP-1126-D1-05`, `CMP-1126-D2-01`, `CMP-1126-D2-03`, `CMP-1126-D3-01`, `CMP-1126-D3-02`, `CMP-1126-D4-03`, `CMP-1128-D2-01`, `CMP-1128-D3-01`, `CMP-1128-D4-02` | NOT VERIFIED |

**Mandatory review of candidate links:** the lead and a different developer must read each referenced ticket's implementation and acceptance, not merely its title. Replace candidates with exact requirement-to-PR-to-test links in the live tracker. If a requirement lacks a passing test, it is uncovered even if its candidate list is long.

### G12.3 Contract-level acceptance matrix: proof needed, not just ticket completion

| Requirement | Required deterministic / automated proof | Required user-level or adversarial proof | Release decision |
|---|---|---|---|
| REQ-01 | Golden CSV and supported text-PDF row/field oracle; unsupported format error test; source row IDs | Import two layouts and one rejected PDF; no silent row drops | P0 if incorrect totals or silent corruption |
| REQ-02 | Golden cents/refund/transfer/dedup/correction tests; idempotent reimport; migration roundtrip | Correct a category and see every downstream number update | P0 if duplicate-count or corrupted money |
| REQ-03 | Offline network egress capture, local data location, deletion/restart test, log secret scan | Disconnect network, ask a question, delete data, restart, verify absence | P0 if unexpected sensitive egress or retained deleted records |
| REQ-04 | Decimal/integer-cent oracle, invalid arguments, evidence-ID integrity, zero denominator | Click a numerical claim and reconcile all displayed source transactions | P0 if fabricated amount or inconsistent sums |
| REQ-05 | Pinned model/adapter hash, training manifest, held-out split audit, base-vs-tuned paired run | Ambiguous and malicious prompts must not bypass tool allowlist | P1 if tuned model missing; P0 if fabricated money reaches user |
| REQ-06 | Multi-turn state, abstention, tone boundaries, context reset, errors | Ask follow-up after a correction; switch tone without changing amounts | P1 if core chat cannot finish |
| REQ-07 | Seven-card schema validation, deterministic guess delta, evidence-linked story cards | Full guess → reveal → receipts → Confessional flow on fresh fixture | P1 if core story cannot finish |
| REQ-08 | Chart totals reconcile to underlying tool outputs; rank ties and sparse data | Compare charts/awards against receipts; accessible text equivalents | P1 for false visual numbers |
| REQ-09 | Scenario input validation, transparent assumptions, no real-world action execution | Compare baseline vs hypothetical, then return to unchanged actuals | P1 if scenarios mutate records |
| REQ-10 | Keyboard/axe-style audit, reduced-motion check, mobile-width browser suite | Screen-reader labels, tab sequence, responsive and animation-off walkthrough | P1 for blocked essential journey |
| REQ-11 | CI green from clean checkout; pinned dependencies; integration and smoke suites | Two reviewers independently run documented install and demo | P1 if clean install fails |
| REQ-12 | Locked split, benchmark JSON, denominators, CIs, reproducibility commands | Independent rerun and paper-to-artifact number check | P1 if results cannot be reproduced |

### G12.4 Mandatory cross-feature integration journeys

These are **additional release-level acceptance tests** to be implemented within the existing 96 tickets, not fictitious completed tickets. Name each Playwright/pytest test and link it to its CI artifact.

| Journey ID | Exact flow | Invariants / pass condition | Primary / independent reviewer |
|---|---|---|---|
| E2E-01 | Fresh install → import CSV → review → ask merchant total → X-Ray | Display, DB and evidence rows agree to the cent | D1 / D2 |
| E2E-02 | Import PDF → correct category → Wrapped → chart → chat | Correction propagates to every view; no stale cache | D1 / D4 |
| E2E-03 | Reimport same statement → refund/transfer → month comparison | No duplicate, transfer counted as configured, correct signs | D2 / D1 |
| E2E-04 | Missing month/account → Wrapped → ask comparison | Explicit coverage warning; no unsupported conclusion | D1 / D3 |
| E2E-05 | Guess → reveal → award → receipts → Confessional | Same deterministic numbers and source IDs across cards/chat | D2 / D3 |
| E2E-06 | Confessional → What If? → return to actuals | Hypothetical is labeled and cannot mutate actual records | D3 / D2 |
| E2E-07 | Gentle → Direct → Roast → opt out → restart | Style changes; evidence unchanged; opt-out respected | D3 / D4 |
| E2E-08 | Offline session → chat → delete all → restart | No sensitive payload egress; no recoverable app records in documented scope | D1 / D4 |
| E2E-09 | Keyboard-only → mobile width → reduced motion | All core controls usable, chart alternatives and pig fallback | D4 / D1 |
| E2E-10 | Base model vs tuned model → same held-out cases | Same tools/prompts/test cases; differences and errors saved | D3 / D2 |
| E2E-11 | Empty/partial data → unsupported PDF → malformed tool call | Graceful error/abstention; never invented transactions | D3 / D1 |
| E2E-12 | Clean clone → install → fixture → full demo → benchmark rerun | No private setup, missing file, hidden service or hard-coded demo response | D4 / D3 |

### G12.5 Ticket-level evidence manifest and enforcement

Every one of the 96 issue descriptions must contain these fields before the corresponding meeting: `Requirement IDs`, `Owner`, `Independent reviewer`, `Estimated hours`, `Actual hours`, `Dependency IDs`, `User-visible behavior`, `Input/output schema`, `Supported and unsupported cases`, `Fixture ID`, `Automated test ID`, `Manual/E2E test ID`, `PR/commit`, `CI run URL`, `Screenshot/log`, `Result (PASS/FAIL/BLOCKED/DEFERRED)`, `Last verified timestamp`, `Known limitations`. **No evidence link = NOT VERIFIED, not PASS.**

**PR gate:** tests pass; independent reviewer verifies at least one adversarial case; API/schema change is reflected in contracts; source IDs are preserved; no real financial data or secrets in logs; frontend states include loading/empty/error; documentation updated. For a model-only ticket, substitute saved eval outputs and a reproducible command for screenshots. For a UI-only ticket, require browser screenshots and a keyboard check.

**Effort fairness:** 24 tickets per developer is count parity, not workload parity. At kickoff assign estimates and dependency risk (1–3); report estimated and actual hours per developer at every meeting; rebalance implementation or pair reviews when projected hours differ by more than 15%, without silently changing acceptance criteria. Every developer must show frontend, non-frontend, test and integration contributions in the final contribution ledger.

### G12.6 Gate-by-gate completeness scorecard (fill with actual evidence)

| Gate | Must be demonstrable | Evidence to attach | Default status |
|---|---|---|---|
| Nov 12 / Meeting 1 | Contracts, supported import, exact totals, base SLM and chat shell | CI, golden fixture, baseline dataset/hash | PENDING |
| Nov 14 / Meeting 2 | Import → correct → ask → X-Ray | E2E-01 and E2E-03, source-ID audit | PENDING |
| Nov 19 / Meeting 3 | All four Wrapped contributions plus tuned checkpoint | Story integration PRs, adapter hash, dev-set comparison | PENDING |
| Nov 21 / Meeting 4 | Complete interactive beta and corrections reflected everywhere | E2E-02, 04–07 and browser videos | PENDING |
| Nov 26 / Meeting 5 | Feature-complete candidate and locked-set metrics | Benchmark JSON, privacy run, pilot notes, defect register | PENDING |
| Nov 28 / Meeting 6 | Coding/robustness fixes, ablations, full release candidate | E2E-08–12, stress logs, ablation tables | PENDING |
| Nov 30 | Clean-checkout independent regression and paper-ready artifacts | CI run, tagged candidate, frozen metrics manifest | PENDING |
| Dec 1 noon ET | Unanimous code-freeze approval; no open P0/P1 | Signed release checklist, hashes, defect report | PENDING |
| Dec 1–3 | ACL report with figures matching frozen outputs | PDF, paper-source links, reproducibility appendix | PENDING |

### G12.7 Quantitative coverage and honest claims

Report separately: `ticket completion = evidenced PASS tickets / 96`; `requirement coverage = requirements with mapped passing tests / 12`; `journey success = passing E2E journeys / 12`; `critical issue count = open P0 + P1`; `numerical correctness = passing supported golden cases / tested supported cases`; `grounding = verified numerical claims / checked numerical claims`; `model comparison = paired tuned minus baseline metric with uncertainty`; `privacy = named egress/deletion checks passed / attempted`; `cross-functional contribution = developers with frontend + backend/data/model + test evidence / 4`. Never combine these into an unexplained single “product completeness” percentage. Report denominators and exclusions.

**Release rules:** Any open P0/P1 or failed mandatory journey means NO-GO for a claim of complete MVP. A deferred core requirement requires an explicit narrower MVP statement and an updated pitch/demo/paper; it does not count as passed. Stretch features cannot compensate for missing core behavior. Small user pilots establish usability signals, not retention, product-market fit, willingness to pay, or investor traction. Proposed thresholds in G9 are hypotheses; if they are missed, report the actual result rather than changing the test after the fact.

### G12.8 Completeness audit procedure for December 1

1. Export all 96 issues and confirm 24 per developer, 20/12/20/12/20/12 per meeting, no duplicates and no unowned issues.
2. Inspect each ticket's actual code/test evidence and independently verify requirement mapping; candidate keyword links above are not accepted without review.
3. Execute all 12 E2E journeys on a clean checkout; save pass/fail, run time, fixture hash and screenshot/log.
4. Reconcile every numerical UI claim and chart against the deterministic transaction oracle; inspect refunds, transfers, missing periods and corrections.
5. Independently rerun base/tuned evaluation on the frozen holdout and confirm model/data hashes, denominators, uncertainty and failure categories.
6. Run offline, deletion, sensitive-log and malformed-input tests on documented target hardware; record limitations.
7. Confirm all four developers contributed code across frontend and non-frontend surfaces and peer-reviewed another domain.
8. Match every demo/pitch/README/paper feature claim to one of `IMPLEMENTED + VERIFIED`, `IMPLEMENTED + UNVERIFIED`, `PROPOSED`, or `OUT OF SCOPE`; only the first may be presented as working.
9. Obtain four sign-offs for the release ledger, tag commit/model/fixtures, and freeze at noon ET December 1; use December 1–3 for the ACL report.

**Known residual risk:** The backlog cannot guarantee all real-world statement formats, consumer-device configurations, security threats, or user outcomes. Evidence-based completeness is bounded by explicitly supported formats, fixtures, target devices and tests.

## G7a. Original four-week plan (superseded)

The earlier illustrative four-week plan is superseded by the date-specific 96-ticket schedule above. Use the schedule above as the single source of truth for deadlines, developer ownership, and release gates.

## G8. Academic evaluation — two complementary studies

### Study 1: Does fine-tuning improve the SLM?

Compare **untuned Qwen3-1.7B vs Compass-tuned Qwen3-1.7B** on held-out scenarios, same tools, same hardware and decoding settings. Optionally include Qwen3-4B as a capacity reference. Report tool-call accuracy, numerical grounding, unsupported-claim rate, conversational coherence, nonjudgmental human ratings, agency preservation, and latency/memory. Human raters should score blinded responses and record inter-rater agreement.

A proposed nonjudgmental score for human review is:

$$
J=0.30R+0.25A+0.20E+0.15U+0.10T
$$

where R = respectful language, A = autonomy preservation, E = contextual empathy, U = avoidance of unsupported assumptions, and T = appropriate tone; each is scaled 0–1. These weights are a starting rubric, **not validated science**. Keep factual correctness separate and mandatory.

### Study 2: Does the experience improve financial understanding?

Compare (1) conventional dashboard, (2) static Wrapped, (3) interactive Wrapped + tuned SLM, using equivalent synthetic financial data. Measure comprehension, delayed recall if feasible, engagement, judgment, intent to return, and spending-estimate calibration. Avoid claiming improved long-term financial behavior from a short usability study.

Guess error:

$$
G=|\widehat S-S|,\qquad G_{\%}=100\frac{|\widehat S-S|}{S}\quad(S>0)
$$

For repeated sessions, track whether normalized guess error decreases, controlling for changes in category and data difficulty. Use actual participant data only with informed consent and appropriate privacy procedures.


## G9. Explicit benchmark protocol and success gates

**Benchmark is not a single leaderboard.** Compass needs an **SLM benchmark**, a **financial reliability benchmark**, a **consumer-device benchmark**, and a **product-experience study**. All figures below are **proposed MVP targets**, not achieved results or industry standards.

| Evaluation | Baseline / comparator | Dataset / method | Proposed pass criterion |
|---|---|---|---|
| SLM specialization | Untuned Qwen3-1.7B vs Compass LoRA-tuned 1.7B; optional 4B reference | 200+ held-out synthetic, multi-turn conversations, separated by fictional user/profile and merchant pattern | Clear improvement in blinded nonjudgmental ratings without degrading grounding/tool use |
| Tool selection | Gold tool-call labels and arguments | 100+ intent cases, ambiguous cases included | ≥90% correct tool choice on supported intents; report argument exact match separately |
| Financial arithmetic | Deterministic Python `Decimal` / integer-cent oracle | 100+ unit fixtures plus edge cases: refunds, transfers, missing accounts, zero denominators | 100% exact arithmetic on supported fixtures |
| Numerical grounding | Verified transaction provenance | 100+ generated answers, every numerical claim checked | ≥99% grounded numerical claims; **zero fabricated transactions** in demo |
| Nonjudgmental dialogue | Blinded human evaluation, 2+ raters | 50+ scenarios including debt, shame, essentials and opt-outs | Mean ≥4/5; report inter-rater agreement and failure examples |
| Local feasibility | Quantized tuned model on actual target laptops | Cold start, warm latency, peak RAM, tokens/sec, offline test | Define hardware-specific target after Week 1 measurements; no untested universal speed claim |
| Product engagement | Dashboard vs static Wrapped vs interactive Compass | Same synthetic financial records, counterbalanced tasks | Report completion, comprehension, recall, perceived judgment, and confidence intervals; no guaranteed uplift |

**Data leakage controls:** train/dev/test split by *fictional persona and underlying transaction scenario*, not merely by paraphrase. Record model ID/revision, dataset version, LoRA configuration, seed, quantization, hardware, runtime, inference settings and evaluation scripts. Publish anonymized or synthetic examples only.

**Training schedule (authoritative accelerated calendar):** November 10–14 baseline, hardware feasibility, and locked evaluation split; November 16–19 synthetic training data, Colab QLoRA/LoRA run, and first checkpoint; November 20–21 interim paired comparison and integration; November 23–28 fixed-set evaluation, quantization/local feasibility, robustness and ablations; November 30 final reproducibility rerun; December 1 noon ET freeze and December 1–3 paper. The earlier four-week cadence is superseded. Free Colab GPU availability is variable; scope runs to checkpoint frequently. DPO is optional after a reliable SFT baseline, not a critical-path dependency.

## G10. Money Wrapped — chart and metric design system

**Rule: one chart = one human question = one surprising verified fact = one optional conversation.** Do not create decorative analytics for their own sake. Use accessible labels, plain-language captions, transaction counts, coverage warnings and Financial X-Ray links. Every graph is generated from deterministic calculations; the SLM writes the narrative and asks follow-ups.

| Visual | Human question | Core metric | Interactive reveal |
|---|---|---|---|
| **Ranked horizontal bars** | Where did my money actually go? | Merchant/category spend and share | Guess the top merchant before the bars reorder |
| **Calendar heatmap** | Which days got expensive? | Daily spend, purchase count | Tap a bright day to reveal purchases and context |
| **Slope chart** | What changed since last month? | Absolute and % category change | Drag a prediction for October, then reveal the actual line |
| **Cumulative line** | When did spending accelerate? | Running monthly total vs prior comparable period | Scrub through the month to find the turning point |
| **100% stacked bar** | What was my spending mix? | Category share of eligible expenses | Reveal a category's share and the underlying merchants |
| **Dot / lollipop plot** | Which habits are frequent vs expensive? | Purchase frequency and average ticket | Contrast '11 small visits' with '2 large purchases' |
| **Small multiples** | Did my patterns change across months? | Per-month normalized category or merchant spend | Flip between three months, highlighting one story at a time |
| **Guess vs actual dumbbell** | How well do I know my spending? | Estimate, actual and absolute error | The user places the first dot; actual appears afterward |

**Prefer** horizontal bars, heatmaps, slopes and dumbbells over pie charts, 3D graphics, gauges, or dense Sankey diagrams. Use percentages only with meaningful denominators; display dollars and number of purchases alongside ratios. Avoid shame-coded red/green for moral judgments. Reduced-motion and screen-reader equivalents are required.

### Wrapped metrics that are both useful and memorable

| Metric | Formula / operational definition | Possible story title | Caveat |
|---|---|---|---|
| Top merchant | `argmax_v spend(v, month)` | Your most loyal relationship | Exclude transfers; normalize aliases |
| Visit frequency | `count(eligible transactions at merchant)` | You went back HOW many times? | Purchases ≠ visits when split transactions |
| Average ticket | `merchant_spend / merchant_count` | Your usual order | Only if count > 0 |
| Category share | `category_spend / total_eligible_expenses` | Where the plot thickened | Warn on incomplete accounts |
| Month-on-month delta | `current - prior` | Biggest plot twist | Comparable coverage needed |
| Percent change | `100 * (current-prior)/prior` | The comeback / the escalation | Undefined when prior = 0 |
| Most expensive day | `argmax_day daily_eligible_spend` | The day that did the most | Could reflect rent/essentials; don't roast |
| Small-purchase accumulation | Sum/count of eligible purchases below user-defined threshold | The little things added up | Threshold is user-controlled, not universal |
| Recurring merchant cadence | Repeated merchant charges at similar intervals | The recurring character | Detect patterns; don't assume subscription |
| Guessing accuracy | `abs(guess-actual)` and `100*abs(guess-actual)/actual` | You were off by… | Relative error undefined at actual=0 |
| Spending concentration | `top_3_merchant_spend / total_eligible_spend` | Three names, one plot | Merchants may represent necessities |
| Spending variability | `std(daily_spend)` with zero-spend days included | Calm month or rollercoaster? | Contextualize with pay/rent dates |
| Conditional scenario | `avoided_count * observed_avg_ticket` | What if you skipped three? | A hypothetical, not promised savings |

**Narrative sequencing:** (1) *prediction* → (2) *dramatic reveal* → (3) *comparison* → (4) *contextual question* → (5) *receipt drawer* → (6) *user chooses interpretation* → (7) *optional What If?* → (8) *takeaway card*. The SLM must not invent motives or tell the user which spending was 'bad'.

**Example, fictional data:** 11 Taco Bell transactions total $143; user guesses $80. Reveal **$63 underestimation** and an average of **$13.00 per transaction**. Ask whether this spending felt worthwhile; show the 11 dated receipts. A conditional scenario of three fewer similar purchases is **$39.00**, not a guarantee. Offer 'Keep it', 'Explore alternatives', and 'Not enough context' as equally legitimate choices.

**Story ranking:** retain the existing evidence-aware score, but use diversity constraints (no repeated merchant in consecutive cards), sensitivity filters (no joking about medical, debt hardship or essentials), and user-goal relevance. Score emotional interest from *surprise and contrast*, never from inferred moral failure.

## G11. Relationship to Pranav's original model

**Pranav's Idea 1** was a bank-hosted assistant with a hosted LLM; **Idea 2** was a privacy-first local statement-chat application using PDF/OCR ingestion, normalization, SQLite, a local model (Ollama/llama.cpp), natural-language queries, deterministic Python/SQL calculations and a simple UI. **Compass is an evolution of Idea 2, not a wholly separate architecture.**

| Dimension | Pranav Idea 2 | Compass refinement |
|---|---|---|
| Privacy | Local processing and storage | Retained, with explicit offline tests and threat model |
| Data | Multi-bank PDFs, OCR and normalization | Retained; CSV-first MVP with supported PDFs and provenance |
| Database | SQLite | Retained; corrections, coverage and evidence IDs added |
| AI | Local model for statement Q&A | **Fine-tuned domain-specific SLM is the central conversation orchestrator** |
| Calculations | Python/SQL tools | Retained; exact arithmetic and evidence validator |
| UI | Functional statement-chat UI | Distinctive neo-editorial product, Wrapped, awards, guessing, Confessional |
| Evaluation | Accuracy and basic utility | Added SLM fine-tuning study, nonjudgmental ratings, consumer hardware and engagement study |
| Commercialization | Project prototype | Free/Story Pass/Plus, differentiated positioning, pricing validation |

**Similarity estimate:** Roughly **80–90% of the original technical foundation** is retained as a qualitative architecture comparison, **not a measured code-overlap percentage**. The major new contribution is specialized model training plus interaction design and research evaluation. Credit the original proposal explicitly in the team README.

# H. What's missing before Compass becomes an investable product?

We now have a coherent product concept, a distinctive visual direction, a credible technical architecture, and a four-week development plan.

But a successful class project and an investable consumer business are not the same thing.

## H1. Outstanding decisions

Product readiness checklist

0 of 12

Interview 10–15 students and young adults about financial avoidance, humor, and existing tools

Test the neo-editorial visual identity with target users

Validate whether people prefer guessing, Wrapped, awards, roasts, or conversational reflection

Test willingness to pay for Story Pass and Compass Plus

Verify Colab GPU/VRAM; benchmark Qwen3-1.7B, optionally Qwen3-4B, and set local consumer latency targets

Finalize supported CSV/PDF formats and benchmark fixtures

Specify transfer, refund, duplicate, missing-account, and correction rules

Define sensitive spending categories and humor boundaries

Complete a privacy threat model, including logs, backups, storage, and deletion

Finalize synthetic SFT data, held-out base-vs-tuned tests, human judgment rubric, and product-study baselines

Run comparative usability tests against conventional financial reports

Confirm team ownership, sprint capacity, and professor requirements

## H2. Key product risks and mitigations

| Risk                        | Why it matters                                       | Mitigation                                                             |
| --------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------- |
| Novelty wears off           | A funny first audit may not lead to retention        | Test repeated monthly usage and longitudinal comparisons               |
| Humor feels judgmental      | Users may avoid the app rather than engage           | User-selected tone, sensitive-category exclusions, clear opt-outs      |
| Statement import friction   | Manual uploads could prevent repeat usage            | Simplify imports, support corrections, and evaluate the workflow       |
| Incorrect financial results | Trust can be lost immediately                        | Deterministic arithmetic, evidence references, comprehensive tests     |
| Incomplete data             | Insights may misrepresent overall spending           | Coverage warnings, account selection, explicit uncertainty             |
| Local model performance     | Slow responses could undermine the experience        | Benchmark early, quantize, and test smaller models without silently using cloud inference     |
| Weak monetization           | Users may enjoy the product without paying           | Validate actual purchase behavior before implementing subscriptions    |
| Easy imitation              | Competitors could reproduce Wrapped-style interfaces | Build a recognizable brand, strong UX, and evidence of user preference |

## H3. What we should deliberately exclude from the MVP

We should not attempt automatic bank synchronization, payment initiation, lending recommendations, investment management, advanced tax advice, social financial rankings, or unrestricted AI-generated financial recommendations.

We should also avoid spending most of Sprint 2 on elaborate animations. The central interaction needs to work before we polish every transition.

## H4. What would make the investor case stronger?

The most convincing evidence would be a small, well-designed pilot demonstrating that users:

- Complete Compass audits more frequently than conventional spending reviews.
- Recall financial insights more accurately.
- Feel comfortable enough to discuss spending they might otherwise avoid.
- Return when a new month's data becomes available.
- Show actual willingness to pay for a premium experience.

We should also measure whether the application works accurately and efficiently on ordinary consumer hardware.

A compelling brand gets attention. Demonstrated behavior change and retention create a stronger business case.


## H5. Post-MVP stretch goals — ranked by value and feasibility

These are **not** part of the four-week acceptance criteria. Do not market them as shipped features or include them in Plus entitlements until implemented.

| Priority | Stretch goal | User value | Major implementation / privacy consideration |
|---|---|---|---|
| P1 | **Spotify Wrapped-style annual Money Wrapped** | Beautiful year-in-review, top merchants, habit arcs, awards, shareable cards | Need 12 months of comparable data; redaction before sharing |
| P1 | **Native texting interface (SMS/RCS)** | Ask Compass questions from Messages, receive optional check-ins | Third-party delivery necessarily exposes message content/metadata; explicit opt-in and privacy disclosure; carrier/API cost |
| P1 | **Mobile apps with on-device inference** | Mainstream consumer accessibility | Quantization, battery, thermal limits, secure mobile storage |
| P1 | **One-click desktop installation** | No Python, Ollama or terminal setup | Code signing, installers, model download, device compatibility |
| P1 | **Recurring monthly stories and personal callbacks** | Retention beyond a one-off novelty | Local scheduled processing; explicit notifications consent |
| P1 | **Accessibility and language support** | Wider audience | Screen-reader chart summaries, reduced motion, multilingual evaluation |
| P2 | **Optional bank sync** | Lower recurring import friction | Account aggregator and cloud/privacy trade-offs; clear opt-in |
| P2 | **Offline voice conversations** | More natural interaction | Local ASR/TTS models, microphone permissions, storage |
| P2 | **Multi-account and household views** | Better context | Consent boundaries; shared-device privacy |
| P2 | **Goal-aware What If? and forecasts** | Longitudinal decisions | Uncertainty bands, cash-flow assumptions, no guaranteed projections |
| P2 | **User-controlled long-term memory** | More personalized conversations | Local memory editor, deletion, opt-in, no hidden inference of motives |
| P2 | **Personalized story themes and visual skins** | Fun and paid differentiation | Keep financial data legible and evidence accessible |
| P2 | **Shareable privacy-safe Wrapped cards** | Organic growth | No raw amounts/merchant names unless user approves |
| P2 | **Preference optimization (DPO)** | Improve conversational tone | Human-labeled pairs; check for regression in factual correctness |
| P2 | **Secure multi-device sync** | Seamless continuity | End-to-end encryption, key management, recovery |
| P3 | **Community-created story packs** | New content without model retraining | Content moderation, consistent data schemas |
| P3 | **University financial-wellness offering** | Distribution and education | No identifiable student spending data to sponsors |
| P3 | **Explainable spending anomaly alerts** | Proactive value | False-positive management and non-alarmist language |
| P3 | **Personalized micro-lessons** | Financial literacy | Evidence-backed curricula and learning evaluation |

**Priority order after launch:** installation + mobile feasibility → recurring Wrapped → texting with explicit privacy trade-offs → optional import automation. A true offline-only promise is **incompatible with sending messages through an external SMS/RCS provider**; make this a separate opt-in mode, not a silent exception.

# Final investor pitch

compass.

# Your money has a story. Let's talk about it.

Financial technology has become very good at tracking money.\
\
&#x20;   But a perfectly accurate dashboard is useless if someone never wants to open it.\
\
&#x20;   Young adults don't necessarily need another lecture about spending responsibly. They need a way to understand their financial behavior that feels personal, approachable, and worth their attention.

Compass turns private financial records into interactive stories, surprising discoveries, candid conversations, and practical insights.\
\
&#x20;   It combines the excitement of a personalized Wrapped experience, the directness of a financial audit, and the reliability of deterministic calculations.\
\
&#x20;   Underneath the personality is a local-first architecture designed to keep users in control of their financial information.\
\
&#x20;   We begin with students and young adults, but our ambition is broader: make financial self-awareness something people genuinely want to experience.

# Good with numbers. Good with people.

A financial assistant with receipts, perspective, and a personality.

## Final product recommendation

I would commit to Compass as a conversational financial audit platform, with Money Wrapped as its signature experience and the original local statement-chat system as its technical foundation.

The strongest part of the concept is not the roast alone, or the guessing game alone. It's the complete experience: a user encounters a financial truth, understands it, responds to it, and decides what it means for their life.

For the four-week project, success means delivering that complete loop **powered by a demonstrably fine-tuned local SLM**, with reliable calculations, a consistent visual identity, and measured base-vs-tuned improvements or transparently reported limitations.

For the longer-term business, success means proving that people return to Compass not because they are forced to manage their finances, but because they are genuinely curious about what Compass will tell them next.

That's the product I'd build—and the proposition I'd take into user testing before making stronger investor claims.
---

## Quick-start development checklist

- [ ] Confirm Colab GPU type/VRAM with `!nvidia-smi` and record runtime limits.
- [ ] Record base-model license and permitted distribution terms.
- [ ] Benchmark Qwen3-1.7B before any fine-tuning.
- [ ] Define synthetic profiles, schema, privacy rules, and held-out evaluation split.
- [ ] Implement deterministic finance tools with provenance.
- [ ] Fine-tune a QLoRA/LoRA adapter in **Sprint 2, Week 3**.
- [ ] Compare base vs tuned model with blinded judgment review.
- [ ] Quantize/export and benchmark on ordinary consumer devices.
- [ ] Test offline operation, deletion, and unexpected outbound requests.
- [ ] Demonstrate the full Guess → Reveal → Confessional → Evidence → What If? loop.

**Status:** proposal and execution README; no training, security audit, model benchmark, or consumer deployment has yet been demonstrated by this document.
