from rich.cells import cell_len

from buildguild.banner import BANNER_LINES, COMPACT_BANNER_LINES, render_banner


def test_banner_contains_quest_title_and_prompt():
    banner = render_banner().plain

    assert "B U I L D   G U I L D" in banner
    assert "QUEST I: THE BROKEN HELP CENTER" in banner
    assert "[404] HELP CENTER" in banner
    assert "> run start" in banner
    assert "> choose name + difficulty" in banner
    assert "> mentor: Maya waits beyond setup_" in banner
    assert len(BANNER_LINES) >= 20
    assert len({cell_len(line) for line in BANNER_LINES}) == 1


def test_compact_banner_keeps_fixed_width():
    banner = render_banner(width=60).plain

    assert "QUEST I: THE BROKEN HELP CENTER" in banner
    assert "Objective: Measure the baseline retriever." in banner
    assert len({cell_len(line) for line in COMPACT_BANNER_LINES}) == 1
    assert max(cell_len(line) for line in COMPACT_BANNER_LINES) <= 60


def test_banner_right_border_stays_in_same_display_column():
    for banner_lines in (BANNER_LINES, COMPACT_BANNER_LINES):
        width = cell_len(banner_lines[0])

        for line in banner_lines:
            assert cell_len(line) == width
            assert line[-1] in {"╗", "║", "╝"}


def test_full_banner_nested_panel_right_edge_is_aligned():
    title_index = next(
        index for index, line in enumerate(BANNER_LINES) if "QUEST I: THE BROKEN HELP CENTER" in line
    )
    panel_lines = BANNER_LINES[title_index - 1 : title_index + 7]

    right_edges = {
        cell_len(line[: line[1:-1].rfind(border) + 2])
        for line in panel_lines
        for border in ("╗", "║", "╝")
        if border in line[8:-1]
    }

    assert len(panel_lines) == 8
    assert len(right_edges) == 1
