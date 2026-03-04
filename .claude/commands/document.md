---
description: Update documentation to reflect implementation changes
context: fork
agent: documentation
---

# /document

Analyze implementation changes and update all affected documentation to keep it accurate and current.

## Arguments

`$ARGUMENTS` — implementation summary, git ref, or description of changes to document

## Workflow

Delegates to the **documentation** agent. The agent will:

1. **Analyze implementation changes** from `$ARGUMENTS` (git diff, implementation summary, or description)
2. **Identify affected docs** — existing docs referencing changed code, new docs needed
3. **Update documentation** following documentation-standards skill:
   - Update frontmatter `last_updated` on modified files
   - Use correct file locations and templates
4. **Verify references** — ensure all file paths and API references still match code

## Output

Documentation update summary with files modified, files created, and reference verification.

## Usage

```
/document                         # document recent changes (git diff)
/document HEAD~1..HEAD            # document last commit changes
/document the authentication implementation just completed
/document $ARGUMENTS
```
