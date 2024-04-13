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


class Location(BaseModel):
    """
    Planets, spaceships and special places on the ground
    """

    name: str
    description: str
    image: str
    type: str = "planet"
    connected_names: list[str]
    connected_locs: list["Location"] = []
    resources: list[str] = []
    active: bool = True
    trigger: ActionTrigger

    def __repr__(self):
        return f"<{self.name}: {self.type}; provides {self.resources}; {self.active}>"

    def draw(self):
        IMAGES[self.image].draw_sized(150, 850, 200, 200)
        arcade.draw_text(text=self.name, start_x=300, start_y=950, bold=True, **FONT_SETTINGS)
        arcade.draw_text(text=self.description, start_x=300, start_y=900, multiline=True, width=600, **FONT_SETTINGS)

    def add_connection(self, location):
        self.connected_locs.append(location)

    def activate(self, ship):
        self.active = False
        if self.trigger.activate_clear_cargo:
            ship.cargo = ""
        if self.trigger.activate_gain_crew_member:
            ship.crew.append(self.trigger.activate_gain_crew_member)

    def contact(self, ship):
        if self.active:
            if (self.trigger.require_good is None or (ship.cargo == self.trigger.require_good)) and (
                self.trigger.require_crew_member is None or (self.trigger.require_crew_member in ship.crew)
            ):
                self.activate(ship)
                return self.trigger.activated_message
            return self.trigger.not_activated_message
        return ""


def create_galaxy(fn=DEFAULT_GALAXY):
    """Loads entire playing environment from a JSON file"""
    j = json.load(open(fn, encoding="utf-8"))
    galaxy = [Location(**loc) for loc in j]

    # builds connection graph
    for location in galaxy:
        location.connected_locs = []
        for targetname in location.connected_names:
            target = None
            for p in galaxy:
                if p.name == targetname:
                    target = p
            if target is None:
                raise ValueError(f"connection not found when building galaxy for '{targetname}'")
            location.add_connection(target)

    return galaxy
