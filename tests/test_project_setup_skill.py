from pathlib import Path


def test_project_setup_skill_is_minimal_and_lists_core_parts():
    text = Path("skills/project-setup.md").read_text()

    assert "Keep it minimal" in text
    assert "skills/maya-product-lead.md" in text
    assert "skills/ari-data-guide.md" in text
    assert "app/retrieval.py" in text
    assert "uv run --extra dev invoke data" in text
    assert "uv run --extra dev invoke tour" not in text
    assert "uv run buildguild status" in text
    assert "analysis/quest_01_product_requirements.md" in text
    assert "analysis/quest_01_implementation_spec.md" in text
    assert "analysis/baseline_report.md" in text
    assert "Maya -> Ari -> implementation -> evaluation report -> Maya review" in text
