# Quest Status

Use this skill whenever the player asks for Quest 1 status, uses `/quest-status`, or asks what to do next.

This skill is agent-agnostic. Codex, Claude Code, OpenCode, and a plain chat agent should all follow the same status contract.

## Preferred Path

If it is safe and available, run:

```text
uv run buildguild status
```

If running `uv` would trigger cache, permission, environment, or approval friction, do not request permission just for status. Inspect files directly instead.

## Direct Inspection

Read:

- `.buildguild/state.json`

Check whether these files exist:

- `requirements/quest_01_product_requirements.md`
- `notes/quest_01_data_tour.md`
- `specs/quest_01_implementation_spec.md`
- `reports/baseline_report.md`
- `app/ask.py`
- `app/rag.py`
- `app/retrieval.py`
- `evals/run_baseline.py`
- `evals/metrics.py`

## Stage Order

Report the first incomplete stage:

1. Product discovery
   - Needs `quest_01.product_onboarding_completed = true`.
   - Needs `requirements/quest_01_product_requirements.md`.

2. Tour the data
   - Needs `notes/quest_01_data_tour.md`.
   - Needs `quest_01.data_tour_completed = true`.
   - Next action: ask the coding agent to use `skills/ari-data-guide.md`; Streamlit is only the visual companion.

3. Write implementation spec
   - Needs `specs/quest_01_implementation_spec.md`.
   - Needs `quest_01.implementation_spec_completed = true`.

4. Implement baseline evaluation
   - Needs `app/ask.py`.
   - Needs `app/rag.py`.
   - Needs `app/retrieval.py`.
   - Needs `evals/run_baseline.py`.
   - Needs `evals/metrics.py`.

5. Run baseline evaluation
   - Needs `reports/baseline_report.md`.

6. Maya report review
   - Needs `quest_01.maya_report_review_passed = true`.

7. Quest complete

## Response Format

Keep it short:

```text
Quest 1 Status
Stage: <stage>

Done:
- ...

Missing:
- ...

Next:
<one concrete next action>
```

Do not role-play Maya in status output. Do not start product discovery. Only report current state and the next action.
