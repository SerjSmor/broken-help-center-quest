from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from buildguild.state import load_state


QUEST_KEY = "quest_01"
PRODUCT_REQUIREMENTS_PATH = Path("requirements/quest_01_product_requirements.md")
DATA_TOUR_NOTES_PATH = Path("notes/quest_01_data_tour.md")
IMPLEMENTATION_SPEC_PATH = Path("specs/quest_01_implementation_spec.md")
REPORT_PATH = Path("reports/baseline_report.md")
IMPLEMENTATION_FILES = [
    Path("app/ask.py"),
    Path("app/rag.py"),
    Path("app/retrieval.py"),
    Path("evals/run_baseline.py"),
    Path("evals/metrics.py"),
]


@dataclass(frozen=True)
class Status:
    stage: str
    completed: list[str]
    missing: list[str]
    next_action: str


def inspect_status() -> Status:
    state = load_state()
    quest = state.get(QUEST_KEY, {})

    onboarding_done = bool(quest.get("product_onboarding_completed"))
    product_requirements_found = PRODUCT_REQUIREMENTS_PATH.exists()
    data_tour_notes_found = DATA_TOUR_NOTES_PATH.exists()
    data_tour_completed = bool(quest.get("data_tour_completed"))
    implementation_spec_found = IMPLEMENTATION_SPEC_PATH.exists()
    implementation_spec_completed = bool(quest.get("implementation_spec_completed"))
    implementation_complete = all(path.exists() for path in IMPLEMENTATION_FILES)
    report_found = REPORT_PATH.exists()
    maya_report_review_passed = bool(quest.get("maya_report_review_passed"))

    completed: list[str] = []
    missing: list[str] = []

    _record(completed, missing, onboarding_done, "Product onboarding completed")
    _record(completed, missing, product_requirements_found, "Product requirements found")
    _record(completed, missing, data_tour_notes_found, "Data tour notes found")
    _record(completed, missing, data_tour_completed, "Data tour completed")
    _record(completed, missing, implementation_spec_found, "Implementation spec found")
    _record(completed, missing, implementation_spec_completed, "Implementation spec completed")
    _record(completed, missing, implementation_complete, "Baseline implementation detected")
    _record(completed, missing, report_found, "Baseline report found")
    _record(completed, missing, maya_report_review_passed, "Maya report review passed")

    if not onboarding_done or not product_requirements_found:
        return Status(
            stage="Product discovery",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/maya-product-lead.md, complete the four discovery checkboxes, and create requirements/quest_01_product_requirements.md.",
        )
    if not data_tour_notes_found or not data_tour_completed:
        return Status(
            stage="Tour the data",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/ari-data-guide.md, inspect the dataset, write notes/quest_01_data_tour.md, and set quest_01.data_tour_completed = true.",
        )
    if not implementation_spec_found or not implementation_spec_completed:
        return Status(
            stage="Write implementation spec",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/write-technical-spec.md and create specs/quest_01_implementation_spec.md.",
        )
    if not implementation_complete:
        return Status(
            stage="Implement baseline evaluation",
            completed=completed,
            missing=missing,
            next_action='Implement: python -m app.ask "How do I connect a domain?" and python -m evals.run_baseline',
        )
    if not report_found:
        return Status(
            stage="Run baseline evaluation",
            completed=completed,
            missing=missing,
            next_action="Run: python -m evals.run_baseline",
        )
    if not maya_report_review_passed:
        return Status(
            stage="Maya report review",
            completed=completed,
            missing=missing,
            next_action="Ask your coding agent to use skills/maya-tests-outputs.md so Maya can review reports/baseline_report.md.",
        )
    return Status(
        stage="Quest complete",
        completed=completed,
        missing=missing,
        next_action="Quest 1 complete. You have a baseline report. Quest 2 can optimize from here.",
    )


def print_status(console: Console | None = None) -> None:
    console = console or Console()
    status = inspect_status()
    console.print("[bold]BuildGuild Status[/bold]")
    console.print("Current quest:")
    console.print("Quest 1 - The Bot Works. Nobody Knows If It Is Good.")
    console.print(f"Stage: {status.stage}")
    console.print("Progress:")
    for item in status.completed:
        console.print(f"\\[x] {item}")
    for item in status.missing:
        console.print(f"\\[ ] {item}")
    console.print("Next action:")
    console.print(status.next_action)


def _record(completed: list[str], missing: list[str], condition: bool, label: str) -> None:
    if condition:
        completed.append(label)
    else:
        missing.append(label)
