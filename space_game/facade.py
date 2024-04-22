import os
from typing import Optional

from pydantic import BaseModel

from space_game.lang import LANG
from space_game.location import create_galaxy
from space_game.game import SpaceGame
from space_game.config import BASE_PATH


class LocationData(BaseModel):
    name: str
    image: str
    description: str


class GameData(BaseModel):
    game_id: str
    location: LocationData
    cargo: Optional[str] = None
    crew: list[str] = ["panda"]
    commands: list[str]
    message: Optional[str] = None
    solved: bool  # added, was missing in the original facade, but gui required it

GAMES = {}  # TODO: move this to a database asap (SQLModel)


def _get_game_data(game_id, game):
    return GameData( # data exchange object
        game_id=game_id,
        location=LocationData(
            name=game.location.name,
            image=game.location.image,
            description=game.location.description,
        ),
        cargo=game.cargo,
        crew=[str(s) for s in game.crew],
        commands=[cmd.name for cmd in game.get_commands()],
        message=game.message,
        solved=game.solved,  # added
    )


def start_game() -> GameData:
    galaxy = create_galaxy(os.path.join(BASE_PATH, f"galaxy_{LANG}.json"))
    game = SpaceGame(location=galaxy["Pandalor"])  # core business object
    game_id = "1"
    GAMES[game_id] = game
    return _get_game_data(game_id, game)
    
    
def execute_command(game_id: str, command: str) -> GameData:
    """call the callback function given by 'command'"""
    game = GAMES[game_id]
    for cmd in game.get_commands():
        if cmd.name == command:
            cmd.callback()
            break
    return _get_game_data(game_id, game)
    








