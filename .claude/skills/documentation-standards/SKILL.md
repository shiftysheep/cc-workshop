---
name: documentation-standards
description: MUST BE USED when creating or updating documentation, specs, plans, or ADRs
---

# Documentation Standards Skill

## When to Use

Load this skill when creating or updating any documentation file: plans, specs, ADRs,
PRDs, or research documents. Ensures correct file location, frontmatter, and
structure are applied consistently across all phases.

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

See [output templates](references/templates.md) for Plan, Spec, ADR, and PRD
starter structures.

## Related

- **code-review** — documentation is one of the four review dimensions; use severity
  classification from code-review when flagging doc issues
- **testing** — test documentation (fixtures, coverage rationale) follows the same
  frontmatter and location conventions
