---
name: test-first-change
description: Reproduce a reported Python bug with a regression test, then make a small fix and refactor under tests. Use when asked for a test-first bug fix or red-green-refactor workflow.
argument-hint: "[bug and acceptance condition]"
---

# Test a change before fixing it

1. Read the named code and original tests. Run the original suite and report its actual result.
2. Add a regression in a new test file for the requested behavior. Preserve existing tests and production code.
3. Run it. Stop after a failure that demonstrates the bug; explain the actual and expected values. An import or
   syntax error is not evidence of the bug. If the new test already passes, report that no failing bug was
   reproduced and stop without changing production code. Otherwise wait for the person to approve the fix.
4. After approval, make the smallest production change. Preserve the test's expected behavior. Run all tests.
5. Ask before refactoring. Keep public names and behavior; remove duplication only where it reduces maintenance.
6. Run all tests after the refactor. Report changed files, actual results and anything not executed. Never claim
   a test ran from reading it. Do not install packages or alter data unless the person asks.
