# Project Setup

Use this skill when the player asks what this repo is, how the pieces fit together, or what to run.

Keep it minimal. Do not start a roleplay scene.

## Explain The Setup

BuildGuild Quest 1 is a repo-based game:

- Maya handles product discovery: `skills/maya-product-lead.md`.
- Ari handles data tour plus technical spec: `skills/ari-data-guide.md`.
- The backend starter retriever is `app/retrieval.py`.
- The player implements the evaluator/report around that retriever.

## Key Commands

```text
uv run --extra dev invoke data
uv run buildguild status
uv run --extra dev invoke test
```

## Main Artifacts

```text
analysis/quest_01_product_requirements.md
analysis/quest_01_implementation_spec.md
analysis/baseline_report.md
.buildguild/state.json
```

## Flow

```text
Maya -> Ari -> implementation -> evaluation report -> Maya review
```

If processed data is missing, run `uv run --extra dev invoke data` before the tour.
