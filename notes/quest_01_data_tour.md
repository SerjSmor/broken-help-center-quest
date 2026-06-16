# Quest 1 Data Tour Notes

## Dataset Shape

The processed Quest 1 dataset contains 20 help-center documents and 20
evaluation questions:

- Documents live in `data/processed/documents.jsonl`.
- Evaluation questions live in `data/processed/eval_questions.jsonl`.
- Document fields are `id`, `title`, `url`, and `body`.
- Evaluation question fields are `id`, `question`, `expected_answer_contains`,
  and `expected_doc_ids`.

Each evaluation question currently has exactly one expected source document.
The dataset is intentionally small enough for a simple baseline RAG evaluator.

## Retrieval Inputs

The useful retrieval text is the document `title` plus `body`.

The titles contain strong task labels, such as:

- `doc_001`: `Connecting a domain`
- `doc_005`: `Setting up online payments`
- `doc_020`: `Troubleshooting SSL`

The bodies are short help-center snippets. Body lengths range from 12 to 20
words, with an average of 15.8 words. The shortest examples are
`doc_011` (`Configuring shipping`) and `doc_014`
(`Connecting email marketing`), both at 12 words. The longest examples are
`doc_001` (`Connecting a domain`) and `doc_002` (`Publishing your site`), both
at 20 words.

The `url` field is source metadata for citations, not document content. It can
be shown in reports, but the baseline should not rely on URL path text as the
main retrieval body.

Quest 1 should retrieve over title plus body. Title-only retrieval would miss
important answer terms, while body-only retrieval would throw away useful labels
like `Troubleshooting SSL`, `Adding products`, and `Managing SEO settings`.

## Evaluation Labels

`expected_doc_ids` supports a retrieval metric such as
`retrieval_hit_rate@5`: a question passes retrieval if at least one expected
source document appears in the top five retrieved documents.

`expected_answer_contains` supports a simple answer-quality metric such as
`answer_match_rate`: a generated answer passes if it includes the required
expected terms for that question.

All expected answer terms are present in the corresponding source document body.
Examples:

- `q_001` expects `doc_001` and answer terms `domain`, `DNS`.
- `q_005` expects `doc_005` and answer terms `payment provider`,
  `verification`.
- `q_020` expects `doc_020` and answer terms `SSL`, `certificate`.

Retrieval and answer quality measure different failures. A run can retrieve the
right document but omit required terms in the answer, or it can miss the source
document and therefore fail answer matching.

The baseline report should include these metrics:

- `retrieval_hit_rate@5`
- `answer_match_rate`
- `average_answer_length`
- `num_failed_questions`

## Likely Failure Cases

Several questions have overlapping vocabulary with other articles:

- `q_001` asks how to connect a domain. `doc_001` is expected, but `doc_020`
  also mentions `domain` because SSL troubleshooting happens after domain
  connection.
- `q_020` asks why SSL is not ready after connecting a domain. `doc_020` is
  expected, but `doc_001` also matches `connecting` and `domain`.
- `q_013` asks where to see site analytics. A simple overlap check can rank
  several broad `site` articles near or above the analytics article unless the
  retriever gives enough weight to `analytics`.
- `q_012` asks about coupon codes. The word `create` appears in several
  articles, including blog posts, templates, email marketing, members area, and
  bookings.
- Store-related articles can be close together: products, payments, shipping,
  coupons, and bookings all mention commerce or operational setup concepts.

The report should highlight risky examples where common words pull in nearby
but incorrect documents. Those examples are useful product evidence, not just
debugging trivia.

## Report Requirements

The final baseline report should be readable without inspecting code. It should
include:

- Metric definitions in product-readable language.
- Baseline retrieval score.
- Baseline answer-quality score.
- Average answer length.
- Failed question count.
- Positive examples with question, expected docs, retrieved docs, generated
  answer, and matched terms.
- Negative examples with question, expected docs, retrieved docs, generated
  answer, missing terms, and failure reason.
- The command that generated the report.

Each evaluation result row should preserve enough detail to diagnose whether a
failure came from retrieval, answer generation, or both.

## Implications For Technical Spec

The implementation spec should require a small, repeatable baseline RAG flow:

- Load processed documents and evaluation questions from JSONL files.
- Index document title plus body.
- Retrieve top five documents per question.
- Generate a short answer from retrieved context.
- Evaluate retrieval with `retrieval_hit_rate@5`.
- Evaluate answer terms with `answer_match_rate`.
- Track `average_answer_length` and `num_failed_questions`.
- Write `reports/baseline_report.md` with aggregate metrics and concrete
  positive and negative examples.

Quest 1 should stay limited to a classic baseline. Do not add agentic RAG,
query planning, reranking, hybrid search, Slack, GitHub API integrations, or
dashboards.
