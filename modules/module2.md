# Module 2: MCP, Plan Mode, and the Agent SDK

In this module we'll install our first MCP server, explore how tools load on demand via ToolSearch,
switch to a more capable model for planning, and build a real feature using the
Strands Agent SDK.

---

## Key Concepts

| Concept | Why it matters |
|---------|---------------|
| **Context window** | The total amount of text Claude can see at once. Your conversation history, file contents, tool results, and system instructions all share this space. When it fills up, older content is summarised or dropped. |
| **Plan mode** | A read-only mode (`Shift+Tab` twice) where Claude explores the codebase, asks clarifying questions, and produces a plan — but cannot write or edit files until you approve. Used before consequential, multi-step work. |
| **Context rot** | The gradual degradation of response quality as the context window fills up. Claude 4.6 models handle long contexts better than earlier generations, but they are not immune — older content still gets compressed or dropped in very long sessions, causing Claude to lose track of earlier instructions, decisions, or important details. |
| **Context poisoning** | When incorrect, misleading, or contradictory information enters the context and skews all subsequent responses. Common sources: a failed tool call Claude misinterprets, a wrong assumption made early in a session that gets reinforced, or a bad test result Claude reasons from incorrectly. Unlike context rot, poisoning can happen even in a mostly empty context. |

## Glossary

| Term | Definition |
|------|-----------|
| **MCP (Model Context Protocol)** | An open standard that lets AI assistants connect to external tools and data sources. An MCP server is a program that exposes capabilities — like fetching documentation — as tools Claude can call. |
| **Token** | The basic unit Claude uses to process text. Roughly 1 token ≈ 4 characters. Your context window holds a fixed number of tokens, which is why managing what's in it matters. |
| **Tool call** | When Claude invokes one of its available tools (e.g. `Read`, `Bash`) to perform an action. You'll see these logged in the terminal as Claude works. |
| **PRD (Product Requirements Document)** | A document describing what a feature should do, without specifying how to implement it. We use one to give Claude clear, stable requirements before it starts planning. |
| **Strands Agent SDK** | A Python library for building AI agents. We use it to give todd its own agent loop — send a prompt, get a response — backed by Claude on Amazon Bedrock. |
| **Subagent** | An isolated Claude instance spawned for a focused subtask. Each subagent gets a fresh context window, restricted tools, and its own model. Built-in types — Explore, Plan, General-purpose — keep expensive work from polluting the main conversation. |
| **Learning test** | A test that verifies assumptions about an external library you don't control. Exercises the real library directly — not mocks — so behavioural changes surface immediately on upgrades. |
| **Amazon Bedrock** | AWS's managed AI service. We use it as the authentication and inference layer for Claude so we don't need a direct Anthropic API key. |

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
| `Agent` | Spawns a subagent to handle a focused subtask |

**Context7 MCP tools** (installed in step 2)

| Tool | What it does |
|------|-------------|
| `resolve-library-id` | Converts a library name (e.g. `typer`) into a Context7 ID |
| `query-docs` | Fetches current, version-specific documentation for a library |

---

## 1. Configure the Language Server

A language server gives Claude real-time type feedback as it generates code — instead
of waiting for `mypy` to run at commit time, you see red squiggles the moment a type
error is introduced.

**Install the Pyright plugin:**

```shell
claude plugin install pyright-lsp@claude-plugins-official
```

Or discover it interactively: type `/plugins` → **Discover** → search for `pyright-lsp`.

**Ensure the binary is available:**

```shell
# Using uv (recommended for this project)
uv tool install pyright

# Or via npm
npm install -g pyright
```

**VS Code users:** You get an additional tool for free. The Claude Code IDE extension
automatically provides `getDiagnostics`, which bridges all of VS Code's diagnostics
(Pylance, ESLint, and any other language extensions) directly into Claude Code. This
is complementary to the LSP plugin — `getDiagnostics` runs automatically on file
changes, while the LSP tool requires explicit tool calls. Install pyright-lsp above
for both capabilities.

