#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "python-pptx",
# ]
# ///
# mypy: disable-error-code="no-untyped-def, no-untyped-call"
"""Generate the Claude Code Workshop PowerPoint presentation."""

import os
from dataclasses import dataclass, field
from pptx import Presentation  # type: ignore[import-not-found]
from pptx.dml.color import RGBColor  # type: ignore[import-not-found]
from pptx.util import Pt  # type: ignore[import-not-found]

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
TEMPLATE = os.path.join(SCRIPT_DIR, "template-converted.pptx")
OUTPUT = os.path.join(SCRIPT_DIR, "workshop-slides.pptx")

# Styling constants
DARK_TEXT = RGBColor(0x33, 0x33, 0x33)
BG_IMAGE = os.path.join(REPO_ROOT, "images", "powerpoint_background.png")

# Template layout indices (from template-converted.pptx)
LAYOUT_TITLE = 0
LAYOUT_SECTION = 2
LAYOUT_TWO_COLUMN = 5
LAYOUT_CONTENT = 6
LAYOUT_CLOSING = 7

# Bullet type alias
Bullet = str | tuple[str, str, int] | dict[str, str | int]


@dataclass
class SlideData:
    """Base class for all slide types."""

    title: str
    notes: str = ""


@dataclass
class TitleSlide(SlideData):
    subtitle: str = ""


@dataclass
class SectionSlide(SlideData):
    layout: int = -1  # Set after LAYOUT_SECTION is defined

    def __post_init__(self) -> None:
        if self.layout == -1:
            self.layout = LAYOUT_SECTION


@dataclass
class ContentSlide(SlideData):
    bullets: list[Bullet] = field(default_factory=list)


@dataclass
class ImageSlide(SlideData):
    image: str = ""  # Relative to REPO_ROOT


@dataclass
class TwoColumnSlide(SlideData):
    left: list[Bullet] = field(default_factory=list)
    right: list[Bullet] = field(default_factory=list)


