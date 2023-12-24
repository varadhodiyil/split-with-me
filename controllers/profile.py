"""User Profile."""

from typing import Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView


class ProfileController(HTTPMethodView):
    """User Profile API."""

    def get(self: Self, request: Request) -> None:
        """Get Profile.

        Args:
        ----
            request (Request): Sanic Request
        """
        return json({"status": True})
