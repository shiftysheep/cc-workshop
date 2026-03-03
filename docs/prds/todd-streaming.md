# PRD: todd Streaming Output

## Overview

Show Claude's output token-by-token as it generates, rather than waiting for the
complete response. After this milestone, todd feels responsive — users see progress
immediately instead of waiting for a full response before anything appears.

## Usage

```shell
uv run todd
todd> explain how the ADW works
Explaining the ADW...
[text appears progressively as Claude generates it]
```

## Requirements

### Functional

- Text responses stream to the terminal as tokens arrive
- Tool calls display inline as they start and complete:
  - `[read src/todd/cli.py]` when the Read tool is called
  - `[read complete: 42 lines]` when it returns
- `Ctrl+C` during generation stops the stream gracefully (no traceback, prompt returns)
- After the stream completes, a newline is printed before the next `todd> ` prompt

### Non-Functional

- Streaming requires the SDK's stream event API (not the query function)
- Single-shot mode (`uv run todd "prompt"`) also streams

## Dependencies

No new dependencies beyond `strands-agents`.

## Implementation Notes

- Switch from the `query()` function to the SDK's streaming interface
- Handle `text_delta` events by writing to stdout without newlines
- Handle `tool_use` events by displaying the tool name and input
- Handle `tool_result` events by displaying the result summary
- Flush stdout after each write to ensure tokens appear immediately
- Catch `KeyboardInterrupt` to stop streaming and return to the prompt

## Out of Scope

- Rich terminal formatting (colors, spinners, progress bars)
- Streaming to a file or other output targets
