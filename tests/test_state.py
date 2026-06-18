import json

from buildguild.state import load_state, update_quest_state


def test_load_state_creates_default_state(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"

    state = load_state(state_path)

    assert state["quest_01"]["product_onboarding_completed"] is False
    assert state["quest_01"]["implementation_spec_completed"] is False
    assert state["quest_01"]["maya_report_review_passed"] is False
    assert state_path.exists()


def test_update_quest_state_preserves_unknown_keys(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"
    state_path.parent.mkdir()
    state_path.write_text(
        json.dumps(
            {
                "quest_01": {"implementation_spec_completed": False},
                "custom": {"keep": True},
            }
        )
    )

    state = update_quest_state(
        "quest_01",
        {"product_onboarding_completed": True},
        state_path,
    )

    assert state["quest_01"]["product_onboarding_completed"] is True
    assert state["quest_01"]["implementation_spec_completed"] is False
    assert state["quest_01"]["maya_report_review_passed"] is False
    assert state["custom"]["keep"] is True
