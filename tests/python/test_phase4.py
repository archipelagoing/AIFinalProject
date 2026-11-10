"""Pure scenario contracts and rendered acceptance stories for Phase 4."""

from dataclasses import replace
from pathlib import Path

import pytest

from compass import analytics, db, importer, scenarios as s
from compass.contracts import TransactionType as Kind, parse_amount_cents

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def rows():
    conn = db.connect(":memory:")
    for filename in importer.DEMO_STATEMENTS:
        assert importer.import_statement(conn, (ROOT / "fixtures" / filename).read_bytes(), filename).ok
    result = db.list_transactions(conn)
    conn.close()
    return result


def inputs(**changes):
    values = dict(baseline_surplus_cents=74706, new_rent_cents=150000,
                  rent_mode="replace", existing_rent_cents=127500)
    return s.ScenarioInputs(**(values | changes))


@pytest.mark.parametrize("changes,projected,delta", [
    ({}, 52206, 22500),
    ({"rent_mode": "additional"}, -75294, 150000),
    ({"new_rent_cents": 100000}, 102206, -27500),
    ({"new_rent_cents": 127500}, 74706, 0),
    ({"new_rent_cents": 0}, 202206, -127500),
    ({"rent_mode": "additional", "new_rent_cents": 0, "existing_rent_cents": None}, 74706, 0),
    ({"added_spending_cents": 2500, "income_adjustment_cents": -10000}, 39706, 22500),
    ({"added_spending_cents": 1, "income_adjustment_cents": 2}, 52207, 22500),
])
def test_exact_scenario_formula(changes, projected, delta):
    result = s.calculate_scenario(inputs(**changes))
    assert result.projected_surplus_cents == projected
    assert result.rent_delta_cents == delta
    assert result.difference_from_baseline_cents == projected - 74706
    assert result.six_month_static_cents == 6 * projected
    assert result.cumulative_months == () and result.savings_target_gap_cents is None


@pytest.mark.parametrize("field,value", [
    ("new_rent_cents", -1), ("added_spending_cents", -1), ("existing_rent_cents", -1),
    ("rent_mode", "other"), ("existing_rent_cents", None),
    ("savings_target_cents", -1), ("starting_balance_cents", True),
    ("income_adjustment_cents", float("nan")), ("new_rent_cents", float("inf")),
    ("added_spending_cents", 0.1), ("baseline_surplus_cents", "74706"),
    ("new_rent_cents", True), ("existing_rent_cents", 127500.0),
    ("savings_target_cents", False), ("income_adjustment_cents", 2**63),
])
def test_input_types_and_ranges_are_strict(field, value):
    with pytest.raises(ValueError):
        inputs(**{field: value})


@pytest.mark.parametrize("text", ["NaN", "Infinity", "-inf", "", "1.001", "1,500", "$1500", "1e3"])
def test_ui_money_parser_rejects_nonfinite_ambiguous_or_fractional_cents(text):
    with pytest.raises(ValueError):
        parse_amount_cents(text)


@pytest.mark.parametrize("changes", [
    {"baseline_surplus_cents": 2**63 - 1, "rent_mode": "additional", "new_rent_cents": 0},
    {"baseline_surplus_cents": -(2**63), "income_adjustment_cents": -1},
    {"baseline_surplus_cents": 0, "new_rent_cents": 0, "existing_rent_cents": 0,
     "income_adjustment_cents": 1, "starting_balance_cents": 2**63 - 1},
    {"baseline_surplus_cents": -2, "new_rent_cents": 0, "existing_rent_cents": 0,
     "savings_target_cents": 2**63 - 1},
])
def test_result_overflows_are_rejected_before_rendering(changes):
    with pytest.raises(ValueError, match="64-bit"):
        s.calculate_scenario(inputs(**changes))


@pytest.mark.parametrize("target,gap", [(50000, 2206), (52206, 0), (60000, -7794)])
def test_savings_target_and_user_starting_value_are_exact(target, gap):
    result = s.calculate_scenario(inputs(savings_target_cents=target, starting_balance_cents=-10000))
    assert result.savings_target_gap_cents == gap
    assert len(result.cumulative_months) == 6
    for number, row in enumerate(result.cumulative_months, 1):
        assert row.month_number == number
        assert row.cumulative_change_cents == number * 52206
        assert row.starting_value_plus_change_cents == -10000 + number * 52206
    negative = s.calculate_scenario(inputs(rent_mode="additional", starting_balance_cents=100000))
    assert negative.cumulative_months[-1].starting_value_plus_change_cents == 100000 - 6 * 75294


