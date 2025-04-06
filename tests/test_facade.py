# code from step 8 in refactoring.md

from space_game.facade import start_game, execute_command, GameData


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
