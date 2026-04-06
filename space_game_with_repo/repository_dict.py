
from copy import deepcopy

import base32_lib as base32

from space_game.location import Location
from space_game.models import GameState
from space_game.errors import DuplicateEntry, NoEntryFound

galaxies = {}
games = {}


def create_game(location: str) -> GameState:
    game_id = base32.generate(length=10, checksum=True)
    game_state = GameState(
        game_id=game_id,
        location=location,
    )
    games[game_id] = game_state

    # copy all locations
    galaxies[game_id] = {}
    for name in galaxies.get("default", []):
        galaxies[game_id][name] = deepcopy(galaxies["default"][name])
    return game_state


def get_game(game_id) -> GameState:
    if game_id in games:
        return games[game_id]
    raise NoEntryFound(f"no game with id {game_id}")


def update_game(game_id: str, game_state: GameState) -> GameState:
    games[game_id] = game_state
    return game_state


def get_location(game_id: str, name: str) -> Location:
    if game_id not in galaxies or name not in galaxies[game_id]:
        raise NoEntryFound(f"planet {name} not found for game {game_id}")    
    return galaxies[game_id][name]


def add_location(location: Location) -> Location:
    galaxies.setdefault("default", {})
    if location.name in galaxies["default"]:
        raise DuplicateEntry(f"location '{location.name}' already exists")
    galaxies["default"][location.name] = location
    return location


def update_location(game_id: str, location: Location):
    pass


def delete_location(game_id: str, name: str) -> None:
    if game_id in galaxies and name in galaxies[game_id]:
        del galaxies[game_id][name]


def add_location_batch(locations: list[Location]) -> list[str]:
    result = []
    for loc in locations:
        add_location(loc)
        result.append(loc.name)
    return result
