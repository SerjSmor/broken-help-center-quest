# BuildGuild Status

Report the player's current BuildGuild Quest 1 status.

## Instructions

Run or inspect the equivalent of:

```text
uv run buildguild status
```

If running `uv` would trigger environment/cache friction, do not request permissions just for status. Instead, inspect:

- `.buildguild/state.json`
- `requirements/quest_01_product_requirements.md`
- `specs/quest_01_implementation_spec.md`
- `reports/baseline_report.md`
- Required implementation files in `app/` and `evals/`

Then report:

- Current stage.
- Completed steps.
- Missing steps.
- Next recommended action.

## Quest 1 Stages

1. Product discovery.
2. Tour the data.
3. Write implementation spec.
4. Implement baseline RAG.
5. Run baseline evaluation.
6. Maya report review.
7. Quest complete.

Keep the answer short and actionable.
