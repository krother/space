from fastapi.responses import JSONResponse

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
