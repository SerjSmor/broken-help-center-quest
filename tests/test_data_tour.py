from pathlib import Path

from tools.data_tour import load_data


def test_data_tour_loads_documents_and_questions():
    documents, questions = load_data()

    assert len(documents) >= 20
    assert len(questions) >= 20
    assert {"id", "title", "url", "body"} <= documents[0].keys()
    assert {"id", "question", "expected_answer_contains", "expected_doc_ids"} <= questions[0].keys()
    assert all(document["url"].startswith("/help/") for document in documents)
    assert all("example.local" not in document["url"] for document in documents)


def test_tour_task_and_docs_are_present():
    tasks = Path("tasks.py").read_text()
    readme = Path("README.md").read_text()
    persona = Path("skills/maya-product-lead.md").read_text()
    app = Path("tools/data_tour.py").read_text()

    assert "def tour" in tasks
    assert "streamlit run tools/data_tour.py" in tasks
    assert "uv run --extra dev invoke tour" in readme
    assert "data_tour_completed" in readme
    assert "uv run --extra dev invoke tour" in persona
    assert "Ari checklist" in app
    assert "What this dataset is" in app
    assert "Example help article" in app
    assert "Example labeled evaluation question" in app
    assert "Example likely failure case" in app
    assert "Overlapping topic cluster" in app
    assert "Use skills/ari-data-guide.md to tour the data with me." in app
    assert "notes/quest_01_data_tour.md" in app
    assert "Guided examples" in app
    assert "Expected help articles" in app
    assert "Article content" in app
    assert "Expected doc links" not in app
