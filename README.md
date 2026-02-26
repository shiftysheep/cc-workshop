# Claude Code Workshop

This course will guide you through the basics of Claude Code up through some of the advanced use cases.


## Prerequisites

- [Claude Code](https://code.claude.com/docs/en/setup#installation)
- Claude Code api access or subscription
- [Windows: git](https://git-scm.com/downloads/win)
- [Astral UV](https://docs.astral.sh/uv/getting-started/installation/#installation-methods)
- AWS Bedrock access — see [SETUP.md](SETUP.md) for configuration

## Introduction

Claude Code is an agentic tool originally focused around coding tasks.
As the models become more capable and with proper configuration this tool can be used for much more.
We'll be focusing on utilizing the terminal version but you should be able to follow along utilizing the IDE extension versions as well.
Throughout this workshop we will be building out an application repository to explore the capabilities of Claude Code.
The tools we build can be the building blocks to take into your own projects or help you build your own.
As we progress through the course we will use the `/module` command in Claude to migrate our application into a more heavily structured agentic codebase.
This will allow us to slowly introduce topics and focus on key aspects of the tool and agentic coding as we progress.


## How Modules Work

Each module lives in `modules/moduleN.md` and walks you through the exercises for that milestone.
When you finish a module, run `/module` in Claude Code — it merges your current branch forward into the next module branch, carrying everything you've built with it.
This keeps each module self-contained while letting your work accumulate naturally across the workshop.

## Get Started

When you're ready proceed to [Module1](modules/module1.md).
