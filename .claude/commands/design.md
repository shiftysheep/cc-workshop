---
description: Design architecture and produce technical specifications
context: fork
---

# /design

Design software architecture and produce a technical specification document to `docs/specs/`.

## Arguments

`$ARGUMENTS` — feature, component, or system to design (can reference research output, PRD, or concept)

## Workflow

1. **Read input** — consume any referenced research findings, PRD, or feature description from `$ARGUMENTS`
2. **Analyze requirements** — identify functional requirements, constraints, and quality attributes
3. **Delegate to Plan subagent** (use Task tool with `subagent_type: "Plan"`) for architecture design:
   - Provide full requirements context in the prompt
   - Ask it to produce components, interfaces, data models, and risk assessment
4. **Produce spec document** — write output to `docs/specs/spec-<feature>.md` following documentation-standards skill

## Delegate to Plan Subagents

Use the Task tool with `subagent_type: "Plan"` for architecture and design work.
Plan subagents excel at structured analysis and design with clear outputs.

## Output

Spec document at `docs/specs/spec-<feature>.md` with:

```
## Spec: <Feature Name>

### Overview
### Architecture
### Components
### Interfaces (APIs, contracts)
### Data Models
### Risks and Mitigations
```

## Usage

```
/design User authentication system
/design REST API for task management
/design $ARGUMENTS
```
