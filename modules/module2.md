# Module 2: MCP, Plan Mode, and the Claude Agent SDK

In this module we'll install our first MCP server, explore how it affects context,
switch to a more capable model for planning, and build a real feature using the
Claude Agent SDK.

---

## Key Concepts

| Term | Definition |
|------|-----------|
| **MCP (Model Context Protocol)** | An open standard that lets AI assistants connect to external tools and data sources. An MCP server is a program that exposes capabilities — like fetching documentation — as tools Claude can call. |
| **Context window** | The total amount of text Claude can see at once. Your conversation history, file contents, tool results, and system instructions all share this space. When it fills up, older content is summarised or dropped. |
| **Token** | The basic unit Claude uses to process text. Roughly 1 token ≈ 4 characters. Your context window holds a fixed number of tokens, which is why managing what's in it matters. |
| **Tool call** | When Claude invokes one of its available tools (e.g. `Read`, `Bash`) to perform an action. You'll see these logged in the terminal as Claude works. |
| **PRD (Product Requirements Document)** | A document describing what a feature should do, without specifying how to implement it. We use one to give Claude clear, stable requirements before it starts planning. |
| **Claude Agent SDK** | A Python/TypeScript library that exposes the same agent loop powering Claude Code — built-in tools, subagent spawning, session management — so you can embed Claude's capabilities directly in your own programs. |
| **Amazon Bedrock** | AWS's managed AI service. We use it as the authentication and inference layer for Claude so we don't need a direct Anthropic API key. |
| **Context rot** | The gradual degradation of response quality as the context window fills up. Older content gets compressed or dropped, causing Claude to lose track of earlier instructions, decisions, or important details. Long-running sessions are most vulnerable. |
| **Context poisoning** | When incorrect, misleading, or contradictory information enters the context and skews all subsequent responses. Common sources: a failed tool call Claude misinterprets, a wrong assumption made early in a session that gets reinforced, or a bad test result Claude reasons from incorrectly. Unlike context rot, poisoning can happen even in a mostly empty context. |

---

## Tools in this module

As Claude works you'll see it calling tools in the terminal output. Here's what each
one does:

**Built-in tools**

| Tool | What it does |
|------|-------------|
| `Read` | Reads a file from the filesystem |
| `Write` | Creates a new file |
| `Edit` | Makes targeted edits to an existing file |
| `Glob` | Finds files by pattern (e.g. `**/*.py`) |
| `Grep` | Searches file contents with regex |
| `Bash` | Runs a shell command |
| `Task` | Spawns a subagent to handle a focused subtask |

**Context7 MCP tools** (installed in step 1)

| Tool | What it does |
|------|-------------|
| `resolve-library-id` | Converts a library name (e.g. `typer`) into a Context7 ID |
| `query-docs` | Fetches current, version-specific documentation for a library |

---

## Built-in Slash Commands

Claude Code ships with a set of built-in slash commands. You'll use several of them
in this module. Custom commands — which we'll build in Module 3 — extend this list
with your own workflows.

**Session & model**

| Command | Description |
|---------|-------------|
| `/model` | Switch the active model |
| `/resume` | Resume a previous session by ID, name, or picker |
| `/rename` | Rename the current session |
| `/clear` | Clear conversation history |
| `/compact` | Compact conversation to free context, with optional focus instructions |
| `/rewind` | Rewind conversation and/or code to a previous point |

**Context & visibility**

| Command | Description |
|---------|-------------|
| `/context` | Visualize context window usage as a colored grid |
| `/cost` | Show token usage for the current session |
| `/stats` | Show daily usage, session history, and model preferences |
| `/usage` | Show plan limits and rate limit status |
| `/tasks` | List and manage background tasks |
| `/todos` | List current TODO items |

**Configuration**

| Command | Description |
|---------|-------------|
| `/plugin` | Browse and install plugins from the marketplace |
| `/mcp` | Manage MCP server connections |
| `/permissions` | View or update tool permissions |
| `/memory` | Edit CLAUDE.md memory files |
| `/init` | Initialize a project with a CLAUDE.md |
| `/statusline` | Configure the status line |
| `/config` | Open settings |
| `/theme` | Change the color theme |
| `/vim` | Enable vim-style editing |

**Utilities**

| Command | Description |
|---------|-------------|
| `/plan` | Enter plan mode |
| `/export` | Export the conversation to a file or clipboard |
| `/copy` | Copy the last response to clipboard |
| `/debug` | Read the session debug log |
| `/doctor` | Check Claude Code installation health |
| `/help` | Show usage help |
| `/exit` | Exit the session |

> **Note:** MCP servers can also expose prompts that appear as slash commands in the
> format `/mcp__<server>__<prompt_name>`.

---

## 1. Install the Context7 MCP Server

Context7 is an MCP server that injects live, version-specific library documentation
into Claude's context on demand. Instead of relying on potentially outdated training
data, Claude fetches current docs from the source and uses them to generate accurate
code.

