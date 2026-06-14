# Agent Context

This file gives coding agents and maintainers quick context on the implementation stages.

BuildGuild Broken Help Center is a repo-based learning project for users working with coding agents such as Codex, Claude Code, or OpenCode.

The intended quest flow is:

```text
status -> agent-mediated Maya onboarding -> data tour -> technical spec -> learner implementation -> Maya report review
```

Implemented so far:

- Repo shell.
- Python Invoke task runner.
- State helper.
- Status command.
- CLI router.
- Sample data pipeline.
- Maya persona scaffold in `skills/maya-product-lead.md`.

Important constraints:

- Do not generate `issues/quest_01_baseline.md` for the learner.
- Product discovery must produce `requirements/quest_01_product_requirements.md` before the learner writes the engineering ticket.
- The technical spec at `specs/quest_01_implementation_spec.md` is the implementation ticket. There is no separate ticket-review gate.
- `maya-tests-outputs` is the required Maya report-review skill after `reports/baseline_report.md` exists.
- Maya report review is roleplay product acceptance, not code review.
- Quest 1 is complete only after `quest_01.maya_report_review_passed = true`.
- Maya should recommend the Streamlit data tour before implementation: `uv run --extra dev invoke tour`.
- Do not mark `quest_01.data_tour_completed = true` until the learner confirms they ran and reviewed the tour.
- During Maya discovery, always show the three discovery checkboxes from `skills/maya-product-lead.md`.
- Start with hidden checkbox labels (`???`) and reveal a label only after the learner asks a qualifying question.
- The learner can ask for tips; tips should nudge without revealing exact checkbox labels or exact right questions.
- Do not run `uv`, `buildguild run skill product-onboarding`, or any command to start Maya discovery. Read `skills/maya-product-lead.md` and role-play directly.
- Do not ship a complete baseline RAG solution in the starter repo.
- Product onboarding is not a local fallback chat. Use `skills/maya-product-lead.md` and reveal facts gradually.
- When the three discovery gates are complete, create `requirements/quest_01_product_requirements.md`, then update `.buildguild/state.json` with `quest_01.product_onboarding_completed = true` and leave `quest_01.data_tour_completed = false`.
- Keep agentic RAG, reranking, hybrid retrieval, Slack, GitHub API, and dashboards out of Quest 1 scope.

Useful commands:

```text
uv run --extra dev invoke data
uv run --extra dev invoke test
uv run buildguild status
```

Do not show bare `buildguild ...` commands in learner-facing output unless the instructions also explain that the project environment must be activated. Prefer `uv run buildguild ...`.

Upcoming implementation phases:

- Learner scaffolding in `app/` and `evals/`.
- Quest validator skill.
- Reference implementation kept outside the starter repo.
