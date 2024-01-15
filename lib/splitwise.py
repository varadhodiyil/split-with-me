"""SplitWise utils."""


from http import HTTPStatus
from typing import Self

from aiohttp import ClientSession, ClientTimeout

from . import RequestType


class MadError(Exception):
    """Raised when Splitwise doesn't like us."""


class Splitwise:
    """SplitWise Utils."""

    def __init__(self: Self, api_key: str) -> None:
        """Splitwise utils.

        Args:
        ----
            api_key (str): _description_
        """
        self._api_key = api_key

    async def make_request(
        self: Self, url: str, method: RequestType, data: None | dict = None
    ) -> dict:
        """Make Request.

        Args:
        ----
            url (str): endpoint
            method (RequestType): _description_
            data (None | dict, optional): _description_. Defaults to None.

        Returns:
        -------
            dict: _description_
        """
        headers = {"Authorization": f"Bearer {self._api_key}"}
        async with ClientSession(
            "https://secure.splitwise.com/",
            timeout=ClientTimeout(5),
            headers=headers,
        ) as session:
            result = await session.request(
                method.value,
                f"/api/v3.0{url}",
                data=data,
                params=data,
            )
            body = await result.json()
            if result.status == HTTPStatus.OK:
                return body

            msg = "Status : %s Error : %s"
            raise MadError(msg, (result.status, body))
