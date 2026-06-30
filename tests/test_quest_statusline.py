from pathlib import Path

from tools.quest_statusline import build_status_line


def test_statusline_starts_with_quest_setup(tmp_path):
    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [0/10] Quest setup -> buildguild start"


def test_statusline_points_to_product_discovery_after_setup(tmp_path):
    write_state(tmp_path, {})

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [1/10] Mike onboarding -> mike-data-onboarding"


def test_statusline_points_to_product_discovery_after_mike_onboarding(tmp_path):
    write_state(tmp_path, {"customer_pain_onboarding_completed": True})
    write_valid_article_type_frequency(tmp_path)

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [3/10] Product discovery -> /quest-status"


def test_statusline_points_to_ari_spec_after_product_discovery(tmp_path):
    write_state(
        tmp_path,
        {
            "customer_pain_onboarding_completed": True,
            "product_onboarding_completed": True,
            "implementation_spec_completed": False,
        },
    )
    write_valid_article_type_frequency(tmp_path)
    write_file(tmp_path, "analysis/quest_01_product_requirements.md")

    line = build_status_line(tmp_path)

    assert line == "BuildGuild Q1 [5/10] Tour + spec -> ari-data-guide"


def test_statusline_points_to_maya_review_after_report(tmp_path):
    write_state(
        tmp_path,
        {
            "customer_pain_onboarding_completed": True,
            "product_onboarding_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": False,
        },
    )
    write_valid_article_type_frequency(tmp_path)
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

    assert line == "BuildGuild Q1 [9/10] Maya review -> maya-tests-outputs"


def test_statusline_marks_complete_after_maya_review(tmp_path):
    write_state(
        tmp_path,
        {
            "customer_pain_onboarding_completed": True,
            "product_onboarding_completed": True,
            "implementation_spec_completed": True,
            "maya_report_review_passed": True,
        },
    )
    write_valid_article_type_frequency(tmp_path)
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

    assert line == "BuildGuild Q1 [10/10] Complete -> watch repo"


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


def write_valid_article_type_frequency(root: Path) -> None:
    write_file(
        root,
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
        root,
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
        root,
        "analysis/article_type_frequency.csv",
        "article_type,count\n"
        "Domains,4\n"
        "Bookings,4\n"
        "Billing,3\n"
        "Design,2\n"
        "Site Management,2\n",
    )
