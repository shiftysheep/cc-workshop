---
description: Propagate changes from the current module branch forward through all downstream module branches via PRs.
---
# Purpose

Automate the cascading merge of changes from an earlier module branch through all
subsequent module branches. Each step creates an update branch, merges the previous
module, pushes, creates a PR, merges the PR, and syncs — then moves to the next
downstream branch.

Respects branch protection: every change goes through a PR via an `update/` branch.

## Variables

CURRENT_BRANCH = !`git branch --show-current`

## Instructions

Propagate changes forward from a source module branch through all downstream module
branches (up to module-5).

- If $ARGUMENTS contains a module branch name (e.g. "module-2"), use that as the
  source instead of CURRENT_BRANCH.
- If $ARGUMENTS contains "dry-run", print the planned operations without executing.
- All commits require `PRE_COMMIT_ALLOW_NO_CONFIG=1` (no .pre-commit-config.yaml on
  module-2+).

## Workflow

### 1. Determine the source branch

- Use $ARGUMENTS module name if provided, otherwise CURRENT_BRANCH.
- Validate it matches `module-N` where N is 1–4. If module-5, report "nothing
  downstream" and stop. If not a module branch, ask the user.
- Extract the module number N.

### 2. Dry-run check

If $ARGUMENTS contains "dry-run": list each downstream step
(module-(N+1) through module-5) and the operations that would run, then stop.

### 3. Ensure source is current

```
git checkout module-N
git pull origin module-N
```

### 4. For each downstream branch M from (N+1) through 5

**4a. Skip check (idempotency)**

Run `git merge-base --is-ancestor module-(M-1) module-M`. If true, report
"module-M already contains module-(M-1)" and skip to next.

Check `git ls-remote --heads origin update/module-M-propagate`. If a remote
branch exists, check for an open or merged PR. Resume or skip accordingly.

**4b. Create update branch**

```
git checkout module-M
git pull origin module-M
git checkout -b update/module-M-propagate
```

**4c. Merge previous module**

```
git merge module-(M-1) --no-edit
```

If conflicts: report conflicting files, show conflict markers, work with the
user to resolve interactively. After resolution:

```
git add <resolved files>
PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit --no-edit
```

**4d. Push and create PR**

```
git push -u origin update/module-M-propagate
gh pr create --base module-M --head update/module-M-propagate \
  --title "Propagate module-(M-1) into module-M" \
  --body "Automated forward-merge of module-(M-1) changes via /propagate."
```

**4e. Merge the PR**

```
gh pr merge <pr-number> --merge
```

If merge fails, report the error and ask the user how to proceed.

**4f. Sync local**

```
git checkout module-M
git pull origin module-M
```

### 5. Return to original branch

```
git checkout <source branch>
```

## Output

Print a summary table:

```
Propagation complete from module-N:
  module-N → module-(N+1): ✓ clean merge
  module-(N+1) → module-(N+2): ✓ resolved 1 conflict
  ...
Returned to module-N.
```
