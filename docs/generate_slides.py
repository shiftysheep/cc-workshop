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


# All 37 slides in exact order
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
        ],
        notes="Claude Code is not a chatbot — it's an agentic tool that operates on your codebase. It reads files, writes code, runs commands, and manages its own workflow through subagents. The extensibility layers — MCP, commands, skills, hooks, agents — are what make it a platform, not just a tool. Each of these extension points will get dedicated coverage in later modules. Transition: Before diving into the modules, let's establish the vocabulary.",
    ),
    # Slide 7: Core Concepts (1/2)
    TwoColumnSlide(
        title="Core Concepts (1/2)",
        left=[
            ("Model", " - Different capabilities for different tasks", 0),
            ("Context Window", " - Finite space for prompts, tools, history", 0),
            ("Tools", " - Gives the model agency, but consume context", 0),
            ("Context Engineering", " — Shape what's in the context window", 0),
            ("Context Rot", " — Quality degrades as context fills", 0),
            ("Context Poisoning", " — Bad info corrupts reasoning", 0),
        ],
        right=["These concepts thread through every module."],
        notes="Context is finite and precious. Everything we build in the workshop is designed to manage it well. Transition: The next concepts are about how we structure agent work.",
    ),
    # Slide 8: Core Concepts (2/2)
    TwoColumnSlide(
        title="Core Concepts (2/2)",
        left=[
            ("Progressive Disclosure", " — Reveal info incrementally", 0),
            ("Back Pressure", " — Resist bad output via hooks", 0),
            ("Sandboxing", " — Isolation limits blast radius", 0),
            ("Delegation", " - Offload work to subagents for context savings", 0),
            ("Agent Teams", " — Leader/worker coordination", 0),
        ],
        right=["These concepts define how agents work at scale."],
        notes="These concepts define how agents work at scale. We'll see each one in practice as we progress through the modules. Transition: Let's start building. Module 1.",
    ),
    # Slide 9: Module 1 Section Header
    SectionSlide(
        title="Module 1: Project Scaffolding",
        notes="Module 1 establishes the foundation. Everything built here — the project structure, quality gates, CLAUDE.md — persists through all subsequent modules. The key insight is that Claude is a general-purpose agentic tool: describe what you want in natural language, get a working project with quality enforcement from commit one. Transition: Here's what we actually do.",
    ),
    # Slide 10: M1 What We Do
    ContentSlide(
        title="Let's get to work",
        bullets=[
            "Open `modules/module1.md` for our list of tasks",
        ],
        notes="Participants follow the steps in module1.md at their own pace. Flag down an assistant if you get stuck.",
    ),
    # Slide 11: M1 Why It Matters
    ContentSlide(
        title="Summarizing what we have seen",
        bullets=[
            (
                "Describe intent, get results: ",
                "Natural language prompts produce working structure with quality gates",
                0,
            ),
            (
                "Quality from commit one: ",
                "Pre-commit hooks (ruff, mypy, bandit) enforce standards automatically",
                0,
            ),
            (
                "CLAUDE.md as persistent memory: ",
                "Three scopes — global, project, personal — shape every session",
                0,
            ),
            (
                "Built-in tools: ",
                "Write, Edit, Bash, Read — Claude's core capabilities for file operations",
                0,
            ),
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
        notes="Context is finite and precious. Rot happens gradually (long sessions). Poisoning happens suddenly (one bad assumption). Subagents are the primary defense against both — each gets a fresh context window. MCP tools are deferred via ToolSearch — no idle context cost. Once loaded, definitions do consume context, so selective loading matters. This is progressive disclosure at the tool level. Model selection is about cost-quality tradeoffs, not just 'use the best model.' Transition: Module 3 builds the orchestration layer.",
    ),
    # Slide 17: Module 3 Section Header
    SectionSlide(
        title="Module 3: ADW Foundations",
        notes="Module 3 builds the full extensibility layer. We create commands, skills, hooks, rules, and custom agents — all in .claude/. The key insight: all of this is markdown and configuration — no code. Claude's behavior is shaped by prose instructions, not programming. This is prompt-driven orchestration. Transition: What we do.",
    ),
    # Slide 18: M3 What We Do (1/2)
    ContentSlide(
        title="M3: What We Do (1/2)",
        bullets=[
            "Generate Architecture Reference Document with Mermaid diagrams",
            "Claude as documentation tool — no code written, just analysis",
            "Install document-skills plugin from the marketplace",
            "Plan orchestration commands from PRD (docs/prds/adw-commands.md)",
            "Observe: Claude reads .claude/ scaffolding to understand patterns",
            "Claude explores phase commands, skills, agents before planning",
        ],
        notes="The ARD generation is a powerful demo of Claude as a non-coding tool. It reads the existing ADW spec and produces a visual reference with 5 Mermaid diagrams. The document-skills plugin adds capabilities like PowerPoint and Word generation — installed at project scope so the whole team gets it. When planning the orchestration commands, Claude reads the existing phase commands to understand the composition patterns. This is plan mode used for configuration, not code. Transition: The commands we build.",
    ),
    # Slide 19: M3 What We Do (2/2)
    ContentSlide(
        title="M3: What We Do (2/2)",
        bullets=[
            "Build 4 orchestration commands from PRD:",
            {"text": "/feature — single-agent, 7 sequential phases", "level": 1},
            {"text": "/bug — single-agent, 6 phases (no design)", "level": 1},
            {
                "text": "/team:feature — multi-agent, parallel analysis + coordinated implementation",
                "level": 1,
            },
            {
                "text": "/team:bug — multi-agent, parallel analysis, 6 phases",
                "level": 1,
            },
            "Create custom agents (.claude/agents/ + YAML frontmatter)",
            "Explore PostToolUse lint hook — back pressure after every write",
            "Create .claude/rules/ for path-scoped context",
        ],
        notes="The four commands compose the seven existing phase commands. /feature and /bug are sequential — one phase at a time. /team:feature and /team:bug spawn parallel workers for analysis, then coordinate implementation. Custom agents are created alongside commands — each agent gets its own model, tool allowlist, skills, and constraints. All defined in markdown, no code. The PostToolUse hook runs ruff + mypy after every file write — this is back pressure in action. .claude/rules/ adds path-specific context (e.g., different rules for src/ vs tests/). Transition: Why these patterns matter.",
    ),
    # Slide 20: M3 Why It Matters
    ContentSlide(
        title="M3: Why It Matters",
        bullets=[
            ("Commands vs Skills: ", "Explicit invocation vs automatic loading", 0),
            (
                "Agent design = API design: ",
                "Model, tools, skills, scope — composable workers",
                0,
            ),
            (
                "Progressive disclosure: ",
                "Context at the right scope, at the right time",
                0,
            ),
            ("Back pressure via hooks: ", "Resists bad output after every write", 0),
            (
                "Prompt-driven orchestration: ",
                "All extensibility defined in markdown, no code",
                0,
            ),
        ],
        notes="The commands-vs-skills distinction is a key design decision. Commands are explicit — the user or orchestrator invokes them. Skills are implicit — Claude loads them when the task matches. Custom agents are the third extensibility primitive — each scoped with its own model, tools, and constraints. Back pressure via hooks closes the loop immediately: write bad code, get feedback instantly, fix before moving on. The entire system is defined in markdown — no Python, no YAML, just prose. Transition: Let's visualize the four-layer context system.",
    ),
    # Slide 21: The Four-Layer Context System (with image)
    ImageSlide(
        title="The Four-Layer Context System",
        image="images/fourlayer_context_system.png",
        notes="This is the architectural insight of Module 3. The four layers form a progressive disclosure system. CLAUDE.md is always present (broad but essential). Rules narrow to specific directories. Skills narrow to specific task types. Hooks narrow to specific actions. The key insight: context is delivered at the moment it's needed, at the right scope. This prevents context bloat while ensuring Claude always has what it needs. Transition: Let's dig deeper into when progressive disclosure works and when it doesn't.",
    ),
    # Slide 22: Progressive Disclosure — When & When Not
    TwoColumnSlide(
        title="Progressive Disclosure",
        left=[
            ("Works well", "", 0),
            "",
            "CLAUDE.md → rules/ → skills → hooks",
            "Skills auto-load on keyword match",
            "@import defers large docs until needed",
            "Subagents get fresh, task-specific windows",
        ],
        right=[
            ("Anti-patterns", "", 0),
            "",
            "Dumping 100KB+ in system prompt",
            "Loading all reference docs 'just in case'",
            "Same context for every workflow phase",
            "Hiding context the agent needs now",
        ],
        notes="Progressive disclosure is the difference between a productive session and context rot. Left side: the Four-Layer system we just saw. CLAUDE.md is always-on. Rules fire by directory. Skills fire by task type. Hooks fire by event. Each layer narrows scope. Right side: the anti-patterns. The worst is front-loading everything — Claude's attention degrades when buried under irrelevant context. Nielsen Norman research shows 3+ disclosure levels cause confusion even for humans. The last anti-pattern is important: progressive disclosure doesn't mean hiding information — it means delivering it at the right time. If an agent needs reference docs NOW, load them NOW. Transition: The other side of quality — back pressure.",
    ),
    # Slide 23: Back Pressure — Three Layers
    ContentSlide(
        title="Back Pressure: Three Layers",
        bullets=[
            ("Immediate (block before save)", "", 0),
            {
                "text": "PostToolUse hooks: ruff + mypy after every .py write",
                "level": 1,
            },
            {"text": "Pre-commit hooks: 13 checks block bad commits", "level": 1},
            {
                "text": "Type system: mypy --strict rejects invalid annotations",
                "level": 1,
            },
            ("Workflow-level (resist bad process)", "", 0),
            {
                "text": "TDD: failing test written first — code must make it pass",
                "level": 1,
            },
            {"text": "Plan mode: read-only gate prevents premature coding", "level": 1},
            {
                "text": "Spec-driven: PRDs constrain scope, reject out-of-scope work",
                "level": 1,
            },
            ("Post-hoc (catch after completion)", "", 0),
            {"text": "CI/CD: GitHub Actions blocks merge on failure", "level": 1},
            {"text": "Code review: human gate with required approvals", "level": 1},
        ],
        notes="Back pressure means the system actively resists bad output. Three layers, each catching different problems at different times. Immediate: PostToolUse hooks fire after EVERY file write — the agent sees lint errors within seconds and self-corrects. Pre-commit hooks block the commit entirely. Workflow-level: TDD is the strongest back pressure — you can't claim 'done' if tests fail. Plan mode prevents the most expensive mistake: writing code before thinking. Spec-driven development means the PRD is the contract — anything not in the spec gets rejected. Post-hoc: CI/CD and code review catch what slipped through. Key principle: the earlier you catch problems, the cheaper they are to fix. A PostToolUse lint error costs seconds. A failed CI check costs minutes. A post-merge bug costs hours. Transition: Module 4 puts it all together.",
    ),
    # Slide 24: Anatomy of a Custom Agent (with image)
    ImageSlide(
        title="Anatomy of a Custom Agent",
        image="images/agent_anatomy.png",
        notes="Walk through each field. Name and description control when Claude delegates to this agent. Model selection is a cost decision — Haiku for cheap read-only analysis. Tools is an allowlist — the agent can ONLY use these tools, nothing else. permissionMode controls whether the agent can act without confirmation. maxTurns prevents runaway execution. skills preloads specific skills into the agent's context. The system prompt body (below the frontmatter) is where you define the agent's behavior, output format, and constraints. This is agent design as API design: clear inputs, clear outputs, single responsibility. Transition: Module 4 puts it all together.",
    ),
    # Slide 25: Module 4 Section Header
    SectionSlide(
        title="Module 4: Agentic Delivery Workflows",
        notes="Module 4 is where everything comes together. You'll run the orchestration commands from Module 3 against real PRDs, in parallel worktrees, and observe the difference between single-agent and team execution. This is the practical payoff of all the scaffolding work. Transition: What we do.",
    ),
    # Slide 26: M4 What We Do (1/2)
    ContentSlide(
        title="M4: What We Do (1/2)",
        bullets=[
            "Read orchestrator PRDs (adw-feature.md, adw-bug.md)",
            "Launch 2 parallel Claude instances in worktrees:",
            {"text": "Terminal 1: claude -w adw-feat then /team:feature", "level": 1},
            {"text": "Terminal 2: claude -w adw-bug then /feature", "level": 1},
            "Each worktree is an isolated filesystem copy",
            "No branch switching, no merge conflicts during execution",
        ],
        notes="This is the most hands-on module. Two terminals running simultaneously — one with team coordination, one sequential. claude -w creates an isolated worktree automatically. Emphasize that both instances are reading the same PRDs but executing through different orchestration patterns. The worktree isolation means they can modify the same file paths without conflicts. If time is tight, run one terminal live and demo the other. Transition: What to observe.",
    ),
    # Slide 27: M4 What We Do (2/2)
    ContentSlide(
        title="M4: What We Do (2/2)",
        bullets=[
            "Monitor parallel execution patterns:",
            {
                "text": "Team: bursts of parallel activity, then synthesis pauses",
                "level": 1,
            },
            {
                "text": "Single: steady sequential progress, one phase at a time",
                "level": 1,
            },
            "Inspect state files: agents/{adw_id}/state.json",
            "Compare output: code structure, test coverage, style differences",
            "Analyze session logs (JSONL): tool calls, failures, timing",
        ],
        notes="The observable difference between team and single-agent is the activity pattern. Team runs show bursts (4 workers analyzing simultaneously) followed by pauses (leader synthesizing). Single-agent shows steady progress. State files bridge phases — each phase reads the previous output from state.json. Session log analysis reveals coordination overhead in team runs vs. serial efficiency in single-agent. Both approaches produce working code — the question is which pattern fits your use case. Transition: Why these patterns matter.",
    ),
    # Slide 28: M4 Why It Matters (1/2)
    ContentSlide(
        title="M4: Why It Matters (1/2)",
        bullets=[
            (
                "Code-driven orchestration: ",
                "claude -p /phase + JSON state = resumable pipelines",
                0,
            ),
            (
                "Team orchestration: ",
                "Leader/worker pattern via TeamCreate + SendMessage",
                0,
            ),
            (
                "Worktree isolation: ",
                "Filesystem-level sandboxing for parallel execution",
                0,
            ),
            (
                "State files bridge phases: ",
                "Each phase is stateless; JSON carries context forward",
                0,
            ),
        ],
        notes="Two orchestration patterns: code-driven (Python script chains phases via subprocess) and team-driven (leader coordinates workers via SendMessage). Worktrees are the filesystem isolation layer — the first of four sandboxing layers. State files are the glue: they carry the ADW ID, completed phases, plan file path, and issue description between phases. This makes each phase independently resumable. Transition: The deeper principles.",
    ),
    # Slide 29: M4 Why It Matters (2/2)
    ContentSlide(
        title="M4: Why It Matters (2/2)",
        bullets=[
            (
                "Sandboxing = defense in depth: ",
                "Worktree + subagent + hook + permission (4 layers)",
                0,
            ),
            (
                "Agent design = API design: ",
                "Clear inputs, outputs, single responsibility",
                0,
            ),
            (
                "'Tools build tools' pattern: ",
                "Module 3 commands built Module 4 orchestrators",
                0,
            ),
            (
                "Three feedback layers: ",
                "Hooks (immediate), phases (workflow), logs (post-hoc)",
                0,
            ),
        ],
        notes="Sandboxing layers up: worktrees protect the filesystem, subagents protect the context window, hooks protect code quality, permission modes protect system access. Each layer limits what can go wrong at a different scope. Agent design is API design — the better defined the interface, the more reliably agents compose. 'Tools build tools' is a meta-pattern: the commands we built in Module 3 were used to build the orchestrator scripts in Module 4. Three feedback layers give different perspectives: hooks tell you WHAT went wrong (lint error), phase transitions tell you WHEN (which phase failed), session logs tell you WHY (full behavioral trace). Transition: Let's compare the two execution models.",
    ),
    # Slide 30: Single-Agent vs Team Execution (with image)
    ImageSlide(
        title="Single-Agent vs Team Execution",
        image="images/single_agent_vs_team.png",
        notes="This is the comparison table participants should take away. Single-agent is simpler, more predictable, easier to debug. Team is faster for analysis (parallel workers), but adds coordination overhead. The key question isn't 'which is better' but 'which fits your task.' Simple bugs? Single-agent. Complex features with independent analysis areas? Team. The overhead of leader synthesis is only worth it when the analysis phases are truly independent. Transition: Module 5 covers the operational side.",
    ),
    # Slide 31: Module 5 Section Header
    SectionSlide(
        title="Module 5: Operations & Maintenance",
        notes="Module 5 is about sustained use. Headless mode for CI/CD, session management, cost awareness, and CLAUDE.md maintenance. These are the practices that make Claude Code reliable over weeks and months, not just during a workshop. Transition: What we do.",
    ),
    # Slide 32: M5 What We Do (1/2)
    ContentSlide(
        title="M5: What We Do (1/2)",
        bullets=[
            "Headless mode: claude -p 'prompt' for non-interactive use",
            "Pipe content for analysis: cat file.py | claude -p 'review this'",
            "CI/CD integration: PR review bot, GitHub Actions workflow",
            "Agents from Module 3 power CI — run headless with CLAUDE.md only",
            "--dangerously-skip-permissions for automated environments",
            "CLAUDE.md is the sole instruction set in headless mode",
        ],
        notes="Headless mode is what makes Claude useful in pipelines — no chat box, no confirmations, just input/output. The custom agents defined in Module 3 are the building blocks here: they run autonomously shaped only by CLAUDE.md and their own frontmatter configuration. Piping content is a powerful pattern: feed any text to Claude for analysis. Emphasize the --dangerously-skip-permissions flag name: it's intentionally scary because you're removing a safety layer. Transition: Session management and cost.",
    ),
    # Slide 33: M5 What We Do (2/2)
    ContentSlide(
        title="M5: What We Do (2/2)",
        bullets=[
            "Session management: --continue (latest), --resume (by name/ID)",
            "/rename for descriptive session names",
            "Cost tracking: /cost (session), /stats (daily patterns)",
            "Effort levels: Low / Medium / High — controls reasoning depth",
            "Extended thinking: Alt+T toggles scratchpad for complex reasoning",
            "Checkpointing: Esc+Esc or /rewind to undo without losing session",
        ],
        notes="Sessions persist locally — you can resume any previous session by name or ID. Named sessions make it easy to return to specific work threads. Cost tracking is essential for sustained use — /cost shows the current session, /stats shows daily patterns. Effort levels let you match reasoning depth to task complexity: Low for typos, Medium for most work, High for architecture. Extended thinking gives Claude a scratchpad for longer reasoning chains. Checkpointing is the safety net: Claude snapshots before every action, so you can rewind code, conversation, or both. Transition: The principles behind operations.",
    ),
    # Slide 34: M5 Why It Matters
    ContentSlide(
        title="M5: Why It Matters",
        bullets=[
            ("Headless mode: ", "M3 agents run autonomously in CI/CD pipelines", 0),
            (
                "Session persistence: ",
                "Resume context across days without rebuilding",
                0,
            ),
            (
                "Cost and effort controls: ",
                "Match model, effort, and thinking to task",
                0,
            ),
            (
                "Checkpointing: ",
                "Snapshot before every action — rewind code or conversation",
                0,
            ),
            (
                "CLAUDE.md maintenance: ",
                "Stale config actively misleads — treat as code",
                0,
            ),
        ],
        notes="In CI/CD, Claude runs headless with only CLAUDE.md for guidance — the agents defined in Module 3 power this. This is why CLAUDE.md maintenance matters so much. Session persistence means you can pick up where you left off across days. Cost awareness prevents surprise bills — match the model to the task. Checkpointing is the ultimate safety net for experimentation. CLAUDE.md maintenance is ongoing: stale references, contradictory instructions, and vague directives all degrade Claude's performance. Transition: Let's see the big picture.",
    ),
    # Slide 35: The Progression (with image)
    ImageSlide(
        title="The Progression",
        image="images/progression.png",
        notes="This is the retrospective view. Each module builds on the previous. Module 1 gives you the foundation (project + CLAUDE.md). Module 2 adds context awareness and planning discipline. Module 3 builds the orchestration primitives. Module 4 puts them together with parallel execution. Module 5 adds the operational practices for sustained use. The progression mirrors how you'd adopt Claude Code in practice: start with scaffolding, add planning, build workflows, scale with teams, operationalize. Transition: Let's recap the core concepts.",
    ),
    # Slide 36: 10 Core Concepts Recap
    TwoColumnSlide(
        title="10 Core Concepts Recap",
        left=[
            "1. Context Engineering",
            "2. Context Rot",
            "3. Context Poisoning",
            "4. Progressive Disclosure",
            "5. Dynamic Context Injection",
        ],
        right=[
            "6. Skills vs Commands",
            "7. Agent Design",
            "8. Back Pressure",
            "9. Sandboxing",
            "10. Agent Teams",
        ],
        notes="Quick recap of all ten concepts. Ask participants to call out which modules demonstrated each concept. Context Engineering: every module. Context Rot: Module 2. Context Poisoning: Module 2. Progressive Disclosure: Modules 3-4. Dynamic Context Injection: Module 3. Skills vs Commands: Module 3. Agent Design: Modules 4-5. Back Pressure: Modules 1, 3. Sandboxing: Module 4. Agent Teams: Module 4. Transition: Questions?",
    ),
    # Slide 37: Closing
    SectionSlide(
        title="Questions?",
        layout=LAYOUT_CLOSING,
        notes="Open the floor for questions. If time permits, offer to demo any specific concept live. Repo is available for participants to continue working through modules independently. Point them to code.claude.com for official documentation.",
    ),
]


