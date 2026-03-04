---
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

1. **Analyze scope** from `$ARGUMENTS` — determine what changes to review (git diff, specific files, or PR)
2. **Run quality dimensions**:
   - Quality: ruff, mypy, xenon complexity
   - Security: bandit for vulnerabilities
   - Tests: coverage of changed code, test quality
   - Documentation: public APIs documented
3. **Categorize findings** by severity: Blocking / Important / Suggestion
4. **Optional plan completeness check**: if a plan path is provided, verify all phases were implemented

## Output

Review report with:

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
```

## Usage

```
/review                           # review staged changes
/review HEAD~1..HEAD              # review last commit
/review src/auth.py               # review specific file
/review $ARGUMENTS
```
