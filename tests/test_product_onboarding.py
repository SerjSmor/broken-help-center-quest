from pathlib import Path

from typer.testing import CliRunner

from buildguild.cli import app
from buildguild.skills.product_onboarding import ONBOARDING_INSTRUCTIONS


def test_product_onboarding_command_points_to_agent_skill():
    assert "agent-mediated" in ONBOARDING_INSTRUCTIONS
    assert "Codex" in ONBOARDING_INSTRUCTIONS
    assert "Claude Code" in ONBOARDING_INSTRUCTIONS
    assert "OpenCode" in ONBOARDING_INSTRUCTIONS
    assert "No command is needed to start Maya discovery" in ONBOARDING_INSTRUCTIONS
    assert "should not run uv" in ONBOARDING_INSTRUCTIONS
    assert "skills/maya-product-lead.md" in ONBOARDING_INSTRUCTIONS
    assert "three hidden discovery checkboxes" in ONBOARDING_INSTRUCTIONS
    assert "You can ask Maya for tips" in ONBOARDING_INSTRUCTIONS
    assert "requirements/quest_01_product_requirements.md" in ONBOARDING_INSTRUCTIONS
    assert "product_onboarding_completed = true" in ONBOARDING_INSTRUCTIONS
    assert "Maya must not write the engineering ticket" in ONBOARDING_INSTRUCTIONS


def test_product_onboarding_cli_does_not_role_play_maya(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["run", "skill", "product-onboarding", "--quest", "quest-01"])

    assert result.exit_code == 0
    assert "Product onboarding is agent-mediated" in result.output
    assert "You:" not in result.output
    assert not Path(".buildguild/state.json").exists()


def test_maya_persona_skill_contains_required_context():
    text = Path("skills/maya-product-lead.md").read_text()

    assert "SiteForge" in text
    assert "website-builder" in text
    assert "help-center assistant" in text
    assert "measurable baseline" in text
    assert "Expected quest outcomes" in text
    assert "baseline score" in text.lower()
    assert "Positive examples" in text
    assert "Negative examples" in text
    assert "Agentic RAG" in text
    assert "Do not write the ticket" in text
    assert "Stay in character as Maya" in text
    assert "Do not explain that you are using a skill" in text
    assert "begin immediately with the opening scene" in text
    assert "Quest 1: The Bot Works. Nobody Knows If It Is Good." in text
    assert "what are you talking about?" in text
    assert "Can you remind me your name?" in text
    assert "embarrassingly bad at names" in text
    assert "most important task" in text
    assert "real chance to show your product engineering judgment" in text
    assert "I am bad at data" in text
    assert "tour the data" in text
    assert "uv run --extra dev invoke tour" in text
    assert "quest_01.data_tour_completed = true" in text
    assert "data_tour_completed" in text
    assert "What do you ask Maya first?" in text
    assert "Discovery checklist:" in text
    assert "- [ ] ???" in text
    assert "🧠 That's a very interesting question." in text
    assert "Use this signal only when a question unlocks" in text
    assert "Once a gate is revealed, keep its label visible" in text
    assert "tips" in text
    assert "should not reveal the hidden checkbox labels" in text
    assert "Try asking who suffers when the assistant is wrong." in text
    assert "requirements/quest_01_product_requirements.md" in text
    assert "issues/quest_01_baseline.md" in text


def test_product_requirements_artifact_template_is_in_persona_skill():
    text = Path("skills/maya-product-lead.md").read_text()

    assert "# Quest 1 Product Requirements: Broken Help Center Baseline" in text
    assert "## Company Context" in text
    assert "## Problem" in text
    assert "## User Impact" in text
    assert "## Goal" in text
    assert "## Expected Outcomes" in text
    assert "## Scope" in text
    assert "## Out of Scope" in text
    assert "## Deliverables" in text
    assert "## Success Criteria" in text
    assert "Baseline retrieval score" in text
    assert "Baseline answer-quality score" in text


def test_readme_does_not_tell_learners_to_run_onboarding_command():
    text = Path("README.md").read_text()

    assert "No terminal command is needed to start the Maya conversation" in text
    assert "uv run buildguild run skill product-onboarding" not in text
