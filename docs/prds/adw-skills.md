---
# PRD: ADW Orchestration Skills

## Overview

Create four slash-invocable skills that compose the existing ADW phase skills
(`/research`, `/design`, `/plan`, `/validation`, `/implement`, `/review`,
`/document`) into end-to-end delivery workflows. Two strategies:

1. **Single-agent sequential** (`/feature`, `/bug`) — one Claude instance
   executes phases in order via prose instructions.
2. **Multi-agent parallel** (`/team:feature`, `/team:bug`) — a leader agent
   coordinates specialist workers using `TeamCreate`, `TaskCreate`, and
   `SendMessage`.

## Skills

### `/feature` — Single-Agent Feature Delivery

Location: `.claude/skills/feature/SKILL.md`

Phases: research → design → plan → validation → implement → review → document

Accepts `$ARGUMENTS` as the feature description (or `@file` for a PRD).
Executes phases sequentially. Carries context forward between phases via
inline summaries.

### `/bug` — Single-Agent Bug Fix

Location: `.claude/skills/bug/SKILL.md`

Phases: research → plan → validation → implement → review → document

Same as `/feature` but skips the design phase. Accepts `$ARGUMENTS` as the
bug description (or `@file` for a PRD).

### `/team:feature` — Multi-Agent Feature Delivery

Location: `.claude/skills/team:feature/SKILL.md`

**Group 1 — Parallel Analysis** (4 workers run simultaneously):

| Worker | Perspective | Maps to Phase |
|--------|------------|---------------|
| Researcher | Codebase exploration, prior art, constraints | `/research` |
| Designer | Architecture, interfaces, data models | `/design` |
| Planner | Implementation phases, commit strategy, test plan | `/plan` |
| Validator | Risk assessment, edge cases, compatibility | `/validation` |

Leader synthesises Group 1 outputs into a unified brief.

**Group 2 — Coordinated Implementation** (3 workers):

| Worker | Responsibility | Maps to Phase |
|--------|---------------|---------------|
| Implementer | TDD implementation following the synthesised plan | `/implement` |
| Reviewer | Code review of implementation changes | `/review` |
| Documenter | Documentation updates for changes | `/document` |

Workers coordinate via `SendMessage`. Leader produces final summary.

### `/team:bug` — Multi-Agent Bug Fix

Location: `.claude/skills/team:bug/SKILL.md`

Same as `/team:feature` but Group 1 has 3 workers (no Designer). Phases:
research + plan + validation (parallel) → implement + review + document
(coordinated).

## Requirements

### Skill Structure

- Each skill lives at `.claude/skills/<name>/SKILL.md`
- All skills accept `$ARGUMENTS` (description or `@file` PRD reference)
- Skills MUST NOT set `context: fork` in frontmatter — all four skills
  run in the primary context so team activity remains visible to the user
- Single-agent skills execute phases sequentially with context handoff
- Team skills use `TeamCreate` for setup, `TaskCreate` for work items,
  `SendMessage` for coordination

### Team Behavioural Requirements

- Group 1 workers MUST run in parallel (not sequentially)
- Group 2 starts only after leader synthesises Group 1 outputs
- Each worker receives the original description plus leader context
- Leader produces a final summary when all workers complete

### Context Handoff (single-agent skills)

Between phases, carry forward:
- Key findings and decisions
- File paths created or modified
- Issues or blockers identified

## Out of Scope

- State file persistence between sessions
- Python orchestrator scripts (these are the *work items* the skills build
  in Module 4, not part of the skills themselves)
- Worktree isolation (handled by the invoker, not the skill)
- Resumability from mid-workflow
---
