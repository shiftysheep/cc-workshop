# Module 6: Build a Claude Code Clone (Take-Home Project)

This module is a self-paced capstone project. You'll extend todd from a
single-shot prompt forwarder into an interactive agentic tool — a miniature
Claude Code clone.

**Use your ADW tools.** The commands, agents, and orchestrators you built in
Modules 3-5 are designed for exactly this kind of work. Try running
`/feature` or `/team:feature` against the PRDs below to let Claude drive
the implementation.

**Estimated time:** 2-4 hours across multiple sessions. Use `claude --resume`
to pick up where you left off.

---

## Key Concepts

| Concept | Why it matters |
|---------|---------------|
| **Incremental capability building** | Each milestone adds one layer of capability — tool use, context loading, REPL, streaming — so you always have a working harness |
| **Agent loop** | The core pattern of an agentic system: receive input → select tool → execute → observe → repeat until done |

---

## Glossary

| Term | Definition |
|------|-----------|
| **REPL** | Read-Eval-Print Loop — an interactive prompt that processes one input at a time and shows results immediately |
| **Open agent standards (AGENTS.md)** | Community conventions for describing agent capabilities and configurations in a portable, SDK-agnostic format |
| **Streaming** | Receiving and displaying LLM output token-by-token as it's generated, rather than waiting for the complete response |
| **Session persistence** | Saving conversation history to disk so it survives process restarts and can be resumed later |

---

## Where Todd Stands

After Module 5, todd can:
- `uv run todd "prompt"` — send one prompt to Claude via the Strands Agent SDK, print the response
- No conversation history, no tool use, no streaming, no CLAUDE.md loading

## The Goal

Build an open-source coding agent harness from scratch — no SDK dependency, just
Python and the Anthropic API. Each milestone adds one layer of capability. Work
through them in order; each builds on the last. By the end you'll have a
functional agent that can read files, edit code, load project context, stream
responses, and resume sessions.

**Use your ADW tools.** The commands, agents, and orchestrators you built in
Modules 3-5 are designed for exactly this kind of work. Try running
`/feature` or `/team:feature` against the milestone descriptions below to let
Claude drive the implementation.

---

## Milestone 1: Build the Tool-Use Loop

**Goal:** Implement a basic agent loop in Python — no SDK dependency, just the
Anthropic API.

**What to build:**

The core agent loop follows this pattern:

1. Read user input from the command line
2. Build a message and send it to the Anthropic API with tool definitions
3. Check the response for tool-use blocks
4. If tools were called: execute them, append results, send the updated
   conversation back to the API
5. If no tools were called: print the assistant's text response and exit

Start with just two tools: `read_file` (reads a file and returns its contents)
and `write_file` (writes content to a file path). Define them as JSON tool
schemas and implement the execution logic in Python.

**Acceptance criteria:**
- `uv run todd "read the file pyproject.toml and summarise it"` reads the file
  via tool use and prints a summary
- `uv run todd "create a file called hello.txt with the text 'hello world'"` writes
  the file via tool use
- The agent loops until the model stops requesting tools — no hardcoded turn limit
- No SDK dependency beyond `anthropic` (the official Python client)

**Exercise prompt:**

```
Build a tool-use agent loop in todd. Use the Anthropic Python client directly —
no agent SDK. The loop should: read user input, call the API with tool
definitions for read_file and write_file, execute any tool calls, and loop
until the model responds with text only. Keep it minimal — no streaming, no
REPL, just a single-shot prompt that can use tools.
```

---

## Milestone 2: Open Agent Standards

**Goal:** Implement support for AGENTS.md — a portable file that describes your
agent's capabilities and configuration.

**What to build:**

- On startup, check for an `AGENTS.md` file in the current working directory
- Parse it and include its contents in the system prompt sent to the Anthropic API
- Also check for an `.agents/` directory containing named agent configuration
  files (e.g., `.agents/code-reviewer.md`)
- If `AGENTS.md` exists, prepend its content to the system prompt so the model
  knows what tools are available and how to behave

This makes your harness portable: any project that includes an `AGENTS.md` file
can describe its own agent behaviour without modifying your code.

**Acceptance criteria:**
- Create an `AGENTS.md` in the project root describing todd's tools and behaviour
- `uv run todd "what tools do you have?"` responds based on the AGENTS.md content
- Removing `AGENTS.md` doesn't break the harness — it falls back to a default
  system prompt
- `.agents/` directory files are discoverable but not loaded unless explicitly
  referenced

**Exercise prompt:**

```
Add AGENTS.md support to todd. On startup, check for AGENTS.md in the current
directory and include its contents in the system prompt. Also scan for an
.agents/ directory with named agent configs. Create an AGENTS.md for this
project that describes the available tools (read_file, write_file) and the
agent's purpose.
```

