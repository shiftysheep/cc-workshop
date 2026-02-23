# PRD: todd query command

## Overview

Add a default command to the `todd` CLI that accepts a natural language prompt as a
positional argument, sends it to Claude via the Claude Agent SDK, and prints the
result to stdout.

## Usage

```shell
uv run todd "what model are you running"
```

Expected output:
```
I'm running claude-sonnet-4-6.
```

## Requirements

### Functional

- `todd` accepts a single positional string argument (the prompt)
- The prompt is forwarded to Claude using the `claude-agent-sdk` Python package
- The final result text is printed to stdout
- No tools are required; this is a conversational query only (`allowed_tools=[]`)
- Authentication uses Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`) with standard AWS credential chain

### Non-Functional

- Fail with a clear error message if AWS credentials are not configured
- No streaming output; print the complete result once available

## Dependencies

Add to `pyproject.toml`:

```toml
"claude-agent-sdk>=0.1.0"
```

## Environment

```shell
export CLAUDE_CODE_USE_BEDROCK=1
# AWS credentials via standard chain (profile, instance role, env vars, etc.)
```

## Implementation Notes

Use the async `query` function from `claude_agent_sdk`. The result is available on
messages that have a `result` attribute. Wrap the async entrypoint with
`asyncio.run()` so Typer can call it synchronously.

## Out of Scope

- Conversation history / multi-turn sessions
- Tool use
- Streaming output
- System prompt configuration
