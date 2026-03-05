#!/usr/bin/env bash
# statusline.sh
# Git Bash statusline for Claude Code (Windows).
# Claude Code pipes JSON session data to stdin; this script writes one line to stdout.
#
# Install: copy to ~/.claude/statusline.sh
# Settings:
#   { "statusLine": { "type": "command", "command": "bash ~/.claude/statusline.sh" } }
#
# Requirements: bash, sed, awk, git — all present in Git for Windows. No Python or jq needed.

GREEN=$'\033[0;32m'
YELLOW=$'\033[0;33m'
RESET=$'\033[0m'

# Read all stdin as a single line for sed processing
json=$(cat | tr -d '\n')

# Extract fields with sed — no Python or jq required
model=$(printf '%s' "$json" | sed -n 's/.*"display_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
pct=$(printf '%s' "$json"   | sed -n 's/.*"used_percentage"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p')
raw_dir=$(printf '%s' "$json" | sed -n 's/.*"current_dir"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

# Defaults when fields are absent
[ -z "$model" ]   && model="claude"
[ -z "$pct" ]     && pct="0"
[ -z "$raw_dir" ] && raw_dir="$PWD"

# Normalise Windows backslashes to forward slashes
raw_dir=$(printf '%s' "$raw_dir" | sed 's|\\|/|g')

# Abbreviate home directory to ~
cwd="${raw_dir/#$HOME/\~}"

# Truncate deep paths: more than 3 components → .../<parent>/<last>
cwd=$(printf '%s' "$cwd" | awk -F'/' 'NF > 3 { print ".../" $(NF-1) "/" $NF; next } { print }')

# Git info with ANSI colours (omitted if not in a repo or git unavailable)
git_part=""
if command -v git >/dev/null 2>&1; then
  if git -C "$raw_dir" rev-parse --git-dir >/dev/null 2>&1; then
    branch=$(git -C "$raw_dir" branch --show-current 2>/dev/null)
    if [ -n "$(git -C "$raw_dir" status --porcelain 2>/dev/null)" ]; then
      state="${YELLOW}modified${RESET}"
    else
      state="${GREEN}clean${RESET}"
    fi
    git_part=" | ${state} | ${branch}"
  fi
fi

printf '%s | %s%% context | %s%s\n' "$model" "$pct" "$cwd" "$git_part"