---

## Milestone 3: Load .claude Project Context

**Goal:** Read CLAUDE.md and `.claude/` configuration to make the harness
compatible with Claude Code projects.

**What to build:**

- If `CLAUDE.md` exists in the project root, read it and include it in the
  system prompt (in addition to AGENTS.md if present)
- If `.claude/settings.json` exists, read it for tool permissions and
  environment configuration
- If `.claude/skills/` exists, list available skills and show them to the
  user on startup or when they type `/help`
- Layer the context: AGENTS.md (agent identity) + CLAUDE.md (project rules) +
  settings.json (permissions)

**Acceptance criteria:**
- todd loads CLAUDE.md from the current project and the model follows its
  instructions
- Available skills from `.claude/skills/` are listed when the user asks
- Missing files are handled gracefully — no errors if CLAUDE.md or .claude/
  doesn't exist
- The system prompt clearly separates agent identity (AGENTS.md) from project
  rules (CLAUDE.md)

**Exercise prompt:**

```
Add CLAUDE.md and .claude/ support to todd. Load CLAUDE.md into the system
prompt alongside AGENTS.md. Read .claude/settings.json for configuration.
Scan .claude/skills/ and show available skills to the user. Make sure
everything degrades gracefully when files are missing.
```

---

## Milestone 4: Add REPL and Streaming

**Goal:** Replace the single-shot query with an interactive REPL and enable
streaming responses.

**What to build:**

- Wrap the agent loop in an interactive Read-Eval-Print Loop: prompt the user
  for input, process it through the agent loop, display the result, repeat
- Enable streaming using the Anthropic SDK's streaming API — show tokens as
  they arrive rather than waiting for the complete response
- Add a `/exit` command to quit the REPL cleanly
- Add a `/help` command that lists available skills (including any from
  `.claude/skills/`)
- Handle `Ctrl+C` gracefully — interrupt the current generation without killing
  the process

**Acceptance criteria:**
- `uv run todd` (no arguments) enters interactive REPL mode
- `uv run todd "prompt"` still works as single-shot mode
- Responses stream token-by-token to the terminal
- Tool calls display inline (show what tool was called and its result)
- `/exit` and `Ctrl+C` work without tracebacks

**Exercise prompt:**

```
Add REPL and streaming to todd. Running with no arguments enters interactive
mode. Responses stream token-by-token using the Anthropic streaming API.
Add /exit and /help commands. Handle Ctrl+C to cancel generation without
crashing. Keep single-shot mode working for uv run todd "prompt".
```

---

## Milestone 5: Session Persistence

**Goal:** Save conversation history to disk so sessions survive process restarts.

**What to build:**

- After each turn, append the conversation messages to a JSONL file
- Session files live in `.sessions/` in the project root, named by timestamp
  (e.g., `.sessions/2025-01-15T10-30-00.jsonl`)
- On startup, load the most recent session automatically (or start fresh with
  a `--new` flag)
- Add a `--session <filename>` flag to resume a specific session by name
- Each line in the JSONL file is one message (role + content), making it easy
  to parse and inspect

**Acceptance criteria:**
- Closing and reopening todd resumes the previous conversation
- `uv run todd --new` starts a fresh session
- `uv run todd --session .sessions/2025-01-15T10-30-00.jsonl` resumes a
  specific session
- Session files are valid JSONL — one JSON object per line
- The model remembers context from previous turns in the loaded session

**Exercise prompt:**

```
Add session persistence to todd. Save conversation history as JSONL in a
.sessions/ directory. Load the most recent session on startup. Add --new to
start fresh and --session to resume a specific file. Each line should be one
message object with role and content.
```

---

## Operational Reference

As you build, these operational skills will be useful:

| Skill | How | When |
|-------|-----|------|
| Cost tracking | `/cost`, `/stats` | Monitor spend per session |
| Effort levels | `/model` → low/medium/high | Balance cost vs quality |
| Extended thinking | `Alt+T` | Complex reasoning tasks |
| Checkpointing | `Esc+Esc`, `/rewind` | Recover from wrong directions (file edits only, not bash) |
| Headless testing | `claude -p "prompt"` | Test todd features non-interactively |
| CI/CD patterns | `gh pr diff \| claude -p "review"` | Automate reviews in pipelines |

---

## Further Reading

- [Claude Code docs](https://code.claude.com/docs/en) — the product you're building toward
- [Anthropic API docs](https://docs.anthropic.com/en/api) — the API your harness calls directly
- [AGENTS.md spec](https://github.com/anthropics/agents-md) — the open agent standards convention
- IDE integrations: VS Code extension, JetBrains plugin
- Plugins: `/plugin` marketplace for shared skills

---

[← Module 5](module5.md)
