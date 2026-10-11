from datetime import date
from decimal import Decimal

from orders.report import DATA, OrderLine, load_orders, monthly_summary


def line(order_id, day, units, price, region="North", product="Notebook"):
    return OrderLine(order_id, date.fromisoformat(day), region, product, units, Decimal(price))


def test_load_orders_reads_every_line():
    lines = load_orders(DATA)
    assert len(lines) == 97
    assert lines[0].order_id == 1024
    assert lines[0].unit_price == Decimal("3.50")


def test_summary_has_one_row_per_month_oldest_first():
    rows = monthly_summary([line(2, "2026-02-03", 1, "1.00"), line(1, "2026-01-05", 1, "1.00")])
    assert [r["month"] for r in rows] == ["2026-01", "2026-02"]


def test_orders_counts_distinct_order_ids():
    rows = monthly_summary([line(1, "2026-01-05", 2, "3.50"), line(1, "2026-01-05", 1, "8.75")])
    assert rows[0]["orders"] == 1
    assert rows[0]["units"] == 3


def test_revenue_is_exact():
    rows = monthly_summary([line(1, "2026-01-05", 3, "0.10"), line(2, "2026-01-09", 7, "0.10")])
    assert rows[0]["revenue"] == Decimal("1.00")


def test_summary_of_the_course_file():
    rows = monthly_summary(load_orders())
    assert len(rows) == 6
    assert rows[0] == {"month": "2026-01", "orders": 8, "units": 174, "revenue": Decimal("2085.70")}
    assert sum(r["revenue"] for r in rows) == Decimal("17553.40")
