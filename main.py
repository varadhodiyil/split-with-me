"""Entry point."""
from sanic import Blueprint, Sanic
from sanic_ext import Config

from controllers import CONTROLLERS
from middleware import set_token

app = Sanic("SplitwithMe")
app.register_middleware(set_token, "request")
app.extend(config=Config(oas_ui_default="swagger"))

for route, controller in CONTROLLERS:
    bp = Blueprint(route)
    bp.add_route(controller.as_view(), uri=route)
    app.blueprint(bp)
