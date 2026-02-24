---
name: documentation-standards
description: MUST BE USED when creating or updating documentation, specs, plans, or ADRs
---

# Documentation Standards Skill

## File Location Conventions

| Document Type | Location | Filename Pattern |
|--------------|----------|-----------------|
| Plans | `docs/plans/` | `plan-<feature>.md` |
| Specs | `docs/specs/` | `spec-<feature>.md` |
| ADRs | `docs/adr/` | `adr-<NNN>-<title>.md` |
| PRDs | `docs/prds/` | `prd-<feature>.md` |
| Research | `docs/research/` | `research-<topic>.md` |

## Document Frontmatter Standard

All documentation files MUST include YAML frontmatter:

```yaml
---
doc_type: plan|spec|adr|prd|research
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft|review|approved|superseded
---
```

## Output Templates

### Plan Template
```markdown
---
doc_type: plan
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---
# Plan: <Feature Name>

## Overview
<1-2 sentence summary>

## Phases
### [PHASE-001] <Phase Name>
- **Commit**: `<conventional commit message>`
- **Files**: list of files to create/modify
- **Tests**: test strategy for this phase
- **Acceptance Criteria**: measurable outcomes
```

### Spec Template
```markdown
---
doc_type: spec
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---
# Spec: <Component Name>

## Overview
## Architecture
## Components
## Interfaces
## Data Models
## Risks
```

### ADR Template
```markdown
---
doc_type: adr
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---
# ADR-NNN: <Decision Title>

## Status
## Context
## Decision
## Consequences
```

### PRD Template
```markdown
---
doc_type: prd
created: YYYY-MM-DD
last_updated: YYYY-MM-DD
status: draft
---
# PRD: <Feature Name>

## Problem Statement
## Goals
## Non-Goals
## Requirements
## Success Metrics
```
