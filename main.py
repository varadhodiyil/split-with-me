"""Entry point."""
from sanic import Blueprint, Sanic
from sanic_ext import Config

from controllers import CONTROLLERS
from middleware import parse_token

app = Sanic("SplitwithMe")
app.register_middleware(parse_token, "request")
app.extend(
    config=Config(
        oas_ui_default="swagger",
        cors=True,
        cors_supports_credentials=True,
        cors_send_wildcard=True,
        cors_origins="http://localhost:8100,https://localhost",
    ),
)

app.ext.openapi.add_security_scheme("api_key", "apiKey")

for route, controller, named in CONTROLLERS:
    bp = Blueprint(route)
    named = named or ""  # noqa: PLW2901
    bp.add_route(controller.as_view(), f"{route}{named}")
    app.blueprint(bp)
