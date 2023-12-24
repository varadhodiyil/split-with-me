"""App Middleware. Sets Splitwise instance if Token is valid."""
from sanic.request import Request


async def set_token(request: Request) -> None:
    """Read token from headers and set new Splitwise Instance to request."""
    token = request.headers.get("Authorization")

    if token:
        token = token.split("Bearer")[1]
