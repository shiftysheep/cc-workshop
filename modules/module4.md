# Module 4: Agentic Delivery Workflows

In this module you use the orchestration commands from Module 3 to build
Python orchestrators in parallel worktrees. Two Claude instances run
simultaneously — one team-based, one single-agent — building the scripts
that will power future ADW runs. You'll observe the difference in execution
patterns, compare the output, and analyze the session logs.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **Code-driven orchestration** | Composing a multi-step workflow through a Python script that invokes phase commands via `claude -p /<phase>` and carries state via a JSON file. Sequential, single-agent, robust, and resumable. |
| **Team orchestration** | Composing a multi-step workflow through an agent team where a leader coordinates specialist workers via `TeamCreate`, `TaskCreate`, and `SendMessage`. Parallel where possible, prompt-driven, and defined in a slash command. |
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

## 1. From Building to Running

Module 3 produced four orchestration commands: `/feature`, `/bug`,
`/team:feature`, and `/team:bug`. These commands compose the ADW phase
primitives into end-to-end delivery workflows — two single-agent, two
multi-agent.

Now you'll use them. Two PRDs describe Python orchestrator scripts that will
power future ADW runs. Two Claude instances will build them simultaneously in
separate worktrees: one using the team command, one using the single-agent
command.

> **The tools build the tools.** Module 3 created orchestration commands.
> Module 4 feeds them real PRDs. The commands aren't demos — they're the
> delivery mechanism. What gets built (Python orchestrators) is itself a
> tool for future workflows. Each layer of tooling enables the next.

---

## 2. Read the Orchestrator PRDs

Before launching the runs, read both PRDs so you understand what each
Claude instance will be building:

```
Read docs/prds/adw-feature.md and docs/prds/adw-bug.md
```

`adw-feature.md` defines:
- `adw_feature.py` — 7-phase feature delivery script
- `adw_core.py` — shared state management, phase invocation, ID generation,
  and logging module

`adw-bug.md` defines:
- `adw_bug.py` — 6-phase bug fix script (no design phase)
- Reuses `adw_core.py` from the feature PRD

> **PRDs as work items.** In Modules 2-3 you gave PRDs to Claude directly.
> Here the PRDs pass through commands — `/team:feature` and `/feature` read
> the PRD and execute the full delivery workflow against it. The PRD is both
> the specification and the input.

---

## 3. Launch Two Worktrees

> **Prerequisite: enable agent teams.** The `/team:feature` command uses
> `TeamCreate` and `SendMessage`, which require an experimental feature flag.
> The project's `.claude/settings.json` already sets it — verify it's present
> before continuing:
>
> ```json
> "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" }
> ```
>
> If it's missing, add it to `.claude/settings.json` or export it in your
> shell: `export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

Open two terminal windows. Each runs an independent Claude instance in its
own worktree:

```shell
# Terminal 1: team-based build of the feature orchestrator
claude -w adw-feat
> /team:feature @docs/prds/adw-feature.md

# Terminal 2: single-agent build of the bug orchestrator
claude -w adw-bug
> /feature @docs/prds/adw-bug.md
```

> **Why two worktrees?** Each `claude -w <name>` creates an isolated working
> directory. The team build and single-agent build modify files independently
> — no merge conflicts, no branch switching. When both finish, you merge the
> results. This is the practical application of sandboxing: isolate parallel
> work so failures in one don't affect the other.

Once both are running:

> **What's happening now.** Terminal 1: `/team:feature` created a team,
> spawned 4 Group 1 workers (researcher, designer, planner, validator), and
> they're working in parallel. Terminal 2: `/feature` is running phases
> sequentially — research first, then design, then plan. Watch the
> difference in activity patterns.

Note: if time is tight, launch just one terminal and observe the other via
instructor demo.

---

## 4. How Worktree Isolation Works

While Claude works, here's what's happening under the hood.

**Worktrees as sandboxes.** `claude -w adw-feat` creates
`.claude/worktrees/adw-feat/` with its own working directory and branch
`worktree-adw-feat`. Changes are invisible to the main branch until merged.

**Parallel without conflict.** Two agents modifying different worktrees can
write to the same file paths without conflict. Git handles the isolation at
the filesystem level.

**State files bridge context.** Each phase in the orchestrator runs in a
fresh context window. The state file (`agents/{adw_id}/state.json`) bridges
them: ADW ID, completed phases, plan file path. `--resume` reads state and
restarts from `current_phase`.

**Subprocess chaining vs team coordination.** The single-agent command runs
phases sequentially within one Claude session. The team command spawns
parallel workers. Both produce the same deliverable (a Python orchestrator)
but through different execution strategies.

```
Isolation layers:
  Worktree:   Filesystem isolation — separate working directories
  Subagent:   Context isolation — fresh context window per phase
  Hook:       Quality isolation — lint/type check after every write
  Permission: Access isolation — restricted tool sets per agent
