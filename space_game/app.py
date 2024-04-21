from typing import Any, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from space_game.middleware import PreserveJSONResponse, json_to_html

# libs for testing
from faker import Faker
import random

app = FastAPI(default_response_class=PreserveJSONResponse)

# register middleware that automatically uses JINJA templates
# so we only have to write REST functions
# *** Kudos to Tim Weber for finding out! ***
app.middleware("http")(json_to_html)


class LocationData(BaseModel):
    name: str
    image: str
    description: str


class GameData(BaseModel):

    game_id: str
    location: LocationData
    cargo: Optional[str] = None
    crew: list[str] = ["panda"]
    commands: list[str]
    message: Optional[str] = None


@app.get("/new_game", response_model=GameData)
def new_game() -> GameData:
    return GameData(
        game_id="1234",
        location=LocationData(name="Pandalor", image="pandalor", description="a thick bamboo forest"),
        cargo="bamboo",
        commands=["one", "two", "three"],
    )


@app.get("/action/{game_id}/{command}")
def action(game_id: str, command: str) -> GameData:
    f = Faker()
    return GameData(
        game_id=game_id,
        location=LocationData(
            name=f.city(),
            image=random.choice(["pandalor", "adalov", "colabo", "valuerro"]),
            description=f.sentence(),
        ),
        cargo=random.choice(["peanuts", "starmap", "bamboo", "dna"]),
        crew=["panda"] + [random.choice(["hamster", "python", "pingu", "unicorn", "elephant"]) for _ in range(5)],
        commands=[f.word() for _ in range(4)],
        message="done: " + command,
    )


# Also let FastAPI serve the HTMX "frontend" of our application.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
