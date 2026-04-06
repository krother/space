
from typing import Literal

from pydantic import BaseModel

CrewMember = Literal["panda", "elephant", "hamster", "python", "pingu", "unicorn"]


class GameState(BaseModel):
    game_id: str
    location: str
    cargo: str|None = None
    crew: list[CrewMember] = ["panda"]

    def serialize(self):
        return [
            self.game_id,
            self.location,
            self.cargo,
            ",".join(self.crew)
        ]

    @staticmethod
    def deserialize(data):
        data = list(data)
        data[3] = data[3].split(",")  # split crew
        data = dict(zip(GameState.model_fields.keys(), data))
        return GameState(**data)
