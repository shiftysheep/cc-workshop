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

> **What is a plugin?** A plugin is a packaged bundle of Claude Code extensions —
> commands, skills, agents, hooks, and MCP servers — that you can install in one
> step. The `/plugin` command connects to **marketplaces** (public or enterprise)
> where teams publish and discover these packages. Context7 is a community plugin
> from the public marketplace. In Module 3, we'll install a plugin from our
> enterprise marketplace that adds document authoring skills.
>
> Think of it like npm or pip, but for Claude Code capabilities.

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

## 3. Switch to Opus Plan Mode

For the next task we're going to ask Claude to architect and implement a new feature.
This is exactly the kind of consequential, multi-step work that benefits from a more
capable model and a review step before any code is written.

In the chat box, run:

```
/model opusplan
```

> Run `/model opusplan` to switch. We'll explain what this model alias does after
> you've seen it in action during plan mode.

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

> **Tenet 2: Be specific.** Compare this prompt to a vague "build me a query
> command." The PRD references exact files (`src/todd/`), specifies dependencies
> (`claude-agent-sdk`), defines expected output, and lists what's out of scope.
> Each constraint reduces the space Claude has to guess — and guessing wastes
> context tokens on clarification loops.

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

## 9. Understanding Model Selection

Claude Code supports multiple models, each suited to different tasks:

| Model | Strengths | Typical use |
|-------|-----------|-------------|
| **Opus 4.6** | Deep reasoning, architecture, complex analysis | Planning, code review, design decisions |
| **Sonnet 4.6** | Fast, capable code generation | Implementation, refactoring, most daily work |
| **Haiku 4.5** | Lightweight, very fast | Exploration subagents, simple searches |

The `opusplan` alias you used earlier is a hybrid mode:

| Phase | Model | Purpose |
|-------|-------|---------|
| Planning | Opus 4.6 | Deep reasoning, architecture decisions |
| Execution | Sonnet 4.6 | Code generation, implementation |

Compare to `/model opus` which uses Opus for everything (higher cost). `opusplan`
gives you Opus reasoning where it matters most and Sonnet speed for the rest.

---

## 10. Test the New Command

Once Claude is done, verify it works directly from the chat box:

```shell
!uv run todd "what model are you running"
```

You should see a response from Claude describing which model is active.

---

## 11. Write a Verification Test

Before committing, let's verify the feature with an automated test — not just a
manual check.

In the chat box, enter:

```markdown
Write a test for the todd query command in tests/test_query.py.
The test should verify that the query function returns a non-empty string
when given a simple prompt. Use pytest and mock the Claude Agent SDK call
so the test runs without Bedrock credentials.
```

After Claude creates the test, run it:

```shell
!uv run pytest tests/ -v
```

> **Tenet 1: Verify your work.** The `!uv run todd` check from the previous step
> was a manual spot-check — it proves the feature works *right now*, but it won't
> catch regressions. An automated test locks in the expected behavior permanently.
> This is Anthropic's #1 best practice: "Tests and expected outputs are the single
> highest-leverage thing you can provide."

---

## 12. Commit and Proceed

Ask Claude to commit the changes, then advance to the next module:

```markdown
Commit the changes and then run /module to proceed to module 3.
```

---

[← Module 1](module1.md)
