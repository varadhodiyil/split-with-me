"""User Profile."""

from typing import Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView


class ProfileController(HTTPMethodView):
    """User Profile API."""

    async def get(self: Self, request: Request) -> None:
        """Get Profile."""
        return json({"status": True})

    async def post(self: Self, request: Request) -> None:
        """Update Profile."""
        return json({"status": True})
