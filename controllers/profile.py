"""User Profile."""

from typing import Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView

from lib import RequestType


class ProfileController(HTTPMethodView):
    """User Profile API."""

    async def get(self: Self, request: Request) -> None:
        """Get Profile."""
        model = request.ctx.splitwise
        current_user = (
            await model.make_request(
                "/get_current_user",
                RequestType.GET,
            )
        )["user"]
        return json({"status": True, "result": current_user})

    async def post(self: Self, request: Request) -> None:
        """Update Profile."""
        return json({"status": True})
