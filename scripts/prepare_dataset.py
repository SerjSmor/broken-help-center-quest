from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DIR = ROOT / "data" / "sample"
PROCESSED_DIR = ROOT / "data" / "processed"


def prepare_dataset() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for filename in ("documents.jsonl", "eval_questions.jsonl"):
        source = SAMPLE_DIR / filename
        target = PROCESSED_DIR / filename
        if not source.exists():
            raise FileNotFoundError(f"Missing sample data file: {source}")
        shutil.copyfile(source, target)
        print(f"Wrote {target}")


if __name__ == "__main__":
    prepare_dataset()
