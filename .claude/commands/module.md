---
description: Progress from the current branch to the next module branch.
---
# Purpose

Progress from module branch to module branch bringing our project with us as we build.

## Variables

CURRENT_BRANCH = !` git branch --show-current`

## Instructions

When invoked your task is to switch to the branch of the next module and merge the CURRENT_BRANCH into our next branch. 
This allows us to progressively build our application and bring in further agentic capabilities designed to continue building the next module. 

## Workflow

1. Confirm with the user that we are ready to proceed.
2. Determine the current branch via `CURRENT_BRANCH`.
3. If the branch follows the `module-N` pattern, switch to `module-(N+1)` and merge `CURRENT_BRANCH` into it.
4. If the branch does NOT follow the `module-N` pattern (e.g. `main`), switch to `module-1` — the starting point of the workshop. No merge needed.

## Output

If confirmed, inform the user that the switch was completed and they are ready to start on the next module.