def style_slide(slide, prs):
    """Set background image and dark text on all slide elements."""
    # Add background image covering full slide, sent to back
    pic = slide.shapes.add_picture(BG_IMAGE, 0, 0, prs.slide_width, prs.slide_height)
    # Move picture to back of z-order
    sp_tree = slide.shapes._spTree
    sp_tree.remove(pic._element)
    sp_tree.insert(2, pic._element)

    # Set all text to dark color
    for shape in slide.shapes:
        if shape.has_text_frame:
            for paragraph in shape.text_frame.paragraphs:
                paragraph.font.color.rgb = DARK_TEXT
                for run in paragraph.runs:
                    run.font.color.rgb = DARK_TEXT


def fill_bullets(placeholder, bullets):
    """Fill a placeholder with bullet items."""
    tf = placeholder.text_frame
    tf.clear()
    for i, bullet in enumerate(bullets):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()

        if isinstance(bullet, tuple):
            bold_text, normal_text, level = bullet
            p.level = level
            run = p.add_run()
            run.text = bold_text
            run.font.bold = True
            if normal_text:
                run2 = p.add_run()
                run2.text = normal_text
        elif isinstance(bullet, dict):
            p.text = bullet["text"]
            p.level = bullet.get("level", 0)
        else:
            p.text = bullet
            p.level = 0


