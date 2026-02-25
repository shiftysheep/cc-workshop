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

> **What just happened?** Claude used `Write` and `Bash` to build the entire project
> structure — no manual file creation needed. This is Claude Code as a scaffolding
> tool: describe what you want, get a working foundation. Notice the pre-commit hooks
> in the output — every commit from here will run linting and type checking
> automatically, enforcing quality from the start.

---

## 3. Verify the Setup

Test the new command directly from the chat box using the `!` prefix to run shell
commands:

```shell
!uv run todd hello
```

You should see `Hello from todd.` (or similar) printed to the terminal.

---

## 4. Configure the Status Line

The status line gives you a persistent heads-up display at the bottom of the
terminal. In the chat box, run:

```markdown
/statusline Show {model short name} | {context}% context | {cwd} | {git_status} | {branch} where git status is green "clean" or yellow "modified" using ANSI colors, and omit git fields if not in a repo.
```

> **What just happened?** `/statusline` is a built-in Claude Code slash command that
> configures a persistent display at the bottom of your terminal. You'll see the
> active model, how much of the context window is in use, your working directory, and
> the git status. This HUD becomes more useful in later modules as context management
> and model switching become part of your workflow.

---

## 5. CLI Navigation Essentials

Now that the project is scaffolded, let's learn the shortcuts you'll use every day.

**`@` file references** — type `@pyproject.toml` in the chat box to reference a file
without copying its full content. Claude reads the file on demand.

**`!` bash mode** — prefix with `!` to run shell commands directly (you already used
this in step 3). It's shorthand for asking Claude to run a Bash tool call.

**Multiline input** — `\` + Enter for a quick line continuation, or `Shift+Enter` for
a new line in the prompt.

**`Ctrl+G`** — open the current prompt in your default text editor for longer edits.

> **Exercise:** Type `@src/todd/__init__.py` to reference the init file, then run
> `!uv run todd hello` to verify the CLI still works.

---

## 6. Permission Modes

Claude Code has three permission modes, cycled with `Shift+Tab`:

| Mode | Status line | Behavior |
|------|-------------|----------|
| **Normal** (default) | No indicator | Prompts for confirmation on file edits and shell commands |
| **Auto-Accept** | `⚡ auto-accept` | Skips file edit confirmations; still prompts for shell commands |
| **Plan** | `⏸ plan mode` | Read-only — Claude explores and plans but cannot write or edit files |

> **Callout:** You'll use Plan mode extensively in Module 2. For now, cycle through the
> modes with `Shift+Tab` to see the status line update.

---

## 7. Essential Commands

Claude Code ships with built-in slash commands. Here are the ones you'll use most:

| Command | What it does |
|---------|-------------|
| `/context` | Visual grid showing context window usage |
| `/cost` | Token usage and cost for this session |
| `/compact` | Compress conversation to free context — use when responses degrade |
| `/clear` | Reset context entirely between unrelated tasks |
| `/help` | Full command list |

> **Exercise:** Run `/context` and `/cost` to see your current session state.
> You'll revisit these throughout the workshop as context management becomes critical.

---

## 8. Your First CLAUDE.md

CLAUDE.md is the single most impactful Claude Code feature. It provides persistent
project instructions that load automatically every session.

**Three scopes:**

| Scope | File | Shared via git? |
|-------|------|----------------|
| Global (all projects) | `~/.claude/CLAUDE.md` | No |
| Project (team-wide) | `./CLAUDE.md` | Yes |
| Personal (local only) | `./CLAUDE.md.local` | No (gitignored) |

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

## 9. Commit and Proceed

Ask Claude to commit the changes (including the CLAUDE.md update), then advance to
the next module:

```markdown
Commit the changes and then run /module to proceed to module 2.
```

---

[Module 2 →](module2.md)
