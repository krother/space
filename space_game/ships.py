from collections import namedtuple
from functools import partial

import arcade

from space_game.lang import TEXT
from space_game.views import FONT_SETTINGS, IMAGES


Command = namedtuple("Command", ("description", "action"))

TRANSITIONS = {
    ("planet", "planet"): TEXT["warp to"],
    ("planet", "ship"): TEXT["board"],
    ("ship", "planet"): TEXT["back to"],
    ("planet", "surface"): TEXT["beam down to"],
    ("surface", "planet"): TEXT["back to orbit of"],
}


class Spaceship:

    def __init__(self):
        self.location = None
        self.artifacts = 0
        self.cargo = ""

    def draw(self):
        arcade.draw_text(text=TEXT['cargo bay'], start_x=800, start_y=600, **FONT_SETTINGS)
        arcade.draw_text(text=TEXT['artifacts'], start_x=800, start_y=400, **FONT_SETTINGS)

        if self.cargo:
            IMAGES[self.cargo].draw_sized(870, 500, 128, 128)
        for i in range(1, self.artifacts + 1):
            IMAGES[f"artifact{i}"].draw_sized(730 + i * 140, 320, 96, 96)

    def move_to(self, location):
        self.location = location

    def load_cargo(self, resource):
        self.cargo = resource

    def __repr__(self):
        return f"<spaceship at: {self.location.name}>"

    def get_commands(self):
        commands = []
        # move
        for location in self.location.connections:
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
        if self.location.active and self.location.action_name:
            contact = Command(self.location.action_name, partial(self.location.contact, self))
            commands.append(contact)

        return commands
