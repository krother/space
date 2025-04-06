import json
import os

from space_game.config import BASE_PATH
from space_game.errors import GalaxyConstructionError
from space_game.location import Location


DEFAULT_GALAXY = os.path.join(BASE_PATH, "galaxy_EN.json")


class GalaxyGraph:

    @staticmethod
    def create_galaxy(filename=DEFAULT_GALAXY):
        """Loads entire playing environment from a JSON file"""
        j = json.load(open(filename, encoding="utf-8"))
        galaxy = {}
        locs = [Location(galaxy=galaxy, **loc) for loc in j]
        # TODO: think about mutable parameter galaxy
        # builds connection graph
        for location in locs:
            for target_name in location.connected_names:
                target = galaxy.get(target_name)
                if target is None:
                    raise GalaxyConstructionError(
                        f"connection not found when building galaxy"
                        f"for '{target_name}'"
                    )
                location.add_connection(target)

        return galaxy
