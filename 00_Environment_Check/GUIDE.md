# Lab 00: How to check that VS Code, Copilot and the project are ready

## Goal

Check your Copilot access and establish a passing project before any agent edits it. If a feature is missing,
you will have a specific finding and a next action instead of discovering it during another lab.

## What you will learn

- Open the project folder and check which instructions Copilot discovered.
- Distinguish the harness, its interaction mode, and its permission level.
- Record available features and identify questions for your Copilot administrator.
- Run the Python, Java, SQL and dbt baselines with uv and the Maven Wrapper.
- Find monthly credit usage and the token and credit details for a chat response.

Keep [the environment record](resources/environment-record.md) open outside `orders-analytics/`, and write your
results as you go. Copy it to your own notes folder; do not fill the shared template in the repository.

## Part A: Open the project and check your account

This part identifies the folder the agent will work in and the account that grants your Copilot access.

1. Clone the repository using the URL supplied to you. In VS Code, choose **File > Open Folder** and select
   `agentic-workflows-github-copilot/orders-analytics/`. The Explorer should show `python/`, `java/`, `sql/`,
   `dbt/` and `.github/`. The numbered lab folders should be outside that Explorer root.
2. Open **Source Control**. It should show the parent `agentic-workflows-github-copilot` repository on `main`.
   The project setting `git.openRepositoryInParentFolders: "always"` enables this. If it is missing, run
   `git rev-parse --show-prefix` in a terminal in `orders-analytics/`: the result should be `orders-analytics/`.
   Confirm you selected the folder inside the clone before changing an editor setting.
3. Open **Code > About Visual Studio Code** on macOS, or **Help > About** on Windows/Linux. Record the version.
   This guide was checked with 1.141.0; update an older editor through your approved install route.
4. Open the **Copilot status** dashboard in the status bar. Record the plan and monthly credits used. If it asks
   you to sign in, use the GitHub account that has your Copilot seat. Our dashboard showed Copilot Student and
   1% used. Your plan and percentage will differ.

Checkpoint A: the correct folder, parent repository, editor version and account plan are recorded. The project
folder keeps lab text out of normal project exploration; it is not a filesystem access restriction.

## Part B: Check the harness and modes

This part separates three controls that can otherwise look like one setting.

A **harness** runs the agent loop and its tools. A **mode** changes how it proceeds, such as planning first. A
**permission level** decides which actions ask for your approval. Changing the model does not change the harness.

1. Open Chat with **Toggle Chat**. Start a **New Chat**, open **Session Target**, and select **Copilot**.
2. Open the mode control below the chat input. Record the offered names. Our Copilot harness offered
   **Interactive**, **Plan** and **Autopilot**; its agent picker offered **Agent** and extension-provided agents,
   with no built-in **Ask** role. Local sessions have a different role picker. Do not assume an answer-only role
   exists on your chosen target.
3. Keep **Interactive** and **Manual permissions** for this check. Inspect the current setting; avoid enabling
   broader permissions to make a missing feature appear. A request to “read only” is guidance to the model,
   so still inspect the tools it uses.

