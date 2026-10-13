# Lab 04: How to give Copilot your team's rules

## Goal

Ask Copilot for the same review three times: with no rules, after you add your team's rules in
`.github/copilot-instructions.md`, and after you add a rule that applies only to review files. Nothing changes
between the runs except two short Markdown files, and the review changes with them. Then ask for a reply in another
folder and see the review rule stay out of it: a file-type rule applies only where its pattern matches.

## What you will learn

- Write team rules in `.github/copilot-instructions.md` and check that a request used them.
- Compare the same request before and after the rules, and say which differences the rules caused.
- Write a rule for one kind of file with `applyTo`, and check that it reaches those files and no others.
- Tell rules that belong in every request from rules that belong to one kind of file.

## Before you start

You need VS Code with GitHub Copilot signed in ([Lab 00](../00_Setup_Check/) checks this). Nothing else to install,
and no coding.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`04_Team_Rules/project`). Keep this README open elsewhere, for example on GitHub, so Copilot works on the
   team's files, not on the lab text.
2. If VS Code asks whether you trust the folder's authors, trust it.
3. Open the Chat view and start a **New Chat**. In the mode picker choose **Interactive** (on a Local session,
   **Agent**).

The project belongs to a small orders team:

| File | What it is |
|---|---|
| `requests/CR-104-csv-export.md` | A change request: finance wants the monthly report as a CSV file |
| `requests/CR-105-newest-month-first.md` | A second request, used in the challenge |
| `orders/report.py`, `tests/test_report.py` | The monthly report and its tests. You will not open these; Copilot will |

To start over, hover over your first request in the chat and select **Restore Checkpoint**, or copy `project`
again from the repository.

## Part A: Ask for a review with no rules

Every team has habits nobody writes down: who may take on work, what counts as proof, how a review is laid out. A
new colleague learns them in a few weeks. Copilot starts every chat without them. This part shows what it does
when it has to guess.

1. Open `requests/CR-104-csv-export.md` and read it. Note three things: the **Owner** line is empty; the
   background says K. Osei wrote the current report, which does not make K. Osei the owner of this request; and
   nothing has been built yet.
2. Predict: who will the review name as owner, and will it approve the request?
3. Paste this request:

   ```text
   Review requests/CR-104-csv-export.md against the current code
   and write the review to reviews/CR-104.md.
   ```

4. Expand the steps: the agent reads the request, then `orders/report.py` and perhaps the tests, then creates the
   review. If it asks to run a command, select **Skip**. This lab runs nothing.
5. Open `reviews/CR-104.md` and answer four questions:
   - Does it name an owner? Where did that name come from?
   - Does it approve the request, although nothing has been built?
   - Does it say the tests pass? Nobody ran them in this chat.
   - What headings does it use?
6. Select **Keep** above the file, so the review stays for the comparison in Part B.

Checkpoint: you have a review and an answer to each question. There is no right answer yet, because the team's
habits are written nowhere Copilot can see. If your review looks fine, open
[resources/without-the-rules/CR-104.md](resources/without-the-rules/CR-104.md): an example we wrote of what a
review without rules can look like. It suggests K. Osei, approves, says the tests pass, and uses its own headings.

## Part B: Add the team's rules and ask again

`.github/copilot-instructions.md` is a Markdown file of rules that Copilot adds to every chat request in this
folder. You write it once; nobody has to paste it again.

1. In the Explorer, select **New File...** and type the whole path, `.github/copilot-instructions.md`. VS Code
   creates the `.github` folder too.
2. Paste these rules and save:

   ```markdown
   # Orders team: how we work

   - `requests/` holds change requests. The monthly report is `orders/report.py`; its tests are in `tests/test_report.py`.
   - Never invent an owner. If a request names nobody, write `Owner: unassigned` on its own line. Do not pick someone from another file.
   - A test file is not a test run. Never say a check passed unless you ran it in this chat; say which checks are still to run.
   - Reviews and replies are read-only work: change no code, tests or data, and run no commands.
   ```

   The first line tells Copilot where things are. The other three are habits from Part A's questions.
3. Start a **New Chat**. It does not see Part A's conversation, so only the rules are new.
4. Paste exactly the same request as in Part A:

   ```text
   Review requests/CR-104-csv-export.md against the current code
   and write the review to reviews/CR-104.md.
   ```

5. Under the reply, expand **References**. `copilot-instructions.md` is listed: the rules went with the request,
   although you never mentioned them.
6. Copilot rewrites `reviews/CR-104.md`. Open it: the editor marks the lines Copilot changed, with **Keep** and
   **Undo** buttons. Those marked lines are the difference the rules made. Select **Keep**.

Checkpoint: the review has `Owner: unassigned` on its own line and names nobody else as owner. It does not say the
tests pass; it says which checks are still to run, such as the tests in `tests/test_report.py`. The chat's list of
changed files shows only `reviews/CR-104.md`. The headings are still Copilot's own choice: no rule mentions them yet.

## Part C: Add a rule for review files only

Some rules fit one kind of file. The team lays out every review the same way, with a status line, but a reply to
the person who asked should read like a short message. A rule for one kind of file goes in `.github/instructions/`,
in a file whose name ends in `.instructions.md`. Its header holds `applyTo`, a pattern of file paths: Copilot uses
the rule when it creates or changes a file whose path matches. In `reviews/**`, the `**` stands for any file in
`reviews/`, at any depth.

