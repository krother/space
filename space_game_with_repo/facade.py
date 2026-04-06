
from space_game.repository import (
    create_game,
    get_game,
    update_game,
    update_location,
)
from space_game.ingest import ingest_galaxy
from space_game.game import SpaceGame
from space_game.dto import GameData, LocationData
from space_game.repository import get_location


def _get_game_data(game_id, game: SpaceGame) -> GameData:
    return GameData(
        game_id=game_id,
        location=LocationData(
            name=game.location.name,
            image=game.location.image,
            description=game.location.description,
        ),
        cargo=game.cargo,
        crew=game.crew,
        commands=[cmd.name for cmd in game.get_commands()],
        message=game.message,
        solved=game.solved,
    )


def start_game() -> GameData:
    state = create_game(location="Pandalor")
    game = SpaceGame(state, get_location)
    return _get_game_data(state.game_id, game)


def execute_command(game_id: str, command: str) -> GameData:
    """call the callback function given by 'command'"""
    state = get_game(game_id)
    game = SpaceGame(state, get_location)
    for cmd in game.get_commands():
        if cmd.name == command:
            cmd.callback()
            #if game.location.name == "Adalov":
            #    import pdb;pdb.set_trace()
            update_game(game_id, game.get_state())
            update_location(game_id, game.location)
            break
    return _get_game_data(game_id, game)


#ingest_galaxy()
