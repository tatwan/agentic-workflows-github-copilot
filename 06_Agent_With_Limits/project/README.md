# Release check

The platform team's check that decides whether a release can go ahead, based on how fast each endpoint answers.

| File or folder | What it holds |
|---|---|
| `docs/release-check.md` | The team's rule: when an endpoint counts as too slow |
| `data/before.csv`, `data/after.csv` | The p95 time of each endpoint, in milliseconds, for the last release and for the change |
| `latency_check.py` | The check: compares the two files and says whether the release can go ahead |
| `tests/test_latency_check.py` | Tests for the check |

Run the check from this folder:

```sh
python latency_check.py data/before.csv data/after.csv
```

Run the tests from this folder (Python 3.10 or newer, no packages needed):

```sh
python -m unittest
```

Endpoints, times and names are fictional.
