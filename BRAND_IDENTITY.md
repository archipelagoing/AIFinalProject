# compass. — Brand identity for Alpha 0.2

**Status:** proposed implementation contract, 2026-11-10. The current app and Pages demo retain their earlier styling. Dev 4 owns application in Week 1; all developers use this guide for user-facing copy. This document edits the brand direction; it does not claim a completed redesign or validated audience preference.

## Identity and promise

**Wordmark:** `compass.` — lowercase, with its period. Use “Compass” in ordinary prose and accessibility names where natural. The period is punctuation and a repeatable graphic cue, never the only indicator of status.

**Primary line:** Most financial apps show you what you spent. Compass makes you want to find out.

**Enduring line:** Good with numbers. Good with people.

**Campaign line:** Your bank statement has receipts. Compass has commentary.

**Closing line:** Your money has a story. Let's talk about it.

The tone combines an independent youth editorial brand with the care of a financial tool. Humor is optional; precision and respect are always present. Avoid babyish gamification, casino effects, shame, streak pressure, and claims that participation makes someone financially responsible.

## Three modes, one system

| Mode | Treatment | Rules |
| --- | --- | --- |
| Everyday Compass | Paper canvas, Ink text, generous spacing, restrained Iris accents | Import, home, review and chat stay calm; errors offer a recovery action |
| Money Wrapped | Larger type, Pool/Guava/Voltage panels, cut-paper shapes and small annotations | Facts remain labeled; every card has receipts and skip controls; motion is optional |
| Financial X-Ray | Plain surfaces, tabular numerals, explicit definitions, structured rows | No jokes in calculations, exclusions, provenance, warnings or deletion confirmation |

The mascot is a tiny compass needle used as a commentator. Use an existing icon or a simple code-native needle treatment initially; a full character/animation system is deferred. Product navigation and controls must work without the mascot.

## Color tokens and readable combinations

| Token | Hex | Use |
| --- | --- | --- |
| Paper | `#F5F1E8` | Primary background and quiet panels |
| Ink | `#17171B` | Main text, borders, calculation text |
| Voltage | `#D9FF43` | Selected actions, reveal accents; sparingly |
| Iris | `#8755E8` | Brand accent, primary action fill |
| Pool | `#82DDE5` | Supporting story panels |
| Guava | `#FF806D` | Playful panels; not a semantic error color |
| White | `#FFFFFF` | Utility label color on Iris |

Calculated opaque sRGB contrast ratios:

| Text / background | Ratio | Alpha rule |
| --- | ---: | --- |
| Ink / Paper | 15.86:1 | Body, labels, evidence |
| Ink / Voltage | 15.61:1 | Reveal/action labels |
| Ink / Pool | 11.43:1 | Story text |
| Ink / Guava | 7.29:1 | Story text |
| White / Iris | 4.67:1 | Normal button labels; no opacity reduction |
| Ink / Iris | 3.83:1 | Avoid normal-sized text |
| Paper / Iris | 4.14:1 | Avoid normal-sized text |

Use a minimum design target of 4.5:1 for normal text and 3:1 for large text and visible control boundaries. These pair calculations are not an accessibility audit. Check actual component size, weight, focus, hover, disabled states, transparency, and surrounding colors in the rendered UI. Iris on Paper is for large accents/decorations; use Ink for small links with an underline. A control with a pale fill needs an Ink boundary or another sufficiently visible edge.

Error/warning/success meanings require a literal label and icon, not color alone. Guava is not automatically an error, and green/Voltage is not automatically a positive financial outcome.

## Typography and layout

- Headlines: bold, confident grotesk/system sans, short lines; target 40–64px desktop and 28–40px small-screen hero text, with fluid sizing rather than fixed clipping.
- Body: readable system sans, approximately 16px with 1.5 line height; keep explanatory text to a comfortable measure.
- Financial values: tabular numerals; use a local monospaced fallback for formulas and source IDs. Display amounts with two decimal places and explicit signs/units.
- Start with local/system fonts. Do not add remote font requests. Any later bundled font needs its license recorded.
- Use a consistent 4/8px spacing rhythm. Cards should have a stable title, fact, definition, coverage note, receipts action, and next/skip controls.
- At 390px, stack cards and actions. Evidence grids may scroll within their own container; the page must not overflow horizontally. Financial values and action labels must not be clipped.

## Voice and humor policy

The facts layer is immutable. Copy can surround a verified amount but cannot introduce an extra count, percentage, merchant, comparison, or explanation of motive.

| Surface | Example | Boundary |
| --- | --- | --- |
| Guess prompt | “What do you think you spent on restaurants in May?” | Identify period and net-spending definition before the guess |
| Reveal | “Recorded net restaurant spending: [verified amount].” | Show recorded/partial coverage and receipts |
| Gentle reaction | “A little different from your guess. Want to see the purchases?” | Only mention purchases if the insight has a validated expense-row count |
| Direct reaction | “That was [verified difference] above your estimate.” | Difference comes from code, not generated prose |
| Optional Roast | “You and takeout are getting pretty serious.” | Eligible discretionary topic and separate explicit opt-in |
| Reflection | “Was this convenience, social plans, a priority, or something else?” | User may disagree, skip, or give no context |
| Evidence | “[count] classified expense rows, less [refund amount] in refunds.” | Literal definitions, no punchline |

Off is the default. Gentle/Direct are explicit choices; Roast needs an additional affirmative control and can be disabled immediately. Never escalate tone after a user skips or expresses discomfort. No hardship, medical, rent, debt-distress or identity jokes. For Alpha, only a reviewed allowlist of discretionary category templates may receive playful reactions; unknown/custom categories receive neutral copy.

Context is a user statement, not proof of causation. Do not infer emotions, addiction, financial health, creditworthiness, income security, or protected traits from transactions. No “bad with money” labels, moral scores, leaderboards or achievement pressure for spending less. Awards must describe a measured pattern and can be dismissed.

## Interaction and motion

1. Show eligible month, topic and coverage before asking for a guess. No prior-total leak in the unrevealed card or its accessible label.
2. Accept a nonnegative exact-cent guess; distinguish empty, invalid, zero and unknown data.
3. Reveal on the user's action. Present the amount, signed/absolute difference and a receipts action together.
4. Respect reduced-motion preferences. No autoplay, flashing, timed input or required animation; a plain immediate reveal must work.
5. Preserve keyboard focus through reveal and modal close; announce the result once with an appropriate live region. Controls need visible focus and useful accessible names.
6. Keep skip, ordinary summary, tone-off and evidence available throughout. Do not gate financial tools behind game completion.

## Week 1 design deliverables and review

Dev 4 produces five lightweight annotated screen states: welcome/import, import/review, monthly home, Wrapped/reveal, and Confessional/X-Ray. They may use simple code mockups or sketches; a separate design-tool workflow is not a prerequisite. Each shows empty, missing-data, error and keyboard/focus states where applicable. Dev 1 reviews provenance/privacy text, Dev 2 reviews financial labels, and Dev 3 reviews tone boundaries.

Apply the first cohesive theme to the local Streamlit shell and first audit flow in Week 1. Keep unsupported deeper customization out of the critical path. Pages is a separate legacy demo; do not label its old appearance as the completed new brand.

**Done:** the five-state specification, actual token mapping, desktop/mobile screenshots, keyboard/reduced-motion checks, and shared copy review are linked from the implementation PR. Record outstanding accessibility findings instead of declaring the palette certified.
