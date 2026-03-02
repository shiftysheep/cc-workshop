# Todd — Claude Code Workshop

## Tech Stack

- Python: 3.13+
- Package management: uv
- CLI framework: Typer
- Tests: pytest
- Hooks: pre-commit (ruff, mypy strict, bandit, vulture, xenon)

## Pre-execution Checklist

Before building or running any code, verify that pre-commit hooks are configured and installed. If no `.pre-commit-config.yaml` exists, create one. Always run `uv run pre-commit install` to ensure hooks are active before the first commit.

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
