# Module 5: Operations & Maintenance

This module covers operational skills for sustained Claude Code usage — running
Claude headlessly in scripts and CI, managing sessions and costs, and maintaining
the CLAUDE.md that shapes everything.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **Headless mode** | Running Claude non-interactively with `claude -p "prompt"`. Outputs text, JSON, or streaming JSON. Used in scripts, CI pipelines, and batch operations. |
| **Session persistence** | Claude Code saves all sessions locally. Resume with `--continue` (most recent) or `--resume` (pick by ID/name). |
| **Effort level** | Controls how much reasoning Claude applies. Low/medium/high. Affects cost and quality. Set via `/model`. |
| **Checkpointing** | Automatic snapshots before every Claude action. Rewind with `Esc+Esc` or `/rewind` to undo changes without losing the session. |

---

## Tools in this module

**Built-in tools**

| Tool | What it does |
|------|-------------|
| `Read` | Reads a file from the filesystem |
| `Write` | Creates a new file |
| `Edit` | Makes targeted edits to an existing file |
| `Bash` | Runs a shell command |
| `Glob` | Finds files by pattern (e.g. `**/*.py`) |
| `Grep` | Searches file contents by regex |
| `Task` | Spawns a specialist subagent for focused work |

---

## 1. Headless Mode & Scripting

Headless mode runs Claude non-interactively — no chat box, no confirmation prompts.
The command runs, produces output, and exits.

**Basic usage:**

```shell
claude -p "explain the main function in src/todd/cli.py"
```

**Output formats:**

| Flag | Output | Use case |
|------|--------|----------|
| `--output-format text` | Plain text (default) | Human-readable output |
| `--output-format json` | Full conversation JSON | Structured parsing |
| `--output-format stream-json` | Real-time JSON events | Live progress monitoring |

**Control flags:**

| Flag | Purpose |
|------|---------|
| `--max-turns N` | Limit agentic turns |
| `--max-budget-usd X.XX` | Hard cost cap |
| `--allowedTools "Read,Grep"` | Restrict available tools |

**Piping content:**

```shell
cat src/todd/query.py | claude -p "review this code for type annotation completeness"
```

**Structured output** — use `--json-schema` to get validated JSON responses matching
a schema you define.

> **Exercise:** Write a 3-line shell script that runs `claude -p` on each `.py` file
> in `src/todd/` to check for type annotation completeness:
>
> ```shell
> #!/bin/bash
> for f in src/todd/*.py; do
>   claude -p "Check if all functions in this file have complete type annotations" < "$f"
> done
> ```

---

## 2. CI/CD Integration

Headless mode is what makes Claude useful in pipelines. The pattern is simple:
feed context in, get analysis out, gate on the result.

**PR review bot** — run Claude on a diff:

```shell
gh pr diff 42 | claude -p "Review this diff for bugs, style issues, and missing tests"
```

**Automated analysis on push** — add to any CI pipeline:

```shell
claude -p "Analyze src/ for security vulnerabilities" --max-turns 5 --max-budget-usd 0.50
```

**Sample GitHub Actions workflow:**

```yaml
name: Claude Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude review
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          gh pr diff ${{ github.event.number }} | \
            claude -p "Review this PR diff. Report any bugs, security issues, or style violations." \
            --output-format json \
            --max-turns 5 \
            --dangerously-skip-permissions
```

**`--dangerously-skip-permissions`** — this flag disables all confirmation prompts.
It's named that way intentionally: in CI there's no human to confirm, but you're also
removing a safety layer. Only use it in controlled environments with restricted tool
access.

> **Callout:** CI integration is where headless mode and CLAUDE.md converge — the
> agent runs autonomously, shaped only by configuration. The CLAUDE.md you maintain
> is the only instruction set the CI agent receives.

---

## 3. Session Management

Claude Code saves every session locally. You can resume, rename, and export them.

| Command / Flag | What it does |
|---------------|-------------|
| `claude --continue` (`-c`) | Resume the most recent session |
| `claude --resume` (`-r`) | Pick from a session list by ID or name |
| `/rename <name>` | Give the current session a descriptive name |
| `/export [filename]` | Save conversation to a file |

**Named sessions** make it easy to return to specific work:

```shell
# Name the session while working
/rename todd-query-refactor

# Later, resume by name
claude --resume todd-query-refactor
```

**`--from-pr <number>`** — start or resume a session linked to a specific pull request.
Claude loads the PR context automatically.

> **Exercise:** `/rename` the current session to something descriptive, then exit with
> `/exit`. Resume it with `claude --resume` and verify your conversation history is
> intact.

---

## 4. Cost & Extended Thinking

Understanding cost helps you choose the right model and effort level for each task.

