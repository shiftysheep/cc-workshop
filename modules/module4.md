# Module 4: Agentic Delivery Workflows

In this module we upgrade from prompt-driven orchestration to code-driven orchestration.
We build Python scripts that chain ADW phase commands into resumable, stateful workflows,
run them against a real task, analyze the session logs, and observe a multi-agent team
in action.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **Code-driven orchestration** | Composing a multi-step workflow through a Python script that invokes phase commands via `claude -p /<phase>` and carries state via a JSON file. Robust, resumable, and parallelizable. |
| **Worktree** | A git feature that creates a separate working directory linked to the same repository. Each ADW runs in its own worktree so multiple workflows execute in parallel without conflicts. |
| **State file** | A JSON file at `agents/{adw_id}/state.json` that persists workflow state between phases — completed phases, current phase, issue description, and plan file path. |
| **Sandboxing** | Isolating agent operations to limit blast radius — worktrees for filesystem isolation, subagents with restricted tools, permission modes that prevent unintended changes. |
| **Agent team** | Multiple specialised Claude instances coordinated by a leader agent. The leader creates tasks, assigns them to workers, and synthesises results. Workers operate in parallel with focused scope. |
| **Agent design** | Designing effective agents by defining clear scope, appropriate tool access, quality system prompts, and explicit failure modes. Good agent design prevents scope creep and reduces wasted context. |
| **Session log (JSONL)** | The transcript of a Claude Code session stored as JSON Lines. Contains every tool call, result, and message. Used for post-hoc analysis of agent behaviour and performance tuning. |

---

## Tools in this module

**Built-in tools**

| Tool | What it does |
|------|-------------|
| `Read` | Reads a file from the filesystem |
| `Write` | Creates a new file |
| `Edit` | Makes targeted edits to an existing file |
| `Bash` | Runs a shell command |
| `Glob` | Finds files by pattern (e.g. `**/*.md`) |
| `Grep` | Searches file contents by regex |
| `Task` | Spawns a specialist subagent for focused work |

**Team tools**

| Tool | What it does |
|------|-------------|
| `TeamCreate` | Creates an agent team for multi-agent coordination |
| `SendMessage` | Sends messages between agents on a team |
| `TaskCreate` / `TaskUpdate` | Creates and manages tasks in a team's shared task list |

---

## 1. Prompt-Driven vs Code-Driven

Module 3 introduced the `/feature` and `/bug` skills — prose-based orchestrators
that describe the phase sequence in a SKILL.md. This works for simple cases, but
it has limits: no persistence, no worktree isolation, and no way to resume after
a failure.

Module 4 upgrades to code-driven orchestration: Python scripts that invoke phase
commands as subprocesses, carry state between phases via a JSON file, and run in
isolated git worktrees.

> **From prose to code.** Module 3's `/feature` skill described the phase
> sequence in prose. This works for simple cases but can't resume after a
> failure, can't run in parallel, and loses all context between sessions.
> Code-driven orchestration moves sequencing logic into Python — subprocess
> control, file I/O, and error handling.

---

## 2. Read the Orchestrator PRD

Before entering plan mode, read the PRD that defines what we're building:

```
Read docs/prds/adw-orchestrators.md
```

This PRD defines three workflow variants (`adw_feature.py`, `adw_bug.py`,
`--from-design`), the state schema, phase invocation contract, and worktree
isolation model.

> **PRDs as agent input.** This is the third PRD you've given Claude across
> the workshop. Notice the pattern: clear requirements, explicit out-of-scope,
> usage examples, and just enough implementation guidance to steer without
> over-constraining. A well-written PRD is one of the most effective forms of
> context engineering.

---

## 3. Plan the Orchestrators

Press `Shift+Tab` twice to enter plan mode, then enter:

```markdown
Read docs/prds/adw-orchestrators.md and create a plan to implement the ADW
orchestrator scripts. Research the existing phase commands and agent
definitions to understand the invocation patterns.
```

Claude will explore the `.claude/commands/` directory, read the phase
command definitions, and produce a plan before writing any code.

> **Third time through the cycle.** Module 2: PRD → plan → build (query
> command). Module 3: PRD → plan → build (skills). Module 4: PRD → plan →
> build (orchestrators). The cycle is the same but the complexity increases.
> This is progressive disclosure in your own learning.

---

## 4. How Code-Driven Orchestration Works

While Claude works on its plan, here's what the orchestrators do and why
each design decision matters.

**State as context bridge.** Each phase runs in a fresh `claude` process with
a new context window. The state file (`agents/{adw_id}/state.json`) bridges
them: it records the ADW ID, completed phases, current phase, and the path
to the plan file produced by the `/plan` phase. The `--resume` flag reads
this state and restarts from `current_phase`.

**Subprocess chaining.** Each phase is a separate `claude` process. No
context rot from accumulating seven phases of tool output. Trade-off: lose
in-session context; state file compensates.

**Worktree isolation (sandboxing).** `claude -w {adw_id}` creates an isolated
worktree at `.claude/worktrees/{adw_id}/`. The agent can't modify files on
your main branch. If it goes wrong, delete the worktree — nothing is lost.

**Back pressure at orchestration level.** Non-zero phase exit halts the
entire workflow. Failed validation stops implementation from starting with a
flawed plan. This layers on top of the hook-level back pressure from Module 3:

```
Back pressure layers:
  Hook level:  Write .py → lint-check → exit 2 → Claude fixes → retry
  Phase level: /validation → exit 1 → orchestrator halts → no /implement
```

