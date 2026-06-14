# Write Technical Spec

Use this skill after:

- `requirements/quest_01_product_requirements.md` exists.
- The learner has run and reviewed the data tour.
- `.buildguild/state.json` has `quest_01.data_tour_completed = true`.

The learner and coding agent should collaboratively create:

```text
specs/quest_01_implementation_spec.md
```

This is the actual implementation ticket for Quest 1.

## Workshop Rules

- Do not jump straight to code.
- Ask one engineering question at a time.
- Keep scope aligned with Maya's product requirements.
- Make the learner decide the baseline approach.
- Keep agentic RAG, reranking, hybrid search, dashboards, Slack, and GitHub API out of scope.

## Required Sections

```text
# Quest 1 Technical Spec: Baseline RAG Evaluation

## Product Requirement Source
## Goal
## User-Facing Commands
## Files To Implement
## Data Contracts
## Baseline Retrieval Approach
## Answer Generation Approach
## Evaluation Plan
## Report Format
## Acceptance Criteria
## Out of Scope
## Implementation Order
```

## Evaluation Plan Must Include

- Command: `python -m evals.run_baseline`
- Metrics:
  - `retrieval_hit_rate@5`
  - `answer_match_rate`
  - `average_answer_length`
  - `num_failed_questions`
- Report path: `reports/baseline_report.md`
- Positive examples.
- Negative failed examples.

When the spec is complete, update `.buildguild/state.json`:

```json
{
  "quest_01": {
    "implementation_spec_completed": true
  }
}
```
