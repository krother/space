
import base32_lib as base32
import duckdb
from duckdb import ConstraintException

import space_game.config
from space_game.location import Location
from space_game.models import GameState
from space_game.errors import DuplicateEntry, NoEntryFound


con = duckdb.connect()
con.sql("""
CREATE TABLE games (
    id VARCHAR(10) PRIMARY KEY,
    location VARCHAR(100),
    cargo VARCHAR(50),
    crew VARCHAR(100),
    )     
""")
con.sql("""
CREATE TABLE locations (
    game_id VARCHAR,
    name VARCHAR,
    description VARCHAR,
    image  VARCHAR,
    type  VARCHAR,
    connected_names VARCHAR,
    resources VARCHAR,
    active BOOLEAN,
    action_name VARCHAR,
    require_good VARCHAR,
    require_crew_member VARCHAR,
    activated_message VARCHAR,
    not_activated_message VARCHAR,
    activate_clear_cargo VARCHAR,
    activate_gain_crew_member VARCHAR,
    activate_gain_cargo VARCHAR,
    activate_gain_connection VARCHAR,
    deactivate BOOLEAN,
    
    PRIMARY KEY (game_id, name)
    )
""")

location_cache = {}


def create_game(location: str) -> GameState:
    game_id = base32.generate(length=10, checksum=True)
    game_state = GameState(
        game_id=game_id,
        location=location,
    )
    con.sql("INSERT INTO games VALUES (?,?,?,?)",
            params=game_state.serialize())

    copy_default_locations(game_state.game_id)
    return game_state


def get_game(game_id) -> GameState:
    cursor = con.sql("SELECT * FROM games WHERE id = ?", params=(game_id,))
    result = cursor.fetchall()
    if result:
        return GameState.deserialize(result[0])
    raise NoEntryFound(f"no such game: {game_id}")


def update_game(game_id: str, game_state: GameState) -> GameState:
    con.sql("UPDATE games SET id=?, location=?, cargo=?, crew=? WHERE id=?",
            params=game_state.serialize() + [game_id])
    return game_state


def add_location(location: Location) -> Location:
    try:
        con.sql("INSERT INTO locations VALUES ('default',?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                params=location.serialize())
        return location
    except ConstraintException:
        raise DuplicateEntry(f"location {location.name} already exists")


def get_location(game_id: str, name: str) -> Location:
    if (game_id, name) in location_cache:
        return location_cache[(game_id, name)]
    cursor = con.sql("SELECT * FROM locations WHERE game_id = ? AND name = ?", params=(game_id, name))
    result = cursor.fetchall()
    if result:
        loc = Location.deserialize(result[0][1:])
        location_cache[(game_id, name)] = loc
        return loc
    raise NoEntryFound(f"no entry for game {game_id} and location {name}")


def update_location(game_id: str, location: Location) -> Location:
    delete_location(game_id, location.name)
    data = [game_id] + location.serialize()
    con.sql("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            params=data
    )
    return location


def delete_location(game_id: str, name: str) -> None:
    con.sql("DELETE FROM locations WHERE game_id = ? AND name=?",
            params=(game_id, name))
    if (game_id, name) in location_cache:
        del location_cache[(game_id, name)]


def add_location_batch(locations: list[Location]) -> None:
    data = [
        ["default"] + loc.serialize()
        for loc in locations
    ]
    con.executemany("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    parameters=data)


def copy_default_locations(game_id: str):
    cursor = con.sql("SELECT * FROM locations WHERE game_id = 'default'")
    data = []
    for entry in cursor.fetchall():
        entry = list(entry)
        entry[0] = game_id
        data.append(entry)
    if data:
        con.executemany("INSERT INTO locations VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        parameters=data)
