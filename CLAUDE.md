# Todd — Claude Code Workshop

Todd is a Typer CLI application built progressively through a structured Claude Code
workshop. Each module introduces new agentic capabilities — from project scaffolding
to parallel agent teams.

## Tech Stack

- Python: 3.13+
- Package management: uv
- CLI framework: Typer
- Tests: pytest
- Hooks: pre-commit (ruff, mypy strict, bandit, vulture, xenon)

## Development Commands

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
