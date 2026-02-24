# Module 3: ADW Foundations — Commands, Skills, and Hooks

In this module we use Claude to generate a visual reference document for the ADW
system already present in this branch, then explore the `.claude/` scaffolding that
powers it: phase commands, a reusable skill, and a session capture hook. We close
by using session logs to analyze agent behavior and improve ADW velocity.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **ARD (Architecture Reference Document)** | A technical reference that describes how a system is designed. We use Mermaid diagrams to make it visual and navigable. |
| **Mermaid** | A text-based diagramming syntax that renders inside Markdown. Write diagram definitions as code; get flowcharts, sequence diagrams, and state machines as output. |
| **Custom slash command** | A user-defined command stored in `.claude/commands/<name>.md`. Explicitly invoked with `/<name>`. Claude executes the markdown as a prompt template. |
| **Skill** | A reusable capability stored in `.claude/skills/<name>/SKILL.md`. Claude loads it automatically when the task matches the skill's description — no explicit invocation needed. |
| **Hook** | A script that runs at a Claude Code lifecycle event (e.g. `PostToolUse`, `Stop`, `PreToolUse`). Configured in `.claude/settings.json`. Used for validation, logging, and back pressure. |
| **Dynamic context injection** | Providing Claude with relevant context at the moment it's needed — via hooks, skills, or CLAUDE.md — rather than up front in every prompt. |
| **Progressive disclosure** | Surfacing information incrementally: start with a summary, reveal detail on demand. Prevents overwhelming agents and users with irrelevant context. |
| **Prompt-driven orchestration** | Composing a multi-step workflow through prose instructions in a command or skill. Single-agent commands execute phases sequentially; team commands coordinate parallel specialist workers — both defined in markdown, no code required. |
| **Team orchestration** | Composing a multi-step workflow through an agent team where a leader coordinates specialist workers via `TeamCreate`, `TaskCreate`, and `SendMessage`. Parallel where possible, prompt-driven, and defined in a slash command. |
| **JSONL** | JSON Lines — one JSON object per line. Claude Code session transcripts are stored in this format, making them easy to stream and parse. |

---

## Tools in this module

**Built-in tools**

| Tool | What it does |
|------|-------------|
| `Read` | Reads a file from the filesystem |
| `Write` | Creates a new file |
| `Edit` | Makes targeted edits to an existing file |
| `Glob` | Finds files by pattern (e.g. `**/*.md`) |
| `Bash` | Runs a shell command |

---

## 1. Generate the ADW Architecture Reference Document

Before exploring the scaffolding, let's use Claude to produce a visual map of it.
This is a demonstration of Claude as a documentation tool — no code required.

In the chat box, enter:

```markdown
Read the `.claude/` directory, then generate a comprehensive Architecture Reference Document at `docs/adr/adw.md`.
Include the following Mermaid diagrams:

1. Feature and bug workflow phase sequences (flowchart)
2. Python orchestrator chaining pattern (sequence diagram)
3. ADW component architecture showing the .claude/ directory structure (architecture diagram)
4. ADW state lifecycle from creation to completion (state diagram)
5. State JSON schema (entity relationship diagram)
```

Claude will read the existing files, reason about the system design, and produce a
structured document with all five diagrams.

> **What just happened?** Claude read existing files and produced a technical
> reference — no code was written. This is the same capability that makes Claude
> useful for generating PRDs, ADRs, runbooks, and onboarding docs from existing
> codebase knowledge. The Mermaid diagrams render directly in GitHub, VS Code, and
> most markdown viewers.

Review `docs/adr/adw.md` before continuing. You'll be referencing it throughout this
module and the next.

---

## 2. Skills vs Commands

Before exploring the `.claude/` scaffolding, it's worth understanding the difference
between the two primary extension mechanisms.

**Commands** are explicit. You invoke them directly with `/<name>` or an orchestrator
calls them via `claude -p /<name>`. They're good for defined workflows and phase
execution — tasks with a clear start and finish.

**Skills** are implicit. Claude loads them automatically when the current task matches
the skill's description. They're good for cross-cutting concerns — coding standards,
context management guidelines, domain knowledge — that should influence Claude's
behaviour across many tasks without being explicitly called every time.

The distinction in practice:

| | Command | Skill |
|-|---------|-------|
| **Invocation** | Explicit (`/research`, `/implement`) | Automatic (description match) |
| **Use case** | Phase execution, defined workflows | Standards, guidelines, domain knowledge |
| **Location** | `.claude/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` |
| **Good for** | "Do this specific thing" | "Know this when doing related things" |

> **Four ways to deliver work.** The phase commands are reusable primitives.
> You can compose them in four ways — two single-agent, two multi-agent:
>
> 1. **`/feature`** — single-agent, sequential, all 7 phases
> 2. **`/bug`** — single-agent, sequential, 6 phases (no design)
> 3. **`/team:feature`** — multi-agent, parallel analysis then coordinated
>    implementation, all 7 phases
> 4. **`/team:bug`** — multi-agent, parallel analysis then coordinated
>    implementation, 6 phases (no design)
>
> A PRD at `docs/prds/adw-commands.md` defines all four commands we'll build
> in this module using prompt-driven orchestration.

---

## 3. Install the Skill Creator

The `document-skills` plugin from the Anthropic marketplace includes
`skill-creator` — a guided skill that walks you through building new skills
with correct frontmatter and structure.

In the chat box, run:

```
/plugin
```

Browse to the **Discover** tab, find **document-skills** from the
`anthropic-agent-skills` marketplace, and install it at **project** scope.

