# Quest 1 Product Requirements

## Problem

SiteForge's help-center assistant answers customer questions from help-center
content, but the team does not know whether it is actually useful. The bot
technically works, but there is no repeatable baseline for retrieval quality,
answer quality, or failed examples.

## User Impact

SiteForge customers are small-business owners and operators trying to publish
websites, connect domains, sell products, accept bookings, manage SEO, and
complete related self-serve workflows. Bad assistant answers can create support
tickets, cause customers to abandon important workflows, and reduce trust in the
help center.

Product and support teams also need concrete failure examples so they can see
which customer problems the assistant is failing to solve.

## Scope

Quest 1 should create a classic baseline RAG evaluation for the current
help-center assistant:

- retrieve top-k documents for each evaluation question
- generate an answer from retrieved help-center context
- evaluate retrieval against expected source documents
- evaluate answer quality against expected answer terms
- produce repeatable baseline scores
- produce a markdown report with positive and negative examples

Before implementation, the learner should inspect the data tour:

```text
uv run --extra dev invoke tour
```

## Out of Scope

Do not include advanced retrieval or product integrations in Quest 1:

- agentic RAG
- query planning
- tool use
- multi-hop retrieval
- reranking
- hybrid search
- prompt optimization
- Slack
- GitHub API
- dashboards

## Deliverables

- a repeatable evaluation command
- baseline retrieval metric definitions and scores
- baseline answer-quality metric definitions and scores
- `reports/baseline_report.md`
- positive examples where the baseline found the right document and answered
  with expected terms
- negative examples where retrieval or answer quality failed

## Acceptance Criteria

- The evaluation can be run repeatedly from the repo.
- The report explains each metric in product-readable language.
- The report includes baseline retrieval and answer-quality scores.
- The report includes representative positive examples.
- The report includes representative negative examples with enough detail for
  product and support to understand what failed.
- Quest 1 stays limited to a simple baseline RAG implementation.

## Evaluation Plan

Use the provided evaluation questions, expected answer terms, and expected
source documents. Measure whether retrieved documents include the expected source
material, and whether generated answers include the expected terms. Summarize
the aggregate scores and include concrete examples that show both success and
failure modes.
