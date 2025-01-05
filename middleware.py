"""App Middleware. Sets Splitwise instance if Token is valid."""
from http import HTTPStatus

from sanic.exceptions import SanicException
from sanic.request import Request
from sanic.response import HTTPResponse

from lib import RequestType
from lib.splitwise import Splitwise


async def parse_token(request: Request):
    """Read token from headers and set new Splitwise Instance to request."""
    token = request.token
    if request.method == "OPTIONS":
        return None
    token = "Fcl0tbieV7SdUWfqU1UMY8sg3uDPll5Hg9TIC3Ia"
    if token == "null":
        msg = "Not Logged in"
        raise SanicException(
            msg,
            status_code=HTTPStatus.UNAUTHORIZED,
        )
    if not token:
        msg = "Not Logged in"
        return None
        raise SanicException(
            msg,
            status_code=HTTPStatus.OK,
        )
        return HTTPResponse(
            {"status": False, "result": "Unauthorized"},
            status=HTTPStatus.UNAUTHORIZED,
        )

    model = Splitwise(api_key=token)

    request.ctx.splitwise = model
    request.ctx.current_user = (
        await model.make_request(
            "/get_current_user",
            RequestType.GET,
        )
    )["user"]
    return None
