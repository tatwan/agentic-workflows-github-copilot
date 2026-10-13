# Review of latency_check.py against docs/release-check.md

We wrote this example for this lab to show what a useful review looks like; it is not a recorded Copilot run.

**The check is wrong about GET /orders.** `docs/release-check.md` says an endpoint is too slow when its p95 time is
*more than* 10% higher, and that exactly 10% is still within the limit. GET /orders went from 200 ms
(`data/before.csv`) to 220 ms (`data/after.csv`): 20 / 200 = exactly 10%.

`latency_check.py`, line 27, in `is_too_slow`:

```python
return change_percent(before_ms, after_ms) >= LIMIT_PERCENT
```

`>=` means "10% or more", so exactly 10% counts as too slow. The rule needs `>`:

```python
return change_percent(before_ms, after_ms) > LIMIT_PERCENT
```

**The tests did not catch it.** `tests/test_latency_check.py` tries 5% and 15% slower, but not exactly 10%. Add a
test that `is_too_slow(200, 220)` is false.

**Everything else follows the rule.** The other five endpoints change by +9.0% or less, and GET /exports is listed
as new. With the fix, the release can go ahead.

I did not run the tests or the check: I can only read files.
