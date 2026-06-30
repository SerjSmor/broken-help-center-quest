from __future__ import annotations

from rich.cells import cell_len, set_cell_size
from rich.console import Console
from rich.text import Text


BANNER_WIDTH = 64
COMPACT_BANNER_WIDTH = 58


def _build_full_banner() -> list[str]:
    quest_panel = _inset_box(
        inner_width=BANNER_WIDTH - 2,
        inset=6,
        box_width=46,
        content=[
            "QUEST I: THE BROKEN HELP CENTER",
            "",
            "The support bot has lost its memory.",
            "The docs are noisy. Retrieval is cursed.",
            "",
            "Objective: Measure the baseline retriever.",
        ],
    )
    return _box(
        BANNER_WIDTH,
        [
            "✦        .          *        ✧          .          ✦",
            "        SYS: MEMORY FAULT     IDX: ? ? ?",
            "    /\\/\\        [404] HELP CENTER        /\\/\\",
            " ~~~~~~~~~       corrupted index       ~~~~~~~~~",
            "        ⚠ retrieval signal unstable ⚠",
            "",
            "      ██████╗ ██╗   ██╗██╗██╗     ██████╗",
            "      ██╔══██╗██║   ██║██║██║     ██╔══██╗",
            "      ██████╔╝██║   ██║██║██║     ██║  ██║",
            "      ██╔══██╗██║   ██║██║██║     ██║  ██║",
            "      ██████╔╝╚██████╔╝██║███████╗██████╔╝",
            "      ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝",
            "",
            "                  B U I L D   G U I L D",
            "",
            *quest_panel,
            "",
            "      > run start",
            "      > choose name + difficulty",
            "      > mentor: Mike waits beyond setup_",
            "",
            "      cache: cold     corpus: awake     ranker: ???",
            "✧       .        ✦      NULL      ???       ✦        .",
        ],
    )


def _build_compact_banner() -> list[str]:
    return _box(
        COMPACT_BANNER_WIDTH,
        [
            "✦     .        *        ✧        .       ✦",
            " /\\/\\       [404] HELP CENTER       /\\/\\",
            " ~~~~~~~~     corrupted index     ~~~~~~~~",
            "       SYS: MEMORY FAULT     IDX: ???",
            "             B U I L D   G U I L D",
            "       QUEST I: THE BROKEN HELP CENTER",
            "       Objective: Measure the baseline retriever.",
            "",
            "       > run start",
            "       > choose name + difficulty",
            "       > mentor: Mike waits beyond setup_",
            "",
            "✧     .       ✦       NULL       ???       ✦",
        ],
    )


def render_banner(width: int | None = None) -> Text:
    lines = _select_banner_lines(width)
    text = Text()
    for line in lines:
        _append_styled_line(text, line)
        text.append("\n")
    return text


def print_banner(console: Console | None = None) -> None:
    console = console or Console()
    console.print(render_banner(console.size.width), highlight=False, soft_wrap=True)


def _select_banner_lines(width: int | None) -> list[str]:
    if width is not None and width < BANNER_WIDTH:
        return COMPACT_BANNER_LINES
    return BANNER_LINES


def _box(width: int, content: list[str]) -> list[str]:
    inner_width = width - 2
    return [
        "╔" + ("═" * inner_width) + "╗",
        *[_box_line(line, inner_width) for line in content],
        "╚" + ("═" * inner_width) + "╝",
    ]


def _box_line(line: str, inner_width: int) -> str:
    clipped = set_cell_size(line, inner_width)
    padding = " " * max(0, inner_width - cell_len(clipped))
    return "║" + clipped + padding + "║"


def _inset_box(
    *,
    inner_width: int,
    inset: int,
    box_width: int,
    content: list[str],
) -> list[str]:
    if box_width > inner_width - inset:
        raise ValueError("Inset box does not fit inside banner")

    box_inner_width = box_width - 2
    prefix = " " * inset
    return [
        prefix + "╔" + ("═" * box_inner_width) + "╗",
        *[prefix + _inner_box_line(line, box_inner_width) for line in content],
        prefix + "╚" + ("═" * box_inner_width) + "╝",
    ]


def _inner_box_line(line: str, inner_width: int) -> str:
    clipped = set_cell_size(line, inner_width)
    padding = " " * max(0, inner_width - cell_len(clipped))
    return "║" + clipped + padding + "║"


BANNER_LINES = _build_full_banner()
COMPACT_BANNER_LINES = _build_compact_banner()


def _style_for_line(line: str) -> str:
    content = _line_content(line)
    if _is_big_build_line(content):
        return "bold bright_magenta"
    if "QUEST I" in line:
        return "bold yellow"
    if "Objective:" in line:
        return "bold green"
    if "run start" in line or "choose name" in line or "mentor:" in line:
        return "bold cyan"
    if "B U I L D" in line:
        return "bold bright_cyan"
    if (
        "[404]" in line
        or "corrupted" in line
        or "NULL" in line
        or "???" in line
        or "MEMORY FAULT" in line
        or "unstable" in line
    ):
        return "bright_red"
    if "╔" in line or "╚" in line or "║" in line:
        return "blue"
    return "white"


def _append_styled_line(text: Text, line: str) -> None:
    if _is_horizontal_border(line):
        text.append(line, style="blue")
        return

    if line.startswith("║") and line.endswith("║"):
        text.append(line[0], style="blue")
        content = line[1:-1]
        text.append(content, style=_style_for_line(line))
        text.append(line[-1], style="blue")
        return

    text.append(line, style=_style_for_line(line))


def _is_horizontal_border(line: str) -> bool:
    return line.startswith(("╔", "╚")) and line.endswith(("╗", "╝"))


def _line_content(line: str) -> str:
    if line.startswith("║") and line.endswith("║"):
        return line[1:-1]
    return line


def _is_big_build_line(line: str) -> bool:
    return any(marker in line for marker in ("██████", "██╔", "██║", "╚════"))
