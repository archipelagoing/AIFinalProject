# tests/python/test_no_floats.py
#
# Guard for CMP-1112-D2-02, step 5: fail the build if floats creep into the money path.
# Uses Python's own parser (ast), so comments and docstrings that MENTION floats are ignored.

import ast
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]          # repo root (tests/python/ -> up 2)
MONEY_FILES = ["compass/money.py", "compass/analytics.py"]
BANNED_CALLS = {"float", "round"}                     # round() = banker's rounding


def find_float_problems(source: str) -> list[str]:
    problems = []
    for node in ast.walk(ast.parse(source)):
        # float(...) or round(...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id in BANNED_CALLS:
            problems.append(f"line {node.lineno}: {node.func.id}() call")
        # a float literal such as 0.5 or 1e3
        if isinstance(node, ast.Constant) and type(node.value) is float:
            problems.append(f"line {node.lineno}: float literal {node.value!r}")
    return problems


@pytest.mark.parametrize("rel_path", MONEY_FILES)
def test_no_floats_in_money_code(rel_path):
    path = ROOT / rel_path
    if not path.exists():
        pytest.skip(f"{rel_path} not written yet")
    problems = find_float_problems(path.read_text())
    assert not problems, f"{rel_path} uses floats:\n" + "\n".join(problems)


def test_checker_catches_floats():
    # Proves the guard works, so a passing run actually means something.
    bad = "x = float('5.75')\ny = round(n)\nz = 0.1\n"
    assert len(find_float_problems(bad)) == 3
    good = "# 0.1 + 0.2 is not 0.3\nx = Decimal('0.1')\n"   # comments and strings are fine
    assert find_float_problems(good) == []