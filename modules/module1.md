# Module 1: Project Scaffolding

In this module we set up the `todd` project from scratch — Python packaging, a CLI
framework, code quality tooling, and a status line. Everything built here is the
foundation every subsequent module builds on.

---

## Before You Begin: What is Git?

This workshop uses **git** for version control. If you're new to git, here's what
you need to know:

- **Repository (repo)** — a folder whose history git tracks. This project is one.
- **Commit** — a snapshot of your changes, with a message describing what changed.
- **Branch** — a parallel line of work. We use branches to isolate each module's changes.
- **Push** — sends your local commits to a remote server (GitHub) so others can see them.

That's your git primer — it's all you need to follow along.

---

## What is Claude Code?

Claude Code is Anthropic's official **agent harness** — a framework that wraps a
foundation model with tools, context management, memory, and workflow orchestration.

| Layer | What it provides | Example |
|-------|-----------------|---------|
| **Model** | Raw intelligence | Claude Sonnet, Opus, Haiku |
| **Agent harness** | Tools + context + memory + orchestration | Claude Code |
| **Your configuration** | Project-specific behavior | CLAUDE.md, hooks, commands |

A chat interface sends your message and shows a reply. An agent harness lets Claude
read your files, run your tests, edit your code, and coordinate multi-step workflows —
all within guardrails you define. This workshop teaches you to configure those guardrails.

---

## Key Concepts

| Concept | Why it matters |
|---------|---------------|
| **Back pressure** | A mechanism that actively resists bad output rather than silently accepting it. Pre-commit hooks are one form: they block a commit until quality gates pass, forcing Claude to fix issues immediately rather than drifting from standards. |
| **Project scaffolding** | The initial structure, tooling, and configuration that all subsequent development builds on. A well-scaffolded project enforces quality from the first commit. |

---

## Glossary

| Term | Definition |
|------|-----------|
| **UV** | A fast Python package and project manager. Replaces pip, virtualenv, and pip-tools with a single tool. We use it to manage dependencies and run the CLI. |
| **Typer** | A Python library for building CLI applications using type hints. Minimal boilerplate — define a function, add type annotations, get a fully functional CLI command. |
| **Pre-commit hook** | A script that runs automatically before each `git commit`. Used to enforce code quality gates — linting, type checking, security scanning — before changes enter version control. |
| **CLAUDE.md** | A markdown file that provides persistent project instructions to Claude, loaded automatically every session. Exists at three scopes — global, project, and personal — so teams share conventions while individuals keep local overrides. |
| **Status line** | A persistent display at the bottom of the terminal showing session state — model, context usage, working directory, and git status. Configured once; visible in every session. |

---

## Tools in this module

**Built-in tools**

| Tool | What it does |
|------|-------------|
| `Write` | Creates a new file |
| `Edit` | Makes targeted edits to an existing file |
| `Bash` | Runs a shell command |
| `Read` | Reads a file from the filesystem |

---

## 1. Launch Claude

Open a terminal and launch Claude from the project directory:

```shell
claude
```

> **Note:** If `claude` isn't found, the binary may not be on your system `PATH`.
> Run `which claude` to check, or see the Claude Code installation docs.

---

## 2. Build the Project Scaffold

In the chat box, enter:

> **Approving tool calls:** As Claude works, it will pause to show you each tool call
> and ask for approval. Review what it plans to do and press **Enter** to accept, or
> type `no` to reject. You can also type `!` before a message to run a shell command
> directly.

```markdown
Let's setup our project scaffolding utilizing UV with a src layout. We will be creating a Typer cli application with the name of todd. It should be a single default command that accepts an optional positional prompt argument — running `uv run todd` with no argument prints a greeting. Also setup pre-commit with ruff, mypy, bandit, vulture, and xenon hooks.
```

Claude will create the project structure: `pyproject.toml`, the `src/todd/` package,
a default command wired up with Typer, and code quality tooling.

> **What just happened?** Claude used `Write` and `Bash` to build the entire
> project structure — no manual file creation needed. Claude harnessed our existing
> tooling to respond to our natural language request. CLAUDE.md provided the project
> instructions that shaped everything Claude just built.

Now install the pre-commit hooks Claude created and validate they pass:

```shell
!uv run pre-commit install
!uv run pre-commit run --all-files
```

> **Tenet 3: CLAUDE.md + hooks.** Pre-commit hooks enforce quality from the
> first commit — this is *deterministic* quality. Unlike asking Claude to "be
> careful," a hook guarantees the check runs every time. CLAUDE.md provided the
> project instructions that shaped everything Claude just built. Together, they
> form persistent memory (CLAUDE.md) plus automated gates (hooks).
> This is one form of back pressure we can utilize to drive quality output.

---

## 3. Verify the Setup

Test the new command directly from the chat box using the `!` prefix to run shell commands:

```shell
!uv run todd
```

You should see a greeting message printed to the terminal.

> **Tenet 1: Verify your work.** This manual test is a spot-check — it proves
> the CLI works *right now*. In Module 2, we'll upgrade from manual verification
> to automated tests that catch regressions permanently.

---

## 4. Your First CLAUDE.md

CLAUDE.md is the single most impactful Claude Code feature. It provides persistent
project instructions that load automatically every session.

**Three scopes:**

| Scope | File | Shared via git? |
|-------|------|----------------|
| Global (all projects) | `~/.claude/CLAUDE.md` | No |
| Project (team-wide) | `./CLAUDE.md` | Yes |
| Personal (local only) | `./CLAUDE.local.md` | No (gitignored) |