# All 33 slides in exact order
SLIDES: list[SlideData] = [
    # Slide 1: Title slide
    TitleSlide(
        title="Claude Code in Depth",
        subtitle="Totally not a chat bot:\nharness your context for increased velocity",
        notes="Welcome to the Claude Code workshop. This session takes you from zero to a fully operational agentic delivery system in five progressive modules. Each module builds on the last — by the end, you'll have working orchestration commands, agent teams, and CI/CD integration. The focus is on principles of agentic coding, not just the project we build.",
    ),
    # Slide 2: Prerequisites
    ContentSlide(
        title="Prerequisites",
        bullets=[
            ("Git: ", "Pre-installed on macOS/Linux — Windows users must install", 0),
            ("uv: ", "Python package manager", 0),
            ("Claude Code CLI: ", "Anthropic's agentic coding tool", 0),
            (
                "AWS Profile: ",
                "SSO profile with Bedrock access (InvokeModel permission)",
                0,
            ),
        ],
        notes="These should all be installed before the workshop begins. If you need help you can reach out in the meeting chat or flag down an assistant. ",
    ),
    # Slide 3: Bedrock Configuration
    ContentSlide(
        title="Bedrock Configuration",
        bullets=[
            "In ~/.claude/settings.json, set env variables:",
            {"text": 'CLAUDE_CODE_USE_BEDROCK: "1"', "level": 1},
            {"text": 'AWS_REGION: "us-west-2"', "level": 1},
            {"text": 'AWS_PROFILE: "your-sso-profile.BedrockAccessRole"', "level": 1},
            "Pin model versions (prevents breaking changes):",
            {"text": "Sonnet: us.anthropic.claude-sonnet-4-6", "level": 1},
            {"text": "Haiku: us.anthropic.claude-haiku-4-5-20251001-v1:0", "level": 1},
            {"text": "Opus: us.anthropic.claude-opus-4-6-v1", "level": 1},
            'awsAuthRefresh: "aws sso login --profile=${AWS_PROFILE}"',
        ],
        notes="If you have used the configure.py this was done behind the scenes.",
    ),
    # Slide 4: Workshop Flow
    ContentSlide(
        title="What We'll Build",
        bullets=[
            "M1: Scaffold a Typer CLI app from a natural language prompt",
            "M2: Build a simple CLI LLM tool called todd",
            "M3: Build orchestration commands, agents, hooks, and skills",
            "M4: Run parallel agent teams in isolated worktrees",
            "M5: Wire agents into CI/CD and run headless reviews",
        ],
        notes="Frame this as a hands-on journey. Where we'll progressively build up capabilities and complexity. Transition: Let's start with what Claude Code actually is.",
    ),
    # Slide 5: How Modules Work
    ContentSlide(
        title="How Modules Work",
        bullets=[
            (
                "Each module has a guide: ",
                "`modules/moduleN.md` — follow it step by step",
                0,
            ),
            (
                "When you finish a module: ",
                "run `/module` in Claude Code to advance",
                0,
            ),
            (
                "What `/module` does: ",
                "merges your branch forward into the next module branch",
                0,
            ),
            (
                "Your work carries forward: ",
                "each module builds on everything you've built so far",
                0,
            ),
        ],
        notes="Orient participants before they start. The module files are the source of truth for exercises — they follow those, not the slides. The /module command is the transition mechanism: it merges the current branch into the next, so nothing is lost. Participants work at their own pace; the command handles the git logistics.",
    ),
    # Slide 6: What Is Claude Code?
    ContentSlide(
        title="What Is Claude Code?",
        bullets=[
            (
                "Agentic terminal tool: ",
                "Claude runs in your terminal with full filesystem access",
                0,
            ),
            (
                "Built-in tools: ",
                "Read, Write, Edit, Bash, Glob, Grep, Task (subagents)",
                0,
            ),
            (
                "MCP servers: ",
                "External tool integrations via Model Context Protocol",
                0,
            ),
            (
                "Extensibility layers: ",
                "commands, skills, hooks, agents — all defined in .claude/",
                0,
            ),
            (
                "Plugin marketplace: ",
                "Discover, install, and share packaged extensions via /plugin",
                0,
            ),
        ],
        notes="Claude Code is not a chatbot — it's an agentic tool that operates on your codebase. It reads files, writes code, runs commands, and manages its own workflow through subagents. The extensibility layers — MCP, commands, skills, hooks, agents — are what make it a platform, not just a tool. Plugins package these extensions for distribution: a single plugin can bundle commands, skills, agents, and hooks into one installable unit. Plugin marketplaces — both the public Anthropic marketplace and private enterprise ones — let teams share and discover these packages. Each extension point gets dedicated coverage in later modules. Transition: Before diving into the modules, let's establish the vocabulary.",
    ),
    # Slide 7: Quality Tenets — Foundations
    ContentSlide(
        title="Quality Tenets: Foundations",
        bullets=[
            ("1. Verify your work: ", "Tests and expected outputs are the single highest-leverage thing you can provide", 0),
            ("2. Be specific: ", "Reference files, constraints, patterns — vague prompts produce vague output", 0),
            ("3. CLAUDE.md + hooks: ", "Persistent memory plus automated gates — deterministic quality from commit one", 0),
            ("4. Context is finite: ", "Manage aggressively — performance degrades as the window fills", 0),
        ],
        notes=(
            "These four tenets are foundational — they apply from your very first Claude session. "
            "Each one maps to concepts you'll learn hands-on:\n\n"
            "Vocabulary preview: 'Context window' is the finite space for prompts, tools, and history. "
            "'Context rot' is quality degradation as this fills. 'Context poisoning' is when bad info "
            "enters and corrupts reasoning. These failure modes are why Tenet 4 matters.\n\n"
            "Module mapping: #1 starts in M1 (manual check) and deepens in M2 (automated test). "
            "#2 is demonstrated through PRD-driven workflows starting in M2. "
            "#3 is the M1 headline (CLAUDE.md + pre-commit) and deepens in M3 (PostToolUse hooks). "
            "#4 is the M2 headline (context visualization, subagent isolation).\n\n"
            "Transition: The next four tenets build on these foundations."
        ),
    ),
    # Slide 8: Quality Tenets — At Scale
    ContentSlide(
        title="Quality Tenets: At Scale",
        bullets=[
            ("5. Explore → Plan → Code: ", "Separate thinking from doing — read the codebase before writing to it", 0),
            ("6. Progressive disclosure: ", "Right context, right scope, right time — don't front-load everything", 0),
            ("7. Agent design: ", "Composable workers with model, tools, scope — agent design is API design", 0),
            ("8. Scale with isolation: ", "Worktrees, teams, headless, sandboxing — isolate to scale safely", 0),
        ],
        notes=(
            "These four tenets emerge as you move from individual use to team-scale orchestration.\n\n"
            "Vocabulary preview: 'Progressive disclosure' means surfacing information incrementally. "
            "'Back pressure' means the system actively resists bad output (hooks, TDD, plan mode). "
            "'Sandboxing' isolates agent operations to limit blast radius. "
            "'Delegation' offloads work to subagents for context savings.\n\n"
            "Module mapping: #5 is the M2 headline (plan mode workflow). "
            "#6 is the M3 headline (four-layer context system). "
            "#7 is the M3 headline (custom agents and custom subagents) extended in M4 (team workers). "
            "#8 is the M4 headline (worktrees + teams) extended in M5 (headless/CI).\n\n"
            "Transition: Let's start building. Module 1."
        ),
    ),
    # Slide 9: Module 1 Section Header
    SectionSlide(
        title="Module 1: Pre-commit + CLAUDE.md",
        notes="Module 1 establishes the baseline: set up the tools, configure quality gates, and let Claude build a simple Typer CLI app from a natural language prompt. The workshop starts slow on purpose — scaffolding a CLI is boring but demonstrates Claude operating on your behalf. Claude is doing, not planning. Pre-commit hooks are back pressure (automated quality gates). CLAUDE.md shapes Claude's behavior across sessions. These patterns scale. Transition: What we do in this module.",
    ),
    # Slide 10: M1 Let's get to work
    ContentSlide(
        title="Let's get to work",
        bullets=[
            "Open `modules/module1.md` for our list of tasks",
        ],
        notes="Participants follow the steps in module1.md at their own pace. Flag down an assistant if you get stuck.\n\nPresenter talking points:\n- Install uv (Python package manager)\n- Configure Claude CLI (Bedrock profile)\n- Scaffold a Typer CLI app from a natural language prompt — Claude reads uv docs, decides structure, writes code, tests pass\n- Pre-commit hooks enforce quality gates automatically — ruff, mypy, bandit, etc.\n- Verify Claude followed your CLAUDE.md instructions by inspecting the generated code\n\nThe key insight: Claude is not a chatbot. It's an autonomous tool that can read, write, run commands, make decisions. Pre-commit hooks provide back pressure. CLAUDE.md provides persistent memory.\n\nTransition: Describe what you want, Claude handles the rest. Pre-commit hooks are back pressure before we even name it. CLAUDE.md shaped everything Claude just did.",
    ),
    # Slide 11: M1 Summary
    ContentSlide(
        title="Summarizing what we have seen",
        bullets=[
            ("Pre-commit hooks: ", "Automated quality gates enforce standards", 0),
            ("CLAUDE.md: ", "Persistent memory shapes behavior across sessions", 0),
            ("Simple prompt → full app: ", "Claude scaffolds, writes, tests autonomously", 0),
            ("Back pressure: ", "Hooks reject bad output before it commits", 0),
        ],
        notes="Describe what you want, Claude handles the rest. Pre-commit hooks are back pressure before we even name it. CLAUDE.md shaped everything Claude just did. Transition: Module 2 introduces context management and planning.",
    ),
    # Slide 12: Module 2 Section Header
    SectionSlide(
        title="Module 2: MCP, Plan Mode, and Agent SDK",
        notes="Module 2 introduces the critical concept of context as a finite resource. You'll install your first MCP server, see how MCP tools load on demand via ToolSearch, switch models for planning, and build a real feature through plan mode. The key progression: Module 1 was about Claude doing things for you. Module 2 is about Claude thinking before doing. Transition: What we do in this module.",
    ),
    # Slide 13: M2 What We Do
    ContentSlide(
        title="Let's get to work",
        bullets=[
            "Open `modules/module2.md` for our list of tasks",
        ],
        notes="Participants follow the steps in module2.md at their own pace. Flag down an assistant if you get stuck.",
    ),
    # Slide 14: The Context Window (with image)
    ImageSlide(
        title="The Context Window",
        image="images/context_window_utilization.png",
        notes="This is the most important conceptual slide. Walk through each layer. System prompt and CLAUDE.md are always present — they're the 'tax' on every interaction. MCP tool definitions are deferred via ToolSearch — they load into context only when Claude discovers them. This is progressive disclosure at the tool level. Conversation history is the biggest consumer — this is why /compact and /clear matter. File contents are loaded on demand but can be huge. The 'available space' is what Claude has for actual reasoning. When it shrinks too much, that's context rot in action. Transition: Now let's see how subagents protect this window.",
    ),
    # Slide 15: Subagent Context Isolation (with image)
    ImageSlide(
        title="Subagent Context Isolation",
        image="images/subagent_context_savings.png",
        notes="This diagram shows how subagents protect the main context window. When Claude needs to search 40+ files or do deep research, it spawns a subagent — typically Haiku for cheap exploration, Opus for architecture decisions. Each subagent gets its own fresh context window. The search noise (file contents, failed matches, irrelevant results) stays in the subagent's window. Only a compact summary flows back to the main conversation. This is the primary defense against context rot: delegate the noisy work, keep the main window clean. Point out the three subagent types: two Explore agents running Haiku for fast, cheap searches, and one Plan agent running Opus for deeper reasoning. Transition: Module 3 builds the orchestration layer.",
    ),
    # Slide 16: M2 Summary
    ContentSlide(
        title="Summarizing what we have seen",
        bullets=[
            (
                "Finite context window: ",
                "Prompts, files, tools, history all share one space",
                0,
            ),
            (
                "MCP tools load on demand: ",
                "ToolSearch defers definitions until needed — no idle cost",
                0,
            ),
            (
                "Plan mode = read-only gate: ",
                "Think before writing, prevents costly reverts",
                0,
            ),
            (
                "Subagents isolate context: ",
                "Fresh windows prevent cross-contamination",
                0,
            ),
            ("Model selection: ", "Opus / Sonnet / Haiku for different task types", 0),
        ],
        notes="Context is finite and precious. Rot happens gradually (long sessions). Poisoning happens suddenly (one bad assumption). Subagents are the primary defense against both — each gets a fresh context window. MCP tools are deferred via ToolSearch — no idle context cost. Once loaded, definitions do consume context, so selective loading matters. This is progressive disclosure at the tool level. Model selection is about cost-quality tradeoffs, not just 'use the best model.' Transition: Module 3 builds the orchestration layer.\n\nTenet tracker: #4 (context is finite) and #5 (explore-plan-code) are the headlines. #1 (verify) gets its first test exercise. #2 (be specific) is demonstrated through the PRD workflow.",
    ),
    # Slide 17: Module 3 Section Header
    SectionSlide(
        title="Module 3: ADW Foundations",
        notes="Module 3 builds the full extensibility layer. We create commands, skills, hooks, rules, and custom agents — all in .claude/. The key insight: all of this is markdown and configuration — no code. Claude's behavior is shaped by prose instructions, not programming. This is prompt-driven orchestration. Transition: What we do.",
    ),
    # Slide 18: M3 Let's get to work
    ContentSlide(
        title="Let's get to work",
        bullets=[
            "Open `modules/module3.md` for our list of tasks",
        ],
        notes="Participants follow the steps in module3.md at their own pace. Flag down an assistant if you get stuck.\n\nPresenter talking points:\n- Generate Architecture Reference Document with Mermaid diagrams — Claude as documentation tool, no code written, just analysis\n- Install document-skills plugin from the marketplace\n- Plan orchestration commands from PRD (docs/prds/adw-commands.md) — Claude reads .claude/ scaffolding to understand patterns, explores phase commands, skills, agents before planning\n- Build 4 orchestration commands from PRD: /feature (single-agent, 7 sequential phases), /bug (single-agent, 6 phases), /team:feature (multi-agent, parallel analysis + coordinated implementation), /team:bug (multi-agent, parallel analysis, 6 phases)\n- Create custom agents (.claude/agents/ + YAML frontmatter) — code-reviewer exercise teaches agent anatomy, then three ADW specialist agents\n- Explore PostToolUse lint hook — back pressure after every write",
    ),
    # Slide 19: The Four-Layer Context System (with image)
    ImageSlide(
        title="The Four-Layer Context System",
        image="images/fourlayer_context_system.png",
        notes="This is the architectural insight of Module 3. The four layers form a progressive disclosure system. CLAUDE.md is always present (broad but essential). Rules narrow to specific directories. Skills narrow to specific task types. Hooks narrow to specific actions. The key insight: context is delivered at the moment it's needed, at the right scope. This prevents context bloat while ensuring Claude always has what it needs. Transition: Let's dig deeper into when progressive disclosure works and when it doesn't.",
    ),
    # Slide 20: Progressive Disclosure (with image)
    ImageSlide(
        title="Progressive Disclosure",
        image="images/progressive_disclosure.png",
        notes="Progressive disclosure is the difference between a productive session and context rot. The four-layer funnel: CLAUDE.md (always-on) → rules/ (directory-scoped) → skills (task-scoped) → hooks (event-scoped). Each layer narrows scope and timing. Anti-patterns include: dumping 100KB+ in system prompt, loading all reference docs 'just in case', same context for every workflow phase, hiding context the agent needs now. Nielsen Norman research shows 3+ disclosure levels cause confusion even for humans. Progressive disclosure doesn't mean hiding information — it means delivering it at the right time. If an agent needs reference docs NOW, load them NOW. Transition: The other side of quality — back pressure.",
    ),
    # Slide 21: Back Pressure (with image)
    ImageSlide(
        title="Back Pressure",
        image="images/back_pressure.png",
        notes="Back pressure is the system's resistance to bad output. Pre-commit hooks (M1) are the first layer — reject malformed commits. PostToolUse hooks (M3) are the second layer — inspect write operations before they land. Plan mode (M2) is architectural back pressure — think before writing. Tests (M1-M2) are verification back pressure — prove it works before you commit it. The goal: detect failure as early as possible. The later a failure is caught, the more expensive it is to fix. Hooks are cheap back pressure. They run synchronously, provide immediate feedback, and cost nothing if output is correct. Transition: Module 4 builds on this foundation by adding team-based orchestration.",
    ),
    # Slide 22: M3 Summary
    ContentSlide(
        title="Summarizing what we have seen",
        bullets=[
            (
                "Four-layer context system: ",
                "CLAUDE.md → rules/ → skills/ → hooks/",
                0,
            ),
            (
                "Progressive disclosure: ",
                "Deliver context at the right time and scope",
                0,
            ),
            (
                "Back pressure: ",
                "Hooks and gates reject bad output early",
                0,
            ),
            (
                "Custom agents: ",
                "YAML frontmatter + markdown instructions",
                0,
            ),
            (
                "Orchestration commands: ",
                "Phase-driven workflows via /command",
                0,
            ),
        ],
        notes="Module 3 is the turning point. We went from 'Claude does things' (M1) and 'Claude plans things' (M2) to 'Claude orchestrates workflows' (M3). The four-layer context system is the architectural win. Back pressure is the quality win. Custom agents are the extensibility win. Orchestration commands are the productivity win. Everything from here scales on this foundation.\n\nTenet tracker: #6 (progressive disclosure) is the M3 headline. #3 (CLAUDE.md + hooks) deepened with PostToolUse. #7 (agent design) introduced through custom agent YAML.",
    ),
    # Slide 23: Module 4 Section Header
    SectionSlide(
        title="Module 4: Team Orchestration",
        notes="Module 4 scales from single-agent workflows to multi-agent teams. You'll create worker agents that operate in parallel, coordinate via leader agents, and execute in isolated worktrees. The key insight: team orchestration is just phase-driven workflows with parallel execution. Each worker gets its own fresh worktree and context window. Leaders delegate, workers execute, results merge. This is how you scale Claude to multiple simultaneous work streams. Transition: What we do.",
    ),
    # Slide 24: M4 What We Do (1/2)
    ContentSlide(
        title="M4: What We Do (1/2)",
        bullets=[
            "Plan team worker agents from PRD (docs/prds/team-workers.md)",
            "Create 3 worker agents: backend-dev, frontend-dev, test-engineer",
            "Build orchestrator commands for team workflows: /team:feature, /team:bug",
            "Wire worktree isolation into team commands (each worker in its own worktree)",
        ],
        notes="Walk through the PRD for team workers. Point out the three worker agents: backend-dev (API implementation), frontend-dev (UI implementation), test-engineer (integration tests). Each worker operates in a separate worktree — this is the isolation mechanism. The leader agent (delegator) coordinates work via the /team:feature and /team:bug commands. Workers run in parallel when phases allow, sequentially when dependencies exist. Transition: Part 2.",
    ),
    # Slide 25: M4 What We Do (2/2)
    ContentSlide(
        title="M4: What We Do (2/2)",
        bullets=[
            "Test parallel execution with /team:feature 'add health endpoint'",
            "Observe worktree isolation: each worker in separate git worktree",
            "Inspect agent coordination: leader delegates, workers execute",
            "Merge results: leader collects worker outputs, integrates changes",
        ],
        notes="The test scenario is a health endpoint — simple enough to see the pattern clearly. Backend-dev implements the endpoint. Frontend-dev updates the client. Test-engineer adds integration tests. All three run in parallel. Each worker operates in its own worktree, so there are no conflicts. The leader agent merges results back into the main branch. Transition: Let's look at how worktrees provide isolation.",
    ),
    # Slide 26: Worktree Isolation (with image)
    ImageSlide(
        title="Worktree Isolation",
        image="images/worktree_isolation.png",
        notes="This diagram shows how worktrees isolate parallel work. Each worker agent gets its own worktree — a separate working directory linked to the same git repository. Workers can write, commit, and test without interfering with each other. The leader agent operates in the main worktree and coordinates merges. This is the primary isolation mechanism for team orchestration. It prevents file conflicts, context contamination, and race conditions. Point out the three worktrees (backend, frontend, test) and the main worktree (leader). Transition: Module 5 extends this to CI/CD and headless execution.",
    ),
    # Slide 27: Module 5 Section Header
    SectionSlide(
        title="Module 5: CI/CD and Headless Execution",
        notes="Module 5 takes everything we've built and wires it into CI/CD. You'll configure GitHub Actions to trigger Claude agents on PR events, run headless reviews, and enforce quality gates. The key insight: agents are just executables. If they run in your terminal, they can run in CI. Sandboxing and permissions prevent overreach. This is where Claude becomes part of your delivery pipeline. Transition: What we do.",
    ),
    # Slide 28: M5 What We Do (1/2)
    ContentSlide(
        title="M5: What We Do (1/2)",
        bullets=[
            "Configure GitHub Actions workflow (.github/workflows/claude-review.yml)",
            "Wire PR events to trigger code-review agent",
            "Test headless execution: open PR, see agent comment with review",
            "Inspect sandboxing: agent has read-only access, can't push commits",
        ],
        notes="The workflow listens for pull_request events. When a PR opens or updates, it triggers the code-review agent. The agent runs headless (no interactive session), reads the PR diff, analyzes the changes, and posts a review comment. Sandboxing is enforced via environment variables and permissions — the agent can read but not write. This prevents accidental damage. Transition: Part 2.",
    ),
    # Slide 29: M5 What We Do (2/2)
    ContentSlide(
        title="M5: What We Do (2/2)",
        bullets=[
            "Extend to other CI gates: /team:test (parallel test execution)",
            "Add security scanning: bandit + Claude analysis",
            "Configure failure notifications: Slack or email on agent failure",
            "Review audit logs: agent decisions, tool usage, token costs",
        ],
        notes="The /team:test command runs test-engineer agents in parallel — one per test suite. Security scanning combines bandit (static analysis) with Claude's reasoning (context-aware checks). Failure notifications use existing CI mechanisms (Slack, email, PagerDuty). Audit logs capture agent decisions, tool usage, and token costs — this is how you measure ROI. Transition: Let's look at the CI integration architecture.",
    ),
    # Slide 30: CI Integration Architecture (with image)
    ImageSlide(
        title="CI Integration Architecture",
        image="images/ci_integration.png",
        notes="This diagram shows the full CI integration. GitHub Actions triggers on PR events. The runner environment has Claude CLI installed and configured. Agents run headless via /agent:run command. Results post back to GitHub as PR comments. Sandboxing is enforced via read-only filesystem mounts and restricted API tokens. The key insight: this is just automation — agents are executables, CI is a scheduler. The architecture is simple by design. Transition: Let's recap the full progression.",
    ),
    # Slide 31: The Progression (with image)
    ImageSlide(
        title="The Progression",
        image="images/progression.png",
        notes="This slide shows the full five-module progression. M1: CLAUDE.md + pre-commit (foundational quality). M2: Context management + subagents (efficiency). M3: Four-layer context + orchestration (scale). M4: Team workers + worktrees (parallelization). M5: CI/CD + headless (automation). Each module builds on the last. The principles — progressive disclosure, back pressure, isolation, delegation — compound. By M5, you have a fully operational agentic delivery system. Transition: Let's review how the eight tenets mapped to this progression.",
    ),
    # Slide 32: Tenets — Full Coverage Recap
    ContentSlide(
        title="Tenets of Quality Output — Recap",
        bullets=[
            ("1. Verify: ", "M1 manual check → M2 automated test → M3 lint hooks → M4 CI gates", 0),
            ("2. Be specific: ", "M2 PRD workflow → M3 orchestration PRDs → M4 orchestrator PRDs", 0),
            ("3. CLAUDE.md + hooks: ", "M1 CLAUDE.md + pre-commit → M3 PostToolUse → M5 maintenance", 0),
            ("4. Context is finite: ", "M2 /context viz + subagent isolation → M3 progressive disclosure", 0),
            ("5. Explore → Plan → Code: ", "M2 plan mode → M3 plan-before-build → M4 phase sequences", 0),
            ("6. Progressive disclosure: ", "M3 four-layer system → M3 skills auto-load → M4 state files", 0),
            ("7. Agent design: ", "M3 custom agents → M4 team workers → M5 custom subagents", 0),
            ("8. Scale with isolation: ", "M4 worktrees + teams → M5 headless/CI + sandboxing", 0),
        ],
        notes=(
            "This is the payoff slide. Walk through each tenet and ask participants to recall "
            "the specific exercises. Every tenet from slides 6-7 now has hands-on coverage.\n\n"
            "FOUNDATIONAL (1-3): Verification progressed from manual spot-check (M1) through "
            "automated test (M2) to automated hooks (M3) to CI gates (M4-5). "
            "Specificity was demonstrated every time a PRD drove the work. "
            "CLAUDE.md + hooks threaded from M1 through M5 — the longest-running tenet.\n\n"
            "INTERMEDIATE (4-6): Context management was the M2 headline. "
            "Plan mode enforced the explore-plan-code discipline. "
            "Progressive disclosure was built as a four-layer system in M3.\n\n"
            "ADVANCED (7-8): Agent design started with custom agents and custom subagents in M3, "
            "scaled to team workers in M4, and was operationalized in M5 (headless/CI). "
            "Isolation layered up: worktrees (M4) + subagents (M2) + hooks (M3) + permissions (M4-5).\n\n"
            "Sources: code.claude.com/docs/en/best-practices, "
            "simonwillison.net (agentic engineering), "
            "github.com/anthropics/prompt-eng-interactive-tutorial"
        ),
    ),
    # Slide 33: Closing
    SectionSlide(
        title="Questions?",
        layout=LAYOUT_CLOSING,
        notes="Open the floor for questions. If time permits, offer to demo any specific concept live. Repo is available for participants to continue working through modules independently. Point them to code.claude.com for official documentation.",
    ),
]