def test_each_month_baseline_and_identified_rent_come_from_effective_analytics(rows):
    for month in sorted({row.posted_date[:7] for row in rows}):
        summary = analytics.summarize_month(rows, month)
        rent = s.identify_rent(summary.rows)
        assert rent.existing_rent_cents == 127500
        result = s.calculate_scenario(inputs(baseline_surplus_cents=summary.totals.surplus_cents,
                                            new_rent_cents=127500, existing_rent_cents=rent.existing_rent_cents))
        assert result.projected_surplus_cents == summary.totals.surplus_cents
        assert len(rent.candidates) == 1
        assert rent.candidates[0].effective_type == Kind.EXPENSE


def test_rent_detection_does_not_sum_housing_guess_missing_or_merge_multiple_charges(rows):
    rent = s.identify_rent(analytics.summarize_month(rows, "2026-05").rows).candidates[0]
    furniture = replace(rent, id="furniture", description="FURNITURE", amount_cents=-10000)
    assert s.identify_rent([rent, furniture]).existing_rent_cents == 127500
    assert s.identify_rent([furniture]).existing_rent_cents is None
    assert s.identify_rent([rent, replace(rent, id="second")]).existing_rent_cents is None
    assert len(s.identify_rent([rent, replace(rent, id="second")]).candidates) == 2
    assert not s.identify_rent([rent.with_classification("unknown", "Housing")]).candidates
    assert not s.identify_rent([rent.with_classification("expense", "Shopping")]).candidates
    for category in ["Rent", "Housing/Rent"]:
        assert s.identify_rent([furniture.with_classification("expense", category)]).existing_rent_cents == 10000
    refund = replace(rent, amount_cents=1000, predicted_type=Kind.REFUND)
    assert not s.identify_rent([refund]).candidates


