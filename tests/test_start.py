import pytest
from rich.console import Console

from buildguild.start import configure_player, print_difficulty_intro


def test_configure_player_saves_name_and_default_easy(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"

    state = configure_player(name="Mira", path=state_path)

    assert state["player"]["name"] == "Mira"
    assert state["player"]["difficulty"] == "easy"
    assert state["player"]["setup_completed"] is True
    assert state_path.exists()


def test_configure_player_rejects_unknown_difficulty(tmp_path):
    state_path = tmp_path / ".buildguild" / "state.json"

    with pytest.raises(ValueError, match="Difficulty must be one of"):
        configure_player(name="Mira", difficulty="nightmare", path=state_path)


def test_difficulty_intro_uses_guidance_framing():
    console = Console(record=True, force_terminal=False)

    print_difficulty_intro(console)
    output = console.export_text()

    assert "How much guidance do you want on this quest?" in output
    assert "Apprentice mode" in output
    assert "Builder mode" in output
    assert "Expert mode" in output
    assert "Maya and Ari" not in output
