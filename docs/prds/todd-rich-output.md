# PRD: Rich Terminal Output for todd

## Overview

Add rich terminal formatting to `todd`'s query command output using the `rich`
Python library. When the LLM response contains markdown — headings, bold text,
code blocks, lists — render it with colours, syntax highlighting, and proper
structure instead of dumping raw markdown to the terminal.

## Usage

```shell
uv run todd "explain the strands agent lifecycle"
```

Expected output renders markdown headings in colour, bold/italic formatting
inline, fenced code blocks with syntax highlighting, and bulleted lists with
proper indentation — all within the terminal.

```shell
# Piped output falls back to plain text
uv run todd "list Python built-in types" | head -20
```

When stdout is not a TTY (piped or redirected), rich formatting is disabled
and plain text is printed instead.

## Requirements

### Functional

- Render markdown headings (`#`, `##`, `###`) with coloured, bold output
- Render inline formatting: **bold**, *italic*, `inline code`
- Render fenced code blocks with syntax highlighting (e.g. ` ```python `)
- Auto-detect language from fenced code block info strings; fall back to plain
  text highlighting when no language is specified
- Render bulleted and numbered lists with proper indentation
- Word-wrap output to terminal width with a configurable maximum (default 100
  columns)

### Non-Functional

- No noticeable latency — formatting is applied after the response is received,
  not during generation
- Graceful fallback to plain text when the terminal does not support colour
  (e.g. `NO_COLOR` environment variable, dumb terminal, piped output)

## Dependencies

Add to `pyproject.toml`:

```toml
"rich"
```

## Implementation Notes

- Primary file to modify: `src/todd/query.py` (or the module responsible for
  printing the LLM response)
- Use `rich.console.Console` with `rich.markdown.Markdown` to render the
  response
- Detect whether stdout is a TTY (`sys.stdout.isatty()`); if not, print the
  raw response text without rich formatting
- Pattern: receive the full LLM response string, then pass it through
  `Console().print(Markdown(response))` before output

## Out of Scope

- REPL / interactive multi-turn mode (module 6)
- Streaming responses rendered incrementally (module 6)
- Custom colour themes or user-configurable styles
- Rich formatting for error messages or CLI help text
