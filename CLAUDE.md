# Todd — Claude Code Workshop

## Tech Stack

- Python: 3.13+
- Package management: uv
- CLI framework: Typer
- Tests: pytest
- Hooks: pre-commit (ruff, mypy strict, bandit, vulture, xenon)

## Pre-execution Checklist

Before building or running any code, verify that pre-commit hooks are configured and installed. If no `.pre-commit-config.yaml` exists, create one. Always run `uv run pre-commit install` to ensure hooks are active before the first commit.
