# Lab 06: answers

Use these after you finish the lab, to compare with your own result. Copilot's wording and code change from run
to run, so compare the facts listed here, not the text. The files were written by hand to show a correct result;
they are not a saved Copilot chat.

- `project/`: the project after Parts B and C. `.github/agents/reviewer.agent.md`; `latency_check.py` with `>` on
  line 27; `tests/test_latency_check.py` with `test_exactly_ten_percent_is_ok` (6 tests, OK). The check prints
  `Release can go ahead: no endpoint is too slow.` and exits 0. The starting project prints
  `Release blocked: GET /orders too slow.` and exits 1. With the new test and the old `>=`, the run ends
  `FAILED (failures=1)`.
- `challenge/`: the test-runner agent for Challenge 1 and the expected outcomes of both challenges (`answers.md`).
- `going-further/report.md`: the performance report from Going further, made from the fixed check's output.

The reviewer file to paste is `../resources/reviewer.agent.md`; the test and check output after the fix is
`../resources/after-the-fix/output.txt`.