**Session cost tracking:**

| Command | What it shows |
|---------|-------------|
| `/cost` | Token usage and pricing for this session |
| `/stats` | Daily usage patterns and session history |

**Model cost tiers:**

| Model | Relative cost | Best for |
|-------|--------------|----------|
| Haiku | Lowest | Exploration, simple searches, code review |
| Sonnet | Medium | Code generation, implementation, most tasks |
| Opus | Highest | Architecture decisions, complex reasoning, planning |

**Effort levels** — accessible via `/model`, then select effort:

| Level | Behavior | Use case |
|-------|----------|----------|
| Low | Minimal reasoning | Simple edits, typo fixes |
| Medium | Balanced (default) | Most development tasks |
| High | Maximum reasoning | Architecture, complex debugging |

**Extended thinking** — `Alt+T` toggles extended thinking, which gives Claude a
scratchpad for longer reasoning chains. `Ctrl+O` shows the thinking process in
verbose mode.

When extended thinking matters: complex debugging where the root cause isn't obvious,
architecture decisions with multiple trade-offs, multi-step reasoning across many files.

> **Exercise:** Run `/cost` to see your current session usage. Then switch effort levels
> via `/model` and compare the cost difference on a simple task.

---

## 5. Checkpointing & Recovery

Claude Code automatically snapshots your codebase before every action. If something
goes wrong, you can rewind without losing your session.

**`Esc+Esc`** — open the rewind menu. Choose to restore:
- **Code only** — revert file changes, keep the conversation
- **Conversation only** — roll back context, keep file changes
- **Both** — full restore to a previous point

**`/rewind`** — same menu, accessed from the command line.

**When to use checkpointing:**
- Undo a bad implementation without starting over
- Recover from context poisoning (bad info entered the conversation)
- Try alternative approaches from the same starting point

> **Exercise:** Make an intentional bad change (e.g., delete a function), then press
> `Esc+Esc` to open the rewind menu and restore the code. Notice that your conversation
> history is preserved — you didn't lose the session.

**Limitation:** Checkpointing only tracks changes made by Claude. External processes
(manual edits, other tools) aren't captured in the rewind history.

---

## 6. CLAUDE.md Maintenance

A CLAUDE.md that drifts out of date is worse than no CLAUDE.md — it actively misleads
Claude with stale instructions.

**Anti-patterns to avoid:**

| Anti-pattern | Problem |
|-------------|---------|
| Too long (>200 lines) | Noise drowns out signal; Claude gives less weight to each instruction |
| Contradictory instructions | Claude picks one arbitrarily; behavior becomes unpredictable |
| Stale file references | Claude tries to read files that no longer exist |
| Vague directives ("be careful") | No actionable constraint; Claude ignores them |

**Audit checklist** — run through this periodically:

- [ ] Are all referenced files still present?
- [ ] Are tool and command names current?
- [ ] Are there conflicting instructions?
- [ ] Is the tech stack accurate?
- [ ] Are test commands still correct?
- [ ] Do coding standards match what's actually enforced?

**Evolution pattern:** After each significant project change — new dependency, refactored
module, changed conventions — review the CLAUDE.md for staleness. Treat it like any
other config file: it needs maintenance.

> **Exercise:** Audit the workshop's CLAUDE.md. After four modules of work, identify
> anything that's become stale or could be improved. Check file references, command
> names, and tech stack accuracy.

> **Callout:** A well-maintained CLAUDE.md is worth more than any amount of prompt
> engineering in individual conversations. It's the compound interest of AI-assisted
> development — small investments in accuracy pay off across every session.

---

## 7. Further Reading

These features extend Claude Code beyond what we've covered in the workshop.

**IDE integrations** — Claude Code works inside your editor:
- VS Code: install the "Claude Code" extension from the Extensions marketplace
- JetBrains: install the Claude Code plugin
- Both provide inline diffs, file references, and plan review within the editor

**Plugins** — `/plugin` to browse the marketplace. Plugins bundle skills, hooks, agents,
and MCP servers into installable packages. You installed Context7 (Module 2) and
document-skills (Module 3) this way.

**Sandbox configuration** — OS-level filesystem and network isolation for autonomous
agent work. Configure in `settings.json` under `"sandbox"`. Useful when running agents
with `bypassPermissions` on untrusted input.

**Browser automation** — `claude --chrome` for web testing, Playwright MCP for
automated UI interaction. Useful for end-to-end testing and visual verification.

**Desktop app & cloud** — `claude.ai/code` for browser-based Claude Code, `/desktop`
to hand off sessions between terminal and desktop.

> **Callout:** These features extend Claude Code beyond the terminal. Explore them as
> your workflow matures.

---

[← Module 4](module4.md)
