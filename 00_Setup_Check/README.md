# Lab 00: How to check you are ready

## Goal

Check that VS Code and Copilot can do what every lab asks of them: you are signed in, you can pick a mode, Copilot
finds an answer in a file, and it stops to ask you before it runs a command. Work down the list. When every row you
need is a pass, you are ready. Rows 5 and 6 are optional: they are only for the labs that need Python or uv.

## What you will learn

- Pick the mode that only reads and the mode that acts.
- See in the chat's steps which files Copilot read.
- Read a command before you allow it, and allow it once.
- Know which labs your setup is ready for.

## Before you start

You need VS Code with the GitHub Copilot extension and a Copilot seat. Rows 1 to 4 need nothing else, and no coding.

1. Get this repository's files: on GitHub, select **Code > Download ZIP** and unzip it. Git is not needed. If you
   already cloned the repository, use your clone.
2. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`00_Setup_Check/project`). Keep this README open somewhere else, for example on GitHub in your browser.
3. If VS Code asks whether you trust the authors of the folder, trust it. It holds two text files.

Each Copilot request uses a little of your monthly allowance. This check sends two to four short requests.

## 1. Copilot is signed in

1. Look for the Copilot icon in the Status Bar at the bottom of the window. Hover over it.
2. Open the Chat view (**View > Chat**).

Pass: the Chat view shows a box where you can type, with no sign-in button. The **Accounts** menu (the person icon
at the bottom of the Activity Bar on the left) shows the GitHub account that holds your Copilot seat.

## 2. The mode picker shows a read-only mode and a mode that acts

1. Start a **New Chat**.
2. Open the mode picker in the chat input, the menu that shows the current mode.
3. Find the permissions menu next to it and check that it says **Manual permissions**, the default.

Pass: the picker offers a mode that only reads and reports, **Plan** (on some setups **Ask** as well), and a mode
that acts, **Interactive** (or **Agent**). The labs say Plan and Interactive; if your picker shows Ask instead of
Plan, or Agent instead of Interactive, use those. Manual permissions means Copilot stops and asks you before most commands.

## 3. Copilot finds an answer in a file

1. In the mode picker choose **Plan**.
2. Paste this request:

   ```text
   When and where is the next team lunch, and who do I tell if I can't come?
   Say which file you read.
   ```

3. When the reply arrives, expand the steps shown in it.

Pass: the reply says Thursday 22 October at 12:30, at Olive Tree on Market Street, and that you tell Sam by Tuesday.
The steps show that Copilot read `team-notes.md`. Open the file yourself and compare. No file changed. Copilot
could only know those facts from the file, so a right answer means it read it.

## 4. Copilot asks before it runs a command

1. Start a **New Chat** and choose **Interactive** (or **Agent**) in the mode picker.
2. Paste this request:

   ```text
   Copy team-notes.md to team-notes-copy.md with a terminal command.
   ```

3. The chat stops and shows the command it wants to run, for example `cp team-notes.md team-notes-copy.md`
   (`Copy-Item` on Windows). Read it before you answer: it copies one file and changes nothing else.
4. Open the arrow next to **Allow** and choose **Allow Once**, the narrowest answer.

Pass: the chat waited for your answer before the command ran, and `team-notes-copy.md` now appears in the Explorer
with the same text as the notes. You can delete the copy: right-click it in the Explorer and choose **Delete**.

A command can change or delete files. Undo and Restore Checkpoint in the chat cover Copilot's edits, not what a
command did, so reading the command first is how you stay in charge. [Lab 06](../06_Agent_With_Limits/) and
[Lab 07](../07_Organize_Files_And_Notes/) build on this.

## 5. Optional: Python 3.10 or newer

For [Lab 02](../02_Plan_Then_Build/), and to let Copilot run the tests in Lab 06. Those labs use only what ships with
Python: no packages to install.

1. In the same chat, paste:

   ```text
   Which Python version do I have? Check in the terminal.
   ```

2. If the chat stops at a command such as `python --version`, `python3 --version` or `py --version`, read it and
   choose **Allow Once**.

