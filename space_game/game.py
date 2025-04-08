from space_game.lang import TEXT
from pydantic import BaseModel
from typing import Any, Callable, Generator, Literal
from space_game.logging_util import logger
from space_game.location import Location
from functools import partial


TRANSITIONS = {
    ("planet", "planet"): TEXT["warp to"],
    ("planet", "ship"): TEXT["board"],
    ("ship", "planet"): TEXT["back to"],
    ("planet", "surface"): TEXT["beam down to"],
    ("surface", "planet"): TEXT["back to orbit of"],
}

CrewMember = Literal[
    "panda", "elephant", "hamster", "python", "pingu", "unicorn"
]


class Command(BaseModel):
    """
    Available action at a given moment in the game.
    Each command consists of a name that can be used as a label
    and a callback function that executes the command.
    Implements the Command pattern.
    """

    name: str
    callback: Callable

    def execute(self):
        logger.info(f"exceuting command '{self.name}'")
        self.callback()


class SpaceGame(BaseModel):
    """
    Manages the complete game mechanics
    """

    location: Location
    cargo: str = ""
    crew: list[CrewMember] = ["panda"]
    message: str = ""

    @property
    def solved(self) -> bool:
        """True when the game is finished"""
        return self.location.name == "Rainbow portal"

    def move_to(self, location: Location) -> None:
        """Callback function for move commands"""
        self.location = location
        self.message = f"moved to {self.location.name}"

    def load_cargo(self, resource: str) -> None:
        """Callback function for picking up items"""
        self.cargo = resource
        self.message = f"your ship loaded {self.cargo}"

    def get_commands(self) -> Generator[Command, Any, Any]:
        """
        Returns available commands at a given moment during the game.
        """
        for location in self.location.connected_locs:
            yield MoveCommand(game=self, target=location)
        for resource in self.location.resources:
            yield LoadCargoCommand(game=self, resource=resource)
        if self.location.active and self.location.trigger.action_name:
            yield Command(
                name=self.location.trigger.action_name,
                callback=partial(self.location.contact, self),
            )


class MoveCommand(Command):

    def __init__(self, game: SpaceGame, target: Location):
        source = game.location
        transition = (source.type, target.type)
        prefix = TRANSITIONS.get(transition, "move to")
        super().__init__(
            name=f"{prefix} {target.name}",
            callback=partial(game.move_to, target),
        )


class LoadCargoCommand(Command):

    def __init__(self, game: SpaceGame, resource: str):
        # TODO: introduce Literal type for resources
        super().__init__(
            name=f"{TEXT['collect']} {TEXT[resource]}",
            callback=partial(game.load_cargo, resource),
        )
