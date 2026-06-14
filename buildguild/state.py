from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DEFAULT_STATE: dict[str, Any] = {
    "quest_01": {
        "product_onboarding_completed": False,
        "data_tour_completed": False,
        "implementation_spec_completed": False,
        "maya_report_review_passed": False,
    }
}

STATE_PATH = Path(".buildguild/state.json")


def load_state(path: Path = STATE_PATH) -> dict[str, Any]:
    if not path.exists():
        save_state(DEFAULT_STATE.copy(), path)
        return json.loads(json.dumps(DEFAULT_STATE))

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        data = {}

    return _with_defaults(data)


def save_state(state: dict[str, Any], path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def update_quest_state(quest_key: str, updates: dict[str, Any], path: Path = STATE_PATH) -> dict[str, Any]:
    state = load_state(path)
    quest_state = state.setdefault(quest_key, {})
    quest_state.update(updates)
    save_state(state, path)
    return state


def _with_defaults(data: dict[str, Any]) -> dict[str, Any]:
    state = json.loads(json.dumps(DEFAULT_STATE))
    for key, value in data.items():
        if isinstance(value, dict) and isinstance(state.get(key), dict):
            state[key].update(value)
        else:
            state[key] = value
    return state
