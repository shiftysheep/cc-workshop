# PRD: ADW Higher-Order Skills

## Overview

Create two user-invocable skills — `/feature` and `/bug` — that compose the
existing ADW phase commands into end-to-end workflows. Each skill accepts a
description as its argument and orchestrates the phase sequence through prose
instructions (prompt-driven orchestration).

## Skills

### `/feature` — Full ADW Sequence

Accepts a feature description and runs all seven phases in order:

1. `/research` — Explore codebase and gather context
2. `/design` — Produce a technical specification
3. `/plan` — Create a phased implementation plan with atomic commits
4. `/validation` — Verify plan quality, atomicity, and traceability
5. `/implement` — TDD implementation with atomic commits
6. `/review` — Code quality, security, and test coverage review
7. `/document` — Update documentation to reflect changes

### `/bug` — Bug Fix Sequence

Accepts a bug description and runs six phases (skips design):

1. `/research` — Investigate the bug and its root cause
2. `/plan` — Create a phased fix plan
3. `/validation` — Verify the plan addresses the root cause
4. `/implement` — TDD implementation with atomic commits
5. `/review` — Code quality, security, and test coverage review
6. `/document` — Update documentation to reflect changes

## Requirements

### Skill Structure

- Each skill lives at `.claude/skills/<name>/SKILL.md`
- Frontmatter must include:
  - `name` — skill name (`feature` or `bug`)
  - `description` — what the skill does and when to use it
  - `user-invocable: true` — makes the skill callable as `/<name>`
  - `argument-hint` — placeholder text shown in the slash menu

### Orchestration Behaviour

- Execute phase commands sequentially — complete one before starting the next
- After each phase, summarize output and carry relevant context forward
- Use `$ARGUMENTS` to pass the user's input to the first phase
- Present a final summary when all phases are complete

### Context Handoff

Between phases, carry forward:
- Key findings and decisions
- File paths created or modified
- Issues or blockers identified

## Out of Scope

- State file persistence between sessions (Module 4)
- Python orchestrator scripts (Module 4)
- Worktree isolation (Module 4)
- Resumability from mid-workflow (Module 4)
