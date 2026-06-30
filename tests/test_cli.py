from typer.testing import CliRunner

from buildguild.cli import app


def test_cli_status_runs(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "BuildGuild Status" in result.output
    assert "uv run buildguild start" in result.output


def test_cli_rejects_unknown_skill():
    runner = CliRunner()

    result = runner.invoke(app, ["run", "skill", "unknown", "--quest", "quest-01"])

    assert result.exit_code != 0
    assert "Unknown skill" in result.output


def test_cli_rejects_unknown_quest():
    runner = CliRunner()

    result = runner.invoke(app, ["run", "skill", "maya-tests-outputs", "--quest", "quest-99"])

    assert result.exit_code != 0
    assert "Only quest-01" in result.output


def test_cli_maya_tests_outputs_prints_agent_instructions():
    runner = CliRunner()

    result = runner.invoke(app, ["run", "skill", "maya-tests-outputs", "--quest", "quest-01"])

    assert result.exit_code == 0
    assert "Maya report review is agent-mediated" in result.output
    assert "analysis/baseline_report.md" in result.output
    assert "maya_report_review_passed = true" in result.output


def test_cli_status_renders_checkbox_markers(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "[ ] Mike data onboarding completed" in result.output
    assert "[ ] Product onboarding completed" in result.output


def test_cli_banner_prints_opening_screen():
    runner = CliRunner()

    result = runner.invoke(app, ["banner"])

    assert result.exit_code == 0
    assert "B U I L D   G U I L D" in result.output
    assert "QUEST I: THE BROKEN HELP CENTER" in result.output
    assert "> run start" in result.output


def test_cli_start_saves_name_and_difficulty(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    runner = CliRunner()

    result = runner.invoke(app, ["start", "--name", "Serj", "--difficulty", "hard"])

    assert result.exit_code == 0
    assert "Quest setup complete: Serj chose hard difficulty." in result.output
    assert "Next: use skills/mike-data-onboarding.md" in result.output

    status = runner.invoke(app, ["status"])

    assert status.exit_code == 0
    assert "Name: Serj" in status.output
    assert "Difficulty: hard" in status.output
    assert "skills/mike-data-onboarding.md" in status.output
