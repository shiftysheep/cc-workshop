---
# PRD: ADW Feature Orchestrator

## Overview

Create two Python scripts that implement code-driven orchestration for feature
delivery:

- `adw_feature.py` — 7-phase sequential workflow script
- `adw_core.py` — shared module for state management, phase invocation, ID
  generation, and logging

These scripts are the *output* of running `/team:feature @docs/prds/adw-feature.md`
in Module 4 of the workshop. They represent code-driven orchestration: where
Module 3's commands describe workflows in prose, these scripts implement them
in Python with state persistence and resumability.

## Usage

```shell
# Full feature delivery
uv run python adw_feature.py "Add retry logic to HTTP client"

# Skip research and design — human has already produced a spec
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
- State file must be valid JSON at all times (atomic write: temp file + rename)

### Workflow Phases

`adw_feature.py` runs these phases in order:

1. `research` — Explore codebase and gather context
2. `design` — Produce a technical specification
3. `plan` — Create a phased implementation plan
4. `validation` — Verify plan quality and traceability
5. `implement` — TDD implementation with atomic commits
6. `review` — Code quality, security, and test coverage review
7. `document` — Update documentation to reflect changes

### Flags

- `--from-design` — skip research and design phases; start from `plan`
- `--resume <adw_id>` — read existing state and restart from `current_phase`

### Phase Invocation

- Each phase invoked via subprocess: `claude -p /<phase_name>`
- Phases execute sequentially — one must complete before the next starts
- Non-zero exit from a phase halts the workflow and updates `status` to `failed`
- Each ADW runs via `claude -w {adw_id}`, creating an isolated worktree at
  `.claude/worktrees/{adw_id}/` on branch `worktree-{adw_id}`

### Non-Functional

- Fail with a clear error message if `claude` CLI is not on PATH
- Log phase transitions to stderr with timestamps
- Multiple ADWs can run in parallel without branch or filesystem conflicts

## Scripts

Both scripts share `adw_core.py` which provides:
- State management (create, read, update functions)
- Phase invocation via `subprocess.run()`
- ADW ID generation (8-char hex)
- Atomic state writes (temp file + rename pattern)
- Logging and error handling

## Implementation Notes

Use `subprocess.run()` to invoke `claude -p /<phase>`. Capture stdout/stderr
and write to JSONL output files. Update state before and after each phase
invocation to support resumability.

## Out of Scope

- Multi-agent team orchestration (that is what invokes this script in Module 4)
- GitHub PR creation at workflow end
- Parallel phase execution (phases are always sequential)
- Custom model selection per phase
---
