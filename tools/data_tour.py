from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_PATH = ROOT / "data" / "processed" / "documents.jsonl"
QUESTIONS_PATH = ROOT / "data" / "processed" / "eval_questions.jsonl"
SAMPLE_DOCUMENTS_PATH = ROOT / "data" / "sample" / "documents.jsonl"
SAMPLE_QUESTIONS_PATH = ROOT / "data" / "sample" / "eval_questions.jsonl"


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def data_path(primary: Path, fallback: Path) -> Path:
    return primary if primary.exists() else fallback


def load_data() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    documents = load_jsonl(data_path(DOCUMENTS_PATH, SAMPLE_DOCUMENTS_PATH))
    questions = load_jsonl(data_path(QUESTIONS_PATH, SAMPLE_QUESTIONS_PATH))
    return documents, questions


def document_lookup(documents: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {doc["id"]: doc for doc in documents}


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
    col_c.metric("Expected doc links", linked)

    st.divider()

    tab_examples, tab_articles, tab_questions = st.tabs(
        ["Guided examples", "Help articles", "Eval questions"]
    )

    with tab_examples:
        st.subheader("Guided examples")
        st.write("Each evaluation question points to the article the baseline should retrieve.")
        question_ids = [question["id"] for question in questions]
        selected_id = st.selectbox("Choose an evaluation question", question_ids)
        question = next(item for item in questions if item["id"] == selected_id)

        st.markdown(f"**Question:** {question['question']}")
        st.markdown(
            "**Expected answer terms:** "
            + ", ".join(f"`{term}`" for term in question.get("expected_answer_contains", []))
        )

        st.markdown("**Expected documents:**")
        for doc_id in question.get("expected_doc_ids", []):
            doc = docs_by_id.get(doc_id)
            if doc is None:
                st.warning(f"Missing document: {doc_id}")
                continue
            with st.expander(f"{doc['id']} - {doc['title']}", expanded=True):
                st.caption(doc["url"])
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
                st.caption(doc["url"])
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
