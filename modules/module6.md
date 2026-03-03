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

Build these capabilities incrementally. Each milestone has a PRD in `docs/prds/`
that defines the feature. Work through them in order — each builds on the last.

---

## Milestone 1: Interactive REPL

**PRD:** `docs/prds/todd-repl.md`

Replace the single-shot query with an interactive terminal loop:
- Read-eval-print loop with prompt handling
- Conversation history (accumulating messages across turns)
- Graceful exit (Ctrl+C, /exit)
- Session display (show Claude's responses as they complete)

---

## Milestone 2: Tool Use

**PRD:** `docs/prds/todd-tools.md`

Register tools with the Strands Agent SDK so todd can act on the filesystem:
- Read, Write, Edit — file operations
- Bash — shell command execution
- Glob, Grep — search operations
- Permission prompts before destructive operations

---

## Milestone 3: Streaming Output

**PRD:** `docs/prds/todd-streaming.md`

Show Claude's output token-by-token as it generates:
- Stream text responses to the terminal
- Display tool calls and their results inline
- Handle interrupts (Ctrl+C to stop generation)

---

## Milestone 4: CLAUDE.md Loading

**PRD:** `docs/prds/todd-context.md`

Discover and load context engineering files:
- Auto-discover CLAUDE.md (project root, user home, .claude/ directory)
- Load as system prompt content
- Support @file import syntax

---

## Milestone 5: Session Persistence

**PRD:** `docs/prds/todd-sessions.md`

Save and resume conversations:
- Serialize conversation history to disk
- `todd --continue` (most recent) and `todd --resume` (by name)
- `/rename` for session naming

---

## Milestone 6 (Optional): Claude Code Session Viewer

**PRD:** `docs/prds/session-viewer.md`

Build a local web app for browsing Claude Code session history:
- FastAPI + Jinja2 server-rendered app
- Scans `~/.claude/projects/` for JSONL session files
- Session list page with search, filters, and pagination
- Session detail page with messages styled by type (user, assistant, tool use)
- REST API at `/api/sessions` for programmatic access
- Subagent session discovery with parent-child navigation

This ties together everything from the workshop: JSONL parsing (Module 5),
Python tooling (Module 1), API design, and the session log format you analyzed
in the headless mode exercises.

> **Use your ADW tools.** Run `/feature @docs/prds/session-viewer.md` to let
> the orchestrator drive the implementation, or work through it interactively.

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

- [Claude Code docs](https://code.claude.com/docs/en) — the product you're cloning
- [Strands Agent SDK](https://github.com/strands-agents/sdk-python) — the library powering todd
- IDE integrations: VS Code extension, JetBrains plugin
- Plugins: `/plugin` marketplace for shared skills

---

[← Module 5](module5.md)
