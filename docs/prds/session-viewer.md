Build a local, read-only web application for browsing Claude Code session history.
Claude Code stores conversation transcripts as JSONL files under ~/.claude/ — there's no built-in way to search, filter, or review past sessions. This tool fills that gap.

Core concept:
A FastAPI + Jinja2 server-rendered app that scans ~/.claude/projects/ and ~/.claude/transcripts/ for JSONL session files, parses them into structured messages, and presents them through a browseable web UI.

Session list page (/sessions):
- Table of all sessions showing title (extracted from first user message), project name, date, message count, and source (projects vs transcripts)
- Text search on session titles, dropdown filter by project, filter by source
- Pagination (configurable page size, default 25)
- Subagent sessions shown with visual indicators — parent sessions display child count, subagent rows show the agent slug and link back to the parent

Session detail page (/sessions/{id}):
- Full conversation rendered chronologically with each message type styled distinctly:
- User messages (blue) — render content as markdown, handle both flat content field and nested message.content format
- Assistant messages (gray) — display model name, render text blocks as markdown, show thinking blocks (collapsible, gold background) and tool use blocks (collapsible, orange background) inline
- Tool use/result messages (orange/green) — collapsible, show prettified JSON input and raw output
- System messages (purple) — plain text
- Session metadata header: project, date, token usage breakdown (input/output/cache), context window utilization percentage, git branch, working directory
- Expand All / Collapse All controls for thinking and tool blocks
- Navigation to parent session (if subagent) or list of child subagent sessions (if parent)

Subagent discovery:
- Claude Code spawns subagents whose transcripts live at ~/.claude/projects/{project}/{parentSessionId}/subagents/agent-{agentId}.jsonl
- Discover these automatically, build parent-child relationships, and enable bidirectional navigation between them

Data parsing requirements:
- Parse JSONL files line-by-line, skipping malformed lines gracefully
- Support a discriminated union of message types (user, assistant, tool_use, tool_result, system, summary, progress) with a RawMessage fallback for unknown types
- Handle two message formats: flat test-fixture style ({"type": "user", "content": "..."}) and real Claude Code nested style ({"type": "user", "message": {"role": "user", "content": "..."}})
- Normalize timestamps from both Unix milliseconds and ISO 8601 strings

Caching & performance:
- Lazy loading — no filesystem scan at startup, scan on first request
- Summary cache with configurable TTL (default 60s) and incremental refresh (only re-scan directories whose mtime changed)
- Detail cache with LRU eviction (default max 50 sessions, 300s TTL), invalidated on file mtime change
- Manual refresh endpoint and cache statistics API

REST API (/api/):
- GET /api/sessions — paginated, filtered session list (JSON)
- GET /api/sessions/{id} — full session detail (JSON)
- POST /api/refresh — force cache refresh
- GET /api/cache/stats — cache hit rates and sizes

Tech stack: Python 3.11+, FastAPI, Pydantic v2 with discriminated unions, Jinja2 templates, markdown + bleach for safe rendering,
Highlight.js (CDN) for syntax highlighting, vanilla CSS and JS (no framework), uv for package management.

Non-goals: No authentication (local-only), no write operations, no data persistence beyond the cache, macOS-only for v1.
