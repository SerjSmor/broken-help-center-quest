from pathlib import Path

from tools.quest_statusline import build_status_line


def test_statusline_starts_with_product_discovery(tmp_path):
    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [0/9] Product discovery -> /quest-status"


def test_statusline_points_to_data_tour_after_product_discovery(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "data_tour_completed": False,
        },
    )
    write_file(tmp_path, "requirements/quest_01_product_requirements.md")

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [2/9] Tour data -> ari-data-guide"


def test_statusline_stays_on_data_tour_until_notes_exist(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "data_tour_completed": True,
        },
    )
    write_file(tmp_path, "requirements/quest_01_product_requirements.md")

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [3/9] Tour data -> ari-data-guide"


def test_statusline_points_to_maya_review_after_report(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "data_tour_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": False,
        },
    )
    write_file(tmp_path, "requirements/quest_01_product_requirements.md")
    write_file(tmp_path, "notes/quest_01_data_tour.md")
    write_file(tmp_path, "specs/quest_01_implementation_spec.md")
    for path in (
        "app/ask.py",
        "app/rag.py",
        "app/retrieval.py",
        "evals/run_baseline.py",
        "evals/metrics.py",
        "reports/baseline_report.md",
    ):
        write_file(tmp_path, path)

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [8/9] Maya review -> maya-tests-outputs"


def test_statusline_marks_complete_after_maya_review(tmp_path):
    write_state(
        tmp_path,
        {
            "product_onboarding_completed": True,
            "data_tour_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": True,
        },
    )
    write_file(tmp_path, "requirements/quest_01_product_requirements.md")
    write_file(tmp_path, "notes/quest_01_data_tour.md")
    write_file(tmp_path, "specs/quest_01_implementation_spec.md")
    for path in (
        "app/ask.py",
        "app/rag.py",
        "app/retrieval.py",
        "evals/run_baseline.py",
        "evals/metrics.py",
        "reports/baseline_report.md",
    ):
        write_file(tmp_path, path)

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [9/9] Complete -> Quest 2 ready"


def write_state(root: Path, quest_state: dict[str, bool]) -> None:
    write_file(
        root,
        ".buildguild/state.json",
        '{\n  "quest_01": {\n'
        + ",\n".join(f'    "{key}": {str(value).lower()}' for key, value in quest_state.items())
        + "\n  }\n}\n",
    )


def write_file(root: Path, relative_path: str, text: str = "") -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
