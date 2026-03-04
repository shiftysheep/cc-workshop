---
name: code-review
description: MUST BE USED when reviewing code, evaluating merge readiness, or assessing quality
---

# Code Review Skill

## When to Use

Load this skill when reviewing code changes, evaluating merge readiness, conducting
security audits, or assessing implementation quality. Applied by the validation and
review agents across all phases.

## Review Dimensions

Evaluate code across four dimensions in every review:

1. **Quality**: Readability, maintainability, complexity, adherence to patterns
2. **Security**: OWASP top 10, input validation, secrets exposure, dependency vulnerabilities
3. **Tests**: Coverage of new code, test quality, edge cases, mocking appropriateness
4. **Documentation**: Public API docs, inline comments for non-obvious logic, updated READMEs

## Severity Classification

| Severity | Label | Action Required |
|----------|-------|----------------|
| Must fix before merge | **Blocking** | PR cannot merge until resolved |
| Should fix, may merge with tracking | **Important** | Create follow-up issue |
| Nice to have, optional | **Suggestion** | Author discretion |

## Quality Tools Reference

These tools match `.pre-commit-config.yaml` configuration:

```bash
uv run ruff check src/            # linting (E, W, F, I, N, UP, B, C4, PLC, PLE, PLW, RUF)
uv run ruff format --check src/   # formatting
uv run mypy --strict src/         # type checking
uv run bandit -r src/             # security scanning
uv run vulture --min-confidence 80 src/  # dead code detection
uv run xenon --max-absolute B --max-modules B --max-average A src/  # complexity
```

## Findings Format

Each finding MUST include:

```
[SEVERITY] file/path.py:line_number
Description of the issue
Remediation: how to fix it
```

Example:
```
[Blocking] src/auth.py:42
Hardcoded secret in connection string
Remediation: Move to environment variable, use os.environ.get("DB_PASSWORD")

[Important] src/utils.py:18
Function exceeds complexity threshold B (current: C)
Remediation: Extract helper functions to reduce cyclomatic complexity

[Suggestion] src/models.py:95
Missing docstring on public method
Remediation: Add brief description of parameters and return value
```

## Review Output Structure

```
## Code Review Report

### Summary
<Overall assessment, merge readiness>

### Blocking Issues
<List or "None">

### Important Issues
<List or "None">

### Suggestions
<List or "None">

### Quality Tool Results
<Output from ruff, mypy, bandit, vulture, xenon>

### Recommendation
APPROVE | REQUEST_CHANGES | NEEDS_DISCUSSION
```

## Related

- **testing** — tests are a core review dimension; use testing skill for coverage and TDD standards
- **documentation-standards** — documentation is a core review dimension; use documentation-standards for file location and frontmatter conventions
