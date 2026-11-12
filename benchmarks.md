For Compass, I recommend 12 specific benchmarks, divided into four groups: financial accuracy, local SLM performance, personalized discovery, and real-user experience.

Because today is November 12 and nothing has shipped, these should be treated as proposed evaluation targets—not results. Your team has roughly 19 calendar days until the December 1 code freeze, so the benchmarks must be achievable, reproducible, and useful in your ACL-style report.

## 1. The 12 benchmarks I would actually use

| #  | Benchmark                      | Dataset / evaluation method                                                 | Pass target                                   |
| -- | ------------------------------ | --------------------------------------------------------------------------- | --------------------------------------------- |
| 1  | Financial calculation accuracy | 150 deterministic financial questions with independently calculated answers | 100%                                          |
| 2  | Statement import accuracy      | 10–15 supported CSV/text-PDF fixtures with labeled transactions             | ≥98% precision and recall                     |
| 3  | Tool selection accuracy        | 100 labeled user queries with expected tool names                           | ≥90%                                          |
| 4  | Tool argument accuracy         | Same queries, checking merchant, dates, categories and amounts              | ≥85% exact match                              |
| 5  | Numerical grounding            | 100 generated responses checked against tool outputs                        | 100% on release-critical cases                |
| 6  | Multi-turn task success        | 30 conversations, each 3–5 turns                                            | ≥80%                                          |
| 7  | Insight precision              | 50 surfaced insights independently verified against transactions            | ≥95%                                          |
| 8  | Pattern discovery recall       | 30 planted financial patterns in synthetic histories                        | ≥80%                                          |
| 9  | Recurring detection F1         | 100 labeled recurring and nonrecurring merchant patterns                    | ≥0.85                                         |
| 10 | Local inference performance    | 30 repeated queries on the target machine                                   | Report p50/p95 latency, RAM, tokens/sec       |
| 11 | Offline privacy verification   | Network-disabled end-to-end workflow and traffic monitoring                 | Zero unauthorized financial-data egress       |
| 12 | User discovery yield           | 5–8-person comparison against a conventional dashboard                      | Report validated discoveries per five minutes |

The first five are correctness-oriented. Benchmarks 7–9 test the differentiating insight engine. Benchmark 12 tests whether that differentiation is actually useful.

## 2. The three most important experimental comparisons

For your research paper, these are more valuable than simply reporting a model accuracy score.

Experiment A — Does fine-tuning help?

Model

Compare the same Qwen3-1.7B model before and after QLoRA fine-tuning.

| Baseline       | Base model + identical tools                          |
| -------------- | ----------------------------------------------------- |
| Treatment      | Fine-tuned model + identical tools                    |
| Primary metric | Tool selection accuracy                               |
| Secondary      | Argument accuracy, multi-turn success, hallucinations |

Success criterion: Meaningful improvement over baseline without reduced numerical reliability. Report actual percentage-point differences and paired uncertainty intervals.

Experiment B — Does proactive discovery help?

Product

Compare a reactive Compass experience with the revised proactive insight engine.

| Baseline       | Chat + standard financial dashboard                        |
| -------------- | ---------------------------------------------------------- |
| Treatment      | Proactive insight feed + guided audit                      |
| Primary metric | Validated discoveries per user                             |
| Secondary      | Time to first discovery, insight usefulness, comprehension |

Success criterion: At least one additional meaningful discovery per user in a five-minute session, as a provisional pilot threshold.

Experiment C — Is the financial intelligence reliable?

System

Compare deterministic ground truth against the complete financial reasoning pipeline.

| Reference      | Independently computed transaction totals            |
| -------------- | ---------------------------------------------------- |
| System         | Compass tool selection → execution → narrated answer |
| Primary metric | End-to-end numerical correctness                     |
| Secondary      | Evidence attribution, abstention, import coverage    |

Success criterion: No incorrect financial totals in the release-critical test suite.

## 3. Exact benchmark formulas

These are the definitions I would put into your evaluation scripts.

| Metric                  | Formula                                                               |
| ----------------------- | --------------------------------------------------------------------- |
| Financial accuracy      | Correct answers ÷ total evaluated questions                           |
| Tool selection accuracy | Correct tool choices ÷ total tool-selection cases                     |
| Argument exact match    | Calls with all required arguments correct ÷ evaluated calls           |
| Grounding rate          | Supported numerical claims ÷ all numerical claims                     |
| Insight precision       | Valid displayed insights ÷ all displayed insights                     |
| Discovery recall        | Seeded meaningful patterns discovered ÷ eligible seeded patterns      |
| Recurring F1            | \\(2PR/(P+R)\\)                                                       |
| Discovery yield         | Independently validated discoveries ÷ participants                    |
| Relative discovery lift | \\((Y\_{\text{revised}}-Y\_{\text{baseline}})/Y\_{\text{baseline}}\\) |
| p95 latency             | 95th percentile of end-to-end response times                          |

