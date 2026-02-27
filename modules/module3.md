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
| **Hook** | A script that runs at a Claude Code lifecycle event (e.g. `PreToolUse`, `PostToolUse`, `Stop`). Configured in `.claude/settings.json`. Used for validation, logging, and back pressure. See [hook events](https://code.claude.com/docs/en/hooks#hook-events). |
| **Context engineering** | Intentionally shaping what's in the context window to improve Claude's output — what to include, what to exclude, and when to reset. CLAUDE.md, skills, hooks, and subagents are all context engineering tools. |
| **Dynamic context injection** | Providing Claude with relevant context at the moment it's needed — via hooks, skills, or CLAUDE.md — rather than up front in every prompt. A specific context engineering technique. |
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

Before exploring the `.claude/` scaffolding, it's worth understanding the structural
difference between the two primary extension mechanisms.

**Skills are capability bundles.** A skill is a directory — `.claude/skills/<name>/` —
containing a `SKILL.md` file with YAML frontmatter and instructions, plus optional
`references/` subdirectory, scripts, and templates. Claude loads a skill automatically
when the current task matches the skill's description. Think of them as "know this when
relevant": coding standards, domain knowledge, architectural context, or how to operate
a tool. In this repo:

- `.claude/skills/code-review/SKILL.md` — auto-loaded when Claude is doing code review
- `.claude/skills/documentation-standards/` — has a `references/templates.md` file with doc templates

> **Skills are the right place to teach Claude how to use CLI tools.** When your project
> uses a custom CLI (like `todd`, `bb.py`, or a deployment tool), a skill can bundle the
> command reference, common flags, and usage patterns that Claude needs to operate it
> correctly. Because skills load automatically when the task matches, Claude gets the
> tool knowledge exactly when it's about to use it — not on every turn.

**Commands are focused workflows.** A command is a single markdown file at
`.claude/commands/<name>.md`. It acts as a prompt template for a reproducible action.
You invoke it explicitly with `/<name>`. Think of them as "do this specific thing":
implement a feature, research a topic, run a phase. In this repo:

- `.claude/commands/implement.md` — the explicit `/implement` workflow

> **Commands and skills have merged.** A file at `.claude/commands/review.md` and a
> file at `.claude/skills/review/SKILL.md` both create a `/review` command. Commands
> still work, but skills are the superset — they can do everything a command can, plus
> bundle supporting files, reference material, and scripts alongside the instructions.

The distinction in practice:

| | Command | Skill |
|-|---------|-------|
| **Invocation** | Explicit (`/research`, `/implement`) | Automatic (description match) |
| **Structure** | Single `.md` file | Directory (`SKILL.md` + optional `references/`, scripts) |
| **Use case** | Phase execution, defined workflows | Standards, guidelines, domain knowledge |
| **Location** | `.claude/commands/<name>.md` | `.claude/skills/<name>/SKILL.md` |
| **Good for** | "Do this specific thing" | "Know this when doing related things" |
| **Frontmatter** | N/A (just markdown) | `disable-model-invocation`, `context: fork`, `allowed-tools` |

> **Skills can behave exactly like commands.** Set `disable-model-invocation: true`
> in a skill's frontmatter to prevent auto-loading — it will only run when the user
> invokes it via `/skill-name`. Add `context: fork` to run it in an isolated subagent
> (useful for workflows that shouldn't pollute the main context). This gives you
> command-style explicit invocation with skill-level bundled references and scripts.

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

## 4. Custom Subagents

In Module 2 you saw built-in subagents (Explore, Plan, General-purpose). Now you'll
create your own.

**Anatomy of a custom subagent.** Each agent lives at `.claude/agents/<name>.md` and
consists of YAML frontmatter plus a system prompt body:

```yaml
---
name: code-reviewer
description: Read-only code reviewer for style and correctness analysis
model: sonnet
tools:
  - Read
  - Glob
  - Grep
permissionMode: default
maxTurns: 10
skills:
  - code-review
---

You are a code reviewer. Analyze the provided code for:
- Correctness and potential bugs
- Style consistency with project conventions
- Type annotation completeness
- Test coverage gaps

Report findings as a structured list with file:line references.
Do not suggest fixes — only identify issues.
```

> **Model selection matters.** Haiku is fast and cheap but designed for
> exploration and search — not analysis. Code review requires reasoning about
> correctness, patterns, and edge cases. Use sonnet or opus for analytical
> agents. Reserve haiku for agents that primarily search and retrieve.

**Frontmatter fields:**

| Field | Purpose | Example values |
|-------|---------|---------------|
| `name` | Display name | `code-reviewer` |
| `description` | When Claude should delegate to this agent | Free text |
| `model` | Which model to use | `sonnet`, `opus`, `haiku` |
| `tools` | Allowlist of available tools | `[Read, Glob, Grep]` |
| `permissionMode` | Permission level | `default`, `bypassPermissions` |
| `maxTurns` | Maximum agentic turns | `10`, `20` |
| `skills` | Skills to preload | `[code-review]` |
| `memory` | Memory scope | `user`, `project`, `local` |
| `isolation` | Execution isolation | `worktree` |

> **Exercise:** Create `.claude/agents/code-reviewer.md` with the configuration above.
> Then ask Claude to "review the todd query command" and observe it delegating to your
> custom subagent.

You'll see three more agents (implementation.md, validation.md, documentation.md)
when you explore the `.claude/` scaffolding in the next section.

---

## 5. Plan the Orchestration Commands

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

## 6. How Claude Researches the Scaffolding

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

## 7. Review and Build

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

## 8. Explore the Lint Check Hook

Hooks run at Claude Code lifecycle events. A `PostToolUse` hook fires after every
`Write` or `Edit` tool call — the right moment to validate what Claude just wrote
before it moves on.

> **Available hook events** include `PreToolUse` (block before execution),
> `PostToolUse` (validate after execution), `Notification`, `Stop`,
> `SubagentStart`/`SubagentStop`, `SessionStart`, and more. See the
> [hook events reference](https://code.claude.com/docs/en/hooks#hook-events)
> for the complete list.

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

## 9. Understanding Dynamic Context Injection

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

## 10. CLAUDE.md as a Context Engineering Tool

You've now seen CLAUDE.md as project-level configuration. It's also a powerful context
engineering tool with several advanced features.

> **Tip:** Use `/memory` to see all loaded memory files and their sources. Auto-memory
> (`~/.claude/projects/<project>/memory/`) stores Claude's learnings across sessions —
> the first 200 lines of `MEMORY.md` load automatically at startup.

**Import syntax** — use `@path/to/file` inside CLAUDE.md to pull in content from other
files. This lets you maintain shared rules, tech stack details, or architecture decisions
in separate files while keeping CLAUDE.md as the entry point.

> **Markdown links for progressive disclosure.** Instead of inlining all context,
> use markdown links to reference deeper documentation:
> ```markdown
> # Architecture
> See [ADW Architecture](docs/adr/adw.md) for the full architecture reference.
> See [API Conventions](docs/api-conventions.md) for endpoint patterns.
> ```
> Claude follows links when the current task needs that context — it won't load
> the architecture reference when fixing a typo. This keeps CLAUDE.md concise
> while making deep context available on demand. The `@import` syntax always
> includes content inline; markdown links let Claude choose when to drill down.

**`.claude/rules/` directory** — path-specific rules that apply only to matching
directories. For example, a rule for `src/` that enforces typing conventions won't
fire when Claude is editing test files.

| File | Applies to |
|------|-----------|
| `.claude/rules/src.md` | Files under `src/` |
| `.claude/rules/tests.md` | Files under `tests/` |
| `.claude/rules/docs.md` | Files under `docs/` |

**`CLAUDE.local.md`** — personal overrides not committed to git. Use for
individual editor preferences, personal workflow notes, or debugging flags that
shouldn't affect teammates.

**`settings.local.json`** — the same pattern for settings. Local overrides that don't
affect the team configuration.

**Team conventions** — the project CLAUDE.md serves as a team contract. Shared standards
(tech stack, commit conventions, code style) go in the committed CLAUDE.md. Personal
preferences (verbosity, editor, shortcuts) go in `CLAUDE.local.md`.

> **Exercise:**
> 1. Create `.claude/rules/src.md` with a rule about error handling for `src/`
>    files (e.g., "Functions in src/ should raise `TypeError` or `ValueError`
>    for invalid arguments — never silently return `None`. Use the patterns
>    established in existing modules.")
> 2. Add an `@docs/adr/adw.md` import to the project CLAUDE.md so Claude always has the
>    ADW architecture reference
> 3. Create a `CLAUDE.local.md` with a personal preference (e.g., preferred
>    verbosity level or a debugging note)

> **Callout:** CLAUDE.md, skills, hooks, and `rules/` form a four-layer context system.
> CLAUDE.md is always-on, `rules/` are path-scoped, skills are task-scoped, and hooks are
> event-scoped. Together they let you shape Claude's behavior precisely without
> overloading any single mechanism.

**Anti-patterns to watch for:**

| Anti-pattern | Problem |
|-------------|---------|
| Too long (>200 lines) | Noise drowns out signal; Claude gives less weight to each instruction |
| Contradictory instructions | Claude picks one arbitrarily; behavior becomes unpredictable |
| Stale file references | Claude tries to read files that no longer exist |
| Vague directives ("be careful") | No actionable constraint; Claude ignores them |

**Maintenance checklist** — run through this after significant project changes:

- [ ] Are all referenced files still present?
- [ ] Are tool and command names current?
- [ ] Are there conflicting instructions?
- [ ] Is the tech stack accurate?
- [ ] Are test commands still correct?
- [ ] Do coding standards match what's actually enforced?

Treat CLAUDE.md like any other config file: small investments in accuracy pay off
across every session.

---

## 11. Commit and Proceed

Ask Claude to commit the changes, then advance to the next module:

```markdown
Commit the new command files and then run /module to proceed to module 4.
```

---

[← Module 2](module2.md) | [Module 4 →](module4.md)
