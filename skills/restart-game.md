# Restart Game

Use this skill when the player asks to restart Quest 1, reset the game, or clear generated quest outputs.

This is destructive. Do not run the reset immediately.

## Confirmation

First explain exactly what will happen:

- Delete generated Quest 1 output files:
  - `analysis/article_type_frequency.csv`
  - `analysis/quest_01_product_requirements.md`
  - `analysis/quest_01_implementation_spec.md`
  - `analysis/baseline_report.md`
  - `analysis/quest_01_eda.py`
  - `analysis/ask.py`
  - `analysis/rag.py`
  - `analysis/run_baseline.py`
  - `analysis/metrics.py`
- Reset `.buildguild/state.json` to the default Quest 1 flags.
- Keep starter files, including `app/retrieval.py`, skills, docs, and any prepared WixQA data.

Then ask the player to confirm with this exact phrase:

```text
RESET_QUEST_01
```

If the player does not provide that exact phrase, do not reset anything.

## Deterministic Script

After exact confirmation, run:

```text
python3 scripts/restart_quest.py --confirm RESET_QUEST_01
```

Do not delete files manually. The script is the source of truth for what gets reset.

## Completion

After the script succeeds, tell the player to run:

```text
uv run buildguild status
```

The expected next stage is product discovery with Maya.