def add_text_to_shape(
    shape, text: str, font_size: int = 18, bold: bool = False
) -> None:
    """Add text to a shape."""
    if not hasattr(shape, "text_frame"):
        return

    text_frame = shape.text_frame
    text_frame.clear()
    p = text_frame.paragraphs[0]
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.color.rgb = DARK_TEXT
    run.font.bold = bold


def add_bullet_points(
    text_frame, bullets: list[Bullet], base_level: int = 0
) -> None:
    """Add bullet points to a text frame."""
    text_frame.clear()

    for bullet in bullets:
        # Handle different bullet formats
        if isinstance(bullet, str):
            # Simple string bullet
            p = text_frame.add_paragraph()
            p.text = bullet
            p.level = base_level
            p.font.size = Pt(18)
            p.font.color.rgb = DARK_TEXT

        elif isinstance(bullet, tuple):
            # Tuple format: (bold_text, regular_text, level)
            bold_text, regular_text, level = bullet
            p = text_frame.add_paragraph()

            # Add bold part
            run1 = p.add_run()
            run1.text = bold_text
            run1.font.size = Pt(18)
            run1.font.bold = True
            run1.font.color.rgb = DARK_TEXT

            # Add regular part
            run2 = p.add_run()
            run2.text = regular_text
            run2.font.size = Pt(18)
            run2.font.color.rgb = DARK_TEXT

            p.level = base_level + level

        elif isinstance(bullet, dict):
            # Dict format: {"text": "...", "level": N}
            p = text_frame.add_paragraph()
            p.text = bullet["text"]
            p.level = bullet.get("level", 0)
            p.font.size = Pt(18)
            p.font.color.rgb = DARK_TEXT


