"""Friends Controller."""
import random
from typing import TYPE_CHECKING, Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate

from lib import RequestType
from lib.expense import Expense

if TYPE_CHECKING:
    from lib.splitwise import Splitwise

from sanic.log import logger


class FriendsController(HTTPMethodView):
    """Friends Controller."""

    @openapi.secured("api_key")
    async def get(self: Self, request: Request) -> None:
        """List Friends.

        Args:
        ----
            request (Request): Request
        """
        model: Splitwise = request.ctx.splitwise

        friends = await model.make_request("/get_friends", RequestType.GET)

        mapped = [
            {
                "id": friend["id"],
                "first_name": friend["first_name"],
                "last_name": friend["last_name"],
                "balance": friend["balance"],
                "picture": friend["picture"],
                "updated_at": friend["updated_at"],
            }
            for friend in friends["friends"]
        ]
        return json({"status": True, "result": mapped})


class FriendController(HTTPMethodView):
    """Friend Controller."""

    @openapi.secured("api_key")
    async def get(self: Self, request: Request, friend_id: int) -> None:
        """Get Info about friend."""
        model: Splitwise = request.ctx.splitwise
        mapped = []
        info_only = int(request.args.get("fetch_all", 1))
        params = {
            "limit": int(request.args.get("limit", 20)),
            "offset": int(request.args.get("page", "0")),
            "friend_id": friend_id,
            "visible": 1,
            "order": "date",
        }
        if info_only == 1:
            params["offset"] = params["offset"] * params["limit"]
            expenses = await model.make_request(
                "/get_expenses",
                RequestType.GET,
                params,
            )
            current_user = request.ctx.current_user

            mapped = [
                {
                    "cost": expense["cost"],
                    "description": expense["description"],
                    "details": expense["details"],
                    "date": expense["date"],
                    "currency_code": expense["currency_code"],
                    "friendship_id": expense["friendship_id"],
                    "created_by": expense["created_by"],
                    "users": list(
                        filter(
                            lambda x: x["user_id"] == current_user["id"],
                            expense["users"],
                        ),
                    ),
                }
                for expense in expenses["expenses"]
            ]

        friend_info = None
        if info_only or params["offset"] == 0:
            friend_info = (
                await model.make_request(f"/get_friend/{friend_id}", RequestType.GET)
            )["friend"]
        return json(
            {
                "status": True,
                "result": mapped,
                "detail": friend_info,
            },
        )

    @openapi.definition(
        body={"application/json": Expense.model_json_schema()},
        secured="api_key",
    )
    @validate(json=Expense)
    async def post(self: Self, request: Request, friend_id: int, body: Expense) -> None:
        """Create new Expense."""
        model: Splitwise = request.ctx.splitwise

        members = body.members
        share = round(body.cost / len(members), 2)
        diff = round(body.cost - round(share * len(members), 2), 2)

        rand = random.choice(members)  # noqa: S311

        post_body = body.model_dump()

        for i, member in enumerate(members):
            _mem_data = {
                f"users__{i}__user_id": member,
                f"users__{i}__paid_share": body.cost if body.paid_by == member else 0,
                f"users__{i}__owed_share": share + diff if rand == member else share,
            }
            post_body.update(_mem_data)
        if body.paid_by not in members:  # user paid but no split
            _mem_data = {
                f"users__{i+1}__user_id": body.paid_by,
                f"users__{i+1}__paid_share": body.cost,
                f"users__{i+1}__owed_share": 0,
            }
            post_body.update(_mem_data)

        post_body.pop("paid_by")
        post_body.pop("members")
        post_body["date"] = post_body["date"].isoformat()

        result = await model.make_request(
            "/create_expense",
            RequestType.POST,
            post_body,
        )
        logger.info(
            "%s Added a new expense",
            request.ctx.current_user["first_name"],
        )

        return json({"status": True, "result": result})