def delete_original_slides(prs, count):
    """Delete the first N slides (original template slides)."""
    # We must delete from the beginning, always removing index 0
    # because indices shift after each removal
    for _ in range(count):
        sldIdLst = prs.slides._sldIdLst
        rNs = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
        sldId_elem = sldIdLst[0]  # Always remove first slide
        rId = sldId_elem.get(rNs + "id")
        sldIdLst.remove(sldId_elem)
        prs.part.drop_rel(rId)


def set_notes_font_size(prs):
    """Set speaker notes font size to 18pt for readability."""
    for slide in prs.slides:
        if slide.has_notes_slide:
            for paragraph in slide.notes_slide.notes_text_frame.paragraphs:
                paragraph.font.size = Pt(18)
                for run in paragraph.runs:
                    run.font.size = Pt(18)


def add_title_slide(prs, layout_idx, title_text, subtitle_text=None, notes_text=""):
    """Add a slide with centered title and optional subtitle."""
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:  # Title
            ph.text = title_text
        elif ph.placeholder_format.idx == 1 and subtitle_text:  # Subtitle
            ph.text = subtitle_text

    if notes_text:
        notes = slide.notes_slide
        notes.notes_text_frame.text = notes_text

    style_slide(slide, prs)
    return slide


def add_section_header(prs, layout_idx, title_text, notes_text=""):
    """Add a section header slide with centered title only."""
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:  # Title
            ph.text = title_text

    if notes_text:
        notes = slide.notes_slide
        notes.notes_text_frame.text = notes_text

    style_slide(slide, prs)
    return slide


