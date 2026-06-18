import json
from pathlib import Path

from scripts.restart_quest import CONFIRMATION, restart_quest


def test_restart_quest_removes_outputs_and_resets_state(tmp_path):
    output_files = [
        "analysis/quest_01_product_requirements.md",
        "analysis/quest_01_implementation_spec.md",
        "analysis/baseline_report.md",
        "analysis/quest_01_eda.py",
        "analysis/ask.py",
        "analysis/rag.py",
        "analysis/run_baseline.py",
        "analysis/metrics.py",
    ]
    for relative_path in output_files:
        write_file(tmp_path, relative_path, "generated\n")
    write_file(tmp_path, "app/retrieval.py", "starter\n")
    write_file(
        tmp_path,
        ".buildguild/state.json",
        json.dumps(
            {
                "quest_01": {
                    "product_onboarding_completed": True,
                    "implementation_spec_completed": True,
                    "maya_report_review_passed": True,
                },
                "player": {
                    "name": "Serj",
                    "difficulty": "hard",
                    "setup_completed": True,
                    "level": 2,
                    "title": "Baseline Builder",
                    "xp": 500,
                    "achievements": {
                        "product_hunch": True,
                        "data_intuition": True,
                        "baseline_before_optimization": True,
                    },
                }
            }
        ),
    )

    removed = restart_quest(tmp_path)

    assert set(removed) >= {Path(path) for path in output_files}
    for relative_path in output_files:
        assert not (tmp_path / relative_path).exists()
    assert (tmp_path / "app/retrieval.py").read_text() == "starter\n"

    state = json.loads((tmp_path / ".buildguild/state.json").read_text())
    assert state == {
        "quest_01": {
            "product_onboarding_completed": False,
            "implementation_spec_completed": False,
            "maya_report_review_passed": False,
        },
        "player": {
            "name": None,
            "difficulty": "easy",
            "setup_completed": False,
            "level": 1,
            "title": "New Builder",
            "xp": 0,
            "achievements": {
                "product_hunch": False,
                "data_intuition": False,
                "baseline_before_optimization": False,
            },
        }
    }


def test_restart_skill_documents_confirmation_and_script():
    text = Path("skills/restart-game.md").read_text()

    assert CONFIRMATION in text
    assert "python3 scripts/restart_quest.py --confirm RESET_QUEST_01" in text
    assert "Do not delete files manually" in text
    assert "app/retrieval.py" in text


def write_file(root: Path, relative_path: str, text: str) -> None:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
