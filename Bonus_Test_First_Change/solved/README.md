# Test-first change: answers

These files are hand-written examples to compare with your own work, not a saved Copilot session.

| Stage | Command from that project | Result |
|---|---|---|
| Starter | `python -m unittest -v` | 4 tests OK |
| Starter plus the prepared regression | `python -m unittest -v` | 6 tests run, 4 subtest failures: `1.0` and `1` in both export paths |
| Green example, with the regression | `python -m unittest -v` | 6 tests OK |
| `project/`, after refactoring | `python -m unittest -v` | 6 tests OK |
| `challenge/project/` | `python -m unittest -v` | 8 tests OK |

The green example formats each value with `.2f` in both functions. The refactored answer keeps the two public
functions and shares the CSV-writing loop in `_write_rows`. Both paths produce `2026-03,1.00` for either input.
The challenge checks `0.00`, `-2.50`, unchanged inputs and a header-only empty file.
A private helper is one possible cleanup; the required outcome is unchanged behavior and readable code.
