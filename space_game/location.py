from typing import Optional

from pydantic import BaseModel


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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIXME: should galaxy be modified here?
        self.galaxy = kwargs["galaxy"]  # dirty hack because pydantic copies
        self.galaxy[self.name] = self

    def __repr__(self) -> str:
        return (
            f"<{self.name}: {self.type};"
            f"provides {self.resources}; {self.active}>"
        )

    def add_connection(self, location) -> None:
        self.connected_locs.append(location)

    def activate(self, game):
        """triggers an event"""
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
            self.connected_locs.append(
                self.galaxy[self.trigger.activate_gain_connection]
            )

    def contact(self, game):
        if self.active:
            if (
                self.trigger.require_good is None
                or (game.cargo == self.trigger.require_good)
            ) and (
                self.trigger.require_crew_member is None
                or (self.trigger.require_crew_member in game.crew)
            ):
                self.activate(game)
                game.message = self.trigger.activated_message
            else:
                game.message = self.trigger.not_activated_message
