# Lab 08: How to turn a spreadsheet into a report, and what it cost

## Goal

Ask Copilot to turn a file of orders into a one-page report with a chart, then check one number in it yourself
before you trust the rest. The data holds three cancelled orders. Count them as sales and the report names the
wrong best-selling product and shows March falling when it grew. Finally, read what the work cost in AI credits,
do the same job again with one tighter request in a new chat, and compare the two.

## What you will learn

- Ask an agent for a report from a CSV file and open what it made, chart included.
- Work out one number from the data before you read the report, and check the report against it.
- Read what a chat cost: the credits for each response, the session and the month.
- Write one request that says what counts, what to produce and what not to do, and compare it with your first try.

## Before you start

You need VS Code with GitHub Copilot signed in ([Lab 00](../00_Setup_Check/) checks this). Nothing to install, and
no coding.

1. In VS Code choose **File > Open Folder** and open the `project` folder inside this lab
   (`08_Analyze_Data_And_Cost/project`). Keep this README open elsewhere, for example on GitHub, so Copilot works
   on the data, not on the lab text.
2. If VS Code asks whether you trust the folder's authors, trust it. It holds only text files.
3. Open the Chat view and start a **New Chat**. Note the model shown in the model picker; Part D compares two
   chats, so keep the same model for both if your picker lets you.

The project is one sales file from a small online tea shop:

| File | What it is |
|---|---|
| `data/orders-2026-q1.csv` | 40 orders from January to March 2026, one row per order |
| `README.md` | What the columns mean |

To start over, hover over your first request in the chat and select **Restore Checkpoint**, or copy `project`
again from the repository.

## Part A: Choose the number you will check

A report gives you numbers to agree with. Work one out from the data first, so you have something to check it
against.

1. Open `data/orders-2026-q1.csv`. Each row is one order. `amount` is `quantity` times `unit_price`, and
   `status` is `completed` or `cancelled`.
2. Press **Ctrl+F** (**Cmd+F** on macOS) and search for `cancelled`. The search box counts the matches.
3. Search for `Gift box`. Read the four rows and add up the amounts of the completed ones. Then add the cancelled
   one too.

Checkpoint:

| What | Value |
|---|---|
| Cancelled orders | 3 |
| Gift box, completed orders only | 34.50 + 69.00 + 69.00 = **172.50** |
| Gift box, cancelled order counted too | 172.50 + 103.50 = **276.00** |

Gift box is small enough to add by hand and holds a cancelled order, so the report's figure shows which rule the
agent used, even if the report does not say.

## Part B: Ask for the report

Ask the way you would ask a colleague, in one line, and watch what the agent decides on its own.

1. In the chat's mode picker choose **Interactive** (on a Local session, **Agent**).
2. Paste this request:

   ```text
   Make a one-page report for the shop owner from data/orders-2026-q1.csv: revenue by month as a chart, and revenue by product.
   ```

3. Expand the steps. The agent reads the CSV, then chooses a file format, a way to draw the chart and how to do
   the sums. Your request settled none of those.
4. If the chat stops to ask before running a command, read the command first:
   - It installs something (`pip install`, `npm install`): choose **Skip** and reply
     `No installs, please. Write the report in Markdown with the chart as an SVG file.`
   - It only reads the CSV and prints totals: your choice. **Allow** it once if you can tell what it does
     ([Lab 06](../06_Agent_With_Limits/) covers approvals), or **Skip** it, and the agent works from the file it read.
5. Open the report. For a Markdown file (`.md`), right-click it in the Explorer and choose **Open Preview**
   (**Ctrl+Shift+V**, **Cmd+Shift+V** on macOS). For an HTML file, right-click it, choose **Reveal in File
   Explorer** (**Reveal in Finder** on macOS, **Open Containing Folder** on Linux) and open it in your browser.

Checkpoint: a report file and a chart of revenue by month, with a product breakdown. Format, file names and layout
vary from run to run. If the report has no product breakdown, reply `Add revenue by product as a table.` before
you go on.

## Part C: Check one number

1. Find Gift box in the report's product breakdown and compare it with Part A.
   - **172.50**: the agent left the cancelled orders out.
   - **276.00**: it counted them as sales.
   - Anything else: an arithmetic slip. Reply `List the Gift box rows you added for that number.`
2. Search the report for `cancel`. Does it tell the shop owner what it did with cancelled orders? Without that
   line, even a right number leaves the reader guessing.
3. See what is at stake. If your report counted the cancelled orders, it is in front of you; if not, open
   [resources/with-cancelled](resources/with-cancelled/), a report we wrote that counts them. Counted, they make
   Gift box the best seller and March lower than February (372.00 against 386.00). Paid sales in fact grew, from
   282.50 to 321.00, and Herbal tea sold most.
4. Whatever you got, send this follow-up, so the report states its rule:

   ```text
   Count completed orders only; cancelled orders are not sales.
   Under the total, say how many cancelled orders were left out and what they were worth.
   ```

5. Open the report again and check Gift box once more.

Checkpoint:

| In the report | Value |
|---|---|
| Total revenue | 772.75 from 37 completed orders |
| Left out | 3 cancelled orders, worth 183.50 |
| By month | January 169.25, February 282.50, March 321.00: each bar higher than the last |
| Gift box | 172.50 |
| Top product by revenue | Herbal tea 100 g, 209.25 |

