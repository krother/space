import os

import base32_lib as base32
from pymongo import MongoClient

import space_game.config
from space_game.location import Location
from space_game.models import GameState
from space_game.errors import DuplicateEntry, NoEntryFound


conn = MongoClient()
db = conn.get_database(os.getenv("MONGODB_DATABASE"))


def create_game(location: str) -> GameState:
    game_id = base32.generate(length=10, checksum=True)
    game_state = GameState(
        game_id=game_id,
        location=location,
    )
    j = game_state.model_dump()
    copy_default_locations(game_id)
    result = db.games.insert_one(j)
    # result.inserted_id
    return game_state


def get_game(game_id) -> GameState:
    result = db.games.find_one({"game_id": game_id})
    if result:
        return GameState(**result)  # includes database id
    raise NoEntryFound(f"no game with id {game_id}")


def update_game(game_id: str, game_state: GameState) -> GameState:
    j = game_state.model_dump()
    db.games.update_one({"game_id": game_id}, {"$set": j})
    return game_state


def get_location(game_id: str, name: str) -> Location:
    result = db.locations.find_one({"game_id": game_id, "name": name})
    if result:
        return Location(**result)  # includes database id
    raise NoEntryFound(f"no entry for game {game_id} and location {name}")


def add_location(location: Location) -> Location:
    if db.locations.find_one({"game_id": "default", "name": location.name}):
        raise DuplicateEntry(f"location '{location.name}' already exists")
    j = location.model_dump()
    j["game_id"] = "default"
    db.locations.insert_one(j)
    return location


def update_location(game_id: str, location: Location) -> Location:
    j = location.model_dump()
    db.locations.update_one({"game_id": game_id, "name": location.name}, {"$set": j})
    return location


def delete_location(game_id: str, name: str) -> None:
    db.locations.delete_one({"game_id": game_id, "name": name})


def add_location_batch(locations: list[Location]) -> list[str]:
    result = []
    data = []
    for loc in locations:
        j = loc.model_dump()
        j["game_id"] = "default"
        data.append(j)
        result.append(loc.name)
    db.locations.insert_many(data)
    return result


def copy_default_locations(game_id: str):
    docs = []
    for d in db.locations.find({"game_id": "default"}):
        d["game_id"] = game_id
        del d["_id"]
        docs.append(d)
    if docs:
        db.locations.insert_many(docs)