1. Select **New File...** again and type `.github/instructions/reviews.instructions.md`. Paste and save:

   ```markdown
   ---
   applyTo: "reviews/**"
   ---
   # How we write reviews

   - Start with the request ID and title as the heading, then the `Owner:` line.
   - Then three sections with these headings, in this order: `## Evidence`, `## Decision`, `## Next step`.
   - Under Decision, write one status line: `Review status: ready`, `Review status: needs verification` or `Review status: rejected`. Use needs verification when the request has no test results.
   - Under Next step, name the check to run and the file it checks.
   ```

   The lines between the two `---` are the header. Everything below them is the rule.
2. Start a **New Chat** and paste the same request a third time:

   ```text
   Review requests/CR-104-csv-export.md against the current code
   and write the review to reviews/CR-104.md.
   ```

3. Expand the steps. Before it writes the review, Copilot may open `reviews.instructions.md`: it is about to change a
   file that matches the pattern. Under the reply, **References** lists both rule files. Select **Keep**.

Checkpoint: the review has the headings Evidence, Decision and Next step, in that order, and the line
`Review status: needs verification` under Decision, because nothing has been built or tested. Next step names a
check and its file, for example the tests in `tests/test_report.py` plus a check that the January line of the CSV
file reads `2026-01,8,174,2085.70`. `Owner: unassigned` is still there: the team rules still apply.

Now ask for a file the pattern does not match. Predict first: will the reply to J. Park have the review headings?

4. Start a **New Chat** and paste:

   ```text
   Write a short reply to J. Park in replies/CR-104.md
   saying what we still need before CR-104 can go ahead.
   ```

5. Open `replies/CR-104.md` and expand **References**.

Checkpoint: the reply has no Evidence, Decision or Next step headings and no `Review status` line. References lists
`copilot-instructions.md` but not `reviews.instructions.md`, because `replies/CR-104.md` does not match
`reviews/**`. The team rules still hold: the reply names no owner for the work and does not say any test passed.

| Rule file | Reaches |
|---|---|
| `.github/copilot-instructions.md` | Every request in this folder |
| `.github/instructions/reviews.instructions.md` | Only work on files under `reviews/` |

## If your run looks different

| What you see | What to do |
|---|---|
| References does not list `copilot-instructions.md`, and the review ignores the rules | Check the path: `.github` must sit directly inside the folder you opened, next to `requests`. Open **Configure Chat** (the gear in the Chat view) > **Instructions** to see the rule files Copilot found. If you cloned this repository with Git, Copilot may look for rules at the top of the repository instead: copy the `project` folder somewhere outside the repository, open the copy and repeat Part B |
| There is no References list under the reply | Expand the steps and look for a read of the rule file, or check Configure Chat > Instructions |
| The review still uses its own headings after Part C | Check the file name ends in `.instructions.md`, the file is in `.github/instructions/`, and the header line is exactly `applyTo: "reviews/**"`. Then start a New Chat |
| References for the reply lists the review rule | Look in the steps for a file in `reviews/` that the agent changed. Start a New Chat and ask again |
| Copilot asks to run a command, such as the tests | Select **Skip**. Reviews here are read-only |

## What you can do now

- Write team rules in `.github/copilot-instructions.md` and confirm in References that a request used them.
- Run the same request before and after the rules and name each difference the rules caused.
- Write a rule for one kind of file with `applyTo`, and show it reaches review files and not replies.
- Decide whether a new rule belongs in every request or with one kind of file.

## Challenge

1. **Write a rule for replies.** Add `.github/instructions/replies.instructions.md` with `applyTo: "replies/**"`.
   Your team wants every reply to start with `Hi` and the person's name, stay under 100 words, and end with a list
   headed `What we need from you`. In a New Chat, ask for the reply to J. Park again. Expected: the reply follows
   all three, and References lists `replies.instructions.md` and not the review rule. Then ask for the CR-104
   review in a New Chat: References lists the review rule, not yours.
2. **Review a request that has an owner.** In a New Chat ask: `Review requests/CR-105-newest-month-first.md
   against the current code and write the review to reviews/CR-105.md.` Expected: `Owner: M. Novak`, because the
   request names one; `Review status: needs verification`; the three headings. A careful review also notices that
   two tests in `tests/test_report.py` expect the oldest month first and will have to change.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **A handover file for work that spans several chats.** Rules say how the team works; they do not say where a task
  stands. At the end of a long session, ask: `Write HANDOVER.md: what is done, what was checked, what is left and
  the next step.` In the next chat, ask Copilot to read `HANDOVER.md` first, and check what it says against the
  files before you trust it: a handover can claim a check that never ran. A line in `copilot-instructions.md`, such
  as `If HANDOVER.md exists, read it before you start`, asks for that in every chat.
- **Let Copilot draft the rules.** Type `/init` in the chat: Copilot reads the project and writes a
  `copilot-instructions.md`. Cut it to the rules your team agrees on. Long rules files are hard to keep true.
- **One file for several agents.** `AGENTS.md` at the top of the project is read by Copilot and by other coding
  agents. Keep one source for each rule, not copies in several files.
- **A rule loaded by task.** A `description` line in the header lets Copilot load a rule when a request matches its
  description, whatever file it touches.
- **Rules for you alone.** Rule files in `~/.copilot/instructions` apply in every project you open.
- **Rules guide; they do not stop anything.** A rule saying "run no commands" is a request to the model. To make
  sure an agent cannot edit or run something, limit its tools and approvals, as in [Lab 06](../06_Agent_With_Limits/).
- **Rules versus skills.** These rules reach every matching request. A skill, as in [Lab 05](../05_Make_A_Skill/),
  is a method Copilot reads when you call it or when a task matches it.

## Resources

- [Use custom instructions in VS Code](https://code.visualstudio.com/docs/agent-customization/custom-instructions):
  file locations, `applyTo` patterns and how to check which rules were used
- [Adding repository custom instructions for GitHub Copilot](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
  (GitHub Docs)
- [AGENTS.md](https://agents.md/): the shared format for agent rules
- [Back to the labs](../README.md)
