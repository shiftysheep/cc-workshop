#!/usr/bin/env python3
"""PostToolUse hook: runs ruff and mypy on written/edited .py files."""

import json
import shutil
import subprocess
import sys


def _run_check(cmd: list[str]) -> int:
    """Run cmd; print output and return 2 on failure, 0 on success."""
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout, end="")
        print(result.stderr, end="", file=sys.stderr)
        return 2
    return 0


def _lint(file_path: str) -> int:
    """Run ruff then mypy on file_path; return 2 on first failure."""
    if (rc := _run_check(["uv", "run", "ruff", "check", "--fix", file_path])) != 0:
        return rc
    return _run_check(["uv", "run", "mypy", "--strict", file_path])


def main() -> int:
    """Read hook JSON from stdin and lint any .py file_path."""
    try:
        hook_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0  # fail-open on malformed input

    file_path = hook_data.get("tool_input", {}).get("file_path", "")
    if not file_path or not file_path.endswith(".py"):
        return 0

    if not shutil.which("uv"):
        return 0  # fail-open if uv not installed

    return _lint(file_path)


if __name__ == "__main__":
    sys.exit(main())