def add_content_slide(prs, layout_idx, title_text, bullets, notes_text=""):
    """Add a slide with title and bullet list content."""
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    title_ph = None
    content_ph = None

    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:  # Title
            title_ph = ph
        elif ph.placeholder_format.idx in (1, 10, 11):  # Content area
            content_ph = ph

    if title_ph:
        title_ph.text = title_text

    if content_ph:
        fill_bullets(content_ph, bullets)

    if notes_text:
        notes = slide.notes_slide
        notes.notes_text_frame.text = notes_text

    style_slide(slide, prs)
    return slide


def add_image_slide(prs, layout_idx, title_text, image_path, notes_text=""):
    """Add a slide with title and a full-width image in the content area."""
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    title_ph = None
    content_ph = None

    for ph in slide.placeholders:
        if ph.placeholder_format.idx == 0:
            title_ph = ph
        elif ph.placeholder_format.idx in (1, 10, 11):
            content_ph = ph

    if title_ph:
        title_ph.text = title_text

    # Remove the content placeholder and add the image in its place
    if content_ph:
        left = content_ph.left
        top = content_ph.top
        width = content_ph.width
        height = content_ph.height
        # Remove placeholder
        sp = content_ph._element
        sp.getparent().remove(sp)
        # Add image
        slide.shapes.add_picture(image_path, left, top, width, height)

    if notes_text:
        notes = slide.notes_slide
        notes.notes_text_frame.text = notes_text

    style_slide(slide, prs)
    return slide


