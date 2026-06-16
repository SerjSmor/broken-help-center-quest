from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_PATH = ROOT / "data" / "processed" / "documents.jsonl"
QUESTIONS_PATH = ROOT / "data" / "processed" / "eval_questions.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if not DOCUMENTS_PATH.exists() or not QUESTIONS_PATH.exists():
        raise FileNotFoundError(
            "Processed WixQA data is missing. Run: uv run --extra dev invoke data"
        )
    documents = load_jsonl(DOCUMENTS_PATH)
    questions = load_jsonl(QUESTIONS_PATH)
    return documents, questions


def document_lookup(documents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {doc["id"]: doc for doc in documents}


def find_first_question(
    questions: list[dict[str, Any]], expected_doc_id: str
) -> dict[str, Any] | None:
    for question in questions:
        if expected_doc_id in question.get("expected_doc_ids", []):
            return question
    return None


def find_docs_by_terms(documents: list[dict[str, Any]], terms: list[str]) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    for doc in documents:
        haystack = f"{doc['title']} {doc['body']}".lower()
        if any(term.lower() in haystack for term in terms):
            found.append(doc)
    return found


def render_article_snapshot(doc: dict[str, Any]) -> None:
    st.markdown(f"**{doc['id']} - {doc['title']}**")
    st.caption(f"Source path: {doc['url']}")
    st.write(doc["body"])


def render_eval_snapshot(question: dict[str, Any], docs_by_id: dict[str, dict[str, Any]]) -> None:
    st.markdown(f"**Question:** {question['question']}")
    st.markdown(
        "**Expected answer terms:** "
        + ", ".join(f"`{term}`" for term in question.get("expected_answer_contains", []))
    )
    st.markdown(
        "**Expected source docs:** "
        + ", ".join(f"`{doc_id}`" for doc_id in question.get("expected_doc_ids", []))
    )
    for doc_id in question.get("expected_doc_ids", []):
        doc = docs_by_id.get(doc_id)
        if doc:
            render_article_snapshot(doc)


def render_ari_checklist(
    documents: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    docs_by_id: dict[str, dict[str, Any]],
) -> None:
    st.subheader("Ari's guided EDA")
    st.write(
        "Ari is your coding agent in EDA mode. The Streamlit tour is the visual "
        "companion; Ari should inspect the data files, explain the checks, and write "
        "`notes/quest_01_data_tour.md` before the quest moves on."
    )
    st.code("Use skills/ari-data-guide.md to tour the data with me.", language="text")

    st.markdown("### What this dataset is")
    st.write(
        f"You are looking at **{len(documents)} Wix help-center articles** and "
        f"**{len(questions)} labeled WixQA evaluation questions**. In the game story, "
        "SiteForge uses this public benchmark because it mirrors the same website-builder "
        "support surface without exposing proprietary production data. Each article is a source "
        "the baseline RAG system can retrieve. Each evaluation question tells us which "
        "article should be found and which answer terms should appear."
    )

    if documents:
        st.markdown("### Example help article")
        render_article_snapshot(documents[0])
        st.caption(
            "Ari's read: retrieval should use the title and article content. "
            "The source path is useful for reporting, but it is not the content."
        )

    example_question = questions[0] if questions else None
    if example_question is not None:
        st.markdown("### Example labeled evaluation question")
        render_eval_snapshot(example_question, docs_by_id)
        st.caption(
            "Ari's read: expected_doc_ids supports retrieval scoring. "
            "expected_answer_contains supports answer-quality scoring."
        )

    ssl_question = find_first_question(questions, "doc_020")
    if ssl_question is not None:
        st.markdown("### Example likely failure case")
        render_eval_snapshot(ssl_question, docs_by_id)
        domain_doc = docs_by_id.get("doc_001")
        if domain_doc is not None:
            with st.expander("Nearby article that could confuse retrieval: doc_001 - Connecting a domain"):
                render_article_snapshot(domain_doc)
        st.caption(
            "Ari's read: SSL and domain setup share vocabulary. A simple retriever may "
            "pull the domain article when the expected source is the SSL article."
        )

    store_docs = find_docs_by_terms(documents, ["product", "payment", "shipping", "coupon"])
    if store_docs:
        st.markdown("### Overlapping topic cluster")
        st.write(
            "Store-related articles share terms that may compete during retrieval. "
            "These are good candidates for negative examples if the baseline misses."
        )
        for doc in store_docs[:4]:
            with st.expander(f"{doc['id']} - {doc['title']}"):
                render_article_snapshot(doc)

    st.markdown("### EDA checklist")
    checklist = [
        (
            "Dataset shape understood",
            "Count documents and questions, then list the fields each row provides.",
        ),
        (
            "Retrieval inputs inspected",
            "Sample titles and article bodies, compare short and long articles, and decide what to index.",
        ),
        (
            "Evaluation labels understood",
            "Inspect expected document ids and expected answer terms separately.",
        ),
        (
            "Likely failure cases identified",
            "Look for overlapping topics such as domains and SSL, or products and payments.",
        ),
        (
            "Report requirements captured",
            "Define what the baseline report must include for Maya to trust it.",
        ),
    ]

    for label, description in checklist:
        st.checkbox(label, value=False, help=description)

    st.info(
        "Checking boxes here is only for your own tour progress. Quest progress is completed "
        "when Ari writes notes/quest_01_data_tour.md and updates .buildguild/state.json."
    )


def main() -> None:
    st.set_page_config(page_title="BuildGuild Data Tour", page_icon="🧭", layout="wide")
    documents, questions = load_data()
    docs_by_id = document_lookup(documents)

    st.title("BuildGuild Data Tour")
    st.caption("Quest 1: Broken Help Center")

    st.write(
        "Before you build the baseline RAG system, inspect the help-center data. "
        "The goal is to understand what the assistant will retrieve from and how evaluation questions are labeled."
    )

    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Help articles", len(documents))
    col_b.metric("Eval questions", len(questions))
    linked = sum(len(q.get("expected_doc_ids", [])) for q in questions)
    col_c.metric("Expected sources", linked)

    st.divider()

    tab_ari, tab_examples, tab_articles, tab_questions = st.tabs(
        ["Ari checklist", "Guided examples", "Help articles", "Eval questions"]
    )

    with tab_ari:
        render_ari_checklist(documents, questions, docs_by_id)

    with tab_examples:
        st.subheader("Guided examples")
        st.write("Each evaluation question names the help article content the baseline should retrieve.")
        question_ids = [question["id"] for question in questions]
        selected_id = st.selectbox("Choose an evaluation question", question_ids)
        question = next(item for item in questions if item["id"] == selected_id)

        st.markdown(f"**Question:** {question['question']}")
        st.markdown(
            "**Expected answer terms:** "
            + ", ".join(f"`{term}`" for term in question.get("expected_answer_contains", []))
        )

        st.markdown("**Expected help articles:**")
        for doc_id in question.get("expected_doc_ids", []):
            doc = docs_by_id.get(doc_id)
            if doc is None:
                st.warning(f"Missing document: {doc_id}")
                continue
            with st.expander(f"{doc['id']} - {doc['title']}", expanded=True):
                st.caption(f"Source path: {doc['url']}")
                st.markdown("**Article content**")
                st.write(doc["body"])

    with tab_articles:
        st.subheader("Help articles")
        query = st.text_input("Filter articles by title or body", "")
        filtered_docs = [
            doc
            for doc in documents
            if query.lower() in f"{doc['title']} {doc['body']}".lower()
        ]
        st.write(f"Showing {len(filtered_docs)} of {len(documents)} articles.")
        for doc in filtered_docs:
            with st.expander(f"{doc['id']} - {doc['title']}"):
                st.caption(f"Source path: {doc['url']}")
                st.markdown("**Article content**")
                st.write(doc["body"])

    with tab_questions:
        st.subheader("Eval questions")
        for question in questions:
            with st.expander(f"{question['id']} - {question['question']}"):
                st.markdown(
                    "**Expected answer terms:** "
                    + ", ".join(f"`{term}`" for term in question.get("expected_answer_contains", []))
                )
                st.markdown(
                    "**Expected document ids:** "
                    + ", ".join(f"`{doc_id}`" for doc_id in question.get("expected_doc_ids", []))
                )


if __name__ == "__main__":
    main()
