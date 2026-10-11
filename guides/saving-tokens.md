# Saving tokens and AI credits

Checked 6 Oct 2026 against GitHub Docs. Rates and allowances change; check GitHub's models-and-pricing page
before you budget.

## How a request is billed

Since 1 June 2026, chat, agent and other AI features in Copilot bill in **AI credits**. One AI credit
is $0.01 of model usage, worked out from the tokens a request uses and that model's prices. Code completions
and next edit suggestions are not billed.

```text
cost    = new input tokens x input price
        + cached tokens    x cached-input price
        + cache-write tokens x cache-write price   (Anthropic and newer OpenAI models)
        + output tokens    x output price          (prices per million tokens)
credits = cost / $0.01
```

Output costs about 5 to 8 times input, because the model needs one pass for each token it writes. Cached
input costs about a tenth of input, because the provider reuses work it already did for the same prefix.

**Worked example** (ILLUSTRATIVE token counts, Claude Sonnet 5.5 prices checked 6 Oct 2026): one agent turn
sends 40,000 tokens, 32,000 of them cached, and writes 1,200. New input 8,000 x $2.00 = 1.60 credits; cached
32,000 x $0.20 = 0.64; output 1,200 x $10.00 = 1.20; total 3.44 credits. With nothing cached the same turn
costs 9.20 credits; on GPT-5 mini, 0.52.

## Why long sessions cost more

Each agent turn sends the context window again: system instructions, tool definitions, instructions files,
the conversation so far and every tool result. History and tool results grow every turn, so a long session
costs more than its last message suggests. These reset the cache, so the next turn pays full input price:
switching model, returning to an old session after the cache has expired, changing reasoning level or
context size, adding or removing tools or MCP servers.

When the window fills, Copilot compacts older conversation into a summary; `/compact` does it on request.
The summary can drop details. For an unrelated task, start a new chat instead.

## Habits that cut usage

| Habit | Why it helps |
|---|---|
| Pick the model tier for the task | A small model is often enough for a well-scoped change |
| Give a clear task, context and stopping condition | Fewer turns spent searching and guessing |
| Start a fresh chat for an unrelated problem | A long thread re-sends its whole history every turn |
| Keep one model per session | Switching resets the cache |
| Research, plan, then implement, as separate steps | Each step stays short and checkable |
| Use tests and linters to catch errors early | Fewer turns spent fixing late mistakes |

Auto model selection takes 10% off model costs on paid plans. Keep instructions files short: they are
re-sent with every request.

Compare runs by **credits per correct result**, not credits per run. A cheap run that fails and is redone
costs more.

## Where to see what you used

| Where | What it shows |
|---|---|
| Copilot status dashboard (VS Code status bar) | Percentage of your monthly AI credits used |
| Context window control (chat input) | Tokens, breakdown, credits for this session |
| Business, Enterprise: Copilot settings, Usage | Usage this cycle, out of your user budget if one is set |
| Individual plans: Billing and licensing, AI usage | Your usage over time |

[Lab 08](../08_See_And_Lower_Session_Cost/README.md) measures three runs of the same task and their credits. Lab 08 is planned and will record its own measured runs.