def add_two_column_slide(
    prs, layout_idx, title_text, left_bullets, right_bullets, notes_text=""
):
    """Add a two-column slide."""
    layout = prs.slide_layouts[layout_idx]
    slide = prs.slides.add_slide(layout)

    placeholders = {ph.placeholder_format.idx: ph for ph in slide.placeholders}

    # Title
    if 0 in placeholders:
        placeholders[0].text = title_text

    # Left content (idx=1)
    if 1 in placeholders:
        fill_bullets(placeholders[1], left_bullets)

    # Right content (idx=2)
    if 2 in placeholders:
        fill_bullets(placeholders[2], right_bullets)

    if notes_text:
        notes = slide.notes_slide
        notes.notes_text_frame.text = notes_text

    style_slide(slide, prs)
    return slide


def render_title(prs, slide_data):
    add_title_slide(
        prs, LAYOUT_TITLE, slide_data.title, slide_data.subtitle, slide_data.notes
    )


def render_section(prs, slide_data):
    add_section_header(prs, slide_data.layout, slide_data.title, slide_data.notes)


def render_content(prs, slide_data):
    add_content_slide(
        prs, LAYOUT_CONTENT, slide_data.title, slide_data.bullets, slide_data.notes
    )


def render_image(prs, slide_data):
    image_path = os.path.join(REPO_ROOT, slide_data.image)
    add_image_slide(prs, LAYOUT_CONTENT, slide_data.title, image_path, slide_data.notes)


