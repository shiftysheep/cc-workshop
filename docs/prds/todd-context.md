# PRD: todd CLAUDE.md Loading

## Overview

Auto-discover and load CLAUDE.md context files as the system prompt, so todd
behaves consistently with project-specific conventions — the same way Claude Code
reads CLAUDE.md on startup.

## Usage

Given a `CLAUDE.md` in the project root:
```markdown
## Project
todd is a Typer CLI built with Python 3.13+ and uv.
Always use type annotations. Run tests with `uv run pytest`.
```

```shell
uv run todd
todd> what's the test command for this project?
Based on the project context, the test command is `uv run pytest`.
```

## Requirements

### Functional

- On startup, search for CLAUDE.md files in this order:
  1. `~/.claude/CLAUDE.md` (global user config)
  2. `~/.claude/CLAUDE.md.local` (global personal overrides)
  3. `./CLAUDE.md` (project root)
  4. `./.claude/CLAUDE.md.local` (project personal overrides)
- Load all discovered files and concatenate their contents
- Pass the combined content as the system prompt to the SDK
- Support `@<filepath>` import syntax: if a CLAUDE.md line starts with `@`,
  read the referenced file and inline its contents
- If no CLAUDE.md files are found, proceed without a system prompt (no error)

### Non-Functional

- File discovery is silent — no output when loading context
- Invalid `@file` references are skipped with a warning to stderr
- Maximum total system prompt size: 100KB (truncate with a warning if exceeded)

## Dependencies

No new dependencies beyond `claude-agent-sdk>=0.1.0`.

## Implementation Notes

- Discovery order matters: later files can override earlier ones
- The `@` import is a simple text substitution before passing to the SDK
- Relative paths in `@` imports resolve from the CLAUDE.md file's directory

## Out of Scope

- `@url` imports
- `@agent` scoped rules
- Hot-reloading CLAUDE.md during a session
