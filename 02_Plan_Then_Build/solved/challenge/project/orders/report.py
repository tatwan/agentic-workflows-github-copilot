"""Monthly summary of the orders file.

One row of data/orders.csv is one order line: an order ID, its date, a region,
a product, units and unit price. An order can have several lines.
"""
from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "orders.csv"


@dataclass(frozen=True)
class OrderLine:
    order_id: int
    order_date: date
    region: str
    product: str
    units: int
    unit_price: Decimal

    @property
    def amount(self) -> Decimal:
        return self.unit_price * self.units


def load_orders(path: Path = DATA) -> list[OrderLine]:
    """Read the orders file into OrderLine records."""
    with open(path, newline="", encoding="utf-8") as f:
        return [
            OrderLine(
                order_id=int(row["order_id"]),
                order_date=date.fromisoformat(row["order_date"]),
                region=row["region"],
                product=row["product"],
                units=int(row["units"]),
                unit_price=Decimal(row["unit_price"]),
            )
            for row in csv.DictReader(f)
        ]


def monthly_summary(lines: list[OrderLine]) -> list[dict]:
    """One row per month, oldest first: month, orders, units and revenue.

    orders counts distinct order IDs; revenue is the sum of units x unit price,
    kept as Decimal so totals are exact.
    """
    months: dict[str, dict] = {}
    for line in lines:
        key = line.order_date.strftime("%Y-%m")
        row = months.setdefault(key, {"month": key, "order_ids": set(), "units": 0, "revenue": Decimal("0")})
        row["order_ids"].add(line.order_id)
        row["units"] += line.units
        row["revenue"] += line.amount
    return [
        {"month": key, "orders": len(r["order_ids"]), "units": r["units"], "revenue": r["revenue"]}
        for key, r in sorted(months.items())
    ]


def export_monthly_csv(lines: list[OrderLine], destination: Path) -> None:
    """Write the monthly summary to a CSV file: month, orders, units, revenue.

    Revenue is written with exactly two decimals (2085.70), as finance expects.
    An existing file at destination is replaced.
    """
    rows = monthly_summary(lines)
    with open(destination, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["month", "orders", "units", "revenue"])
        for row in rows:
            writer.writerow([row["month"], row["orders"], row["units"], f"{row['revenue']:.2f}"])


def main(argv: list[str] | None = None) -> None:
    """Command line: python -m orders.report --output monthly.csv [--input data/orders.csv]"""
    parser = argparse.ArgumentParser(description="Export the monthly summary to a CSV file.")
    parser.add_argument("--input", type=Path, default=DATA, help="orders file to read")
    parser.add_argument("--output", type=Path, required=True, help="CSV file to write")
    args = parser.parse_args(argv)
    if args.output.resolve() == args.input.resolve():
        parser.error("--output must not be the input file")
    export_monthly_csv(load_orders(args.input), args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
