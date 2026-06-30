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

    assert status.stage == "Mike data onboarding"
    assert "skills/mike-data-onboarding.md" in status.next_action
    assert "analysis/article_type_frequency.csv" in status.next_action
    assert status.player_name == "Test Builder"
    assert status.player_difficulty == "easy"


def test_status_after_mike_onboarding_points_to_product_discovery(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_started_state()
    write_valid_article_type_frequency()
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {"customer_pain_onboarding_completed": True},
        }
    )

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "skills/maya-product-lead.md" in status.next_action
    assert "analysis/quest_01_product_requirements.md" in status.next_action


def test_status_after_onboarding_without_requirements_stays_in_discovery(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "easy", "setup_completed": True},
            "quest_01": {
                "customer_pain_onboarding_completed": True,
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    write_valid_article_type_frequency()

    status = inspect_status()

    assert status.stage == "Product discovery"
    assert "Product requirements found" in status.missing


def test_status_after_onboarding_and_requirements_points_to_ari_spec(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    save_state(
        {
            "player": {"name": "Test Builder", "difficulty": "medium", "setup_completed": True},
            "quest_01": {
                "customer_pain_onboarding_completed": True,
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    write_valid_article_type_frequency()
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
                "customer_pain_onboarding_completed": True,
                "product_onboarding_completed": True,
                "implementation_spec_completed": False,
            }
        }
    )
    write_valid_article_type_frequency()
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
                "customer_pain_onboarding_completed": True,
                "product_onboarding_completed": True,
                "implementation_spec_completed": True,
            }
        }
    )
    write_valid_article_type_frequency()
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
                "customer_pain_onboarding_completed": True,
                "product_onboarding_completed": True,
                "implementation_spec_completed": True,
                "maya_report_review_passed": False,
            }
        }
    )
    write_valid_article_type_frequency()
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
                "customer_pain_onboarding_completed": True,
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
    write_valid_article_type_frequency()
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


def write_valid_article_type_frequency() -> None:
    write_file(
        "data/onboarding/articles.csv",
        "article_id,title,article_type\n"
        "kb_001,Connecting a custom domain,Domains\n"
        "kb_002,Fixing DNS propagation delays,Domains\n"
        "kb_003,Changing your site template,Design\n"
        "kb_004,Customizing mobile layout,Design\n"
        "kb_005,Setting up online payments,Billing\n"
        "kb_006,Understanding plan charges,Billing\n"
        "kb_007,Creating booking services,Bookings\n"
        "kb_008,Managing booking calendar availability,Bookings\n"
        "kb_009,Recovering a deleted page,Site Management\n"
        "kb_010,Publishing changes to a live site,Site Management\n",
    )
    write_file(
        "data/onboarding/support_questions.csv",
        "question_id,question,answer,article_ids\n"
        'sq_001,Why is my connected domain still not opening my site?,Check DNS,"kb_001;kb_002"\n'
        "sq_002,Can I change my template after publishing?,Adjust design,kb_003\n"
        "sq_003,Why was I charged after upgrading my plan?,Review charges,kb_006\n"
        'sq_004,How do I accept payments for my store?,Connect payments,"kb_005;kb_006"\n'
        "sq_005,My mobile site layout looks broken.,Use mobile editor,kb_004\n"
        'sq_006,How do I make appointment slots available?,Set services,"kb_007;kb_008"\n'
        "sq_007,I published but my changes are not visible.,Confirm publish,kb_010\n"
        "sq_008,Can I restore a page I deleted by mistake?,Recover page,kb_009\n"
        'sq_009,Why cannot customers book times on my calendar?,Check bookings,"kb_007;kb_008"\n'
        'sq_010,Why does my domain show the old website?,Review DNS,"kb_001;kb_002"\n',
    )
    write_file(
        "analysis/article_type_frequency.csv",
        "article_type,count\n"
        "Bookings,4\n"
        "Domains,4\n"
        "Billing,3\n"
        "Design,2\n"
        "Site Management,2\n",
    )
