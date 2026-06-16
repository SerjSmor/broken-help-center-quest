# Write Technical Spec

Use this skill after:

- `requirements/quest_01_product_requirements.md` exists.
- `notes/quest_01_data_tour.md` exists.
- The learner has completed Ari's data tour.
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
- Retrieval uses the existing backend lexical retriever in `app/retrieval.py`.
- The learner implements the evaluation harness, simple answer generation, CLI path, and report.
- Retrieval evaluates whether the expected WixQA source article appears in the top 5 retrieved documents.
- Answer generation evaluates a simple baseline answer against reference-answer terms.
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
