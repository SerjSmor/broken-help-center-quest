from __future__ import annotations

import argparse
from pathlib import Path

from buildguild.state import DEFAULT_STATE, save_state


ROOT = Path(__file__).resolve().parents[1]
CONFIRMATION = "RESET_QUEST_01"
OUTPUT_PATHS = [
    Path("analysis/article_type_frequency.csv"),
    Path("analysis/quest_01_product_requirements.md"),
    Path("analysis/quest_01_implementation_spec.md"),
    Path("analysis/baseline_report.md"),
    Path("analysis/quest_01_eda.py"),
    Path("analysis/rag.py"),
    Path("analysis/ask.py"),
    Path("analysis/run_baseline.py"),
    Path("analysis/metrics.py"),
]
EMPTY_OUTPUT_DIRS = [
    Path("analysis"),
]


def restart_quest(root: Path = ROOT) -> list[Path]:
    removed: list[Path] = []
    for relative_path in OUTPUT_PATHS:
        path = root / relative_path
        if path.exists():
            path.unlink()
            removed.append(relative_path)

    for relative_path in EMPTY_OUTPUT_DIRS:
        path = root / relative_path
        if path.exists() and path.is_dir() and not any(path.iterdir()):
            path.rmdir()
            removed.append(relative_path)

    save_state(DEFAULT_STATE, root / ".buildguild" / "state.json")
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset BuildGuild Quest 1 outputs and state.")
    parser.add_argument(
        "--confirm",
        required=True,
        help=f"Required confirmation token. Use: {CONFIRMATION}",
    )
    args = parser.parse_args()

    if args.confirm != CONFIRMATION:
        raise SystemExit(f"Refusing to reset. Pass --confirm {CONFIRMATION}")

    removed = restart_quest()
    print("Quest 1 reset complete.")
    if removed:
        print("Removed:")
        for path in removed:
            print(f"- {path}")
    else:
        print("No quest output files were present.")
    print("State reset: .buildguild/state.json")
    print("Settings preserved: .buildguild/settings.json")


if __name__ == "__main__":
    main()
