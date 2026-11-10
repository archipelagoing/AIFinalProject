# compass.

> **Canonical product specification (November 10, 2026).** Engineering tickets, dates, meeting agendas, and test/evidence ledger are maintained separately in [COMPASS_ENGINEERING_PLAN.md](COMPASS_ENGINEERING_PLAN.md).

> **GitHub README math:** Equations use GitHub-supported `$...$` (inline) and `$$...$$` (display) LaTeX delimiters. Render this file in GitHub Markdown, not a plain-text preview.


Canonical product README · Product proposal A–H · SLM strategy · Brand system · See linked engineering plan

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

Compass takes its colors from the materials people associate with money: warm paper, layered banknote greens, copper, nickel, gold, and the piggy bank itself. These are **brand colors**, not claims about official currency-printing specifications; real banknotes vary by country, denomination, ink, age, and lighting.

| Token | Hex | Role |
| --- | --- | --- |
| Paper | `#F4F0E6` | Primary warm background |
| Treasury Cream | `#FFF9ED` | Raised cards and light surfaces |
| Ink | `#18231C` | Primary text and high-contrast data |
| Engraved Black | `#20251F` | Title ink and engraved-style illustration linework |
| Reverse Green | `#315942` | Greenback-inspired surfaces, primary actions, and navigation |
| Banknote Green | `#5F8F68` | Supporting data, progress, and illustrations |
| Banknote Mint | `#C9D9BF` | Soft green surfaces and selected states |
| Serial Green | `#A7D48E` | Bright seal/serial-style detail on Engraved Black only |
| Purple Five | `#7A5B98` | Sparse denomination-inspired accents, badges, and achievement details |
| Penny Copper | `#B86B45` | Editorial warmth, callouts, and the pig's outline |
| Nickel Silver | `#AEB7B2` | Borders, inactive controls, and secondary UI |
| Coin Gold | `#C79A35` | Awards, achievement moments, and premium emphasis |
| Pig Pink | `#EBA3B5` | The mascot and playful moments only |
| Pig Rose Shadow | `#C9758B` | Pig shading and hover/pressed mascot states |
| Ledger Red | `#AE463F` | Errors and negative financial scenarios only |

**Usage rules.** Ink on Paper or Treasury Cream is the default reading pair. Reverse Green is the only saturated brand color intended for text and primary buttons. Engraved Black is a distinct front-of-note/title color; Serial Green may appear only as a high-contrast detail on Engraved Black, never as small text on Paper. Purple Five is deliberately sparse and does not carry status or error meaning. Banknote Green, Coin Gold, Copper, and Pig Pink are accents rather than body-text colors; their exact foreground/background pairings must pass WCAG contrast testing before implementation. Use Mint as a surface, not a text color. The pig must use two approved treatments: Pig Pink on a Reverse Green field (with Cream/Forest details), or Pig Rose Shadow with Copper linework on Paper/Cream. Do not use Pig Pink as small text or place it unoutlined on light paper. Ledger Red means an error, rejected/declined action, or destructive control—not ordinary overspending or a negative monthly total, which uses Copper.

### Typography

- Display: an engraved Roman-inspired serif stack (`Iowan Old Style`, `Palatino`, `Georgia`, serif) for page and card titles only. It references the hand-engraved lettering of U.S. notes without claiming to reproduce the note's custom lettering.
- Body: clean sans-serif typography for navigation and explanations.
- Numbers: tabular or monospaced numerals for totals, calculations, and comparisons.

### Brand mascot

**Primary mascot: a tiny flying piggy bank.** The pig should feel like a charming, slightly cheeky editorial character, not a generic cartoon banking logo. Its silhouette combines a rounded ceramic piggy-bank body, small wings, a coin slot, expressive eyes, and a minimal compass-star accent that ties it to the product name. An alternate static piggy-bank form works for compact UI placements.

**Mascot role:** The pig acts as a companion and guide—celebrating discoveries, reacting to surprising patterns, introducing Money Wrapped awards, and making difficult financial conversations feel less intimidating. It must never mock debt, poverty, income, or essential purchases. Its expression should change with the user's selected Gentle/Direct/Roast tone without changing factual content.

**Visual rules:** Distinctive simple silhouette, legible at favicon size, accessible contrast, no excessive infantilization, no clutter over financial charts. Use Pig Pink/Pig Rose Shadow with restrained Copper, Gold, or Reverse Green details; avoid implying the pig itself is an AI entity with independent financial authority.

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

# G. Technical implementation and formulas

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

## G7. Authoritative engineering delivery and verification

The **96 engineering issues, meeting-by-meeting schedule, test mapping, and release evidence ledger** live in [`COMPASS_ENGINEERING_PLAN.md`](COMPASS_ENGINEERING_PLAN.md). That document is the sole authority for issue assignments, deadlines, and release gates. This README is the sole authority for product scope, intended behavior, technical design, positioning, and proposed pricing. In case of disagreement, **do not silently choose**: open a scope-change issue and update both documents in the same reviewed PR. The engineering plan may not redefine the product without an approved README change.

**Status:** Proposed product and unverified implementation until linked test/CI evidence exists. The December 1 noon ET freeze and December 1–3 ACL report are binding planning targets, not claims of completion.

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

## Canonical document control

- **Product source of truth:** `README.md` (this document).
- **Delivery source of truth:** `COMPASS_ENGINEERING_PLAN.md` (96 issues, dates, acceptance evidence).
- **Machine-readable coverage:** `COMPASS_COVERAGE_MATRIX.csv` (candidate ticket associations requiring independent confirmation).
- **Pricing decision for this consolidated baseline:** Free $0; Plus $8.88/month or $88.88/year; Story Pass $1.50 one-time. These are proposed prices approved for consistency *within this document set*, not proof of willingness to pay or externally approved commercial pricing.
- **Change control:** any scope, price, interface, ticket, benchmark or schedule change requires a reviewed PR updating all affected files and a short decision log entry. Never edit a generated GitHub issue without syncing the plan or recording the deviation.
- **Conflict resolution:** user-facing behavior and scope follow README; delivery dates and ownership follow engineering plan; measured results follow CI artifacts, never prose assertions.