```

> **Sandboxing is defense in depth.** Worktree isolation protects the
> filesystem. Subagents protect the context window. Hooks protect code
> quality. Permission modes protect system access. Each layer limits what
> can go wrong at a different scope.

---

## 5. Monitor the Runs

While both runs execute, observe what each is doing.

**Terminal 1 (team build):** Watch for `TeamCreate`, parallel worker
activity in Group 1 (researcher, designer, planner, validator working
simultaneously), `SendMessage` coordination, and leader synthesis before
Group 2 starts.

**Terminal 2 (single-agent build):** Watch for sequential phase transitions
— research completes → design starts → plan starts. One phase at a time,
each building on the previous.

Check state files as phases complete:

```
Read .claude/worktrees/adw-feat/agents/*/state.json
Read .claude/worktrees/adw-bug/agents/*/state.json
```

> **Observable differences.** The team run shows bursts of parallel activity
> followed by synthesis pauses. The single-agent run shows steady sequential
> progress. Both produce status logs to stderr with timestamps — compare the
> wall-clock time for the analysis phases (Group 1 parallel vs sequential
> research → design → plan → validation).

Note: if either run hasn't finished, you can `Ctrl+C` and still inspect
the state files and partial output. The orchestrators being built support
`--resume` precisely for this case.

---

## 6. Compare the Output

Once both runs complete (or after sufficient phases for comparison):

```
Compare the code produced by the two worktrees. Focus on:
1. adw_core.py — did both approaches produce similar shared modules?
2. adw_feature.py vs adw_bug.py — structural differences
3. Test coverage — did one approach produce more thorough tests?
4. Code style — any differences in naming, structure, or documentation?
```

> **Same PRD, different process, comparable output.** Both commands executed
> the same phase sequence (research through document) against PRDs with
> similar structure. The team approach had multiple specialist perspectives
> during analysis; the single-agent approach had one continuous context. The
> interesting question isn't which is "better" but where the differences
> appear and what caused them.

---

## 7. Analyze Session Logs

```
Find the session logs from both worktree runs and compare them. Show me:
1. Total tool calls in each run
2. Tools used most frequently in each
3. Any tool call failures
4. Time spent in each phase
5. For the team run: how many SendMessage calls, how much coordination
   overhead between workers
```

> **Session logs as feedback loops.** Three layers of feedback: hooks give
> immediate feedback (lint errors after each write), phase transitions give
> workflow-level feedback (pass/fail per phase), and session logs give
> post-hoc feedback (full behavioral analysis). The hook tells you *what*
> went wrong. The phase transition tells you *when*. The session log tells
> you *why*.

---

## 8. What the Orchestrators Do

The commands just built Python scripts that implement code-driven
orchestration. Here's what each component does.

**`adw_core.py`** — the shared engine:
- State management: create, read, update `agents/{adw_id}/state.json`
- Phase invocation: `subprocess.run()` calling `claude -p /<phase>`
- ADW ID generation: 8-character hex identifier
- Atomic writes: temp file + rename to guarantee valid JSON at all times
- Logging: phase transitions to stderr with timestamps

> **This is headless mode.** The `claude -p "prompt"` flag runs Claude
> non-interactively — no chat box, no confirmation prompts. The command runs,
> produces output, and exits. This is how orchestrators chain phases: each
> `claude -p /<phase>` is a self-contained headless invocation that reads
> state from JSON and writes results back.
>
> Key flags for headless execution:
>
> | Flag | Purpose |
> |------|---------|
> | `--output-format text\|json\|stream-json` | Control output format |
> | `--max-turns N` | Limit agentic turns |
> | `--max-budget-usd X.XX` | Hard cost cap |
> | `--allowedTools "Read,Grep"` | Restrict available tools |
>
> You can also pipe content: `cat file.py | claude -p "review this code"`.
> This pattern is the foundation for CI/CD integration — if it runs in your
> terminal, it can run in a pipeline.

**`adw_feature.py`** — 7-phase feature workflow:
- Phases: research → design → plan → validation → implement → review → document
- `--from-design` flag: skip research and design when a spec already exists
- `--resume` flag: restart from `current_phase` in existing state
- Worktree isolation: each run in `claude -w {adw_id}`

**`adw_bug.py`** — 6-phase bug fix workflow:
- Phases: research → plan → validation → implement → review → document
- Shares `adw_core.py` — no duplication
- `--resume` flag; no `--from-design` (not needed for bugs)

```
Orchestration hierarchy:
  /team:feature  →  commands that build orchestrators (M3, prompt-driven)
  adw_feature.py →  orchestrators that chain phases (M4 output, code-driven)
  /implement     →  phase commands that do focused work (M3, pre-existing)
