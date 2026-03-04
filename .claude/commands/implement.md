---
description: Implement a plan using TDD methodology with atomic commits per phase
context: fork
agent: implementation
---

# /implement

Implement a plan using Test-Driven Development, creating one atomic commit per phase.

## Arguments

`$ARGUMENTS` — path to plan file, or description of what to implement

## Workflow

Delegates to the **implementation** agent. The agent will:

1. **Read the plan** — if `docs/plans/${CLAUDE_SESSION_ID}.md` exists, read it as the plan; otherwise read from the path or description in `$ARGUMENTS`
2. **Verify assumptions** — check referenced files and prior phases exist
3. **Implement each phase with TDD**:
   - Red: Write failing tests
   - Green: Minimal implementation
   - Refactor: Improve structure
4. **Quality checks** after each phase: pytest, ruff, mypy
5. **Atomic commit** per phase with conventional commit message

## Output

Implementation summary with phases completed, files changed, tests added, quality results, and commit hashes.

## Usage

```
/implement docs/plans/plan-auth.md
/implement the authentication plan from Phase 1 through Phase 3
/implement $ARGUMENTS
```
