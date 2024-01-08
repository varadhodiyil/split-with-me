"""Base."""
from enum import Enum


class RequestType(Enum):  # noqa: D101
    POST = "POST"
    GET = "GET"
