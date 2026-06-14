import json
from pathlib import Path

from scripts.prepare_dataset import prepare_dataset


def test_prepare_dataset_writes_processed_files():
    prepare_dataset()

    documents_path = Path("data/processed/documents.jsonl")
    questions_path = Path("data/processed/eval_questions.jsonl")

    assert documents_path.exists()
    assert questions_path.exists()

    documents = [json.loads(line) for line in documents_path.read_text().splitlines()]
    questions = [json.loads(line) for line in questions_path.read_text().splitlines()]

    assert len(documents) >= 20
    assert len(questions) >= 20
    assert {"id", "title", "url", "body"} <= documents[0].keys()
    assert {"id", "question", "expected_answer_contains", "expected_doc_ids"} <= questions[0].keys()
