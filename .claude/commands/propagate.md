---
description: Propagate changes from the current module branch forward through all downstream module branches via PRs.
---
# Purpose

Automate the cascading merge of changes from an earlier module branch through all
subsequent module branches. Each step creates an update branch, merges the previous
module, pushes, creates a PR, merges the PR via `--admin`, and syncs — then moves to
the next downstream branch.

Respects branch protection: every change goes through a PR via an `update/` branch.

## Variables

CURRENT_BRANCH = !`git branch --show-current`

## Instructions

Propagate changes forward from a source module branch through all downstream module
branches (up to module-6).

- If $ARGUMENTS contains a module branch name (e.g. "module-2"), use that as the
  source instead of CURRENT_BRANCH.
- If $ARGUMENTS contains "dry-run", print the planned operations without executing.
- All commits require `PRE_COMMIT_ALLOW_NO_CONFIG=1` (no .pre-commit-config.yaml on
  module-2+).

## Workflow

### 1. Determine the source branch

- Use $ARGUMENTS module name if provided, otherwise CURRENT_BRANCH.
- Validate it matches `module-N` where N is 1–5. If module-6, report "nothing
  downstream" and stop. If not a module branch, ask the user.
- Extract the module number N.

### 2. Dry-run check

If $ARGUMENTS contains "dry-run": list each downstream step
(module-(N+1) through module-6) and the operations that would run, then stop.

### 3. Fetch all remote refs

```
git fetch origin
```

This ensures all `origin/module-N` refs are current before any merge. Do not
`git pull` individual branches — work exclusively with remote refs throughout.

### 4. For each downstream branch M from (N+1) through 6

**4a. Skip check (idempotency)**

Run `git merge-base --is-ancestor origin/module-(M-1) origin/module-M`. If true,
report "module-M already contains module-(M-1)" and skip to next.

**4b. Create update branch from remote**

```
git checkout -B update/module-M-propagate origin/module-M
```

Using `-B` and `origin/module-M` directly avoids a separate `git checkout module-M &&
git pull` step and ensures we always start from the current remote state.

**4c. Merge previous module**

```
git merge origin/module-(M-1) --no-edit
```

Merge from the remote ref, not the local branch, so the previous step's PR merge is
always reflected even without a local branch checkout.

If conflicts: report conflicting files, show conflict markers, work with the
user to resolve interactively. After resolution:

```
git add <resolved files>
PRE_COMMIT_ALLOW_NO_CONFIG=1 git commit --no-edit
```

**4d. Push and create PR**

```
git push origin update/module-M-propagate --force
gh pr create --base module-M --head update/module-M-propagate \
  --title "Propagate module-(M-1) into module-M" \
  --body "Automated forward-merge of module-(M-1) changes via /propagate."
```

Use `--force` on push so the command is re-runnable if the update branch already
exists from a previous partial run.

**4e. Merge the PR**

```
gh pr merge <pr-number> --merge --admin
```

`--admin` is required because all module branches are protected. If merge fails,
report the error and ask the user how to proceed.

**4f. Sync remote ref**

```
git fetch origin module-M
```

Fetching only the merged branch updates `origin/module-M` so the next iteration
merges from the fresh state — no branch checkout required.

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
  module-5 → module-6: ✓ clean merge
Returned to module-N.
```
