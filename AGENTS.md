# Agent Context

This file gives coding agents and maintainers quick context on the implementation stages.

BuildGuild Broken Help Center is a repo-based learning project for users working with coding agents such as Codex, Claude Code, or OpenCode.

The intended quest flow is:

```text
start -> status -> agent-mediated Maya onboarding -> Ari data tour -> technical spec -> learner implementation -> Maya report review
```

Implemented so far:

- Repo shell.
- Python Invoke task runner.
- State helper.
- Status command.
- Start command for player name and difficulty.
- CLI router.
- Sample data pipeline.
- Maya persona scaffold in `skills/maya-product-lead.md`.

Important constraints:

- Quest 1 starts with `uv run buildguild start`.
- Setup asks: "What is your name, brave adventurer?" and "How much guidance do you want on this quest?"
- Difficulty is stored at `player.difficulty` in `.buildguild/state.json`.
- Default difficulty is `easy`.
- Difficulty is player-facing guidance level:
  - `easy`: Apprentice mode with direct hints, clear nudges, and frequent check-ins.
  - `medium`: Builder mode with fewer hints; the player drives the investigation.
  - `hard`: Expert mode with minimal spoon-feeding and distracting noise while keeping facts, files, commands, and artifacts correct.
- Do not generate `issues/quest_01_baseline.md` for the learner.
- Product discovery must produce `analysis/quest_01_product_requirements.md` before the learner writes the engineering ticket.
- The technical spec at `analysis/quest_01_implementation_spec.md` is the implementation ticket. There is no separate ticket-review gate.
- `maya-tests-outputs` is the required Maya report-review skill after `analysis/baseline_report.md` exists.
- Maya report review is roleplay product acceptance, not code review.
- Quest 1 is complete only after `quest_01.maya_report_review_passed = true`.
- Maya should hand the learner to Ari's combined data-tour and technical-spec step before implementation.
- Ari is the coding agent in EDA mode, defined in `skills/ari-data-guide.md`.
- Ari should create `analysis/quest_01_implementation_spec.md` with a `## Data Tour Findings` section.
- During Maya discovery, always show the four discovery checkboxes from `skills/maya-product-lead.md`.
- Start with hidden checkbox labels (`???`) and reveal a label only after the learner asks a qualifying question.
- The learner can ask for tips; tips should nudge without revealing exact checkbox labels or exact right questions.
- Do not run any command to start Maya discovery. Read `skills/maya-product-lead.md` and role-play directly.
- Do not ship a complete baseline RAG solution in the starter repo.
- Product onboarding is not a local fallback chat. Use `skills/maya-product-lead.md` and reveal facts gradually.
- When the four discovery gates are complete, create `analysis/quest_01_product_requirements.md`, then update `.buildguild/state.json` with `quest_01.product_onboarding_completed = true`.
- Unlock `product_hunch` after product discovery, `data_intuition` after Ari's spec step, and `baseline_before_optimization` after Maya accepts the report.
- Quest 1 completion levels the player to Level 2, title `Baseline Builder`.
- Quest 2 is not available yet; tell the player to watch the repo for updates.
- After product discovery, use `skills/ari-data-guide.md` for EDA and technical spec writing. Ari may inspect files and run small scripts, but must not implement the baseline evaluator.
- Keep agentic RAG, reranking, hybrid retrieval, Slack, GitHub API, and dashboards out of Quest 1 scope.

Useful commands:

```text
uv run buildguild start
uv run --extra dev invoke data
uv run --extra dev invoke test
uv run buildguild status
```

Repo-local slash command prompts:

```text
.claude/commands/quest-status.md
.codex/commands/quest-status.md
```

Both should delegate to the shared skill:

```text
skills/quest-status.md
```

Claude Code status line support:

```text
.claude/settings.json
tools/quest_statusline.py
```

The statusline script must stay dependency-free and read-only. It should not run `uv`, install packages, or mutate `.buildguild/state.json`.

Do not show bare `buildguild ...` commands in learner-facing output unless the instructions also explain that the project environment must be activated. Prefer `uv run buildguild ...`.

Upcoming implementation phases:

- Quest 2 will arrive in a future repo update.
