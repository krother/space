from typing import Callable

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, Template, TemplateNotFound

from typing import Any

# By default, FastAPI's JSONResponse will render the response and then forget
# the original data that has been passed in. We subclass the default behavior to
# keep the original Python object, so that we can later pass it into Jinja.


class PreserveJSONResponse(JSONResponse):
    """A JSONResponse that remembers the original Python object."""

    def render(self, content: Any) -> bytes:
        # Store the Python object in self.original_data.
        self.original_data = content
        # Use the parent class to convert to JSON.
        return super().render(content)

    def __call__(self, scope, receive, send):
        # This is the ASGI communication interface. Since Starlette's
        # BaseHTTPMiddleware (and thus FastAPI's @app.middleware) will convert
        # responses into its own subclass, our middleware further down below
        # will no longer be able to access our `original_data` property.
        # Therefore, we need another place to store it in, and the ASGI scope is
        # a really good candidate ;)
        scope["preserved_json_data"] = self.original_data
        return super().__call__(scope, receive, send)


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