Pass: the reply names Python 3.10 or newer.

## 6. Optional: uv

For Lab 03 and the SQL bonus. uv is a Python tool that downloads the packages a lab needs on its first run, so you
install nothing else yourself.

1. In the same chat, paste:

   ```text
   Check that uv works: run uv --version, then
   uv run --no-project --with duckdb python -c "import duckdb; print(duckdb.__version__)"
   ```

2. Read each command and choose **Allow Once**.

Pass: the first command prints a uv version, such as `uv 0.12.13`. The second prints `Downloading duckdb` the
first time (about 19 MB) and then a DuckDB version number, such as `1.5.6`. If your computer has no Python, uv
downloads one first; Python is not needed for this row.

## Your result

| Row | Check | Needed for |
|---|---|---|
| 1 | Copilot is signed in | every lab |
| 2 | Plan and Interactive (or Agent) in the mode picker, Manual permissions | every lab |
| 3 | The right answer, and a read of `team-notes.md` in the steps | every lab |
| 4 | The chat waited for Allow Once, and the copy appeared | every lab where Copilot runs a command: 02, 03, 06, 07 |
| 5 | Python 3.10 or newer | 02, and the tests in 06 |
| 6 | A uv version and a DuckDB version | 03 and the SQL bonus |

Rows 1 to 4 ✅: you are ready for Labs 01, 04, 05, 06, 07 and 08. Add row 5 for Lab 02, and row 6 for Lab 03 and
the SQL bonus.

## If a check fails

| What you see | What to do |
|---|---|
| No Copilot icon in the Status Bar | Install the GitHub Copilot extension from the Extensions view, then reload VS Code |
| The Chat view asks you to sign in | Hover over the Copilot icon and select **Use AI Features**, or use **Accounts > Sign in with GitHub to use GitHub Copilot**. Sign in with the account that holds your Copilot seat |
| You are on Copilot Free when your organisation gave you a seat | You signed in with another GitHub account. Sign out from the **Accounts** menu and sign in with the right one |
| The Status Bar shows **Restricted Mode** | You did not trust the folder, and Restricted Mode turns agents off. Run **Workspaces: Manage Workspace Trust** from the Command Palette and trust it |
| The picker has no Plan, or nothing that acts | Open the session target menu in the chat input and choose **Copilot** or **Local**. If neither offers them, your organisation may have turned agent features off: ask your Copilot administrator |
| The reply has the wrong lunch, or the steps show no file read | Check that you opened `00_Setup_Check/project`, not the lab or repository folder. Start a **New Chat** and ask again |
| The copy appeared and nothing asked you | Expand the steps. If Copilot wrote the file with an edit instead of a command, select **Undo** and ask again, adding `Use the terminal.` If a command ran without asking, your permissions are on **Allow all** or an earlier **Always** answer covers it: switch to **Manual permissions** or run **Chat: Reset Tool Confirmations** |
| Python is not found, or the Microsoft Store opens | Install Python 3.10 or newer from python.org. On Windows, tick **Add python.exe to PATH** in the installer. Close and reopen VS Code, then ask again |
| `uv` is not found | Install uv (link below), close and reopen VS Code so the terminal finds it, then ask again |
| uv cannot download DuckDB | Your network may block the Python package index. Ask your IT team for the approved proxy or mirror. Labs 01, 04, 05, 06, 07 and 08 do not need it |

## Resources

- [Set up Copilot in VS Code](https://code.visualstudio.com/docs/copilot/setup): sign in, and check your usage
- [Agents in VS Code](https://code.visualstudio.com/docs/agents/run/agent-harnesses): session targets and modes
- [Approvals and permissions](https://code.visualstudio.com/docs/agents/run/approvals): Manual permissions and
  approving a command
- [Workspace Trust](https://code.visualstudio.com/docs/editing/workspaces/workspace-trust)
- [Python downloads](https://www.python.org/downloads/)
- [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

Next: [Lab 01: How an agent works](../01_How_An_Agent_Works/). Back to [the labs](../README.md).