def create_title_slide(prs, slide_data: TitleSlide) -> None:
    """Create the title slide."""
    slide_layout = prs.slide_layouts[LAYOUT_TITLE]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title_shape = slide.shapes.title
    add_text_to_shape(title_shape, slide_data.title, font_size=44, bold=True)

    # Set subtitle
    if slide_data.subtitle:
        for shape in slide.shapes:
            if shape.has_text_frame and shape != title_shape:
                add_text_to_shape(shape, slide_data.subtitle, font_size=28)
                break

    # Add notes
    if slide_data.notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data.notes


def create_section_slide(prs, slide_data: SectionSlide) -> None:
    """Create a section header slide."""
    slide_layout = prs.slide_layouts[slide_data.layout]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title_shape = slide.shapes.title
    add_text_to_shape(title_shape, slide_data.title, font_size=44, bold=True)

    # Add notes
    if slide_data.notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data.notes


def create_content_slide(prs, slide_data: ContentSlide) -> None:
    """Create a content slide with bullet points."""
    slide_layout = prs.slide_layouts[LAYOUT_CONTENT]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title_shape = slide.shapes.title
    add_text_to_shape(title_shape, slide_data.title, font_size=32, bold=True)

    # Add bullet points
    for shape in slide.shapes:
        if shape.has_text_frame and shape != title_shape:
            add_bullet_points(shape.text_frame, slide_data.bullets)
            break

    # Add notes
    if slide_data.notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data.notes


