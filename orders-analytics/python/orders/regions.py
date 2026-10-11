"""Revenue share by region for the orders file (course-authored).

This module has no tests yet: Lab 10's developer challenge asks you to add them.
"""
from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal

from orders.report import OrderLine


def revenue_share_by_region(lines: list[OrderLine]) -> dict[str, Decimal]:
    """Each region's share of total revenue, in percent, rounded half-even to 1 place.

    Regions are returned largest share first; ties keep alphabetical order.
    """
    totals: dict[str, Decimal] = {}
    for line in lines:
        totals[line.region] = totals.get(line.region, Decimal("0")) + line.amount
    grand_total = sum(totals.values(), Decimal("0"))
    if grand_total == 0:
        return {}
    shares = {
        region: (amount * 100 / grand_total).quantize(Decimal("0.1"), rounding=ROUND_HALF_EVEN)
        for region, amount in totals.items()
    }
    return dict(sorted(shares.items(), key=lambda item: (-item[1], item[0])))


def regions_at_or_above(lines: list[OrderLine], min_share: Decimal) -> list[str]:
    """Regions whose share is at least min_share percent, largest first."""
    return [region for region, share in revenue_share_by_region(lines).items() if share >= min_share]
