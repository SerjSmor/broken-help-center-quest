from __future__ import annotations

from rich.console import Console


ONBOARDING_INSTRUCTIONS = """Product onboarding is agent-mediated in this repo.

No command is needed to start Maya discovery.

Open Codex, Claude Code, or OpenCode and ask it to read:

skills/maya-product-lead.md

The agent should role-play Maya directly from that markdown file. It should not run uv or this onboarding command during product discovery.

Maya should always show the three hidden discovery checkboxes, reveal each checkbox label only after you ask a qualifying question, and help you clarify the task.

You can ask Maya for tips. Tips should nudge you without revealing exact checkbox labels or exact right questions.

When all three checkboxes are complete, the agent should create:

requirements/quest_01_product_requirements.md

Then update .buildguild/state.json while preserving existing keys:

Set quest_01.product_onboarding_completed = true.
Set quest_01.data_tour_completed = false.
Do not change quest_01.implementation_spec_completed.

Maya may create the product requirements artifact after discovery is complete.

The next step is the data tour:

uv run --extra dev invoke tour

Maya must not write the engineering ticket for you. You create it after product requirements and the data tour are complete.
"""


def run() -> None:
    Console().print(ONBOARDING_INSTRUCTIONS)