In the chat box, run:

```
/plugin
```

Browse to the **Discover** tab, find **context7**, and install it at **user** scope.

> **What just happened?** The plugin manager configured a new MCP server for your
> session. Claude now has access to two new tools: `resolve-library-id` and
> `query-docs`. Any time you ask about a library, Claude can pull current docs
> rather than relying on training data.

---

## 2. Examine Context Utilization

MCP servers add tools to Claude's context window on every request. Let's see what
that looks like before we start building.

In the chat box, run:

```
/context
```

The colored grid shows how much of your context window is currently in use. Note the
baseline now that Context7 is installed — tool definitions for MCP servers consume
tokens even when the tools aren't called.

> **Why this matters:** Context is finite. Knowing your utilization helps you decide
> when to use subagents (which get their own fresh context window) versus working
> directly in the main conversation.

---

## 3. Switch to Opus + Plan Mode

For the next task we're going to ask Claude to architect and implement a new feature.
This is exactly the kind of consequential, multi-step work that benefits from a more
capable model and a review step before any code is written.

In the chat box, run:

```
/model opusplan
```

> **What is `opusplan`?** It's a hybrid model alias:
>
> | Phase | Model | Purpose |
> |-------|-------|---------|
> | Planning | Opus 4.6 | Deep reasoning, architecture decisions |
> | Execution | Sonnet 4.6 | Code generation, implementation |
>
> Compare to `/model opus` which uses Opus for everything (higher cost). `opusplan`
> gives you Opus reasoning where it matters most and Sonnet speed for the rest.

---

## 4. Activate Plan Mode and Note the Status Line

Activate plan mode by pressing `Shift+Tab` twice. You'll see the status line update
to show `⏸ plan mode on`.

> **Plan mode** restricts Claude to read-only operations. It will explore your
> codebase, ask clarifying questions, and produce a detailed plan — but it will not
> write or edit any files until you approve.
>
> Notice the model shown in your status line has changed to reflect Opus. This is the
> heads-up display you configured in Module 1 paying off.

---

## 5. Build the todd Query Command

Now let's put it to work. We have a requirements document ready at
`docs/prds/todd-query.md`. Enter this prompt in the chat box:

```markdown
Read docs/prds/todd-query.md and create a plan to implement the todd query command.
```

Claude will read the PRD, explore the existing codebase, and return a plan before
touching any code.

---

## 6. Understanding Subagents and Context

While Claude is working on the plan, here's what's happening under the hood.

**Subagents are isolated Claude instances.** When Claude delegates a focused task
(like exploring files or running searches), it spawns a subagent with:

- Its own fresh context window — verbose search output doesn't pollute your main conversation
- Restricted tools — an Explore subagent has read-only access by design
- Its own model — Claude Code uses Haiku for fast, cheap exploration tasks

**Built-in subagents in Claude Code:**

| Subagent | Model | Tools | Used for |
|----------|-------|-------|----------|
| Explore | Haiku | Read-only | File discovery, code search |
| Plan | Inherits | Read-only | Codebase research during plan mode |
| General-purpose | Inherits | All | Complex multi-step tasks |
| statusline-setup | Sonnet | Specialized | Configures your status line via `/statusline` |
| Claude Code Guide | Haiku | Docs/knowledge | Answers questions about Claude Code features |

**Context flows like this:**

```
Your conversation (limited)
    ├─→ Explore subagent (fresh context) → returns summary
    └─→ Main conversation continues with space preserved
```

This is why delegating expensive searches to subagents is good practice — and it's
exactly what Claude Code does automatically when you're in plan mode.

Subagents also help guard against **context rot** and **context poisoning**. Because
each subagent starts with a fresh context, a noisy or incorrect result from one task
can't accumulate and corrupt the reasoning in the main conversation. If a subagent
goes wrong, you restart that subagent — not your entire session.

---

## 7. Review and Approve the Plan

Claude will present a plan showing:

- Files to create or modify
- The implementation approach for each change
- Dependencies to add

Read it carefully. You can:
- **Accept** — type a confirmation and Claude will begin implementing
- **Refine** — ask follow-up questions or request changes before proceeding
- **Edit directly** — press `Ctrl+G` to open the plan in your editor

> **Take your time here.** Plan mode exists precisely so you don't have to undo
> changes after the fact. The cost of reviewing is much lower than the cost of
> reverting a bad implementation.

---

## 8. Implement the Plan

Once you're satisfied with the plan, confirm it. Claude will switch from Opus to
Sonnet and begin implementing — creating files, updating `pyproject.toml`, and
writing the code described in the plan.

---

## 9. Test the New Command

Once Claude is done, verify it works directly from the chat box:

```shell
!uv run todd "what model are you running"
```

You should see a response from Claude describing which model is active.

---

## 10. Commit and Proceed

Ask Claude to commit the changes, then advance to the next module:

```markdown
Commit the changes and then run /module to proceed to module 3.
```

---

[← Module 1](module1.md)
