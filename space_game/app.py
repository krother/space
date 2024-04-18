from typing import Any, Callable, Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound
from pydantic import BaseModel
from space_game.middleware import PreserveJSONResponse

# libs for testing
from faker import Faker
import random

# Create the FastAPI application.
app = FastAPI(default_response_class=PreserveJSONResponse)


# Set up Jinja to be able to render templates.
jinja_env = Environment(
    loader=FileSystemLoader("templates"),
)


# We define a middleware that converts responses to HTML using a Jinja template
# based on the endpoint function's name.
def get_template(endpoint: Callable | None) -> Template | None:
    """Get Jinja template instance for a given path operation."""
    if endpoint is None:
        # We don't know the function that handled this request, therefore we
        # can't select a corresponding template.
        return None

    # Simply add `.html` to the function name and try to look this up as a
    # template file.
    try:
        return jinja_env.get_template(f"{endpoint.__name__}.html")
    except TemplateNotFound:
        return None


@app.middleware("http")
async def json_to_html(request: Request, call_next):
    # Compute the response.
    response = await call_next(request)

    # Check whether the request is sent by HTMX. It always sets this header, see
    # <https://htmx.org/docs/#request-headers>.
    is_hx = request.headers.get("HX-Request", "") == "true"

    # Check whether the client requested HTML. This is just a proof of concept,
    # more solid `Accept` header parsing would be required.
    wants_html = request.headers.get("Accept", "") == "text/html"

    # Whether the request should be rendered as HTML or not.
    should_render = is_hx or wants_html

    if (
        should_render
        # Has PreserveJSONResponse kept the original Python object for us?
        and "preserved_json_data" in request.scope
        # Is there a Jinja template defined for this endpoint?
        and (template := get_template(request.scope.get("endpoint")))
    ):
        return HTMLResponse(
            template.render(
                data=request.scope["preserved_json_data"],
            )
        )

    # No HTML rendering, return the original response unchanged.
    return response


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
        cargo="medical",
        commands=["one", "two", "three"],
    )


@app.get("/action/{game_id}/{command}")
def action(game_id: str, command: str) -> GameData:
    f = Faker()
    return GameData(
        game_id=game_id,
        location=LocationData(
            name=f.city(),
            image=random.choice(["pandalor", "rorke", "magminus", "vega"]),
            description=f.sentence(),
        ),
        cargo=random.choice(["medical", "food", "gas", "minerals", "nucleons"]),
        crew=["panda"] + [random.choice(["hamster", "python", "pingu", "unicorn", "elephant"]) for _ in range(5)],
        commands=[f.word() for _ in range(4)],
        message="done: " + command,
    )


# Also let FastAPI serve the HTMX "frontend" of our application.
app.mount("/", StaticFiles(directory="static", html=True), name="static")
