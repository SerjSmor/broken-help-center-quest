from __future__ import annotations

from rich.console import Console


INSTRUCTIONS = """Maya report review is agent-mediated.

No command is needed for Maya to review the report.

Open Codex, Claude Code, or OpenCode and ask it to read:

skills/maya-tests-outputs.md

Maya should review:

analysis/baseline_report.md

She should check that the report includes metric definitions, baseline scores, positive examples, and negative failed examples.

If the report passes, update .buildguild/state.json:

quest_01.maya_report_review_passed = true
"""


def run() -> None:
    Console().print(INSTRUCTIONS)
