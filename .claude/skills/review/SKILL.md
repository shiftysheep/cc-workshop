---
name: review
description: Code review with multi-dimensional quality, security, and test analysis
context: fork
agent: validation
---

# /review

Perform a comprehensive code review across quality, security, tests, and documentation dimensions.

## Arguments

`$ARGUMENTS` — git ref, file paths, or description of what to review (defaults to staged/recent changes)

## Workflow

Delegates to the **validation** agent. The agent will:

1. **Read context** — if `docs/specs/${CLAUDE_SESSION_ID}.md` exists, read it as the design spec; if `docs/plans/${CLAUDE_SESSION_ID}.md` exists, read it as the implementation plan. Use these to verify implementation matches intent.
2. **Analyze scope** from `$ARGUMENTS` — determine what changes to review (git diff, specific files, or PR)
3. **Run quality dimensions**:
   - Quality: ruff, mypy, xenon complexity
   - Security: bandit for vulnerabilities
   - Tests: coverage of changed code, test quality
   - Documentation: public APIs documented
4. **Categorize findings** by severity: Blocking / Important / Suggestion
5. **Optional plan completeness check**: if a plan path is provided, verify all phases were implemented
6. **Write review report** to `docs/reviews/${CLAUDE_SESSION_ID}.md`

## Output

Review report at `docs/reviews/${CLAUDE_SESSION_ID}.md` with:

```
## Code Review Report

### Summary
<Overall assessment, merge readiness>

### Blocking Issues
<Must fix before merge>

### Important Issues
<Should fix, may merge with tracking>

### Suggestions
<Optional improvements>

### Quality Tool Results
<ruff, mypy, bandit, vulture, xenon output>

### Recommendation
APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION

## Verdict
PASS | FAIL

<List of issues if FAIL>
```

## Usage

```
/review                           # review staged changes
/review HEAD~1..HEAD              # review last commit
/review src/auth.py               # review specific file
/review $ARGUMENTS
```
