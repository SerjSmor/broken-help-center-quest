from __future__ import annotations

import json
from pathlib import Path
from typing import Any


QUEST_KEY = "quest_01"
STATE_PATH = Path(".buildguild/state.json")
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


def build_status_line(root: Path) -> str:
    checks = inspect_checks(root)
    completed = sum(1 for value in checks.values() if value)
    total = len(checks)

    stage, next_hint = resolve_stage(checks)
    return f"BuildGuild Q1 [{completed}/{total}] {stage} -> {next_hint}"


def inspect_checks(root: Path) -> dict[str, bool]:
    quest = load_quest_state(root)
    return {
        "product_onboarding": bool(quest.get("product_onboarding_completed")),
        "product_requirements": (root / PRODUCT_REQUIREMENTS_PATH).exists(),
        "data_tour_notes": (root / DATA_TOUR_NOTES_PATH).exists(),
        "data_tour": bool(quest.get("data_tour_completed")),
        "implementation_spec_file": (root / IMPLEMENTATION_SPEC_PATH).exists(),
        "implementation_spec_done": bool(quest.get("implementation_spec_completed")),
        "implementation": all((root / path).exists() for path in IMPLEMENTATION_FILES),
        "baseline_report": (root / REPORT_PATH).exists(),
        "maya_review": bool(quest.get("maya_report_review_passed")),
    }


def resolve_stage(checks: dict[str, bool]) -> tuple[str, str]:
    if not checks["product_onboarding"] or not checks["product_requirements"]:
        return "Product discovery", "/quest-status"
    if not checks["data_tour_notes"] or not checks["data_tour"]:
        return "Tour data", "ari-data-guide"
    if not checks["implementation_spec_file"] or not checks["implementation_spec_done"]:
        return "Write tech spec", "write-technical-spec"
    if not checks["implementation"]:
        return "Implement baseline", "app + evals"
    if not checks["baseline_report"]:
        return "Run evaluation", "baseline report"
    if not checks["maya_review"]:
        return "Maya review", "maya-tests-outputs"
    return "Complete", "Quest 2 ready"


def load_quest_state(root: Path) -> dict[str, Any]:
    state_path = root / STATE_PATH
    if not state_path.exists():
        return {}

    try:
        data = json.loads(state_path.read_text())
    except json.JSONDecodeError:
        return {}

    quest = data.get(QUEST_KEY, {})
    if isinstance(quest, dict):
        return quest
    return {}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def main() -> None:
    print(build_status_line(repo_root()))


if __name__ == "__main__":
    main()
