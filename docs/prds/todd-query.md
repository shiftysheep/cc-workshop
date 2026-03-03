# PRD: todd CLI

## Overview

`todd` is a single-purpose CLI that accepts a natural language prompt as a positional
argument, sends it to Claude via the Strands Agent SDK, and prints the result to
stdout. This replaces the scaffold's greeting with a prompt-accepting default command.

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
- The prompt is forwarded to Claude using the `strands-agents` Python package
- The final result text is printed to stdout
- No tools are required; this is a conversational query only (`tools=[]`)
- Authentication uses a `BedrockModel` with standard AWS credential chain

### Non-Functional

- Authentication issues are surfaced by SDK exceptions — no additional handling is needed
- No streaming output; print the complete result once available

## Dependencies

Add to `pyproject.toml`:

```toml
"strands-agents"
```

## Environment

```shell
export CLAUDE_CODE_USE_BEDROCK=1
# AWS credentials via standard chain (profile, instance role, env vars, etc.)
# Strands uses Bedrock/Anthropic models directly — no CLAUDECODE guard var is set,
# so uv run todd works seamlessly inside a Claude Code session.
```

## Implementation Notes

Create an `Agent` using `BedrockModel` from `strands_agents` and `strands_agents.models.bedrock`.
Invoke the agent with the prompt string; the result is the agent's text response.
The call is synchronous — no `asyncio.run()` wrapper needed.

## Out of Scope

- Conversation history / multi-turn sessions
- Tool use
- Streaming output
- System prompt configuration
