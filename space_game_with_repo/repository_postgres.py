
import os

import base32_lib as base32
from sqlalchemy import (
    create_engine,
    Table,
    MetaData,
    Column,
    String,
    Boolean,
    select,
    text,
)
from sqlalchemy.exc import IntegrityError, ProgrammingError

import space_game.config
from space_game.location import Location
from space_game.models import GameState
from space_game.errors import DuplicateEntry, NoEntryFound


metadata = MetaData()

games = Table(
    "games",
    metadata,
    Column("id", String(10), primary_key=True),
    Column("location", String(100)),
    Column("cargo", String(50)),
    Column("crew", String(100)),
)

locations = Table(
    "locations",
    metadata,
    Column("game_id", String, primary_key=True),
    Column("name", String, primary_key=True),
    Column("description", String),
    Column("image", String),
    Column("type", String),
    Column("connected_names", String),
    Column("resources", String),
    Column("active", Boolean),
    Column("action_name", String),
    Column("require_good", String),
    Column("require_crew_member", String),
    Column("activated_message", String),
    Column("not_activated_message", String),
    Column("activate_clear_cargo", String),
    Column("activate_gain_crew_member", String),
    Column("activate_gain_cargo", String),
    Column("activate_gain_connection", String),
    Column("deactivate", Boolean),
)

dbname=os.getenv("POSTGRES_DATABASE")
connection=os.getenv("POSTGRES_CONNECTION")

# create database if it does not exist
try:
    pg = create_engine(
        f"postgresql+psycopg2://{connection}/postgres",
        isolation_level="AUTOCOMMIT"
    )
    with pg.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {dbname}"))
except ProgrammingError:
    pass

engine = create_engine(f"postgresql+psycopg2://{connection}/{dbname}", echo=False)

metadata.create_all(engine)

GAMES_KEYS = ["id", "location", "cargo", "crew"]
LOC_KEYS = [
    "game_id", "name", "description", "image", "type", "connected_names",
    "resources", "active", "action_name", "require_good", "require_crew_member",
    "activated_message", "not_activated_message", "activate_clear_cargo",
    "activate_gain_crew_member", "activate_gain_cargo", "activate_gain_connection",
    "deactivate",
]


def create_game(location: str) -> GameState:
    game_id = base32.generate(length=10, checksum=True)
    game_state = GameState(
        game_id=game_id,
        location=location,
    )
    with engine.begin() as con:
        con.execute(games.insert().values(**dict(zip(GAMES_KEYS, game_state.serialize()))))

    copy_default_locations(game_state.game_id)
    return game_state


def get_game(game_id) -> GameState:
    with engine.connect() as con:
        result = con.execute(select(games).where(games.c.id == game_id)).fetchall()
    if result:
        return GameState.deserialize(result[0])
    raise NoEntryFound(f"no such game: {game_id}")


def update_game(game_id: str, game_state: GameState) -> GameState:
    with engine.begin() as con:
        con.execute(
            games.update().where(games.c.id == game_id)
            .values(**dict(zip(GAMES_KEYS, game_state.serialize())))
        )
    return game_state


def add_location(location: Location) -> Location:
    row = dict(zip(LOC_KEYS, ["default"] + location.serialize()))
    try:
        with engine.begin() as con:
            con.execute(locations.insert().values(**row))
        return location
    except IntegrityError:
        raise DuplicateEntry(f"location {location.name} already exists")


def get_location(game_id: str, name: str) -> Location:
    with engine.connect() as con:
        result = con.execute(
            select(locations).where(locations.c.game_id == game_id, locations.c.name == name)
        ).fetchall()
    if result:
        return Location.deserialize(result[0][1:])
    raise NoEntryFound(f"no entry for game {game_id} and location {name}")


def update_location(game_id: str, location: Location) -> Location:
    delete_location(game_id, location.name)
    row = dict(zip(LOC_KEYS, [game_id] + location.serialize()))
    with engine.begin() as con:
        con.execute(locations.insert().values(**row))
    return location


def delete_location(game_id: str, name: str) -> None:
    with engine.begin() as con:
        con.execute(
            locations.delete().where(locations.c.game_id == game_id, locations.c.name == name)
        )


def add_location_batch(location_list: list[Location]) -> None:
    data = [
        dict(zip(LOC_KEYS, ["default"] + loc.serialize()))
        for loc in location_list
    ]
    with engine.begin() as con:
        con.execute(locations.insert(), data)


def copy_default_locations(game_id: str):
    with engine.connect() as con:
        rows = con.execute(
            select(locations).where(locations.c.game_id == "default")
        ).fetchall()
    data = []
    for entry in rows:
        entry = list(entry)
        entry[0] = game_id
        data.append(dict(zip(LOC_KEYS, entry)))
    if data:
        with engine.begin() as con:
            con.execute(locations.insert(), data)
