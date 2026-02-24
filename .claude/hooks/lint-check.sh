#!/usr/bin/env bash
set -euo pipefail

# Read hook JSON from stdin
hook_json=$(cat)

# Check if jq is available, fail-open if not
if ! command -v jq &> /dev/null; then
  exit 0
fi

# Extract file_path from the hook JSON
file_path=$(echo "$hook_json" | jq -r '.tool_input.file_path // empty')

# Exit 0 if file_path is empty or doesn't end in .py
if [[ -z "$file_path" ]] || [[ ! "$file_path" =~ \.py$ ]]; then
  exit 0
fi

# Check if uv is available, fail-open if not
if ! command -v uv &> /dev/null; then
  exit 0
fi

# Run ruff check --fix
if ! uv run ruff check --fix "$file_path"; then
  exit 2
fi

# Run mypy --strict
if ! uv run mypy --strict "$file_path"; then
  exit 2
fi

# Success
exit 0