def create_image_slide(prs, slide_data: ImageSlide) -> None:
    """Create an image slide."""
    slide_layout = prs.slide_layouts[LAYOUT_CONTENT]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title_shape = slide.shapes.title
    add_text_to_shape(title_shape, slide_data.title, font_size=32, bold=True)

    # Add image
    if slide_data.image:
        image_path = os.path.join(REPO_ROOT, slide_data.image)
        if os.path.exists(image_path):
            # Calculate position (centered below title)
            left = prs.slide_width * 0.1
            top = prs.slide_height * 0.25
            width = prs.slide_width * 0.8

            slide.shapes.add_picture(image_path, left, top, width=width)

    # Add notes
    if slide_data.notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data.notes


def create_two_column_slide(prs, slide_data: TwoColumnSlide) -> None:
    """Create a two-column slide."""
    slide_layout = prs.slide_layouts[LAYOUT_TWO_COLUMN]
    slide = prs.slides.add_slide(slide_layout)

    # Set title
    title_shape = slide.shapes.title
    add_text_to_shape(title_shape, slide_data.title, font_size=32, bold=True)

    # Add content to columns
    text_frames = [
        shape.text_frame
        for shape in slide.shapes
        if shape.has_text_frame and shape != title_shape
    ]

    if len(text_frames) >= 2:
        add_bullet_points(text_frames[0], slide_data.left)
        add_bullet_points(text_frames[1], slide_data.right)

    # Add notes
    if slide_data.notes:
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = slide_data.notes


def generate_presentation() -> None:
    """Generate the PowerPoint presentation."""
    prs = Presentation(TEMPLATE)

    for slide_data in SLIDES:
        if isinstance(slide_data, TitleSlide):
            create_title_slide(prs, slide_data)
        elif isinstance(slide_data, SectionSlide):
            create_section_slide(prs, slide_data)
        elif isinstance(slide_data, ContentSlide):
            create_content_slide(prs, slide_data)
        elif isinstance(slide_data, ImageSlide):
            create_image_slide(prs, slide_data)
        elif isinstance(slide_data, TwoColumnSlide):
            create_two_column_slide(prs, slide_data)

    prs.save(OUTPUT)
    print(f"✓ Presentation generated: {OUTPUT}")
    print(f"  Total slides: {len(SLIDES)}")


if __name__ == "__main__":
    generate_presentation()
