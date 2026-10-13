# Release performance report

Load test: `data/before.csv` (last release) against `data/after.csv` (this change). p95 times in milliseconds.
Rule (`docs/release-check.md`): too slow means more than 10% slower than before.

| Endpoint | Before | After | Change | Status |
|---|---:|---:|---:|---|
| GET /orders | 200 | 220 | +10.0% | ok |
| GET /orders/{id} | 120 | 126 | +5.0% | ok |
| POST /orders | 400 | 416 | +4.0% | ok |
| GET /customers | 150 | 141 | -6.0% | ok |
| GET /reports/monthly | 800 | 872 | +9.0% | ok |
| DELETE /orders/{id} | 90 | 90 | +0.0% | ok |
| GET /exports | - | 310 | - | new |

Release can go ahead: no endpoint is too slow. GET /orders is exactly at the limit, and GET /reports/monthly is
close to it (+9.0%); watch both in the next release.

Source: `python latency_check.py data/before.csv data/after.csv`, run after the fix in Part C.
