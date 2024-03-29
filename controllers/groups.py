"""Groups Controller."""
import random
from typing import TYPE_CHECKING, Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate

from lib import RequestType
from lib.expense import Expense, GroupExpense

if TYPE_CHECKING:
    from lib.splitwise import Splitwise
from sanic.log import logger


class GroupsController(HTTPMethodView):
    """Groups Controller."""

    @openapi.secured("api_key")
    async def get(self: Self, request: Request) -> None:
        """List all Groups."""
        model: Splitwise = request.ctx.splitwise

        groups = await model.make_request("/get_groups", RequestType.GET)

        formatted = [
            {
                "id": group["id"],
                "name": group["name"],
                "simplify_by_default": group["simplify_by_default"],
                "members": group["members"],
                "cover_photo": group["cover_photo"],
            }
            for group in groups["groups"]
        ]

        return json({"status": True, "result": formatted})


class GroupController(HTTPMethodView):
    """Group Controller."""

    @openapi.secured("api_key")
    async def get(self: Self, request: Request, group_id: str) -> None:
        """Get Groups."""
        model: Splitwise = request.ctx.splitwise
        mapped = []
        params = {
            "limit": int(request.args.get("limit", 20)),
            "offset": int(request.args.get("page", "0")),
            "group_id": group_id,
            "visible": 1,
            "order": "date",
        }
        if int(request.args.get("fetch_all", 1)) == 1:
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

        formatted = None
        if params["offset"] == 0:
            group = await model.make_request(f"/get_group/{group_id}", RequestType.GET)
            group = group["group"]
            formatted = {
                "id": group["id"],
                "name": group["name"],
                "simplify_by_default": group["simplify_by_default"],
                "members": group["members"],
                "cover_photo": group["cover_photo"],
            }
        return json(
            {
                "status": True,
                "result": mapped,
                "detail": formatted,
            },
        )

    @openapi.definition(
        body={"application/json": Expense.model_json_schema()},
        secured="api_key",
    )
    @validate(json=Expense)
    async def post(
        self: Self, request: Request, group_id: str, body: GroupExpense
    ) -> None:
        """Add An Expense to group."""
        model: Splitwise = request.ctx.splitwise

        result = {}

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
        post_body["group_id"] = group_id
        result = {}

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
