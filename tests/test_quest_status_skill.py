from pathlib import Path


def test_shared_quest_status_skill_exists():
    text = Path("skills/quest-status.md").read_text()

    assert "agent-agnostic" in text
    assert "uv run buildguild status" in text
    assert ".buildguild/state.json" in text
    assert "player.name" in text
    assert "player.difficulty" in text
    assert "player.setup_completed" in text
    assert "uv run buildguild start" in text
    assert "analysis/quest_01_product_requirements.md" in text
    assert "skills/ari-data-guide.md" in text
    assert "Ari should build the EDA app with the player" in text
    assert "analysis/quest_01_implementation_spec.md" in text
    assert "analysis/baseline_report.md" in text
    assert "Maya report review" in text
    assert "player.achievements" in text
    assert "Quest 2 is not available yet" in text


def test_slash_command_wrappers_delegate_to_shared_skill():
    codex = Path(".codex/commands/quest-status.md").read_text()
    claude = Path(".claude/commands/quest-status.md").read_text()

    assert "skills/quest-status.md" in codex
    assert "skills/quest-status.md" in claude
    assert len(codex.splitlines()) < 12
    assert len(claude.splitlines()) < 12
