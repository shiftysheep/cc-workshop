---
name: module
description: Progress from the current branch to the next module branch.
disable-model-invocation: true
---
# Purpose

Progress from module branch to module branch bringing our project with us as we build.

## Variables

CURRENT_BRANCH = !` git branch --show-current`

## Instructions

When invoked your task is to switch to the branch of the next module and merge the CURRENT_BRANCH into our next branch.
This allows us to progressively build our application and bring in further agentic capabilities designed to continue building the next module.

## Workflow

1. Confirm with the user that we are ready to proceed to the next phase.
2. If confirmed switch to the next numerical branch module branch and merge the CURRENT_BRANCH into the new module branch.

## Output

If confirmed, inform the user that the merge was completed and they are ready to start on the next module.