Checkpoint B: you can name the selected harness, interaction mode and permission level separately. If Copilot is
absent from Session Target, record that and review the [harness prerequisites](https://code.visualstudio.com/docs/agents/run/agent-harnesses).

## Part C: Record feature availability

This part tells you which later exercises you can attempt with the current account and environment.

1. Open the model picker and record what it offers. Our Student seat offered Auto; every reference question
   below used that selection. Use the models available to your account.
2. Enter `/skills` in chat and submit it. Record whether it is recognised and whether any skills are listed.
   Ours listed 30 skills from installed extensions and personal folders. A list proves discovery; it does not
   prove a particular skill was used by the model. An empty list is a valid result before you install project skills.
3. Open **Chat: Open Customizations** from the Command Palette, or **Open Customizations** in Chat. Select
   **Instructions**. Look for the project files, rather than assuming a file on disk was loaded. After starting
   a fresh chat, ours listed both `copilot-instructions.md` files and `java.instructions.md` as Loaded. The small
   file at the parent Git root links to the conventions inside the project: Copilot's always-on file discovery
   uses the Git root. We also saw the parent `AGENTS.md`, so opening a subfolder does not hide ancestor instructions.
4. Select **Hooks** in that editor. Record whether the section is offered or restricted. Our editor offered it
   with no hooks configured. A visible editor does not prove a hook executes or blocks an action; that check belongs
   to the lab that installs a hook. Use the [hook reference for your harness](https://code.visualstudio.com/docs/agent-customization/hooks).
5. Optional: in the terminal run `copilot --help`. Record whether the CLI starts. If the shell cannot find it,
   record “not installed”; that does not establish a policy block. Install it only through your organisation's
   approved route if you need a later CLI exercise.
6. For any unavailable feature, record the observation and who can resolve it. Ask your Copilot administrator
   about agent mode, model availability, preview features, hooks and CLI access as applicable. Record a policy as
   confirmed only after you see the managed setting or the administrator confirms it.

Checkpoint C: each feature has an observation, a status, and a next action if needed. We could not test Agent
Skills with a Copilot Free seat: the active seat was Student. GitHub's plans page excludes “Copilot Chat skills in
IDEs” on Free, but this session did not establish how that applies to Agent Skills. Check your actual seat before
relying on skills. We also could not access a Codespace for this project; the local results do not certify
Codespaces. Use the local route in this guide.

## Part D: Run the project checks

This part establishes the baseline that later changes must preserve. All commands begin in `orders-analytics/`.
The data is synthetic and bundled; the SQL database is recreated from a fixed seed.

1. Check the tools the shell sees:

   ```sh
   uv --version
   java -version
   git --version
   ```

   Our runs used uv 0.12.5 and JDK 21. If Java reports a different major version, select your Java 21 installation
   using your approved JDK setup instructions and reopen the terminal. A JDK is needed for compilation.

2. Create the project environment from its lock:

   ```sh
   uv sync --locked
   ```

   uv creates `.venv/` in this folder and uses the pinned Python selection. Run **Python: Select Interpreter**
   and select this project's `.venv`. The commands below use `uv run`, so they also work without shell activation.

3. Run all four checks with the script outside the agent's project:

   ```sh
   uv run python ../00_Environment_Check/resources/check_setup.py
   ```

   It runs Python tests, the Maven Wrapper, a database rebuild and row counts, and dbt models and tests. Its exit
   status is nonzero if any baseline fails; it still runs the remaining checks. `--verbose` prints full outputs.
   Our fresh copy and working project both ended with:

   ```text
   Python 3.13.15
   PASS  pytest: 5 passed
   PASS  Maven Wrapper: 5 tests, 0 failures, 0 errors, 0 skipped
   PASS  SQL row counts: customers 300, orders 100,000, line_items 249,285, slow_orders.sql rows 85,045
   PASS  dbt build: PASS=17 WARN=0 ERROR=0 SKIP=0 TOTAL=17
   4/4 baselines passed
   ```

4. If a check fails, run that check on its own to read the complete output. Each command below starts from the
   project folder. On Windows, replace `./mvnw` with `.\mvnw.cmd`.

   ```sh
   cd python
   uv run --project .. python -m pytest -q
   cd ..
   ```

   ```sh
   cd java
   ./mvnw test
   cd ..
   ```

   ```sh
   uv run python sql/build_db.py
   uv run python sql/run_query.py sql/row_count.sql
   ```

   ```sh
   cd dbt
   uv run --project .. dbt build --profiles-dir .
   cd ..
   ```

   Maven should report `Tests run: 5, Failures: 0, Errors: 0, Skipped: 0` and `BUILD SUCCESS`. The first online run
   downloaded the pinned compiler 3.16.0, Surefire 3.6.0 and JUnit 5.14.4 successfully. dbt runs 2 seeds, 3 models
   and 12 data tests; its full summary also includes zero `NO-OP` and `REUSED` counts. The row-count query returns
   four rows; its last row is the 85,045 complete orders.

5. Run `git status --short`. In a clean committed clone, only ignored build outputs should have been created,
   leaving this output empty. If it lists source changes, read the diff and resolve them before using a later
   lab's baseline. Save your four results in the environment record.

Checkpoint D: four passing baselines. These counts describe the starting project; they are not targets to
force after a later feature adds a test. If you omit Java, record it as skipped and do not mark the full setup
ready for Java labs.

## Part E: Read a file with Copilot and inspect usage

This part checks one agent action against the source and makes its usage visible.

1. In a fresh Copilot chat, keep Interactive and Manual permissions and send:

   ```text
   Read python/orders/report.py and python/tests/test_report.py. Name the existing test function that checks exact revenue. Use only file-reading tools. Do not edit files, run terminal commands, or access external services.
   ```

2. Expand the completed steps. Check that Copilot read the two named files, then open the test file yourself
   and find the function it named. Decline an unexpected edit, terminal command or external-service request.
   Our three fresh chats used two file reads each and named the correct test; the Python sources were unchanged.
3. Hover over the response's completion details to see its credits and token counts. Record the cost for this
   response. Our three costs were 2.4, 0.3 and 0.3 credits. Parts A–D used no model responses. Installed tools and
   personal skills contribute context, and caching can change cost between fresh chats.
4. Look for the **context window control** in the chat input. If present, open it and record the session tokens
   and credits separately from this response. The [usage documentation](https://code.visualstudio.com/docs/agents/guides/optimize-usage)
   describes it. It was absent in our tested Copilot Chat view even with the chat expanded; we recorded “not shown”
   and used response details. Do not label a sum of input tokens across tool steps as the current context size.
5. Open **Copilot status** again to locate monthly usage. Run `git status --short` and compare with the state
   before the request: there should be no new project edits.

Checkpoint E: an answer verified in the file, observed file-reading calls, no source changes, and response usage
recorded. One successful read does not certify the behavior of a future editing task.

## Troubleshooting

These three failures were triggered in the build copy and recovered before its final passing run.

| Observed message | What to check | Recovery |
|---|---|---|
| `sql/orders.duckdb not found: run  python sql/build_db.py  first` | The database has not been built in this project | From `orders-analytics/`, run `uv run python sql/build_db.py`, then rerun the row-count query |
| `Could not find profile named 'orders_dbt'` | dbt was pointed at `../python`, which has no `profiles.yml` | From `orders-analytics/dbt/`, run `uv run --project .. dbt build --profiles-dir .` |
| `The JAVA_HOME environment variable is not defined correctly,` | The selected JDK path exists and contains Java tools | Select your installed JDK 21 using your platform's setup instructions, reopen the terminal, run `java -version`, then rerun `./mvnw test` in `java/` |

If Maven cannot download artifacts, save the named URL and error for your administrator and use the approved
Maven mirror or proxy. Do not change the plugin pins to make a network restriction look like a passing setup.

## What you can do now

- Open the project and verify its discovered instructions instead of assuming they loaded.
- Name the harness, mode and permissions you will use.
- Separate an unavailable feature from a confirmed organisation policy.
- Establish and record four passing baselines with the project tools.
- Inspect a response's usage and locate monthly usage, recording a missing session control honestly.

## Challenge

1. Complete your environment record. Each required row needs a result; every unavailable or untested feature
   needs a next action. The expected outcome is a readiness decision based on evidence from your machine.
2. Start a fresh read-only chat and ask where `load_orders` gets its default input data. Inspect the file reads
   and verify the answer in `python/orders/report.py`. The expected outcome is a correct source path, no edits,
   and a recorded response cost. Do not repeat the call to match someone else's credit value.

## Resources

- [VS Code harnesses](https://code.visualstudio.com/docs/agents/run/agent-harnesses): targets, modes and permissions.
- [Custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions): discovery and verification.
- [Agent Skills](https://code.visualstudio.com/docs/agent-customization/agent-skills): skill locations and loading.
- [Hooks](https://code.visualstudio.com/docs/agent-customization/hooks): select the correct implementation.
- [GitHub Copilot plans](https://docs.github.com/en/copilot/get-started/plans): your seat's supported features.
- [Usage controls](https://code.visualstudio.com/docs/agents/guides/optimize-usage): credits and tokens at three scopes.
- [uv projects](https://docs.astral.sh/uv/guides/projects/) and [Maven Wrapper](https://maven.apache.org/tools/wrapper/): repeatable installs.

[Back to Lab 00](README.md) · [Back to the lab list](../README.md)
