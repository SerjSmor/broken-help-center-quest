from pathlib import Path

from tools.quest_statusline import build_status_line


def test_statusline_starts_with_quest_setup(tmp_path):
    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [0/8] Quest setup -> buildguild start"


def test_statusline_points_to_product_discovery_after_setup(tmp_path):
    write_state(tmp_path, {})

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [1/8] Product discovery -> /quest-status"


def test_statusline_points_to_ari_spec_after_product_discovery(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "implementation_spec_completed": False,
        },
    )
    write_file(tmp_path, "analysis/quest_01_product_requirements.md")

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [3/8] Tour + spec -> ari-data-guide"


def test_statusline_points_to_maya_review_after_report(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": False,
        },
    )
    write_file(tmp_path, "analysis/quest_01_product_requirements.md")
    write_file(tmp_path, "analysis/quest_01_implementation_spec.md")
    for path in (
        "analysis/ask.py",
        "analysis/rag.py",
        "app/retrieval.py",
        "analysis/run_baseline.py",
        "analysis/metrics.py",
        "analysis/baseline_report.md",
    ):
        write_file(tmp_path, path)

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [7/8] Maya review -> maya-tests-outputs"


def test_statusline_marks_complete_after_maya_review(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": True,
        },
    )
    write_file(tmp_path, "analysis/quest_01_product_requirements.md")
    write_file(tmp_path, "analysis/quest_01_implementation_spec.md")
    for path in (
        "analysis/ask.py",
        "analysis/rag.py",
        "app/retrieval.py",
        "analysis/run_baseline.py",
        "analysis/metrics.py",
        "analysis/baseline_report.md",
    ):
        write_file(tmp_path, path)

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [8/8] Complete -> watch repo"


def write_state(root: Path, quest_state: dict[str, bool]) -> None:
    write_file(
        root,
        ".buildguild/state.json",
        '{\n  "player": {\n'
        '    "name": "Test Builder",\n'
        '    "difficulty": "easy",\n'
        '    "setup_completed": true\n'
        '  },\n'
        '  "quest_01": {\n'
        + ",\n".join(f'    "{key}": {str(value).lower()}' for key, value in quest_state.items())
        + "\n  }\n}\n",
    )


def write_file(root: Path, relative_path: str, text: str = "") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
