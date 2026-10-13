# Release check: response times

Before each release we compare how fast each endpoint of our web service answers, before and after the change.
We use the p95 time: 95 of every 100 requests finish within it.

- An endpoint is **too slow** when its p95 time is more than 10% higher than before. Exactly 10% is still within
  the limit.
- A new endpoint has no time from before. We list it as new; it is never too slow.
- The release goes ahead only when no endpoint is too slow.

Times come from the load test in `data/`: `before.csv` for the last release, `after.csv` for the change.
