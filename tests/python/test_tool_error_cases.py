# tests/python/test_tool_error_cases.py
#
# Ticket CMP-1112-D2-04: every bad tool call in fixtures/tool_error_cases.json must produce
# EXACTLY the error envelope written next to it. That JSON file is the contract handed to
# Dev 4 (see docs/dev4_tool_errors_DRAFT.md); this test keeps code and contract in sync.
#
# HOW THIS FILE RELATES TO THE REPO
#   Goes to:   git_repo/tests/python/test_tool_error_cases.py (new file)
#   Reads:     git_repo/tests/python/fixtures/tool_error_cases.json (new; same folder as
#              ticket 1's golden_money.json and ticket 2's synthetic_oct.json)
#   Tests:     compass/tool_contracts.validate_call (no DB needed) and, for cases marked
#              "needs_db", compass/evidence.call_tool on the synthetic DB from seed_synthetic.py
#
# WHY "EXACT"
#   If someone changes a message or a loc, Dev 4's UI may break silently. An exact match
#   makes that change fail here first, so the fixture (and the hand-off doc) gets updated
#   on purpose. Note: "msg" texts inside details come from Pydantic, so a Pydantic upgrade
#   can change them - re-check the fixture after upgrading.
#
# HOW TO RUN
#   python -m pytest -v tests/python/test_tool_error_cases.py

import json
from pathlib import Path

import pytest

from compass.db import connect
from compass.evidence import call_tool
from compass.seed_synthetic import load_fixture, seed
from compass.tool_contracts import ERROR_CODES, validate_call

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "tool_error_cases.json"
# Found relative to this test file, so it works from any working directory:
#   tests/python/test_tool_error_cases.py -> tests/python/fixtures/tool_error_cases.json

CASES = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
# Loaded once at import time so parametrize can name each test after its case:
#   test_error_case[limit_float], test_error_case[unknown_tool], ...


@pytest.mark.parametrize("case", CASES, ids=[c["name"] for c in CASES])
def test_error_case(case, tmp_path):
    if case.get("needs_db"):
        # e.g. evidence_not_found: the args are valid, the failure comes from the database.
        con = connect(tmp_path / "compass_test.db")
        try:
            seed(con, load_fixture())
            got = call_tool(con, case["tool"], case["raw_json"])
        finally:
            con.close()
    else:
        got = validate_call(case["tool"], case["raw_json"])
    assert got == case["expected"]
    # Whole-dict equality: error code, tool, message and every detail must match.


def test_fixture_covers_every_error_code():
    assert {c["expected"]["error"] for c in CASES} == set(ERROR_CODES)
    # Each code Dev 4 must handle has at least one worked example.


def test_case_names_are_unique():
    names = [c["name"] for c in CASES]
    assert len(names) == len(set(names))
