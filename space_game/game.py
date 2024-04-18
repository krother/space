from functools import partial
from typing import Callable, Optional, Literal

import arcade
from pydantic import BaseModel

from space_game.lang import TEXT
from space_game.views import FONT_SETTINGS, IMAGES
from space_game.location import Location


TRANSITIONS = {
    ("planet", "planet"): TEXT["warp to"],
    ("planet", "ship"): TEXT["board"],
    ("ship", "planet"): TEXT["back to"],
    ("planet", "surface"): TEXT["beam down to"],
    ("surface", "planet"): TEXT["back to orbit of"],
}

CrewMember = Literal["panda", "elephant", "hamster", "python", "pingu", "unicorn"]


class Command(BaseModel):
    """
    Available action at a given moment in the game.
    Each command consists of a name that can be used as a label
    and a callback function that executes the command.
    Implements the Command pattern.
    """

    name: str
    callback: Callable


class SpaceGame(BaseModel):
    """
    Manages the complete game mechanics
    """

    location: Optional[Location] = None
    cargo: str = ""
    crew: list[CrewMember] = ["panda"]
    message: str = ""

    @property
    def solved(self) -> bool:
        """True when the game is finished"""
        location = self.location
        return location.name == "Rainbow portal"

    def draw(self) -> None:
        """Draws the players inventory"""
        arcade.draw_text(text=TEXT['cargo bay'], start_x=800, start_y=600, **FONT_SETTINGS)
        arcade.draw_text(text=TEXT['crew'], start_x=800, start_y=400, **FONT_SETTINGS)

        if self.cargo:
            IMAGES[self.cargo].draw_sized(870, 500, 128, 128)
        for i, c in enumerate(self.crew):
            IMAGES[c].draw_sized(870 + i * 120, 320, 96, 96)

    def move_to(self, location: Location) -> None:
        """Callback function for move commands"""
        self.location = location
        self.message = f"moved to {self.location.name}"

    def load_cargo(self, resource: str) -> None:
        """Callback function for picking up items"""
        self.cargo = resource
        self.message = f"your ship loaded {self.cargo}"

    def get_commands(self) -> list[Command]:
        """
        Returns available commands at a given moment during the game.
        """
        commands = []
        # move
        for location in self.location.connected_locs:
            transition = (self.location.type, location.type)
            prefix = TRANSITIONS.get(transition, "move to")
            move = Command(name=f"{prefix} {location.name}", callback=partial(self.move_to, location))
            commands.append(move)
        # load goods
        for resource in self.location.resources:
            load = Command(
                name=f"{TEXT['collect']} {TEXT[resource]}",
                callback=partial(self.load_cargo, resource),
            )
            commands.append(load)
        # talk to people
        if self.location.active and self.location.trigger.action_name:
            contact = Command(name=self.location.trigger.action_name, callback=partial(self.location.contact, self))
            commands.append(contact)

        return commands
