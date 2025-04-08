import os

from space_game.facade import start_game, execute_command, GameData


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_PATH, "test_data")
MINI_GALAXY = os.path.join(TEST_DATA_PATH, "mini_galaxy.json")

def test_load_galaxy():
    g = start_game(MINI_GALAXY)
    g = execute_command(g.game_id, g.commands[0])
    assert g.location.name == "Space Port"

def test_start_game():
    """game data is created"""
    assert isinstance(start_game(), GameData)


def test_execute_command():
    """command modifies data"""
    game = start_game()
    command = game.commands[0]
    game_new = execute_command(game.game_id, command)
    assert game_new.game_id == game.game_id
    assert game_new != game
