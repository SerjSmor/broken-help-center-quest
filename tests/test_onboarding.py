from buildguild.onboarding import article_type_frequency_is_valid, expected_article_type_counts


def test_expected_article_type_counts_uses_multiple_article_ids():
    counts = expected_article_type_counts()

    assert counts["Domains"] == 4
    assert counts["Bookings"] == 4
    assert counts["Billing"] == 3
    assert counts["Design"] == 2
    assert counts["Site Management"] == 2


def test_article_type_frequency_validation_accepts_correct_output(tmp_path):
    output = tmp_path / "article_type_frequency.csv"
    output.write_text(
        "article_type,count\n"
        "Domains,4\n"
        "Bookings,4\n"
        "Billing,3\n"
        "Design,2\n"
        "Site Management,2\n"
    )

    assert article_type_frequency_is_valid(output_path=output)


def test_article_type_frequency_validation_rejects_wrong_counts(tmp_path):
    output = tmp_path / "article_type_frequency.csv"
    output.write_text("article_type,count\nDomains,999\n")

    assert article_type_frequency_is_valid(output_path=output) is False
