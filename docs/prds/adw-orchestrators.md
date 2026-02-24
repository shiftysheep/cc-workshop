# PRD: ADW Code-Driven Orchestrators

## Overview

Create Python orchestrator scripts that chain the existing ADW phase commands
(`/research`, `/design`, `/plan`, `/validation`, `/implement`, `/review`,
`/document`) into end-to-end delivery workflows. Each orchestrator invokes
phases via `claude -p /<phase>`, carries state between phases through a JSON
file, and runs inside an isolated git worktree.

This replaces the prompt-driven `/feature` and `/bug` skills built in Module 3
with robust, resumable, code-driven equivalents.

## Usage

```shell
# Full feature delivery
uv run python adw_feature.py "Add retry logic to HTTP client"

# Bug fix (skips design phase)
uv run python adw_bug.py "Fix timeout on large file uploads"

# Resume from design — human has already produced a spec
uv run python adw_feature.py --from-design "Add retry logic to HTTP client"

# Resume a failed or interrupted run
uv run python adw_feature.py --resume cc73faf1
```

## Requirements

### State Management

- Each workflow run gets a unique 8-character hex ADW ID (e.g. `cc73faf1`)
- State persists at `agents/{adw_id}/state.json` with schema:
  ```json
  {
    "adw_id": "cc73faf1",
    "issue": "Add retry logic to HTTP client",
    "plan_file": "docs/plans/cc73faf1-add-retry.md",
    "issue_class": "feature",
    "model": "opus",
    "current_phase": "implement",
    "completed_phases": ["research", "design", "plan", "validation"],
    "status": "in_progress"
  }
  ```
- Phase output captured to `agents/{adw_id}/{phase}/raw_output.jsonl`

### Workflow Variants

| Script | Phases | Use Case |
|--------|--------|----------|
| `adw_feature.py` | research → design → plan → validation → implement → review → document | Full feature delivery |
| `adw_bug.py` | research → plan → validation → implement → review → document | Bug fix — no design phase |
| `adw_feature.py --from-design` | plan → validation → implement → review → document | Human-designed — skip research and design |

### Phase Invocation

- Each phase invoked via subprocess: `claude -p /<phase_name>`
- Phases execute sequentially — one must complete before the next starts
- Non-zero exit from a phase halts the workflow and updates state to `failed`
- The `--resume` flag reads existing state and restarts from `current_phase`

### Worktree Isolation

- Each ADW runs via `claude -w {adw_id}`, creating an isolated worktree at
  `.claude/worktrees/{adw_id}/` on branch `worktree-{adw_id}`
- Multiple ADWs can run in parallel without branch or filesystem conflicts

### Non-Functional

- Fail with a clear error message if `claude` CLI is not on PATH
- Log phase transitions to stderr with timestamps
- State file must be valid JSON at all times (atomic write via temp file + rename)

## Scripts

Both scripts share a common `adw_core.py` module containing:
- State management (create, read, update)
- Phase invocation via subprocess
- ADW ID generation
- Logging and error handling

## Implementation Notes

Use `subprocess.run()` to invoke `claude -p /<phase>`. Capture stdout/stderr
and write to JSONL output files. State updates happen before and after each
phase invocation to support resumability.

## Out of Scope

- Multi-agent team orchestration (demonstrated conceptually in module)
- GitHub PR creation at workflow end
- Parallel phase execution (phases are always sequential)
- Custom model selection per phase (uses defaults from phase commands)
