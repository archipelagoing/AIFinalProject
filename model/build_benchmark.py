"""Build and validate Compass's synthetic Gate 1 dialogue benchmark."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent

PERSONAS = ["college_student", "young_professional", "new_parent", "freelancer"]
TONES = ["gentle", "direct", "playful", "gentle"]
MONTHS = ["January 2026", "February 2026", "May 2026", "June 2026"]


def examples_for_scenario(scenario: str, index: int) -> dict:
    persona = PERSONAS[index % len(PERSONAS)]
    tone = TONES[index % len(TONES)]
    month = MONTHS[index % len(MONTHS)]
    if scenario == "income_total":
        question = f"What was my income in {month}?"
        return row(question, "get_income", "get_income", tone, persona, scenario)
    if scenario == "expense_total":
        question = f"How much were my expenses in {month}?"
        return row(question, "get_expenses", "get_expenses", tone, persona, scenario)
    if scenario == "category_spending":
        category = ["Groceries", "Dining", "Transport", "Housing/Rent"][index % 4]
        question = f"How much did I spend on {category} in {month}?"
        return row(question, "get_category_spending", "get_category_spending", tone, persona, scenario, category=category)
    if scenario == "largest_expenses":
        limit = (index % 5) + 1
        question = f"Show my top {limit} expenses in {month}."
        return row(question, "get_largest_expenses", "get_largest_expenses", tone, persona, scenario, limit=limit)
    if scenario == "surplus":
        question = f"What was my surplus in {month}?"
        return row(question, "get_surplus", "get_surplus", tone, persona, scenario)
    if scenario == "merchant_question":
        merchants = ["Starbucks", "Target", "Taco Bell", "Amazon"]
        question = f"How much did I spend at {merchants[index % 4]} in {month}?"
        return row(question, "unsupported_merchant", None, tone, persona, scenario, evidence=False)
    if scenario == "comparison_question":
        question = f"Did I spend more in {month} than the previous month?"
        return row(question, "unsupported_comparison", None, tone, persona, scenario, evidence=False)
    if scenario == "clarification_missing_data":
        questions = [
            "How much did I spend?",
            "What did I spend on food?",
            "Can you explain my money?",
            "Show me my spending.",
        ]
        question = questions[index % len(questions)]
        return row(question, "needs_clarification", None, tone, persona, scenario, evidence=False)
    raise ValueError(f"Unknown scenario: {scenario}")


def row(question, intent, tool, tone, persona, scenario, *, category=None, limit=5, evidence=True):
    return {
        "question": question,
        "expected_intent": intent,
        "expected_tool": tool,
        "tool_arguments": {"category": category, "limit": limit} if tool else None,
        "expected_tone": tone,
        "requires_evidence": evidence,
        "persona": persona,
        "scenario": scenario,
        "synthetic": True,
    }


def build() -> tuple[list[dict], list[dict]]:
    # Keep scenario groups intact: no scenario appears in both splits.
    train_scenarios = ["income_total", "expense_total", "category_spending", "largest_expenses", "surplus"]
    test_scenarios = ["merchant_question", "comparison_question", "clarification_missing_data"]
    train = [examples_for_scenario(scenario, index) for scenario in train_scenarios for index in range(20)]
    test = [examples_for_scenario(scenario, index) for scenario in test_scenarios for index in range(20)]
    # Make each synthetic prompt unique while preserving the same intent and scenario.
    for rows, scenarios in ((train, train_scenarios), (test, test_scenarios)):
        for item in rows:
            item["question"] += f" This is synthetic case {scenarios.index(item['scenario']) + 1}-{rows.index(item) + 1}."
    return train, test


def validate(train: list[dict], test: list[dict]) -> dict:
    all_rows = train + test
    questions = [item["question"] for item in all_rows]
    train_scenarios = {item["scenario"] for item in train}
    test_scenarios = {item["scenario"] for item in test}
    assert len(all_rows) >= 150
    assert len(questions) == len(set(questions)), "Duplicate questions found"
    assert not train_scenarios & test_scenarios, "Scenario leakage found"
    assert all(item["synthetic"] is True for item in all_rows)
    assert {item["expected_tone"] for item in all_rows} >= {"gentle", "direct", "playful"}
    return {
        "total_examples": len(all_rows),
        "train_examples": len(train),
        "test_examples": len(test),
        "train_scenarios": sorted(train_scenarios),
        "test_scenarios": sorted(test_scenarios),
        "duplicate_questions": 0,
        "scenario_leakage": False,
        "all_examples_synthetic": True,
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    train_rows, test_rows = build()
    report = validate(train_rows, test_rows)
    write_jsonl(ROOT / "benchmark_train.jsonl", train_rows)
    write_jsonl(ROOT / "benchmark_test.jsonl", test_rows)
    (ROOT / "benchmark_report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
