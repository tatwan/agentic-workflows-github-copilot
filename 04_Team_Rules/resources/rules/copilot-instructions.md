# Orders team: how we work

- `requests/` holds change requests. The monthly report is `orders/report.py`; its tests are in `tests/test_report.py`.
- Never invent an owner. If a request names nobody, write `Owner: unassigned` on its own line. Do not pick someone from another file.
- A test file is not a test run. Never say a check passed unless you ran it in this chat; say which checks are still to run.
- Reviews and replies are read-only work: change no code, tests or data, and run no commands.
