"""App Middleware. Sets Splitwise instance if Token is valid."""
from http import HTTPStatus

from sanic.request import Request
from sanic.response import HTTPResponse
from sanic import json
from lib.splitwise import Splitwise


async def parse_token(request: Request):
    """Read token from headers and set new Splitwise Instance to request."""
    token = request.token

    if not token:
        # return
        return HTTPResponse(
            {"status": False, "result": "Unauthorized"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    model = Splitwise(api_key=token)

    request.ctx.splitwise = model
    return None
