---
description: Create a phased implementation plan with atomic commits
context: fork
---

# /plan

Create a phased implementation plan with atomic commits, saved to `docs/plans/`.

## Arguments

`$ARGUMENTS` — feature to plan (can reference spec, research output, or description)

## Workflow

1. **Read input** — consume any referenced spec document, research findings, or feature description from `$ARGUMENTS`
2. **Delegate to Plan subagent** (use Task tool with `subagent_type: "Plan"`) for planning:
   - Provide full spec/research context in the prompt
   - Ask it to produce phases with `[PHASE-XXX]` IDs, each representing one atomic commit
   - Each phase should include: files changed, tests strategy, acceptance criteria
3. **Write plan file** to `docs/plans/plan-<feature>.md` following documentation-standards skill

## Delegate to Plan Subagents

Use the Task tool with `subagent_type: "Plan"` for structured implementation planning.

## Phase Structure Requirements

Each phase MUST include:
- `[PHASE-NNN]` identifier
- Conventional commit message
- Files to create or modify
- Tests to write
- Acceptance criteria

## Output

Plan document at `docs/plans/plan-<feature>.md` with:

```
## Plan: <Feature Name>

### Overview
### Phases
#### [PHASE-001] <Name>
- **Commit**: `type(scope): description`
- **Files**: ...
- **Tests**: ...
- **Acceptance Criteria**: ...
```

## Usage

```
/plan Implement user authentication from docs/specs/spec-auth.md
/plan Add REST API endpoints for task CRUD
/plan $ARGUMENTS
```
