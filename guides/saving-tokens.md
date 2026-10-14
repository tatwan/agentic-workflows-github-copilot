# Comparing usage for a correct result

Checked 14 October 2026 against [GitHub's billing explanation](https://docs.github.com/en/copilot/concepts/billing-and-usage/individuals/billing)
and [VS Code's usage guide](https://code.visualstudio.com/docs/agents/guides/optimize-usage).
Rates, allowances and UI controls can change; use the current documentation for your plan.

## What affects usage

Copilot model requests consume tokens: input, output and cached context can have different prices. GitHub converts
this usage to AI credits; one credit represents $0.01 USD. A visible chat response can involve several model calls
and tool results. Code completions and next edit suggestions are not billed in AI credits on paid plans.

Avoid estimating a task's cost from its last message or the length of its visible transcript. Context selection,
caching and compaction can change the billed input. A long follow-up can reuse cached context; a short message can
still require substantial new work. Exact rates and discounts belong in the current pricing page rather than a
fixed example in this guide.

## Make the comparison useful

| Keep or record | Why |
|---|---|
| The same input files and correctness checks | A wrong report is not a cheaper equivalent result |
| Separate untouched workspace copies and New Chats | Earlier generated files can supply the second answer |
| Model, mode and selected tools | Different settings can explain a difference in usage |
| Every turn, repair and retry | The whole task is the comparison unit |
| Permission waits and elapsed time | Waiting on a person differs from model processing time |
| More than one run of each approach | One pair shows an observation, not a general saving |

A fixed model helps a controlled comparison. If your plan only offers Auto, record that constraint and the routed
model if visible; do not claim the model was held constant. Start a new chat when the task changes. Keep a short
record of decisions to carry into the next chat instead of assuming it remembers them.

## Read the numbers your UI exposes

Hover over responses for per-response credits where available. Some sessions expose a context control with tokens
and session usage; others do not. The Copilot status dashboard and account usage pages show allowance or cycle
usage. A monthly percentage cannot isolate one lab. Write `unavailable` when no per-task figure is visible, and
compare correctness, steps and elapsed time instead of inventing a credit total.

[Lab 08](../08_Analyze_Data_And_Cost/) compares two report workflows against the same completed-sales totals. Keep
the generated reports and your comparison sheet with the completed folders. A clear request can remove avoidable
decisions and repairs; check the actual result before concluding it saved time or credits.
