# A build without the plan edit

This folder shows a version of the export where nobody edited the plan. We wrote it for this lab so the
result is the same every time; it is not a recorded Copilot run. Its code and tests are the kind an agent can
write when the request does not say how revenue should look.

| File | What it is |
|---|---|
| `report.py` | The report with an export added. It writes revenue with `round(float(revenue), 2)` |
| `test_export.py` | Two new tests: one row per month, and January's numbers |
| `test-output.txt` | What `python -m unittest` printed: 7 tests, all passed |
| `monthly.csv` | The file the export wrote from `data/orders.csv` |

## What the tests said

```text
.......
----------------------------------------------------------------------
Ran 7 tests in 0.009s

OK
```

## What finance got

```text
month,orders,units,revenue
2026-01,8,174,2085.7
2026-02,8,193,5154.25
2026-03,15,315,5278.1
2026-04,5,76,761.55
2026-05,6,179,3087.5
2026-06,6,126,1186.3
```

Three rows lost their final zero: January, March and May. Finance's import expects two decimals, so the request
is not met.

## Why the tests passed

The January test compares the revenue as a number:

```python
self.assertEqual(float(january["revenue"]), 2085.70)
```

`2085.7` and `2085.70` are the same number, so the test passes for both. The test checks what its author
thought of, not what finance asked for. The export line converts the exact `Decimal` to a `float` and rounds
it; a `float` has no trailing zeros, so `round` gives `2085.7` and the CSV writer prints exactly that.

The test from the lab's plan edit reads the line as text, so it fails on this file:

```text
AssertionError: '2026-01,8,174,2085.7' != '2026-01,8,174,2085.70'
```
