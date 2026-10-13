# Lab 06 challenge: expected outcomes

## 1. An agent that runs but does not edit

File: `test-runner.agent.md` (in this folder), saved as `.github/agents/test-runner.agent.md` in a fresh copy of
`project/` (with the `>=` bug still in place).

- "Run the tests": the agent proposes `python -m unittest` (or `py -m unittest`); an approval prompt appears. Allow
  once: `Ran 5 tests`, `OK`. The bug is still there; no test tries exactly 10%.
- "Change >= to > in is_too_slow": no edit tool, so no Keep/Undo marks. Two outcomes are both acceptable:
  - it says it cannot edit files and gives the change for the person to make; or
  - it proposes a terminal command that rewrites the file (for example a `sed -i` line, or PowerShell
    `(Get-Content ...) -replace ... | Set-Content ...`). That command appears in an approval prompt. Skip it.
- The point: `execute` is a broad tool. A command can change any file the terminal can reach, so an agent with a
  terminal and no edit tool can still edit. Approval is the control left; read every command before allowing it.
  Expected file state after Skip: `latency_check.py` still has `>=` on line 27.

## 2. A reviewer that saves its review

- "Write your review to reviews/latency.md": no `reviews/` folder appears. The reviewer says it has no tool to
  create files and gives the review in the chat.
- What to change so it can save reviews but not touch code: tool lists cannot limit `edit` to one folder. Adding
  `edit` lets the reviewer change `latency_check.py` as well. Reasonable answers:
  - keep it read-only and save the review yourself (copy from the chat, or let the normal agent write it); or
  - give it `edit`, add a rule like Lab 04's (`applyTo: "reviews/**"`, or a line in the agent's instructions: only
    write in `reviews/`), and review every change with Keep and Undo. The rule asks; it does not stop anything.
- An answer that says "add edit and it will only write reviews" misses the point of the lab.
