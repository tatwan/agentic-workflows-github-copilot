# Lab 07: How to organise a messy folder with an agent

## Goal

Ask Copilot to sort a folder of 22 saved files, and get its plan as a table before anything moves. Check the plan
row by row, approve one batch of moves, and check the batch arrived. Two files have names that look like copies:
one is a real copy, the other holds a different number, and a plan that goes by names deletes it. Copilot moves
files with terminal commands, which a checkpoint does not undo, so the plan and a small batch are where you catch
mistakes.

## What you will learn

- Ask an agent for a plan as a table before it changes anything, and check that every file appears once.
- Tell a real duplicate from a look-alike by comparing contents, not names, and correct the plan.
- Approve one batch of moves after reading the command, and check the result in the Explorer.
- Say what a checkpoint cannot undo, and start over from a copy.

## Before you start

You need VS Code with GitHub Copilot signed in ([Lab 00](../00_Setup_Check/) checks this). Nothing to install, and
no coding.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`07_Organize_Files_And_Notes/project`). Keep this README open elsewhere, for example on GitHub, so Copilot works
   on the folder, not on the lab text.
2. If VS Code asks whether you trust the folder's authors, trust it. It holds only text files, images and PDFs.
3. If you ever allowed commands for longer than once, run **Chat: Reset Tool Confirmations** from the Command
   Palette (**Ctrl+Shift+P**, **Cmd+Shift+P** on macOS), so every move waits for you.
4. Open the Chat view, start a **New Chat** and choose **Interactive** (on a Local session, **Agent**). Keep
   **Manual permissions** in the chat input's permissions menu ([Lab 06](../06_Agent_With_Limits/) covers
   approvals).

The project is one team member's downloads:

| File or folder | What it is |
|---|---|
| `inbox/` | 22 files saved from email and chat: notes, CSV files, images and PDFs from two projects, plus admin and personal files |
| `README.md` | What the folder holds |

Starting over works differently in this lab. Copilot has no file tool for moving, so it moves files with a terminal
command such as `mv` (`Move-Item` on Windows), and **Restore Checkpoint** does not reverse terminal commands. To
start over, close the folder and copy `project` again from the repository or the ZIP.

## Part A: Find the look-alikes yourself

An agent will tell you which files are copies. Find out first, so you can check what it says.

1. Expand `inbox/` in the Explorer and count the files: 22.
2. Find three pairs whose names differ by a few characters:
   - `standup-2026-05-12.md` and `standup-2026-05-12 (1).md`
   - `release-q2-notes-draft.txt` and `release-q2-notes-draft (1).txt`
   - `dashboard-mockup-v1.png` and `dashboard-mockup-v2.png`

   A name ending in `(1)` is what a browser or mail app gives the second download of a file with the same name. It
   says nothing about what is inside.
3. Compare the stand-up pair: select one file, **Ctrl**-click (**Cmd**-click on macOS) the other, right-click and
   choose **Compare Selected**. The diff editor highlights lines that differ.
4. Compare the release notes pair the same way.
5. Open both mock-up images.

Checkpoint:

| Pair | What you see | Verdict |
|---|---|---|
| Stand-up notes | No line highlighted | A real duplicate |
| Release notes drafts | One line differs: `100 units` in one, `50 units` in the other | Not a duplicate. Someone changed the discount threshold, and only the owner knows which is right |
| Mock-ups | A blue v1 and a green v2 | Two versions of a design, not copies |

Delete either release notes draft and one of the two thresholds is lost, without anyone deciding. Names tell you
which files to compare; only the contents tell you whether they are the same.

## Part B: Ask for a plan as a table

1. Paste this request:

   ```text
   Sort the files in inbox/ into folders by project. Don't move or delete anything yet.
   First show me your plan as a table: file, new folder, and why.
   If two files look like duplicates, say how you checked.
   ```

2. Expand the steps. The agent lists the folder and reads some files; it may sort images and PDFs by name alone. If
   the chat asks to run a command that moves or deletes a file, choose **Skip**: you asked for a plan.
3. Check the table against the Explorer and against Part A:
   - 22 rows, each file once. A missing file is one the agent forgot to place.
   - No row deletes, merges or renames a file.
   - Both mock-ups go to the same folder, and neither is marked old or replaced.
   - For the two `(1)` files: what did it decide, and did it read both files or go by the name?
4. If the plan disagrees with what you found in Part A, correct it in one reply. For example:

   ```text
   release-q2-notes-draft (1).txt is not a duplicate: it says 50 units where the other says 100.
   Keep both in the release folder, and keep both mock-ups. Show me the updated table.
   ```

   Change the wording to fit the mistake you found. If your plan was right first time, open
   [resources/name-only-plan.md](resources/name-only-plan.md), a plan we wrote from the names alone, and find its
   three wrong decisions.

Checkpoint: a table of 22 rows with a folder per project (`dashboard`, `release`, `meetings`, `admin` and `personal`
are typical; names vary). Both release notes drafts go to the release folder, both mock-ups are kept, and the
stand-up copy is flagged for you to decide, not deleted. `inbox/` still holds 22 files.

## Part C: Move one batch you approved

1. Paste:

   ```text
   Move only the release files now, as in the plan. Leave everything else in inbox/, and don't delete anything.
   ```