def render_two_column(prs, slide_data):
    add_two_column_slide(
        prs,
        LAYOUT_TWO_COLUMN,
        slide_data.title,
        slide_data.left,
        slide_data.right,
        slide_data.notes,
    )


RENDERERS = {
    TitleSlide: render_title,
    SectionSlide: render_section,
    ContentSlide: render_content,
    ImageSlide: render_image,
    TwoColumnSlide: render_two_column,
}


def main():
    prs = Presentation(TEMPLATE)

    # Print available layouts for debugging
    print("Available layouts:")
    for i, layout in enumerate(prs.slide_layouts):
        placeholders_info = [
            (ph.placeholder_format.idx, ph.name) for ph in layout.placeholders
        ]
        print(f"  Layout {i}: {layout.name} — placeholders: {placeholders_info}")
    print()

    original_slide_count = len(prs.slides)
    print(f"Original template has {original_slide_count} slides\n")

    for slide_data in SLIDES:
        renderer = RENDERERS[type(slide_data)]
        renderer(prs, slide_data)

    print(f"Deleting {original_slide_count} original template slides...")
    delete_original_slides(prs, original_slide_count)
    set_notes_font_size(prs)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    prs.save(OUTPUT)
    print(f"\nSaved presentation with {len(prs.slides)} slides to {OUTPUT}")


if __name__ == "__main__":
    main()
