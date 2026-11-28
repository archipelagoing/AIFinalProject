# tests/python/test_no_floats.py
#
# Guard for CMP-1112-D2-02, step 5: fail the build if floats creep into the money path.
# Uses Python's own parser (ast), so comments and docstrings that MENTION floats are ignored.
#
# HOW THIS FILE RELATES TO THE REPO
#   REPLACES:  git_repo/tests/python/test_no_floats.py (ticket 1's file - an EDIT, not a new file)
#   Change for CMP-1112-D2-04: two files added to MONEY_FILES (marked "ticket 3" below).
#   Nothing else in ticket 1's guard is changed, so ticket 1's tests behave exactly as before.
#   Why the new files belong here: tool_contracts.py defines every money field the model sees,
#   and evidence.py sums amounts for explain_total - a float in either would break
#   "money is never wrong" just as surely as one in money.py.

import ast
# Python's own source-code parser. ast.parse(text) -> a tree of every expression in the file.
# Example: ast.parse("x = 0.1") contains Constant(value=0.1), which we can detect by type.

from pathlib import Path
# Builds file paths that work on Windows and macOS/Linux alike.

import pytest

ROOT = Path(__file__).resolve().parents[2]          # repo root (tests/python/ -> up 2)
# parents[0] = tests/python, parents[1] = tests, parents[2] = repo root.

MONEY_FILES = [
    "compass/money.py",
    "compass/analytics.py",
    "compass/tool_contracts.py",   # ticket 3: schemas for every money field in tool args/results
    "compass/evidence.py",         # ticket 3: sums amounts for explain_total, builds results
    "compass/tools.py",            # ticket 3: public Python functions that return money results
]
# Each path is checked by test_no_floats_in_money_code below (one test per file).

BANNED_CALLS = {"float", "round"}                     # round() = banker's rounding
# float("5.75") -> binary float, may be inexact.  round(500.5) -> 500 (banker's), users expect 501.


def find_float_problems(source: str) -> list[str]:
    """Every float() / round() call and float literal in some Python source text.

        find_float_problems("x = 0.1")          -> ['line 1: float literal 0.1']
        find_float_problems("# 0.1 in a comment") -> []
    """
    problems = []
    for node in ast.walk(ast.parse(source)):
        # ast.walk visits every node in the tree, in no particular order.
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
    problems = find_float_problems(path.read_text(encoding="utf-8"))
    # encoding="utf-8" (ticket 3): the new files contain non-ASCII text in comments
    # (e.g. 'Café'); without it Windows reads with cp1252 and may fail to decode.
    assert not problems, f"{rel_path} uses floats:\n" + "\n".join(problems)


def test_checker_catches_floats():
    # Proves the guard works, so a passing run actually means something.
    bad = "x = float('5.75')\ny = round(n)\nz = 0.1\n"
    assert len(find_float_problems(bad)) == 3
    good = "# 0.1 + 0.2 is not 0.3\nx = Decimal('0.1')\n"   # comments and strings are fine
    assert find_float_problems(good) == []
