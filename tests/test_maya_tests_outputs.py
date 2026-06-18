from pathlib import Path

from buildguild.skills.maya_tests_outputs import INSTRUCTIONS


def test_maya_tests_outputs_is_report_review_skill():
    text = Path("skills/maya-tests-outputs.md").read_text()

    assert "roleplay product-acceptance review" in text
    assert "player.difficulty" in text
    assert "analysis/baseline_report.md" in text
    assert "Metric definitions" in text
    assert "Baseline retrieval score" in text
    assert "Retrieval hit rate at 5" in text
    assert "Positive examples" in text
    assert "Negative examples" in text
    assert "maya_report_review_passed" in text
    assert "Quest 1 is accepted" in text
    assert "Product Hunch" in text
    assert "Data Intuition" in text
    assert "Baseline Before Optimization" in text
    assert "Level 1 -> Level 2" in text
    assert "Quest 2 is not available yet" in text


def test_maya_tests_outputs_cli_instructions_match_roleplay_flow():
    assert "No command is needed for Maya to review the report" in INSTRUCTIONS
    assert "skills/maya-tests-outputs.md" in INSTRUCTIONS
    assert "analysis/baseline_report.md" in INSTRUCTIONS
    assert ".buildguild/state.json" in INSTRUCTIONS
    assert "metric definitions" in INSTRUCTIONS
    assert "baseline scores" in INSTRUCTIONS
    assert "positive examples" in INSTRUCTIONS
    assert "negative failed examples" in INSTRUCTIONS
    assert "quest_01.maya_report_review_passed = true" in INSTRUCTIONS
    assert "player.level = 2" in INSTRUCTIONS
    assert "Baseline Builder" in INSTRUCTIONS
