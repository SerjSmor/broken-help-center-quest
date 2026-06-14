from pathlib import Path

from buildguild.state import save_state
from buildguild.status import inspect_status


def test_fresh_status_points_to_onboarding(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "skills/maya-product-lead.md" in status.next_action
    assert "requirements/quest_01_product_requirements.md" in status.next_action


def test_status_after_onboarding_without_requirements_stays_in_discovery(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "Product requirements found" in status.missing


def test_status_after_onboarding_and_requirements_points_to_data_tour(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "data_tour_completed": False,
                "implementation_spec_completed": False,
            }
        }
    )
    Path("requirements").mkdir()
    Path("requirements/quest_01_product_requirements.md").write_text("# Product Requirements\n")

    status = inspect_status()

    assert status.stage == "Tour the data"
    assert "invoke tour" in status.next_action
    assert "data_tour_completed = true" in status.next_action


def test_status_after_data_tour_points_to_implementation_spec(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "data_tour_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    Path("requirements").mkdir()
    Path("requirements/quest_01_product_requirements.md").write_text("# Product Requirements\n")

    status = inspect_status()

    assert status.stage == "Write implementation spec"
    assert "skills/write-implementation-spec.md" in status.next_action
    assert "specs/quest_01_implementation_spec.md" in status.next_action


def test_status_after_implementation_spec_points_to_implementation(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "data_tour_completed": True,
                "implementation_spec_completed": True,
            }
        }
    )
    Path("requirements").mkdir()
    Path("requirements/quest_01_product_requirements.md").write_text("# Product Requirements\n")
    Path("specs").mkdir()
    Path("specs/quest_01_implementation_spec.md").write_text("# Technical Spec\n")

    status = inspect_status()

    assert status.stage == "Implement baseline RAG"
    assert "python -m app.ask" in status.next_action


def test_status_after_report_points_to_maya_review(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "data_tour_completed": True,
                "implementation_spec_completed": True,
                "maya_report_review_passed": False,
            }
        }
    )
    Path("requirements").mkdir()
    Path("requirements/quest_01_product_requirements.md").write_text("# Product Requirements\n")
    Path("specs").mkdir()
    Path("specs/quest_01_implementation_spec.md").write_text("# Technical Spec\n")
    Path("app").mkdir()
    for filename in ("ask.py", "rag.py", "retrieval.py"):
        Path("app", filename).write_text("")
    Path("evals").mkdir()
    for filename in ("run_baseline.py", "metrics.py"):
        Path("evals", filename).write_text("")
    Path("reports").mkdir()
    Path("reports/baseline_report.md").write_text("# Baseline Report\n")

    status = inspect_status()

    assert status.stage == "Maya report review"
    assert "skills/maya-tests-outputs.md" in status.next_action


def test_status_after_maya_review_is_complete(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "quest_01": {
                "product_onboarding_completed": True,
                "data_tour_completed": True,
                "implementation_spec_completed": True,
                "maya_report_review_passed": True,
            }
        }
    )
    Path("requirements").mkdir()
    Path("requirements/quest_01_product_requirements.md").write_text("# Product Requirements\n")
    Path("specs").mkdir()
    Path("specs/quest_01_implementation_spec.md").write_text("# Technical Spec\n")
    Path("app").mkdir()
    for filename in ("ask.py", "rag.py", "retrieval.py"):
        Path("app", filename).write_text("")
    Path("evals").mkdir()
    for filename in ("run_baseline.py", "metrics.py"):
        Path("evals", filename).write_text("")
    Path("reports").mkdir()
    Path("reports/baseline_report.md").write_text("# Baseline Report\n")

    status = inspect_status()

    assert status.stage == "Quest complete"
    assert "Quest 1 complete" in status.next_action
