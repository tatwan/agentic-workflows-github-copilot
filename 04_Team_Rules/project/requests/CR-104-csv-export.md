# CR-104: Monthly report as a CSV file

- Requested by: J. Park, Finance
- Date: 2026-05-12
- Owner:

## What we want

Finance wants the monthly summary as a CSV file they can open in a spreadsheet: one row per month with month,
orders, units and revenue. Revenue should keep two decimals, as in 2085.70.

## Background

- The monthly summary comes from `monthly_summary` in `orders/report.py`. K. Osei wrote the current report.
- The report's tests are in `tests/test_report.py`.
- Nothing has been built for this request yet.
