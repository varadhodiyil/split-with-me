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
    )
)

app.ext.openapi.add_security_scheme("api_key", "apiKey")

for route, controller, named in CONTROLLERS:
    bp = Blueprint(route)
    bp.add_route(controller.as_view(), named if named else route)
    app.blueprint(bp)
