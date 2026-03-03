---
# PRD: ADW Bug Orchestrator

## Overview

Create a Python script that implements code-driven orchestration for bug fixes:

- `adw_bug.py` — 6-phase sequential workflow script (no design phase)
- Reuses `adw_core.py` from the feature orchestrator for state management,
  phase invocation, ID generation, and logging

This script is the *output* of running `/feature @docs/prds/adw-bug.md` in
Module 4 of the workshop. It follows the same patterns as `adw_feature.py`
but skips the design phase — appropriate for bugs where the fix is scoped
to a known root cause rather than requiring architectural design work.

## Usage

```shell
# Bug fix workflow
uv run python adw_bug.py "Fix timeout on large file uploads"

# Resume a failed or interrupted run
uv run python adw_bug.py --resume cc73faf1
```

## Requirements

### State Management

Reuses `adw_core.py`. State schema is identical to the feature orchestrator:

```json
{
  "adw_id": "cc73faf1",
  "issue": "Fix timeout on large file uploads",
  "plan_file": "docs/plans/cc73faf1-fix-timeout.md",
  "issue_class": "bug",
  "model": "opus",
  "current_phase": "implement",
  "completed_phases": ["research", "plan", "validation"],
  "status": "in_progress"
}
```

### Workflow Phases

`adw_bug.py` runs these phases in order:

1. `research` — Investigate the bug and its root cause
2. `plan` — Create a phased fix plan
3. `validation` — Verify the plan addresses the root cause
4. `implement` — TDD implementation with atomic commits
5. `review` — Code quality, security, and test coverage review
6. `document` — Update documentation to reflect changes

### Flags

- `--resume <adw_id>` — read existing state and restart from `current_phase`
- No `--from-design` flag (not applicable for bug fixes)

### Phase Invocation

- Each phase invoked via subprocess: `claude -p /<phase_name> <issue>`
  — headless, no `-w` flag, runs in the current (worktree) directory
- Phases execute sequentially — one must complete before the next starts
- Non-zero exit from a phase halts the workflow and updates `status` to `failed`
- Capture stdout/stderr and append to `agents/{adw_id}/{phase}/raw_output.jsonl`

> **How the orchestrator is launched (not the phases).** Module 4 runs the
> orchestrator inside a worktree: `claude -w {adw_id}`. Individual phase
> invocations do NOT use `-w` — they run headlessly in the current directory.

### Non-Functional

- Fail with a clear error message if `claude` CLI is not on PATH
- Log phase transitions to stderr with timestamps
- Multiple ADWs can run in parallel without branch or filesystem conflicts

## Dependencies

Requires `adw_core.py` (built by the feature orchestrator PRD). Import shared
utilities rather than duplicating them.

## Implementation Notes

Import from `adw_core` for all shared functionality. The only difference from
`adw_feature.py` is the phase list (6 phases, no design) and the absence of
the `--from-design` flag.

## Out of Scope

- Design phase (intentionally excluded — bugs don't require architectural design)
- `--from-design` flag
- GitHub PR creation at workflow end
- Custom model selection per phase
---