2. The agent may create the release folder first. Then the chat stops and shows a command. Before you answer, read
   it:
   - **What it does:** `mv` or `Move-Item` moves a file; `rm`, `del` or `Remove-Item` deletes one.
   - **Which files:** the seven release files from the plan, and no others. A name with spaces, such as
     `release-q2-notes-draft (1).txt`, must be inside quotes, or the command fails or picks the wrong file.
   - **Where to:** the release folder from the plan.
3. If all three match, choose **Allow Once** from the arrow next to **Allow**. If the command moves other files or
   deletes anything, choose **Skip** and say what was wrong. You may get one prompt for the batch or one per file;
   read each one.
4. Check in the Explorer, not in the agent's summary:
   - Count the files in the release folder and in `inbox/`.
   - Open `release-q2-notes-draft (1).txt`.
   - Compare the two release notes drafts again with **Compare Selected**.

Checkpoint:

| Where | Value |
|---|---|
| Release folder | 7 files, both release notes drafts among them |
| `inbox/` | 15 files |
| `release-q2-notes-draft (1).txt` | Still reads `50 units` |
| Deleted | Nothing |

**Restore Checkpoint** on your request would not put these files back: the moves were terminal commands. Your
checks are the plan and the batch, before they run. Seven moves are quick to check; twenty-two at once are not.

## Part D: Finish the sort and decide on the duplicate

1. Paste:

   ```text
   Now move the rest as in the plan, one folder at a time. Don't delete anything.
   ```

2. Read each command and allow it once, as in Part C. After each folder, compare its file count with the table.
3. The stand-up copy is your decision. Run **Compare Selected** on the pair again: no line highlighted. Right-click
   `standup-2026-05-12 (1).md` in the Explorer and choose **Delete**. VS Code moves it to the Trash (the Recycle Bin
   on Windows), so you can still get it back. If the agent offers to delete it with a command, choose **Skip**: `rm`
   and `Remove-Item` delete for good.

Checkpoint:

| Folder | Files |
|---|---|
| dashboard | 8 |
| release | 7 |
| meetings | 1 |
| admin | 3 |
| personal | 2 |
| `inbox/` | none |

Folder names, and where the stand-up note goes, can differ. The counts add up to 21: one fewer than you started
with, and the missing file is the copy you deleted yourself.

## If your run looks different

| What you see | What to do |
|---|---|
| The agent asks to move files before showing a plan | Choose **Skip** and reply `Stop. Show me the plan as a table first.` If files have already moved, copy `project` again |
| The plan deletes a file or puts v1 in an "old" folder | That is the mistake Part B looks for. Correct it with a reply like the one in step 4 |
| A moved text file appears as a new file with Keep and Undo, and the original is still in `inbox/` | The agent copied the file with its edit tools instead of moving it. Select **Undo** on the new files and reply `Move the files with a terminal command; don't recreate them.` |
| The move fails with *No such file or directory* (*Cannot find path* on Windows) | A name with spaces was not in quotes. Reply `The command failed on the names with spaces. Quote each file name.` |
| Files move with no prompt | Commands were allowed for longer than once in an earlier chat, or the permissions menu is set to **Allow all**. Run **Chat: Reset Tool Confirmations**, set **Manual permissions** and copy `project` again |

## What you can do now

- Ask an agent for a plan as a table before it changes a folder, and check that every file appears once and nothing
  is deleted.
- Compare two files before you agree they are duplicates, and correct a plan that went by names.
- Read a move command before you allow it, allow it once, and check the batch in the Explorer.
- Explain why a move made in the terminal has no checkpoint, and start over from a copy.

## Challenge

1. **Three new arrivals.** With your file manager (Finder, File Explorer), copy the three files in
   [resources/new-arrivals](resources/new-arrivals/) into `project/inbox/`. Ask for a plan for just these three, as a
   table, with nothing moved. Check each decision with **Compare Selected** against the file already sorted, then
   approve the moves. Expected: `dashboard-feedback-round2.md` goes to the dashboard folder (a later round, not a
   copy); `dashboard-feedback-round1 (1).md` has one extra line, `- Add a dark mode`, so both versions stay;
   `release-q2-checklist (1).md` matches the checklist in the release folder line for line, a duplicate for you to
   delete.
2. **A file the agent can undo.** Ask `Write INDEX.md listing each folder and its files.` Check every count against
   the Explorer. This time the agent writes a file, so you get Keep and Undo, which a move never offers.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **Your own folders.** Try this on a copy of a real folder, such as your Downloads, never on the original. Approve
  one batch at a time until the plans earn your trust.
- **Plan mode.** In **Plan** mode the agent researches and plans without changing files
  ([Lab 01](../01_How_An_Agent_Works/)). Ask for the table there, then switch to **Interactive** for the moves.
- **Make the habits stick.** "Show a plan table first; never delete; flag duplicates for me" can go in
  `.github/copilot-instructions.md` ([Lab 04](../04_Team_Rules/)) or in a `/sort-inbox` skill
  ([Lab 05](../05_Make_A_Skill/)).

## Resources

- [Approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals) (VS Code docs): what waits for
  you by default, and how long an approval lasts
- [Review code edits](https://code.visualstudio.com/docs/agents/run/review-code-edits) (VS Code docs): what Restore
  Checkpoint puts back, and that it does not reverse terminal commands
- [User interface](https://code.visualstudio.com/docs/getstarted/userinterface) (VS Code docs): selecting several
  files in the Explorer and **Compare Selected**
- [Back to the labs](../README.md)
