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
        "wixqa_expertwritten": [
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
    assert questions == [
        {
            "id": "ew_001",
            "question": "How do I connect my domain?",
            "answer": "Update DNS records at your domain provider.",
            "expected_doc_ids": ["https://support.wix.com/en/article/connect-a-domain"],
        }
    ]


def test_prepare_dataset_writes_processed_files_from_loaded_dataset(tmp_path):
    output_dir = tmp_path / "data" / "processed"

    prepare_dataset(
        "mock/wixqa",
        output_dir=output_dir,
        load_fn=lambda _dataset_name: {
            "kb": [
                {
                    "id": "doc_a",
                    "title": "Article A",
                    "url": "https://support.wix.com/a",
                    "body": "Article A body.",
                }
            ],
            "wixqa_expertwritten": [
                {
                    "id": "q_a",
                    "question": "Question A?",
                    "answer": "Answer A.",
                    "expected_doc_ids": ["doc_a"],
                }
            ],
        },
    )

    assert (output_dir / "documents.jsonl").exists()
    assert (output_dir / "questions.jsonl").exists()
    assert sorted(path.name for path in output_dir.iterdir()) == ["documents.jsonl", "questions.jsonl"]


def test_prepare_dataset_rebuilds_existing_processed_files(tmp_path):
    output_dir = tmp_path / "data" / "processed"
    output_dir.mkdir(parents=True)
    (output_dir / "documents.jsonl").write_text('{"id":"existing"}\n')
    (output_dir / "questions.jsonl").write_text('{"id":"existing"}\n')

    prepare_dataset(
        "mock/wixqa",
        output_dir=output_dir,
        load_fn=lambda _dataset_name: {
            "kb": [
                {
                    "id": "doc_rebuilt",
                    "title": "Rebuilt",
                    "url": "https://support.wix.com/rebuilt",
                    "body": "Rebuilt body.",
                }
            ],
            "wixqa_expertwritten": [
                {
                    "id": "q_rebuilt",
                    "question": "Rebuilt?",
                    "answer": "Rebuilt answer.",
                    "expected_doc_ids": ["doc_rebuilt"],
                }
            ],
        },
    )

    assert "doc_rebuilt" in (output_dir / "documents.jsonl").read_text()
    assert "q_rebuilt" in (output_dir / "questions.jsonl").read_text()
