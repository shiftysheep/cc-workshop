# PRD: todd Session Persistence

## Overview

Save conversation history to disk so sessions can be resumed across terminal
restarts — mirroring the `claude --continue` and `claude --resume` behavior
that participants learned in Module 2.

## Usage

```shell
# Name the session and exit
uv run todd
todd> /rename todd-refactor
todd> /exit

# Resume later
uv run todd --resume todd-refactor
todd> where were we?
[Claude has full context of the previous conversation]

# Or resume the most recent session
uv run todd --continue
```

## Requirements

### Functional

- On `/exit` or `Ctrl+C`, save the conversation history to disk
- Sessions are stored as JSON files in `~/.todd/sessions/<session-id>.json`
- Each session file contains: session ID, name, timestamp, message history
- `/rename <name>` sets a human-readable name for the current session
- `todd --continue` resumes the most recent session by modification time
- `todd --resume <name>` resumes a session by name (substring match)
- `todd --resume` with no argument lists available sessions and prompts for choice
- `/sessions` in the REPL lists available sessions

### Non-Functional

- Session files are human-readable JSON
- A new session is created if no matching session is found for `--resume`
- Session IDs are 8-character hex strings (same pattern as ADW IDs)

## Dependencies

No new dependencies beyond `claude-agent-sdk>=0.1.0`.

## Implementation Notes

- Create `~/.todd/sessions/` on first run if it doesn't exist
- Session ID is generated with `secrets.token_hex(4)`
- The message history stored is the same list passed to the SDK — portable JSON
- On resume, load messages and pass as initial history to the SDK loop

## Out of Scope

- Session encryption or access control
- Cloud sync or backup
- Session branching (multiple paths from one checkpoint)
- `/export` command (can be added later)
