
import json
import os

from space_game.config import BASE_PATH, LANG
from space_game.location import Location
from space_game.repository import add_location

DEFAULT_GALAXY = os.path.join(BASE_PATH, f"galaxy_{LANG}.json")


def ingest_galaxy():
    """Loads entire playing environment from a JSON file"""
    with open(DEFAULT_GALAXY, encoding="utf-8") as f:
        for entry in json.load(f):
            loc = Location(**entry)
            add_location(loc)


if __name__ == "__main__":
    ingest_galaxy()