```

> **Three levels of orchestration.** Phase commands (`/implement`, `/review`)
> do focused single-phase work. Python orchestrators (`adw_feature.py`) chain
> phases with state persistence and resumability. Delivery commands
> (`/team:feature`, `/feature`) orchestrate entire builds with team
> coordination or sequential execution. Each level composes the one below it.

---

## 9. Agent Teams in Practice

A retrospective on what you just observed.

**When teams help.** Parallel analysis (Group 1) produces multiple specialist
perspectives faster than serial. The overhead of leader synthesis is worth it
when the analysis phases are independent — researcher, designer, planner, and
validator can all work from the same PRD simultaneously.

**When single-agent is better.** Sequential dependencies (each phase needs
the previous output) don't benefit from parallelism. Simpler coordination,
less overhead, easier to debug.

**Agent design is API design.** Each worker had clear inputs (feature
description + leader context), clear output (specialist analysis), single
responsibility, and explicit scope. The better defined the interface, the
more reliably it composes.

| | Single-Agent (`/feature`) | Team (`/team:feature`) |
|-|--------------------------|----------------------|
| **Analysis phases** | Sequential — each waits | Parallel — all four simultaneously |
| **Implementation** | Sequential | Coordinated — reviewer and documenter act on implementer output |
| **Coordination** | None (one context) | Leader synthesis + `SendMessage` |
| **Resumability** | Built into output (`--resume`) | Re-run the command |
| **Best for** | Simpler tasks, debugging | Complex tasks, time-sensitive delivery |

> **Agent design is API design.** Defining an agent is like defining an API:
> clear inputs, clear outputs, single responsibility, explicit error handling.
> The better defined the interface, the more reliably it composes.

---

## 10. Commit and Wrap Up

```
Merge the worktree changes and commit the orchestrator scripts
(adw_core.py, adw_feature.py, adw_bug.py) and any generated changes.
```

> **What you built.** Over four modules you went from a bare repository to
> a fully functional agentic delivery system:
>
> - Module 1: Project scaffolding and quality gates
> - Module 2: CLI tool backed by the Claude Agent SDK
> - Module 3: ADW foundations — phase commands, orchestration commands,
>   skills, agents, hooks
> - Module 4: Parallel worktree execution, session log analysis, and
>   orchestrator scripts built by the commands you created
>
> The patterns — PRDs as agent input, plan mode as review gate, hooks as
> back pressure, commands as composable orchestrators, worktrees as
> sandboxes, teams as parallelism — apply to any project where you want
> Claude to do sustained, multi-step work reliably.

> **Workshop Recap — Eight Tenets of Quality Output:**
>
> 1. **Verify your work** — manual check → automated test → lint hooks → CI gates
> 2. **Be specific** — PRD-driven workflows reduce guessing
> 3. **CLAUDE.md + hooks** — persistent memory + automated quality gates
> 4. **Context is finite** — delegate noise to subagents, /compact long sessions
> 5. **Explore → Plan → Code** — think before doing
> 6. **Progressive disclosure** — right context, right scope, right time
> 7. **Agent design** — composable workers with clear interfaces
> 8. **Scale with isolation** — worktrees, subagents, hooks, permissions

---

**Take it home.** Module 5 is a capstone project: extend todd from a single-shot
CLI into a Claude Code clone with interactive chat, tool use, and session management.
Use the ADW commands you built in Module 3 to drive the development.

Run `/module` to switch to the module-5 branch and open the capstone instructions.

---

[← Module 3](module3.md)
