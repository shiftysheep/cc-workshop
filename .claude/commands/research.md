---
description: Research codebase and documentation to answer questions and gather context
context: fork
---

# /research

Research codebase and documentation to answer questions, understand patterns, and gather context before designing or implementing.

## Arguments

`$ARGUMENTS` — research question, topic, or area to investigate

## Workflow

1. **Decompose** the research question into sub-questions: what to find in codebase, what to find in docs
2. **Spawn Explore subagents** (use Agent tool with subagent_type=Explore) for parallel investigation:
   - One for codebase structure and implementation patterns
   - One for existing documentation and specs
3. **Synthesize** findings from all subagents into a unified research report

## Delegate to Explore Subagents

Use the Agent tool with `subagent_type: "Explore"` for read-only codebase and documentation research.
Explore subagents are fast (haiku model) and ideal for parallel searches.

## Output

Produce a research report with:

```
## Research Report: <Topic>

### Codebase Findings
<relevant files, patterns, implementations with file:line references>

### Documentation Findings
<relevant specs, plans, ADRs, READMEs>

### Gaps and Unknowns
<questions that couldn't be answered from existing sources>

### Recommendations
<suggested next steps based on findings>
```

Write the research report to `docs/research/${CLAUDE_SESSION_ID}.md`.

## Usage

```
/research How is authentication currently implemented?
/research What test patterns does this codebase use?
/research $ARGUMENTS
```
