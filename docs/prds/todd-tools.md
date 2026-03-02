# PRD: todd Tool Use

## Overview

Register filesystem and shell tools with the Agent SDK so todd can act on the
codebase — reading files, writing code, running commands. After this milestone,
todd functions as a basic agentic coding tool.

## Usage

```shell
uv run todd
todd> read src/todd/cli.py and tell me what it does
[Claude reads the file and explains it]

todd> add a hello command to the CLI
[Claude reads, edits, and verifies the change]
```

## Requirements

### Functional

- Register these tools with the SDK: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`
- Tool calls are executed automatically during the agent loop
- Tool results (file contents, command output) are passed back to Claude
- For destructive operations (`Write`, `Edit`, `Bash`), display what will happen and
  prompt the user for confirmation before executing
- Tool call display: show the tool name and key argument before executing

### Non-Functional

- Confirmation prompt must be skippable via a `--yes` / `-y` flag on the CLI
- Existing single-shot mode (`uv run todd "prompt"`) also gets tool support
- Authentication uses Amazon Bedrock (`CLAUDE_CODE_USE_BEDROCK=1`)

## Dependencies

No new dependencies beyond `claude-agent-sdk>=0.1.0`.

## Implementation Notes

- The SDK's `allowed_tools` parameter controls which tools are available
- Each tool is a callable that the SDK invokes automatically when Claude requests it
- Wrap each tool call in a confirmation prompt for destructive operations
- The `Bash` tool is the highest-risk tool — limit to a reasonable set of safe commands
  or always require confirmation

## Out of Scope

- Custom tool definitions beyond the standard set
- Sandboxing (filesystem isolation)
- Permission levels or role-based tool access