> **Why LSP matters for agentic workflows.** The `pyright-lsp` plugin works in both
> the CLI and VS Code. The `getDiagnostics` tool is VS Code-only. Together they give
> Claude the same signals a human developer gets from their editor: real-time type
> errors, missing imports, and signature mismatches — caught while Claude is still
> in context, not after the fact at commit time. This tightens the feedback loop
> and reduces the back-and-forth of "run mypy → see error → ask Claude to fix it."

### Enable the LSP Tool

Add `ENABLE_LSP_TOOL` to your `.claude/settings.json` to activate Claude's Language Server Protocol integration:

```json
{
  "env": {
    "ENABLE_LSP_TOOL": "1"
  }
}
```

Save the file and restart Claude Code for the setting to take effect.

---

## 2. Install the Context7 MCP Server

Context7 is an MCP server that injects live, version-specific library documentation
into Claude's context on demand. Instead of relying on potentially outdated training
data, Claude fetches current docs from the source and uses them to generate accurate
code.

In the chat box, run:

```shell
claude plugin install context7 --scope user
```

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

> **Security: the lethal trifecta.** Simon Willison
> [identifies three capabilities](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
> that, combined in an AI agent, create serious security risk:
> **(1)** access to private data, **(2)** exposure to untrusted content, and
> **(3)** the ability to communicate externally. An MCP server can grant all
> three — file-system tools read private data, web-fetching tools ingest
> untrusted content, and API tools can send data out. Claude Code's permission
> prompts are your first line of defense, but they're not a substitute for
> reviewing what tools a plugin actually installs. Before you approve, check
> the tool list and understand what each one does.

> **More MCP examples.** Teams build plugins for nearly any workflow:
> - **Jira/Confluence** — Read Jira tickets and Confluence pages directly from Claude.
>   Pull requirements and meeting notes without switching tools.
> - **Lucidchart** — Diagramming MCP servers let Claude generate or update visual
>   diagrams as part of documentation workflows.
> - Discover more through the `/plugin` marketplace — browse the **Discover** tab
>   to see community and enterprise plugins.

---

## 3. Examine Context Utilization

MCP servers register tools that Claude discovers on demand via ToolSearch. Let's see
what your context looks like before we start building.

In the chat box, run:

```
/context
```

The colored grid shows how much of your context window is currently in use. Note the
baseline now that Context7 is installed — MCP tool definitions are deferred via
ToolSearch and only load into context when Claude needs them. This keeps your idle
context lean.

Now try:

```
/clear
```

This resets your conversation entirely — a fresh context with zero history. You're
back to a clean slate with only your CLAUDE.md and system instructions loaded.

> **When to use each:**
>
> - **`/context`** — check how full your context is. Use it periodically during long
>   sessions to decide whether to continue or start fresh.
> - **`/clear`** — reset when your context is polluted, you're switching tasks, or
>   Claude starts producing degraded responses (a sign of context rot). Cheaper than
>   closing and reopening Claude.

> **Why this matters:** Context is finite. With ToolSearch, MCP tools no longer add
> idle overhead — but once loaded, they stay in context for the session. Subagents
> remain valuable because each gets a fresh context window with only the tools it
> needs.

---

## 4. Switch to Opus Plan Mode

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

## 5. Activate Plan Mode and Note the Status Line

Activate plan mode by pressing `Shift+Tab` twice. You'll see the status line update
to show `⏸ plan mode on`.

> **Plan mode** restricts Claude to read-only operations. It will explore your
> codebase, ask clarifying questions, and produce a detailed plan — but it will not
> write or edit any files until you approve.
>
> Notice the model shown in your status line has changed to reflect Opus. This is the
> heads-up display you configured in Module 1 paying off.

---

## 6. Build the todd Query Command

Now let's put it to work. We have a requirements document ready at
`docs/prds/todd-query.md`. Enter this prompt in the chat box:

```markdown
Read docs/prds/todd-query.md and create a plan to implement the todd query command.
```

Claude will read the PRD, explore the existing codebase, and return a plan before
touching any code.

> **Tenet 2: Be specific.** Compare this prompt to a vague "build me a query
> command." The PRD references exact files (`src/todd/`), specifies dependencies
> (`strands-agents`), defines expected output, and lists what's out of scope.
> Each constraint reduces the space Claude has to guess — and guessing wastes
> context tokens on clarification loops.

---

## 7. Understanding Subagents and Context

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

Subagents also help guard against **context rot** and **context poisoning**. Claude
4.6 models handle long contexts better than earlier generations, but they are not
immune — in extended sessions, older content still gets compressed. Because each
subagent starts with a fresh context, a noisy or incorrect result from one task can't
accumulate and corrupt the reasoning in the main conversation. If a subagent goes
wrong, you restart that subagent — not your entire session.

> **Session management — resuming, naming, and branching.**
>
> - **`claude --continue`** — resumes the most recent session automatically, no picker needed.
> - **`claude --resume`** — interactive picker to choose a named session by title.
> - **`/rename <name>`** — labels the current session for easy recall later.
> - **Rewind (`Esc+Esc`)** — undo Claude's recent file edits and the conversation up to a
>   chosen checkpoint. Only tracks changes made via Write/Edit tools — not bash commands.
> - **Fork (`/fork`)** — creates a new branch of the conversation from the current point,
>   preserving the original session. Useful for trying an alternate approach without losing
>   your current context.

---

## 8. Review and Approve the Plan

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

## 9. Implement the Plan

Once you're satisfied with the plan, confirm it. Claude will switch from Opus to
Sonnet and begin implementing — creating files, updating `pyproject.toml`, and
writing the code described in the plan.

---

## 10. Understanding Model Selection

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

> **Pro tip — effort levels.** Each model also has effort levels (low / medium /
> high). Run `/model`, then press the **left/right arrow keys** to cycle through
> effort levels before confirming. Low for quick edits, high for complex reasoning.
> Extended thinking (`Alt+T`) gives Claude a scratchpad for longer chains. Both
> affect cost and quality.

---

## 11. Test the New Command

Once Claude is done, verify it works directly from the chat box:

```shell
!uv run todd "what model are you running"
```

You should see a response from Claude describing which model is active.

---

## 12. Write a Verification Test

Before committing, let's verify the feature with an automated test — not just a
manual check.

In the chat box, enter:

```markdown
Write a test for the todd query command in tests/test_query.py.
The test should verify that the query function returns a non-empty string
when given a simple prompt. Use pytest and mock the Strands Agent SDK call
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

## 13. Learning Tests

**Learning tests** verify assumptions about external libraries you don't control. When you write mocks, you encode assumptions about how a library behaves — learning tests validate those assumptions by exercising the real library directly.

> **Timing matters.** Write learning tests during the **research** phase — before you
> commit to a plan. If your plan assumes a library behaves a certain way, a learning
> test written early will catch the mistake before you've built on it. Discovering a
> wrong assumption after implementation is much more expensive than discovering it
> during research.

### Exercise

Ask Claude to write learning tests for the Strands Agent SDK:

```markdown
Write learning tests that verify:
1. An Agent created with `tools=[]` cannot invoke any tools — the model
   receives an empty tool list and tool-use requests are absent
2. An Agent created with specific tools only has access to those tools —
   the agent's tool registry matches what you configured
3. Conversation history accumulates across multiple agent calls —
   send two prompts and verify the messages list grows
```

> **When to write learning tests**
>
> - Adding a **new dependency**: lock in your understanding of how it works
> - **Upgrading a version**: catch behavioral changes before they break your mocks
> - **Unsure about behavior**: use tests to explore the library, not guesswork
>
> Think of learning tests as **assumption back pressure** — they make your
> assumptions explicit and testable, so library changes surface immediately
> rather than silently invalidating your mock expectations.

---

## 14. Commit and Proceed

Ask Claude to commit the changes, then advance to the next module:

```markdown
Commit the changes and then run /module to proceed to module 3.
```

---

[← Module 1](module1.md)   [Module 3 →](module3.md)
