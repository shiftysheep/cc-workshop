# Module 4: Building Orchestration Commands

In this module we compose the phase commands from Module 3 into end-to-end
orchestration commands. You'll plan and build four delivery workflows — two
single-agent, two multi-agent — by reading the existing phase command
scaffolding and composing it through plan mode.

---

## Key Concepts

| Concept | Why it matters |
|---------|---------------|
| **Prompt-driven orchestration** | Composing a multi-step workflow through prose instructions in a command or skill. Single-agent commands execute phases sequentially; team commands coordinate parallel specialist workers — both defined in markdown, no code required. |

## Glossary

| Term | Definition |
|------|-----------|
| **Phase command** | A single-responsibility slash command that handles one step of the delivery workflow (e.g. `/research`, `/implement`). Composable building blocks for orchestration. |
| **Orchestration command** | A higher-order slash command that composes phase commands into an end-to-end workflow. Can be single-agent (sequential phases) or multi-agent (parallel workers). |

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

## 1. Plan the Orchestration Commands

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

## 2. How Claude Researches the Scaffolding

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

**Dynamic context injection.** Module 3 introduced the layered context
system — memory files (always present), skills (on-demand), and hooks (at
lifecycle events). The `/feature` command adds a fourth pattern: **explicit
invocation**, where context loading is triggered by the user running the
command directly. Unlike auto-loaded skills, commands fire only when the user
types `/<name>` — giving the user direct control over when orchestration
starts.

> **Progressive disclosure applied here.** Claude doesn't load all skills
> into every context. A code quality skill doesn't fire when writing
> documentation. A hook that validates `.py` files only runs after Python
> writes. The new `/feature` skill will only fire when explicitly invoked.
> Context is revealed at the moment it's needed — no earlier, no later.

> **Phase dependencies drive orchestration.** The PRD defines explicit ordering
> constraints that Claude must encode into the orchestration commands:
>
> - **Single-agent** (`/feature`, `/bug`): phases run sequentially — each phase's
>   output feeds the next. Research produces findings, design produces a spec, plan
>   produces phases, validation gates implementation.
> - **Multi-agent** (`/team:feature`, `/team:bug`): Group 1 workers run in parallel,
>   then a leader synthesises their outputs before Group 2 starts.
>
> When writing your own PRDs for orchestration, define these dependency chains
> explicitly: what each phase outputs, what the next phase needs as input, and which
> phases can safely run in parallel. Without this, Claude will guess at ordering —
> and guessing wastes context on corrections.

---

## 3. Review and Build

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

## 4. Applying the Pattern to Your Own Projects

The orchestration commands Claude just built follow a pattern you can reuse. When you
have your own feature or bug to deliver, write a structured build instruction that
explicitly chains your workflow commands:

````markdown
Read docs/prds/todd-rich-output.md and deliver this feature using the following phases:

1. Run /research to investigate the codebase and gather context
2. Run /design to produce a technical spec
3. Run /plan to create an implementation plan from the spec
4. Run /validation to verify the plan is ready
5. Run /implement to build it using TDD
6. Run /review to check quality before committing
7. Run /document to update affected documentation

Carry forward key findings, file paths, and blockers between phases.
````

This is what the `/feature` command does under the hood — but writing it out
explicitly gives you control over which phases to include, what to skip, and where
to add custom steps (e.g., "run a security scan between review and document").

> **When to use a command vs. a manual prompt.** Use `/feature` or `/bug` for
> standard delivery. Write an explicit prompt when you need to customise the phase
> sequence, skip phases, or insert project-specific steps. Both approaches use the
> same underlying phase commands.

---

## 5. Commit and Proceed

Ask Claude to commit the new command files, then advance to the next module:

```markdown
Commit the new command files and then run /module to proceed to module 5.
```

---

[← Module 3](module3.md) | [Module 5 →](module5.md)