> Project memory can also live at `./.claude/CLAUDE.md`. When scopes overlap,
> project-level instructions take precedence over global.

**Exercise:** Ask Claude to build a proper CLAUDE.md for the project. In the chat box, enter:

```markdown
Create a project CLAUDE.md that covers:
- Project description: todd is a Typer CLI application built as part of the Claude Code workshop
- Tech stack: Python 3.13+, uv, pytest, Typer
- How to run tests: uv run pytest
- How to run the CLI: uv run todd
- Coding standards: ruff (rules E, W, F, I, N, UP, B, C4, PLC, PLE, PLW, RUF), mypy strict
- Commit conventions: conventional commits

Also update the project configuration (pyproject.toml) to match these standards — configure the ruff rules and enable mypy strict mode.
```

> **Callout:** This CLAUDE.md will shape Claude's behavior for the rest of the workshop.
> Every module builds on it. A well-written CLAUDE.md eliminates the need to repeat
> project context in every prompt.

---

## 5. Configure the Status Line

The status line gives you a persistent heads-up display at the bottom of the terminal.
In the chat box, run:

```markdown
/statusline Show {model short name} | {context}% context | {cwd} | {git_status} | {branch} where git status is green "clean" or yellow "modified" using ANSI colors, and omit git fields if not in a repo.
```

> **What just happened?** `/statusline` is a built-in Claude Code slash command that configures a persistent display at the bottom of your terminal.
> You'll see the active model, how much of the context window is in use, your working directory, and the git status.
> This HUD becomes more useful in later modules as context management and model switching become part of your workflow.
> There are many other built-in slash commands you can see if you just type `/` in the chat window.
> For a full list, see the [Anthropic docs on slash commands](https://code.claude.com/docs/en/interactive-mode#built-in-commands).

> **Windows / PowerShell users — two options:**
>
> **Option A (Quick):** Run `/statusline` and include this hint in your prompt:
> "Use PowerShell-compatible syntax — avoid backticks and ANSI escape sequences."
>
> **Option B (Manual):** Copy `scripts/statusline.ps1` to `~\.claude\statusline.ps1`,
> then add a `statusLine` entry to `~\.claude\settings.json`:
> ```json
> {
>   "statusLine": "powershell.exe -NoProfile -File ~/.claude/statusline.ps1"
> }
> ```

> **Pro tip:** Type `/cost` to see token usage and spend for this session, or
> `/stats` for daily patterns. Cost awareness grows more important in later modules.

---

## 6. CLI Navigation Essentials

Now that the project is scaffolded, let's learn the shortcuts you'll use every day.

**`@` file references** — type `@pyproject.toml` in the chat box to reference a file
without copying its full content. Claude reads the file on demand.

**`!` bash mode** — prefix with `!` to run shell commands directly (you already used
this in step 3). It's shorthand for asking Claude to run a Bash tool call.

**Multiline input** — `\` + Enter for a quick line continuation, or `Shift+Enter` for
a new line in the prompt.

**`Ctrl+G`** — open the current prompt in your default text editor for longer edits.

**`Esc+Esc`** — open the rewind menu to undo Claude's changes (code, conversation,
or both). Useful when Claude goes in a wrong direction. Note: only tracks file edits
via Write/Edit tools, not changes made by bash commands.

> **Exercise:** Type `@src/todd/__init__.py` to reference the init file, then run
> `!uv run todd` to verify the CLI still works.

---

## 7. Hands-On: Claude Code for Non-Coding Tasks

Claude Code isn't just for developers. These exercises demonstrate the same agentic
capabilities applied to everyday knowledge work tasks.

> **Prerequisite: Install document skills**
> Before starting, add the Anthropic skills marketplace and install the document-skills plugin:
> ```shell
> claude plugin marketplace add anthropics/skills
> claude plugin install document-skills@anthropic-agent-skills --scope user
> ```
> This gives Claude the ability to create PowerPoint and Excel files directly.
> Restart Claude Code after installing.

---

### Exercise 1: Data Transformation

A sample sales report lives at `data/sales_report.csv`. Ask Claude:

```
Read @data/sales_report.csv and create a formatted Excel spreadsheet with
a summary sheet showing totals by region and a chart of monthly trends.
Save it to data/sales_summary.xlsx
```

> *What to notice:* Claude reads the CSV, creates a multi-sheet .xlsx with
> formulas and charts — no Python script required.

---

### Exercise 2: Research → Presentation

Ask Claude to research a topic and produce a slide deck:

```
Research the repository https://github.com/anthropics/claude-code — what
it does, key features, and how to get started. Create a 5-slide PowerPoint
overview deck and save it to data/claude_code_overview.pptx
```

> *What to notice:* Claude uses web search and the gh CLI to gather info,
> then synthesizes it into a formatted presentation with slides, titles,
> and bullet points.

---

### Exercise 3: Document Generation

A meeting transcript lives at `data/meeting_notes.txt`. Ask Claude:

```
Read @data/meeting_notes.txt and create a structured action-item tracker.
Extract every action item, assign owners where mentioned, set due dates
from context, and save it as data/action_items.md
```

> *What to notice:* Claude parses unstructured text, extracts structured
> data, and produces a formatted deliverable.

---

## 8. Commit and Proceed

Ask Claude to commit the changes (including the CLAUDE.md update), then advance to
the next module:

```markdown
Commit the changes and then run /module to proceed to module 2.
```

---

[Module 2 →](module2.md)
