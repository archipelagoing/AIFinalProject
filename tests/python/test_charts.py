import pytest

from compass import analytics, db, importer
from compass.charts import Chart, ChartRow, bar_chart, guess_actual_chart, heatmap_chart, slope_chart


ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]


def fixture_transactions():
    connection = db.connect(":memory:")
    for filename in importer.DEMO_STATEMENTS:
        assert importer.import_statement(connection, (ROOT / "fixtures" / filename).read_bytes(), filename).ok
    rows = db.list_transactions(connection)
    connection.close()
    return rows


def test_bar_chart_sorts_exact_cent_values_and_keeps_refund_negative():
    chart = bar_chart((ChartRow("Refunds", -125), ChartRow("Food", 12000)))
    assert chart.kind == "bar"
    assert [row.label for row in chart.rows] == ["Food", "Refunds"]
    assert chart.minimum_cents == -125 and chart.maximum_cents == 12000
    assert "zero" in chart.description


def test_daily_heatmap_and_slope_are_source_backed():
    transactions = fixture_transactions()
    may = analytics.summarize_month(transactions, "2026-05")
    heatmap = analytics.daily_heatmap(may)
    expected_dates = {row.posted_date for row in may.expense_rows}
    assert {row.label for row in heatmap.rows} == expected_dates
    assert sum(row.value_cents for row in heatmap.rows) == may.totals.net_expenses_cents
    slope = analytics.monthly_surplus_slope(transactions, ("2026-04", "2026-05"))
    assert [row.value_cents for row in slope.rows] == [
        analytics.summarize_month(transactions, month).totals.surplus_cents
        for month in ("2026-04", "2026-05")]


def test_guess_actual_and_chart_contract_reject_misleading_domain():
    chart = guess_actual_chart(-50, 125, exclusions=("2 transfers excluded",))
    assert [row.value_cents for row in chart.rows] == [-50, 125]
    assert chart.minimum_cents == -50 and chart.maximum_cents == 125
    with pytest.raises(ValueError, match="include zero"):
        Chart("bar", "Bad axis", "Description", (ChartRow("a", -10),), minimum_cents=-5, maximum_cents=0)


def test_chart_contract_rejects_float_or_duplicate_labels():
    with pytest.raises(ValueError):
        ChartRow("bad", 1.5)
    with pytest.raises(ValueError, match="unique"):
        heatmap_chart((ChartRow("2026-05-01", 100), ChartRow("2026-05-01", 200)))


def test_monthly_slope_requires_distinct_imported_periods():
    transactions = fixture_transactions()
    with pytest.raises(ValueError, match="distinct"):
        analytics.monthly_surplus_slope(transactions, ("2026-05", "2026-05"))
    with pytest.raises(ValueError, match="imported activity"):
        analytics.monthly_surplus_slope(transactions, ("2026-05", "2026-12"))
