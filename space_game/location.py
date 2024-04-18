import json
import os
from typing import Optional

import arcade
from pydantic import BaseModel

from space_game.views import BASE_PATH, FONT_SETTINGS, IMAGES


DEFAULT_GALAXY = os.path.join(BASE_PATH, "galaxy_EN.json")


class ActionTrigger(BaseModel):
    """
    Conditions and effects of puzzles at a location
    """

    action_name: Optional[str] = None
    require_good: Optional[str] = None
    require_crew_member: Optional[str] = None
    activated_message: Optional[str] = None
    not_activated_message: Optional[str] = None
    activate_clear_cargo: Optional[str] = None
    activate_gain_crew_member: Optional[str] = None
    activate_gain_cargo: Optional[str] = None
    activate_gain_connection: Optional[str] = None
    deactivate: bool = True


class Location(BaseModel):
    """
    Planets, spaceships and special places on the ground
    """

    galaxy: dict
    name: str
    description: str
    image: str
    type: str = "planet"
    connected_names: list[str]
    connected_locs: list["Location"] = []
    resources: list[str] = []
    active: bool = True
    trigger: ActionTrigger

    def __repr__(self) -> str:
        return f"<{self.name}: {self.type}; provides {self.resources}; {self.active}>"

    def add_connection(self, location) -> None:
        self.connected_locs.append(location)

    def activate(self, game):
        if self.trigger.deactivate:
            self.active = False
        if self.trigger.activate_clear_cargo:
            game.cargo = ""
        if self.trigger.activate_gain_crew_member:
            game.crew.append(self.trigger.activate_gain_crew_member)
        if self.trigger.activate_gain_cargo:
            game.cargo = self.trigger.activate_gain_cargo
        if self.trigger.activate_gain_connection:
            self.connected_names.append(self.trigger.activate_gain_connection)
            self.connected_locs.append(self.galaxy[self.trigger.activate_gain_connection])

    def contact(self, game):
        if self.active:
            if (self.trigger.require_good is None or (game.cargo == self.trigger.require_good)) and (
                self.trigger.require_crew_member is None or (self.trigger.require_crew_member in game.crew)
            ):
                self.activate(game)
                game.message = self.trigger.activated_message
            else:
                game.message = self.trigger.not_activated_message


def create_galaxy(fn=DEFAULT_GALAXY):
    """Loads entire playing environment from a JSON file"""
    j = json.load(open(fn, encoding="utf-8"))
    galaxy = {}

    locs = [Location(galaxy=galaxy, **loc) for loc in j]
    # builds connection graph
    for location in locs:
        location.galaxy = galaxy
        galaxy[location.name] = location
        location.connected_locs = []
        for targetname in location.connected_names:
            target = None
            for p in locs:
                if p.name == targetname:
                    target = p
            if target is None:
                raise ValueError(f"connection not found when building galaxy for '{targetname}'")
            location.add_connection(target)

    return galaxy