> **Sandboxing is defense in depth.** Worktree isolation protects the
> filesystem. Subagents protect the context window. Hooks protect code
> quality. Permission modes protect system access. Each layer limits what
> can go wrong at a different scope.

---

## 5. Review and Build the Orchestrators

Review Claude's plan. Verify it includes:

- `adw_core.py` with state management, phase invocation, and ADW ID generation
- `adw_feature.py` with all 7 phases and `--from-design` / `--resume` flags
- `adw_bug.py` with 6 phases (no design) and `--resume` flag
- Atomic state writes (temp file + rename)
- Non-zero exit halts workflow and sets status to `failed`

Once satisfied, approve the plan.

> **What just happened?** Claude read a PRD, planned by researching your
> existing phase commands and agent definitions, then wrote Python scripts
> that compose those commands into a delivery pipeline. The orchestrators
> don't duplicate what phase commands do — they sequence and manage them.

---

## 6. Run a Single-Agent ADW

Run `adw_bug.py` against a real task in the todd codebase:

```shell
!uv run python adw_bug.py "The todd CLI does not display a helpful error
message when AWS credentials are missing — it shows a raw exception traceback
instead of a user-friendly message"
```

> **Why a bug fix, not a feature?** A bug fix has 6 phases instead of 7 and
> tends to produce smaller changes. In a workshop setting this keeps runtime
> manageable while demonstrating the full orchestration.

Watch the phase transitions log to stderr. Each phase writes its output to
`agents/{adw_id}/{phase}/raw_output.jsonl` and the state file updates after
every transition.

> **Observe the output.** Each phase logged its start and completion. The
> state file tracked progress. If any phase had failed, the orchestrator
> would have halted and you could resume with `--resume {adw_id}`. This is
> the practical difference between prompt-driven and code-driven —
> recoverability.

If time is short, `Ctrl+C` after 2–3 phases and inspect `agents/{adw_id}/state.json`.
The `--resume` flag means nothing is lost.

---

## 7. Analyze the Session Log

```
Find the most recent Claude session log and analyze it. Show me: how many
tool calls were made, which tools were used most frequently, and whether any
tool calls failed. Summarize the agent's decision-making at each phase
transition.
```

Claude will locate the JSONL session log, parse the tool calls, and produce
a behavioral analysis of the ADW run.

> **Session logs as feedback loops.** Three layers of feedback: hooks give
> immediate feedback (lint errors after each write), orchestrator status gives
> phase-level feedback (pass/fail per phase), and session logs give post-hoc
> feedback (full behavioral analysis). The hook tells you *what* went wrong.
> The orchestrator tells you *when*. The session log tells you *why*.

---

## 8. Agent Teams: Concepts and Architecture

So far every ADW run has been single-agent: one Claude instance running all
phases sequentially. Agent teams add a second dimension — parallelism.

**Leader/worker pattern.** One leader agent breaks work into subtasks, assigns
them to specialized workers, and synthesises results. Workers operate with
focused scope and appropriate tool access.

**When to use teams vs single agents.** Sequential workflows stay single-agent
— each phase depends on the previous. Parallelizable work benefits from teams:
review and documentation don't depend on each other and can run simultaneously.

**Agent design principles.** Defining an agent is like defining an API: clear
inputs, clear outputs, single responsibility, explicit error handling. The
three agents from Module 3 (implementation/sonnet, validation/opus,
documentation/sonnet) are already designed as specialists.

| | Single Agent | Team |
|-|-------------|------|
| **Sequential work** | Natural fit | Overhead without benefit |
| **Parallel work** | Blocked — must serialize | Natural fit |
| **Specialization** | One context window | Dedicated context per worker |
| **Coordination** | None needed | TaskCreate / SendMessage |

> **Agent design is API design.** Defining an agent is like defining an API:
> clear inputs, clear outputs, single responsibility, explicit error handling.
> The better defined the interface, the more reliably it composes.

---

## 9. Observe a Multi-Agent Team

Run `/review` and `/document` in parallel on the changes from section 6:

```
Create an agent team with two workers: one to run /review on the changes from
the last ADW run, and one to run /document on the same changes. The workers
should operate in parallel. Summarize both results when they complete.
```

Watch for:
- `TeamCreate` establishing the team
- `TaskCreate` adding work items to the shared task list
- `SendMessage` coordinating between leader and workers
- Idle notifications confirming workers finished

> **Observable parallelism.** We're using a small example to see the mechanics:
> `TeamCreate` establishes the team, `TaskCreate` adds work items, and
> `SendMessage` coordinates between leader and workers. Watch for idle
> notifications — that's the system telling you a worker finished.

> **Teams vs sequential.** The two workers ran simultaneously — review and
> documentation don't depend on each other. This is the same insight behind
> the ADW phase sequence: dependent phases must be sequential, independent
> phases can be parallel. Agent teams make parallelism explicit.

---

## 10. Commit and Wrap Up

```
Commit the orchestrator scripts (adw_core.py, adw_feature.py, adw_bug.py)
and any ADW-generated changes.
```

> **What you built.** Over four modules you went from a bare repository to a
> fully functional agentic delivery system:
>
> - Module 1: Project scaffolding and quality gates
> - Module 2: CLI tool backed by the Claude Agent SDK
> - Module 3: ADW foundations — commands, skills, agents, hooks
> - Module 4: Code-driven orchestration, worktree isolation, and agent teams
>
> The patterns — PRDs as agent input, plan mode as review gate, hooks as back
> pressure, state files as persistence, worktrees as sandboxes, teams as
> parallelism — apply to any project where you want Claude to do sustained,
> multi-step work reliably.

---

[← Module 3](module3.md)
