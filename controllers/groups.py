"""Groups Controller."""
import random
from typing import TYPE_CHECKING, Self

from sanic import json
from sanic.request import Request
from sanic.views import HTTPMethodView
from sanic_ext import openapi, validate


from lib import RequestType
from lib.expense import GroupExpense

if TYPE_CHECKING:
    from lib.splitwise import Splitwise


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

        group = await model.make_request(f"/get_group/{group_id}", RequestType.GET)
        group = group["group"]
        formatted = {
            "id": group["id"],
            "name": group["name"],
            "simplify_by_default": group["simplify_by_default"],
            "members": group["members"],
            "cover_photo": group["cover_photo"],
        }

        return json({"status": True, "result": formatted})

    @openapi.definition(
        body={"application/json": GroupExpense.model_json_schema()},
        secured="api_key",
    )
    @validate(json=GroupExpense)
    async def post(
        self: Self, request: Request, group_id: str, body: GroupExpense
    ) -> None:
        """Add An Expense to group."""
        model: Splitwise = request.ctx.splitwise
        body.group_id = group_id
        result = {}

        group = await model.make_request(f"/get_group/{group_id}", RequestType.GET)
        members = group["group"]["members"]
        share = round(body.cost / len(members), 2)
        diff = round(body.cost - round(share * len(members), 2), 2)

        rand = random.choice(members)["id"]  # noqa: S311

        post_body = body.model_dump()
        is_paid_usr__grp = False
        for i, member in enumerate(members):
            if member["id"] == body.paid_by:
                is_paid_usr__grp = True
            _mem_data = {
                f"users__{i}__user_id": member["id"],
                f"users__{i}__paid_share": body.cost
                if body.paid_by == member["id"]
                else 0,
                f"users__{i}__owed_share": share + diff
                if rand == member["id"]
                else share,
            }
            post_body.update(_mem_data)

        post_body.pop("paid_by")
        if is_paid_usr__grp:
            result = await model.make_request(
                "/create_expense",
                RequestType.POST,
                post_body,
            )

            return json({"status": True, "result": result})

        return json({"status": False, "result": "Paid User not found"})