One well-chosen number tests both the agent's rule and its sums. If it is wrong, ask for the rows behind it before
you trust anything else in the report.

## Part D: Read the cost, then do it in one request

Every response uses AI credits from your monthly allowance (1 credit is 0.01 US dollars). The more the model reads
and writes, the more it costs.

1. **Each response.** Hover over each of Copilot's responses in this chat, from Part B to Part C. A small panel
   shows the credits that turn used. Write them down, one line per turn.
2. **The session.** Hover over or select the context window control in the chat input. It shows the chat's total
   credits and how many tokens (pieces of text the model reads) the conversation holds. If your Chat view has no
   such control, add up the numbers from step 1.
3. **The month.** Select the Copilot icon in the Status Bar at the bottom of VS Code. The dashboard shows how much
   of this month's allowance you have used.
4. Look at the follow-up from Part C: two lines, but the model read far more. Each turn sends the model the whole
   conversation so far: your requests, the CSV, the report it wrote, any command output. So a follow-up that fixes
   a vague request is never free.
5. Now ask once, saying up front what Parts B and C had to add later. Start a **New Chat** (it starts with no
   history), keep **Interactive** and the same model, and paste:

   ```text
   Write a one-page Markdown report for the shop owner in report/q1-sales.md from data/orders-2026-q1.csv.
   Count completed orders only, and say how many cancelled orders were left out and what they were worth.
   Include total revenue and orders, revenue by product as a table, and revenue by month as a bar chart
   saved as report/revenue-by-month.svg and shown in the report.
   Use only data/orders-2026-q1.csv, and don't install anything.
   ```

6. Open `report/q1-sales.md` in the preview and check Gift box again: 172.50, and a line about 3 cancelled orders.
7. Hover over the response and note its credits. Then fill in this table for your two chats:

   | | First chat (Parts B and C) | Second chat (one request) |
   |---|---|---|
   | Turns you sent | | 1 |
   | Commands it asked to run | | |
   | Gift box right the first time? | | |
   | Credits, all turns | | |

Checkpoint: the second chat's report has the same numbers as Part C's checkpoint, after one request. You have the
credits for both chats side by side.

This is an informal comparison, one run of each: credits for the same request vary, and **Auto** may pick a
different model each time. What usually holds is the shape. A request that names the data, the rule, the output and
the limits leaves the agent less to decide and you less to fix, and every turn you avoid is one less re-reading of
the conversation.

## If your run looks different

| What you see | What to do |
|---|---|
| The agent asks to install a package such as `matplotlib` | Choose **Skip** and reply with the Markdown and SVG line from Part B step 4 |
| The chart does not show in the Markdown preview | The image link must point at the SVG file from the report's own folder, for example `revenue-by-month.svg`. Ask: `The chart doesn't show in the Markdown preview. Fix the image link.` |
| The report is HTML and VS Code shows its code | Open it in a browser, as in Part B step 5 |
| No credits appear when you hover | Hover over Copilot's response, not your request. If still nothing, open the Copilot dashboard from the Status Bar; on some plans usage appears only there or on GitHub's billing pages |

## What you can do now

- Ask Copilot for a report from a CSV file and open it, chart included.
- Work out one number from the data first and use it to test the report's rule and its sums.
- Read the credits for a response, a chat and the month.
- Write a request that settles the rule, the output and the limits up front, and compare what it cost with your
  first try.

## Challenge

1. **The same question in two places.** In your first chat, ask `Which product sold the most units?` Then, in a
   **New Chat**, ask `Which product sold the most units in data/orders-2026-q1.csv? Count completed orders only.`
   Expected both times: Herbal tea 100 g, 31 units. Compare the credits: the long chat sends its history along.
2. **Check a number the agent worked out.** Slips hide in derived numbers. Ask in your second chat:
   `By how much did March revenue change compared with February?` Check it with a calculator from the Part C
   checkpoint: (321.00 − 282.50) / 282.50. Expected: up about 13.6%. If the
   answer is down about 3.6%, the cancelled orders came back in.

Answers to compare with when you finish, for the lab and the challenge: [`solved/`](solved/).

## Going further

- **Shorter chats.** Start a new chat when you change topic. `/compact` replaces older turns with a summary, and
  `/fork` (or **Fork Conversation**) branches a chat without repeating what came before.
- **Model choice.** Hover over a model in the model picker to see its cost tier. A cheaper model that needs two
  extra follow-ups can cost more than a stronger one that gets it right the first time.
- **Make the rule permanent.** Put "count completed orders only" in `.github/copilot-instructions.md`
  ([Lab 04](../04_Team_Rules/)) or save the Part D request as a skill ([Lab 05](../05_Make_A_Skill/)). Check it
  pays: run the Part B request in new chats with and without it, check Gift box, compare credits. An instructions
  file is sent with every request in the folder.
- **Where usage shows.** The [saving tokens guide](../guides/saving-tokens.md) lists every place, including
  Business and Enterprise plans.

## Resources

- [Optimize your usage](https://code.visualstudio.com/docs/agents/guides/optimize-usage) (VS Code docs): where
  each usage number appears and what drives it
- [Usage-based billing for individuals](https://docs.github.com/en/copilot/concepts/billing/usage-based-billing-for-individuals)
  (GitHub Docs): what an AI credit is and how tokens are priced
- [Markdown in VS Code](https://code.visualstudio.com/docs/languages/markdown): the preview and how it shows
  images
