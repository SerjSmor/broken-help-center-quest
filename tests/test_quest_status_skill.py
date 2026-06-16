from pathlib import Path


def test_shared_quest_status_skill_exists():
    text = Path("skills/quest-status.md").read_text()

    assert "agent-agnostic" in text
    assert "uv run buildguild status" in text
    assert ".buildguild/state.json" in text
    assert "requirements/quest_01_product_requirements.md" in text
    assert "notes/quest_01_data_tour.md" in text
    assert "skills/ari-data-guide.md" in text
    assert "Streamlit is only the visual companion" in text
    assert "specs/quest_01_implementation_spec.md" in text
    assert "reports/baseline_report.md" in text
    assert "Maya report review" in text


def test_slash_command_wrappers_delegate_to_shared_skill():
    codex = Path(".codex/commands/quest-status.md").read_text()
    claude = Path(".claude/commands/quest-status.md").read_text()

    assert "skills/quest-status.md" in codex
    assert "skills/quest-status.md" in claude
    assert len(codex.splitlines()) < 12
    assert len(claude.splitlines()) < 12
