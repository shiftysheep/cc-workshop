# PRD: todd Interactive REPL

## Overview

Replace todd's single-shot query with an interactive terminal loop. After this
milestone, `uv run todd` opens a persistent session where users can send multiple
prompts to Claude and see responses — like a minimal Claude Code terminal.

## Usage

```shell
uv run todd
```

Expected session:
```
todd> what model are you running?
I'm running claude-sonnet-4-6.

todd> how many tokens was that?
That response used approximately 12 tokens.

todd> /exit
Bye.
```

## Requirements

### Functional

- Entering `uv run todd` (no positional argument) starts the REPL loop
- The loop reads a line of input, sends it to Claude, prints the response, repeats
- Conversation history accumulates across turns (each prompt/response pair added to messages)
- `/exit` or `/quit` typed at the prompt ends the session gracefully
- `Ctrl+C` ends the session gracefully (no traceback)
- The prompt prefix is `todd> `

### Non-Functional

- Existing `uv run todd "prompt"` single-shot mode must continue to work
- No streaming — print the complete response once available (streaming is Milestone 3)
- Authentication uses Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`) with standard AWS credential chain

## Dependencies

No new dependencies beyond Milestone 0 (`strands-agents`).

## Implementation Notes

- Use a `while True` loop with `input("todd> ")` to read prompts
- Maintain a `messages: list` that grows with each turn
- Pass the full message history to the SDK on each call
- Catch `KeyboardInterrupt` to handle Ctrl+C gracefully
- Check for `/exit` or `/quit` before sending to the SDK

## Out of Scope

- Streaming output (Milestone 3)
- Tool use (Milestone 2)
- Session persistence (Milestone 5)
- CLAUDE.md loading (Milestone 4)
