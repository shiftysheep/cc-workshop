# Todd — Claude Code Workshop

## Tech Stack

- Python: 3.13+
- Package management: uv
- CLI framework: Typer
- Tests: pytest
- Hooks: pre-commit (ruff, mypy strict, bandit, vulture, xenon)

## Pre-execution Checklist

Before building or running any code, verify that pre-commit hooks are configured and installed. If no `.pre-commit-config.yaml` exists, create one. Always run `uv run pre-commit install` to ensure hooks are active before the first commit.

```shell
# Run the CLI
uv run todd

# Run tests
uv run pytest

# Run a specific test file
uv run pytest tests/test_query.py

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/ tests/
```

## Python One-Off Scripts

For standalone scripts that don't belong to the main package, use
[PEP 723 inline script metadata](https://peps.python.org/pep-0723/) to embed
dependencies directly in the file:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = ["httpx", "rich"]
# ///
```

Run with `uv run script.py` — no venv or separate requirements file needed.

## Coding Standards

- **Ruff** rules: E, W, F, I, N, UP, B, C4, PLC, PLE, PLW, RUF
- **mypy** strict mode — all functions must have complete type annotations
- **Conventional commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- Prefer simple, readable code over clever abstractions

## Workshop Structure

The repository uses branches for each module (`module-1` through `module-5`). Each
branch builds on the previous. Changes merge upward: lower modules into higher modules.

## What Claude Should Do

- Read existing code before suggesting changes
- Run the full test suite after any code edit
- Use `uv run` for all Python commands (never raw `python` or `pip`)
- Follow existing patterns in the codebase
- Make atomic commits — one logical change per commit

## What Claude Should Not Do

- Skip tests or type checking
- Add dependencies without being asked
- Over-engineer solutions beyond what's requested
- Modify `.claude/` configuration without being asked
