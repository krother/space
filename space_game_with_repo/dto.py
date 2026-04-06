"""
Data exchange classes for the boundary API.

They represent a reduced view of the game state
that may be safely published to players.
"""
from pydantic import BaseModel

from space_game.models import CrewMember


class LocationData(BaseModel):
    name: str
    image: str
    description: str


class GameData(BaseModel):
    game_id: str
    location: LocationData
    cargo: str|None
    crew: list[CrewMember]
    commands: list[str]
    message: str|None = None
    solved: bool

    def __str__(self):
        return "\n".join([
            "-" * 60,
            f"location: {self.location.name}",
            f"          {self.location.description}",
            f"cargo   : {self.cargo}",
            f"crew    : {', '.join(self.crew)}",
            f"\n{self.message}"
        ])
