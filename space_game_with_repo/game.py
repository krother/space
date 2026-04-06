from functools import partial
from typing import Callable

from pydantic import BaseModel

from space_game.models import GameState, CrewMember
from space_game.lang import TEXT
from space_game.location import Location


TRANSITIONS = {
    ("planet", "planet"): TEXT["warp to"],
    ("planet", "ship"): TEXT["board"],
    ("ship", "planet"): TEXT["back to"],
    ("planet", "surface"): TEXT["beam down to"],
    ("surface", "planet"): TEXT["back to orbit of"],
}


class Command(BaseModel):
    """
    Available action at a given moment in the game.
    Each command consists of a name that can be used as a label
    and a callback function that executes the command.
    Implements the Command pattern.
    """
    name: str
    callback: Callable


class SpaceGame:
    """
    Manages the complete game mechanics
    """
    def __init__(self, state: GameState, get_location: Callable[[str, str], Location]):
        self.game_id = state.game_id
        self.get_location = get_location
        self.location: Location = self.get_location(state.game_id, state.location)
        self.cargo: str|None = state.cargo
        self.crew: list[CrewMember] = state.crew
        self.message: str|None = None

    def __repr__(self):
        return f"""
game    : {self.game_id}
location: {self.location.name}
cargo   : {self.cargo}
crew    : {self.crew}
message : {self.message}
"""

    def get_state(self) -> GameState:
        return GameState(
            game_id=self.game_id,
            location=self.location.name,
            cargo=self.cargo,
            crew=self.crew
        )

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

    def get_commands(self) -> list[Command]:
        """
        Returns available commands at a given moment during the game.
        """
        commands = []
        # move
        for loc_name in self.location.connected_names:
            loc = self.get_location(self.game_id, loc_name)
            transition = (self.location.type, loc.type)
            prefix = TRANSITIONS.get(transition, "move to")
            move = Command(name=f"{prefix} {loc.name}", callback=partial(self.move_to, loc))
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