def load_app(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "scenario.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    assert not app.exception and not any(item.label == "Projected monthly surplus" for item in app.metric)
    app.button(key="load_checking").click().run(timeout=30)
    app.button(key="load_savings").click().run(timeout=30)
    return app, path


def metric(app, label):
    assert not app.exception
    return next(item.value for item in app.metric if item.label == label)


def confirm_rent(app):
    return next(item for item in app.checkbox if item.label.startswith("I confirm this existing rent expense"))


def test_streamlit_may_replace_additional_and_complete_formula(monkeypatch, tmp_path):
    app, path = load_app(monkeypatch, tmp_path)
    assert metric(app, "Scenario baseline income") == metric(app, "Verified income") == "$3,700.00"
    assert metric(app, "Scenario baseline net expenses") == metric(app, "Net expenses") == "$2,952.94"
    assert metric(app, "Scenario baseline surplus") == metric(app, "Verified surplus") == "$747.06"
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$522.06"
    assert metric(app, "Six-month static extrapolation") == "$3,132.36"
    assert any("($747.06) + ($0.00) − ($0.00) − ($225.00) = $522.06" in item.value for item in app.markdown)
    assert any("Difference from baseline" in item.value and "−$225.00" in item.value for item in app.markdown)
    app.selectbox(key="scenario_mode").select("additional").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "−$752.94"
    assert any("Negative projected surplus" in item.value for item in app.warning)
    assert any("both costs count" in item.value for item in app.info)
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    app.text_input(key="scenario_new_rent").input("1000.00").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$1,022.06"
    app.text_input(key="scenario_income_adjustment").input("-100.01").run(timeout=30)
    app.text_input(key="scenario_added_spending").input("25.02").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$897.03"
    assert not app.error
    conn = db.connect(path)
    assert len(db.list_transactions(conn)) == 164
    assert all(not row.has_correction for row in db.list_transactions(conn))
    conn.close()


@pytest.mark.parametrize("key,value", [("scenario_new_rent", "NaN"), ("scenario_new_rent", "-1"),
                                      ("scenario_added_spending", "Infinity"), ("scenario_added_spending", "-0.01"),
                                      ("scenario_income_adjustment", "1.001")])
def test_streamlit_invalid_inputs_hide_old_result(monkeypatch, tmp_path, key, value):
    app, _ = load_app(monkeypatch, tmp_path)
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$522.06"
    app.text_input(key=key).input(value).run(timeout=30)
    assert not app.exception and any("Scenario input" in item.value for item in app.error)
    assert not any(item.label in {"Projected monthly surplus", "Six-month static extrapolation"} for item in app.metric)
    assert metric(app, "Scenario baseline surplus") == "$747.06"


def test_streamlit_ambiguous_rent_confirmation_and_context_reset(monkeypatch, tmp_path):
    app, path = load_app(monkeypatch, tmp_path)
    conn = db.connect(path)
    data = b"date,description,amount,account,transaction_id\n2026-05-03,SECOND RENT,-25.00,Checking,rent-two\n"
    assert importer.import_statement(conn, data, "extra.csv", source_namespace="fictional-demo").ok
    row = next(row for row in db.list_transactions(conn) if row.source_transaction_id == "rent-two")
    db.correct_classification(conn, row.id, "expense", "Rent")
    conn.close()
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert any("2 identifiable rent charges" in item.value for item in app.warning)
    assert not any(item.label == "Projected monthly surplus" for item in app.metric)
    app.text_input(key="scenario_existing_2026-05").input("1300.00").run(timeout=30)
    confirm_rent(app).check().run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$522.06"
    app.text_input(key="scenario_existing_2026-05").input("1275.00").run(timeout=30)
    assert not confirm_rent(app).value and not any(item.label == "Projected monthly surplus" for item in app.metric)
    confirm_rent(app).check().run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$497.06"
    conn = db.connect(path)
    db.correct_classification(conn, row.id, "unknown", "Uncategorized")
    # Leave two candidates by labeling a second existing expense as explicit Rent.
    other = next(item for item in db.list_transactions(conn) if item.posted_date.startswith("2026-05") and item.effective_category == "Groceries")
    db.correct_classification(conn, other.id, "expense", "Rent")
    conn.close()
    app.run(timeout=30)
    assert not confirm_rent(app).value
    assert not any(item.label == "Projected monthly surplus" for item in app.metric)


def test_streamlit_missing_rent_requires_explicit_zero_and_rejects_impossible_rent(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    path = tmp_path / "missing.db"
    monkeypatch.setenv("COMPASS_DB_PATH", str(path))
    conn = db.connect(path)
    assert importer.import_statement(conn, b"date,description,amount,account,transaction_id\n2026-05-01,PAYROLL,100,Checking,a\n2026-05-02,ALDI,-10,Checking,b\n", "small.csv").ok
    conn.close()
    app = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert not any(item.label == "Projected monthly surplus" for item in app.metric)
    app.text_input(key="scenario_existing_2026-05").input("11.00").run(timeout=30)
    confirm_rent(app).check().run(timeout=30)
    assert any("cannot exceed" in item.value for item in app.error)
    app.text_input(key="scenario_existing_2026-05").input("0.00").run(timeout=30)
    app.text_input(key="scenario_new_rent").input("0.00").run(timeout=30)
    confirm_rent(app).check().run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$90.00"
    app.selectbox(key="scenario_mode").select("additional").run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$90.00"


def test_streamlit_savings_target_cumulative_table_and_no_inferred_start(monkeypatch, tmp_path):
    app, _ = load_app(monkeypatch, tmp_path)
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert not any("Cumulative change" in item.value.columns for item in app.dataframe)
    app.checkbox(key="scenario_use_target").check().run(timeout=30)
    app.text_input(key="scenario_target").input("600.00").run(timeout=30)
    assert any("Target not met" in item.value and "−$77.94" in item.value for item in app.markdown)
    app.checkbox(key="scenario_use_start").check().run(timeout=30)
    assert any("Scenario input" in item.value for item in app.error)
    assert not any(item.label == "Projected monthly surplus" for item in app.metric)
    app.text_input(key="scenario_start").input("1000.00").run(timeout=30)
    frame = next(item.value for item in app.dataframe if "Cumulative change" in item.value.columns)
    assert len(frame) == 6 and list(frame["Month number"]) == [1, 2, 3, 4, 5, 6]
    assert frame.iloc[-1]["Cumulative change"] == "$3,132.36"
    assert frame.iloc[-1]["User starting value + cumulative change"] == "$4,132.36"
    assert any("not an account balance" in item.value for item in app.caption)
    assert any("No starting balance was inferred" in item.value for item in app.markdown)
    app.checkbox(key="scenario_use_start").uncheck().run(timeout=30)
    assert not any("Cumulative change" in item.value.columns for item in app.dataframe)


def test_streamlit_baseline_month_changes_and_correction_refresh(monkeypatch, tmp_path):
    from streamlit.testing.v1 import AppTest

    app, path = load_app(monkeypatch, tmp_path)
    app.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    app.selectbox(key="scenario_month").select("2026-06").run(timeout=30)
    assert metric(app, "Scenario baseline surplus") == "$1,711.45"
    assert metric(app, "Projected monthly surplus") == "$1,486.45"
    assert any("Baseline excludes $80.00" in item.value for item in app.warning)
    conn = db.connect(path)
    atm = next(row for row in db.list_transactions(conn) if row.effective_type == Kind.UNKNOWN)
    db.correct_classification(conn, atm.id, "expense", "Cash spending")
    conn.close()
    app.run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$1,406.45"
    assert not any("Baseline excludes" in item.value for item in app.warning)
    app.button(key="load_checking").click().run(timeout=30)
    assert metric(app, "Projected monthly surplus") == "$1,406.45"
    fresh = AppTest.from_file(str(ROOT / "app.py")).run(timeout=30)
    fresh.selectbox(key="scenario_month").select("2026-06").run(timeout=30)
    fresh.selectbox(key="scenario_mode").select("replace").run(timeout=30)
    assert metric(fresh, "Projected monthly surplus") == "$1,406.45"
