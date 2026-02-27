# Module 1: Project Scaffolding

In this module we set up the `todd` project from scratch — Python packaging, a CLI
framework, code quality tooling, and a status line. Everything built here is the
foundation every subsequent module builds on.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **UV** | A fast Python package and project manager. Replaces pip, virtualenv, and pip-tools with a single tool. We use it to manage dependencies and run the CLI. |
| **Typer** | A Python library for building CLI applications using type hints. Minimal boilerplate — define a function, add type annotations, get a fully functional CLI command. |
| **Status line** | A persistent display at the bottom of the terminal showing session state — model, context usage, working directory, and git status. Configured once; visible in every session. |
| **Pre-commit hook** | A script that runs automatically before each `git commit`. Used to enforce code quality gates — linting, type checking, security scanning — before changes enter version control. |
| **Project scaffolding** | The initial structure, tooling, and configuration that all subsequent development builds on. A well-scaffolded project enforces quality from the first commit. |

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

## 1. Clone and Launch

Clone the repository and launch Claude from the project directory:

```shell
git clone https://github.com/shiftysheep/cc-workshop.git
cd cc-workshop
claude
```

> **Note:** If `claude` isn't found, the binary may not be on your system `PATH`.
> Run `which claude` to check, or see the Claude Code installation docs.

---

## 2. Build the Project Scaffold

In the chat box, enter:

```markdown
Let's setup our project scaffolding utilizing UV. We will be creating a Typer cli application with the name of todd. Include a hello command.
```

Claude will create the project structure: `pyproject.toml`, the `src/todd/` package,
a `hello` command wired up with Typer, and code quality tooling (ruff, mypy,
pre-commit).

> **What just happened?** Claude used `Write` and `Bash` to build the entire project structure — no manual file creation needed.
> Claude harnessed our existing tooling to respond to our natural language request.
> Notice the pre-commit hooks in the output — these instructions came from our CLAUDE.md that was predefined.
> Now every commit from here will run linting and type checking automatically, enforcing quality from the start.
> This is one form of back pressure we can utilize to drive quality output.

> **Tenet 3: CLAUDE.md + hooks.** Pre-commit hooks enforce quality from the
> first commit — this is *deterministic* quality. Unlike asking Claude to "be
> careful," a hook guarantees the check runs every time. CLAUDE.md provided the
> project instructions that shaped everything Claude just built. Together, they
> form persistent memory (CLAUDE.md) plus automated gates (hooks).

---

## 3. Verify the Setup

Test the new command directly from the chat box using the `!` prefix to run shell commands:

```shell
!uv run todd hello
```

You should see `Hello. How can I assist?` (or similar) printed to the terminal.

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

**Exercise:** Update the project `CLAUDE.md` with proper structure:

```markdown
Update the project CLAUDE.md to include:
- Project description: todd is a Typer CLI application built as part of the Claude Code workshop
- Tech stack: Python 3.13+, uv, pytest, Typer
- How to run tests: uv run pytest
- How to run the CLI: uv run todd
- Coding standards: ruff (rules E, W, F, I, N, UP, B, C4, PLC, PLE, PLW, RUF), mypy strict
- Commit conventions: conventional commits
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
> `!uv run todd hello` to verify the CLI still works.

---

## 7. Commit and Proceed

Ask Claude to commit the changes (including the CLAUDE.md update), then advance to
the next module:

```markdown
Commit the changes and then run /module to proceed to module 2.
```

---

[Module 2 →](module2.md)
