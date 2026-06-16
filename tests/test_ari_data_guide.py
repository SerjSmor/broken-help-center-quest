from pathlib import Path


def test_ari_data_guide_skill_defines_required_eda_flow():
    text = Path("skills/ari-data-guide.md").read_text()

    assert "Ari is not a separate bot" in text
    assert "coding agent in EDA mode" in text
    assert "Do not quiz the learner" in text
    assert "requirements/quest_01_product_requirements.md" in text
    assert "data/processed/documents.jsonl" in text
    assert "data/sample/documents.jsonl" not in text
    assert "Dataset shape understood" in text
    assert "Retrieval inputs inspected" in text
    assert "Evaluation labels understood" in text
    assert "Likely failure cases identified" in text
    assert "Report requirements captured" in text
    assert "title plus body" in text
    assert "app/retrieval.py" in text
    assert "retrieval_hit_rate@5" in text
    assert "answer_match_rate" in text
    assert "notes/quest_01_data_tour.md" in text
    assert "quest_01.data_tour_completed = true" in text
    assert "Do not implement the baseline evaluator" in text
