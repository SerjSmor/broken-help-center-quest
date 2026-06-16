from pathlib import Path

from scripts.prepare_dataset import normalize_dataset, prepare_dataset


def test_normalize_dataset_accepts_huggingface_dataset_like_object():
    dataset = {
        "knowledge_base": [
            {
                "article_id": "https://support.wix.com/en/article/connect-a-domain",
                "title": "Connecting a domain",
                "article_url": "https://support.wix.com/en/article/connect-a-domain",
                "content": "Connect a domain by updating DNS records at your provider.",
            }
        ],
        "expert_written": [
            {
                "question_id": "ew_001",
                "question": "How do I connect my domain?",
                "answer": "Update DNS records at your domain provider.",
                "article_url": "https://support.wix.com/en/article/connect-a-domain",
            }
        ],
    }

    documents, questions = normalize_dataset(dataset)

    assert documents == [
        {
            "id": "https://support.wix.com/en/article/connect-a-domain",
            "title": "Connecting a domain",
            "url": "https://support.wix.com/en/article/connect-a-domain",
            "body": "Connect a domain by updating DNS records at your provider.",
        }
    ]
    assert questions[0]["id"] == "ew_001"
    assert questions[0]["question"] == "How do I connect my domain?"
    assert questions[0]["reference_answer"] == "Update DNS records at your domain provider."
    assert questions[0]["expected_doc_ids"] == [
        "https://support.wix.com/en/article/connect-a-domain"
    ]
    assert "Update" in questions[0]["expected_answer_contains"]


def test_prepare_dataset_writes_processed_files_from_loaded_dataset(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("scripts.prepare_dataset.PROCESSED_DIR", Path("data/processed"))
    monkeypatch.setattr(
        "scripts.prepare_dataset.load_wixqa",
        lambda _dataset_name: {
            "kb": [
                {
                    "id": "doc_a",
                    "title": "Article A",
                    "url": "https://support.wix.com/a",
                    "body": "Article A body.",
                }
            ],
            "qa": [
                {
                    "id": "q_a",
                    "question": "Question A?",
                    "answer": "Answer A.",
                    "expected_doc_ids": ["doc_a"],
                }
            ],
        },
    )

    prepare_dataset("mock/wixqa")

    assert Path("data/processed/documents.jsonl").exists()
    assert Path("data/processed/eval_questions.jsonl").exists()