Also measure abstention correctness: whether Compass refuses to invent an answer when a statement is incomplete, a merchant cannot be resolved, or there is insufficient evidence. Include at least 20 such cases in the model evaluation.

## 4. The benchmark schedule I would use

1. Nov 12–14

   Build fixtures

   Create deterministic transaction datasets, expected outputs, labeled tool calls and a basic test runner. Run initial base-model benchmarks if the runtime is ready.
2. Nov 15–18

   First functional tests

   Test imports, arithmetic, transaction provenance and the first tool-calling pipeline. Begin fine-tuning. Establish the base-model comparison.
3. Nov 19–21

   Integration benchmarks

   Run model comparisons, insight precision, seeded-pattern recall and recurring detection. Test the full Wrapped and conversational workflow.
4. Nov 22–26

   Main evaluation

   Evaluate the integrated application against held-out cases. Conduct the small comparative usability study and record privacy, performance and grounding results.
5. Nov 27–30

   Final verification

   Fix failures, run ablations, repeat tests on the release candidate, and generate tables and figures for the report. Keep final held-out evaluation separate from development tuning.
6. Dec 1–3

   Submission

   Freeze code December 1 at noon ET. Finalize the ACL-style paper, reproducibility instructions, demo and limitations.

## 5. Which developer should own each benchmark?

| Developer | Benchmark ownership                                                                                  |
| --------- | ---------------------------------------------------------------------------------------------------- |
| Dev 1     | Statement import precision/recall, provenance, offline privacy                                       |
| Dev 2     | Financial arithmetic, insight precision, discovery recall, recurring F1                              |
| Dev 3     | Tool selection, argument accuracy, numerical grounding, multi-turn success, base-vs-tuned comparison |
| Dev 4     | Discovery-yield user study, response latency, Wrapped completion, end-to-end testing                 |

Each developer should produce a machine-readable results file and a concise evaluation table. Another developer should review the test fixtures or scoring logic to avoid evaluating their own implementation without independent verification.

## 6. The five metrics I would feature in your presentation

# 100%

Financial arithmetic

Release target

# ≥90%

Tool selection

Model target

# ≥95%

Insight precision

Discovery target

# ≥80%

Pattern recall

Discovery target

# +1 discovery per user

Target improvement over reactive Compass

Measured using independently validated discoveries during a five-minute session

These are targets to test, not numbers to put on a results slide until you have collected evidence.

For the paper, I would also report 95% confidence intervals where appropriate, the number of test cases, failure examples, and results for both the base and fine-tuned models. With only 5–8 usability participants, present discovery-yield findings as preliminary rather than conclusive.

My strongest recommendation: Build one versioned benchmark package, `CompassBench v1`, by November 14. It should contain the financial ground truth, tool-calling cases, seeded behavioral patterns, and evaluation scripts. Keep a held-out split that developers do not train or tune against.

This gives your four developers a common definition of success from the beginning—and gives your final research paper measurable evidence rather than just screenshots of a working app.

inQA, ConvFinQA, and FinanceBench are three established benchmarks worth considering for Compass.

The important distinction is that they test financial reasoning and question-answering—not whether Compass can accurately import bank statements or create interesting Financial Wrapped stories.
Benchmark	What it tests	Fit for Compass
FinQA	Financial calculations from financial reports	Excellent for numerical reasoning
ConvFinQA	Multi-turn financial questions requiring calculations	Excellent for conversational reasoning
FinanceBench	Financial question-answering with supporting evidence	Excellent for grounding and hallucination testing
BFCL	Whether an AI selects and calls functions correctly	Excellent for Compass's tool-calling SLM

I would use FinQA + ConvFinQA + BFCL, then add a small Compass-specific test set for real bank transactions and personalized insights.
Which should you actually use?
Priority	Benchmark	When
1	ConvFinQA	Nov 14 baseline; Nov 26 final
2	BFCL (relevant tool-calling subset)	Nov 14 baseline; Nov 26 final
3	FinQA	Nov 21 and Nov 26
Optional	FinanceBench	Only if report-based financial Q&A is in scope

Useful sources: ConvFinQA dataset · FinQA dataset · BFCL leaderboard · FinanceBench overview. BFCL specifically tests function selection and arguments, including multi-turn calls. 
Proceedings of Machine Learning Research+1


One important caveat: FinQA and ConvFinQA focus on corporate financial reports, while Compass analyzes personal transactions. Their scores will demonstrate transferable reasoning ability, not prove that Compass works on bank statements.

For that reason, I'd use three established benchmarks plus CompassBench, your own small test set of transaction questions, recurring patterns, and grounded discoveries.

That gives your paper both recognizable academic benchmarks and evidence that the actual product works.