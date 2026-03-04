---
description: Validate an implementation plan for quality, atomicity, and traceability
context: fork
agent: validation
---

# /validation

Validate an implementation plan before handing it off for implementation. Checks structure, atomicity, traceability, and completeness.

## Arguments

`$ARGUMENTS` — path to plan file, or description of what to validate

## Workflow

Delegates to the **validation** agent. The agent will:

1. **Read the plan** — if `docs/plans/${CLAUDE_SESSION_ID}.md` exists, read it as the plan; otherwise read from the path or description in `$ARGUMENTS`
2. **Validate structure**:
   - Each phase has a `[PHASE-NNN]` identifier
   - Each phase maps to exactly one atomic commit
   - Conventional commit format used
3. **Validate atomicity**: No phase contains changes too large for one commit
4. **Validate traceability**: Plan phases trace back to spec or requirements
5. **Validate completeness**: Test strategy present, acceptance criteria defined per phase
6. **Generate assessment** with readiness checklist

## Output

Quality assessment with:

```
## Plan Validation Report

### Overall Assessment
READY | NOT READY | NEEDS REVISION

### Readiness Checklist
- [ ] All phases have [PHASE-NNN] identifiers
- [ ] All phases have atomic commit scope
- [ ] Conventional commit format used
- [ ] Test strategy defined per phase
- [ ] Acceptance criteria defined per phase
- [ ] Traceability to spec/requirements

### Issues Found
<Blocking / Important / Suggestions>

### Recommendation
<Proceed to implement / Revise plan first>
```

## Usage

```
/validation docs/plans/plan-auth.md
/validation the authentication implementation plan
/validation $ARGUMENTS
```
