import json

from buildguild.achievements import complete_quest_1, unlock_achievement


def test_unlock_achievement_adds_xp_once(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"

    state = unlock_achievement("product_hunch", state_path)
    state = unlock_achievement("product_hunch", state_path)

    assert state["player"]["achievements"]["product_hunch"] is True
    assert state["player"]["xp"] == 100


def test_complete_quest_1_unlocks_final_badge_and_levels_player(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"
    state_path.parent.mkdir()
    state_path.write_text(
        json.dumps(
            {
                "player": {
                    "level": 1,
                    "title": "New Builder",
                    "xp": 250,
                    "achievements": {
                        "product_hunch": True,
                        "data_intuition": True,
                    },
                }
            }
        )
    )

    state = complete_quest_1(state_path)

    assert state["player"]["level"] == 2
    assert state["player"]["title"] == "Baseline Builder"
    assert state["player"]["xp"] == 500
    assert state["player"]["achievements"]["baseline_before_optimization"] is True
