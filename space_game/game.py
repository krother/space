from collections import namedtuple
from functools import partial
from typing import Optional, Literal

import arcade
from pydantic import BaseModel

from space_game.lang import TEXT
from space_game.views import FONT_SETTINGS, IMAGES
from space_game.location import Location


Command = namedtuple("Command", ("description", "action"))

TRANSITIONS = {
    ("planet", "planet"): TEXT["warp to"],
    ("planet", "ship"): TEXT["board"],
    ("ship", "planet"): TEXT["back to"],
    ("planet", "surface"): TEXT["beam down to"],
    ("surface", "planet"): TEXT["back to orbit of"],
}

CrewMember = Literal["panda", "elephant", "hamster", "python", "pingu", "unicorn"]


class SpaceGame(BaseModel):

    game_id: str
    location: Optional[Location] = None
    cargo: str = ""
    crew: list[CrewMember] = ["panda"]

    @property
    def solved(self):
        location = self.location
        return location.name == "Alien Space Station" and not location.active

    def draw(self):
        arcade.draw_text(text=TEXT['cargo bay'], start_x=800, start_y=600, **FONT_SETTINGS)
        arcade.draw_text(text=TEXT['crew'], start_x=800, start_y=400, **FONT_SETTINGS)

        if self.cargo:
            IMAGES[self.cargo].draw_sized(870, 500, 128, 128)
        for i, c in enumerate(self.crew):
            IMAGES[c].draw_sized(870 + i * 120, 320, 96, 96)

    def move_to(self, location):
        self.location = location

    def load_cargo(self, resource):
        self.cargo = resource

    def get_commands(self):
        commands = []
        # move
        for location in self.location.connected_locs:
            transition = (self.location.type, location.type)
            prefix = TRANSITIONS.get(transition, "move to")
            move = Command(f"{prefix} {location.name}", partial(self.move_to, location))
            commands.append(move)
        # load goods
        for resource in self.location.resources:
            load = Command(
                f"{TEXT['collect']} {TEXT[resource]}",
                partial(self.load_cargo, resource),
            )
            commands.append(load)
        # talk to people
        if self.location.active and self.location.trigger.action_name:
            contact = Command(self.location.trigger.action_name, partial(self.location.contact, self))
            commands.append(contact)

        return commands