> **The skill marketplace.** Claude Code supports shared skills distributed
> through marketplaces. The `anthropic-agent-skills` marketplace is maintained
> by Anthropic and includes productivity skills (document processing, frontend
> design) and meta-skills (skill-creator, MCP builder). Installing a plugin
> gives Claude access to the skills it contains — they appear in the `/` menu
> and Claude can load them automatically by description match.

---

## 4. Plan the Orchestration Commands

Now activate plan mode and give Claude the PRD. Claude will research the
existing scaffolding to understand what it's composing before proposing a plan.

Press `Shift+Tab` twice to enter plan mode, then enter:

```markdown
Read docs/prds/adw-commands.md and plan how to create the four orchestration
commands described in the PRD: /feature, /bug, /team:feature, and /team:bug.
Research the existing phase commands and agent definitions to understand
the invocation and team coordination patterns.
```

Claude will begin exploring the codebase — reading phase commands, existing
skills, and the hook configuration — to understand the patterns before
planning.

> **Plan mode as research.** In Module 2 you used plan mode to plan a code
> change. Here you're using it to plan `.claude/` configuration. The mechanism
> is the same: Claude explores the codebase in read-only mode, reasons about
> the existing structure, and produces a plan before writing anything. Plan
> mode isn't just for code — it works for any task where understanding the
> current state matters before changing it.

---

## 5. How Claude Researches the Scaffolding

While Claude works on its plan, here's what it's exploring and why it matters.

**Phase commands as primitives.** Claude reads the seven commands in
`.claude/commands/` — research, design, plan, validation, implement, review,
document. Each is a single-responsibility slash command: one clear job,
defined inputs, defined output. This is what makes them composable — the
orchestration commands can chain them both sequentially (single-agent) and
in parallel (team-based) because each phase is self-contained.

**Existing skills as patterns.** Claude reads existing commands AND skills to
understand patterns. The new commands compose phase commands; the team variants
also use TeamCreate/SendMessage for parallel worker coordination. Commands are
stored in `.claude/commands/<name>.md`, while skills in `.claude/skills/<name>/SKILL.md`
show structure with YAML frontmatter, instructions, and optional `references/`.

**Dynamic context injection.** Skills, hooks, and CLAUDE.md form a layered
context system:

| Mechanism | When it fires | Use case |
|-----------|--------------|----------|
| `CLAUDE.md` | Every session, always | Project-wide constants |
| **Skill** | When task matches description | Standards loaded on demand |
| **Hook** | At lifecycle events | Validation, back pressure |

The new `/feature` command adds a fourth pattern: **explicit invocation** of
orchestration workflows. Unlike auto-loaded skills, commands fire only when
the user types `/<name>` — giving the user direct control over when
orchestration starts.

> **Progressive disclosure applied here.** Claude doesn't load all skills
> into every context. A code quality skill doesn't fire when writing
> documentation. A hook that validates `.py` files only runs after Python
> writes. The new `/feature` skill will only fire when explicitly invoked.
> Context is revealed at the moment it's needed — no earlier, no later.

---

## 6. Review and Build

Claude will present a plan for the four command files. Review it, then confirm.

Verify the plan includes:
- `/feature` and `/bug`: correct phase sequences, `$ARGUMENTS`, context handoff between phases
- `/team:feature` and `/team:bug`: Group 1 parallel workers (4 for feature, 3 for bug), leader synthesis step, Group 2 coordinated workers
- File locations: `.claude/commands/feature.md`, `.claude/commands/bug.md`, `.claude/commands/team:feature.md`, `.claude/commands/team:bug.md`

Once satisfied, approve the plan. Claude will create the command files in
`.claude/commands/`.

> **What just happened?** You gave Claude a PRD and it produced four
> orchestration commands that compose the seven existing phase commands. The
> team commands introduce `TeamCreate` and `SendMessage` — the first time
> these tools appear in the workshop. No code was written — just markdown
> configuration. This is the power of the `.claude/` scaffolding: commands
> are primitives, they compose each other, and the entire system is defined
> in markdown.

---

## 7. Explore the Lint Check Hook

Hooks run at Claude Code lifecycle events. A `PostToolUse` hook fires after every
`Write` or `Edit` tool call — the right moment to validate what Claude just wrote
before it moves on.

Enter this prompt:

```markdown
Read `.claude/hooks/lint-check.py` and `.claude/settings.json`. Explain: what the
PostToolUse hook does, when it fires, what it runs, and what happens when a check
fails.
```

> **Back pressure via hooks.** When the hook exits 2, Claude receives the error output
> and must fix the issue before continuing. This is back pressure — the system
> actively resists bad output rather than silently accepting it. Claude can't drift
> from quality standards because the hook closes the loop immediately after every file
> write. This is how hooks enforce constraints without adding them to every prompt.

---

## 8. Understanding Dynamic Context Injection

You've now explored three mechanisms for injecting context into Claude:

| Mechanism | When it fires | Use case |
|-----------|--------------|----------|
| `CLAUDE.md` | Every session, always | Project-wide constants: tech stack, conventions, goals |
| **Skill** | When task matches description | Cross-cutting standards loaded on demand |
| **Hook** | At lifecycle events | Validation, back pressure, enforcing quality gates |

Together these form a layered context system. `CLAUDE.md` is the foundation — always
present. Skills add domain knowledge when it's relevant. Hooks fire at specific
moments to inject or capture context dynamically.

> **Progressive disclosure applied here.** We don't put everything in `CLAUDE.md`
> because not every task needs every piece of context. A code quality skill doesn't
> need to load when Claude is writing documentation. A hook that injects the current
> ADW state only fires during a workflow run. Context is revealed at the moment it's
> needed — no earlier, no later.

---

## 9. Commit and Proceed

Ask Claude to commit the changes, then advance to the next module:

```markdown
Commit the new command files and then run /module to proceed to module 4.
```

---

[← Module 2](module2.md)
