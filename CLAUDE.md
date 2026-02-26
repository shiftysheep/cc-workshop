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

# Type checking
uv run mypy src/

# Linting
uv run ruff check src/ tests/

# Install pre-commit hooks (run once after clone)
uv run pre-commit install
```

## Coding Standards

- **Ruff** rules: E, W, F, I, N, UP, B, C4, PLC, PLE, PLW, RUF
- **mypy** strict mode — all functions must have complete type annotations
- **Conventional commits** — `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`
- Prefer simple, readable code over clever abstractions
