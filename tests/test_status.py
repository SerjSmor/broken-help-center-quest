from pathlib import Path

from buildguild.state import save_state
from buildguild.status import inspect_status


def test_fresh_status_points_to_onboarding(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    status = inspect_status()

    assert status.stage == "Quest setup"
    assert "uv run buildguild start" in status.next_action


def test_status_after_setup_points_to_onboarding(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_started_state()

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "skills/maya-product-lead.md" in status.next_action
    assert "analysis/quest_01_product_requirements.md" in status.next_action
    assert status.player_name == "Test Builder"
    assert status.player_difficulty == "easy"


def test_status_after_onboarding_without_requirements_stays_in_discovery(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "Product requirements found" in status.missing


def test_status_after_onboarding_and_requirements_points_to_ari_spec(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "medium", "setup_completed": True},
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    write_file("analysis/quest_01_product_requirements.md", "# Product Requirements\n")

    status = inspect_status()

    assert status.stage == "Tour data and write implementation spec"
    assert "skills/ari-data-guide.md" in status.next_action
    assert "analysis/quest_01_implementation_spec.md" in status.next_action
    assert "Data Tour Findings" in status.next_action


def test_status_after_spec_file_without_state_stays_on_ari_spec(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    write_file("analysis/quest_01_product_requirements.md", "# Product Requirements\n")
    write_file("analysis/quest_01_implementation_spec.md", "# Technical Spec\n")

    status = inspect_status()

    assert status.stage == "Tour data and write implementation spec"
    assert "Implementation spec completed" in status.missing


def test_status_after_implementation_spec_points_to_implementation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": True,
            }
        }
    )
    write_file("analysis/quest_01_product_requirements.md", "# Product Requirements\n")
    write_file("analysis/quest_01_implementation_spec.md", "# Technical Spec\n")

    status = inspect_status()

    assert status.stage == "Implement baseline evaluation"
    assert "python analysis/ask.py" in status.next_action


def test_status_after_report_points_to_maya_review(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": True,
                "maya_report_review_passed": False,
            }
        }
    )
    write_file("analysis/quest_01_product_requirements.md", "# Product Requirements\n")
    write_file("analysis/quest_01_implementation_spec.md", "# Technical Spec\n")
    write_file("app/retrieval.py", "")
    for path in ("analysis/ask.py", "analysis/rag.py", "analysis/run_baseline.py", "analysis/metrics.py"):
        write_file(path, "")
    write_file("analysis/baseline_report.md", "# Baseline Report\n")

    status = inspect_status()

    assert status.stage == "Maya report review"
    assert "skills/maya-tests-outputs.md" in status.next_action


def test_status_after_maya_review_is_complete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": True,
                "maya_report_review_passed": True,
            },
            "player": {
                "name": "Test Builder",
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
    )
    write_file("analysis/quest_01_product_requirements.md", "# Product Requirements\n")
    write_file("analysis/quest_01_implementation_spec.md", "# Technical Spec\n")
    write_file("app/retrieval.py", "")
    for path in ("analysis/ask.py", "analysis/rag.py", "analysis/run_baseline.py", "analysis/metrics.py"):
        write_file(path, "")
    write_file("analysis/baseline_report.md", "# Baseline Report\n")

    status = inspect_status()

    assert status.stage == "Quest complete"
    assert "Quest 1 complete" in status.next_action
    assert "Quest 2 is not available yet" in status.next_action
    assert status.player_level == 2
    assert status.player_title == "Baseline Builder"
    assert status.player_xp == 500
    assert status.achievements == [
        "Product Hunch",
        "Data Intuition",
        "Baseline Before Optimization",
    ]


def write_file(relative_path: str, text: str) -> None:
    path = Path(relative_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def save_started_state() -> None:
    save_state(
        {
            "player": {
                "name": "Test Builder",
                "difficulty": "easy",
                "setup_completed": True,
            }
        }
    )
