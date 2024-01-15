"""Expense Utils."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class Expense(BaseModel):
    """Base Expense Model."""

    cost: float
    description: str
    details: str = ""
    date: datetime

    members: list[int]
    paid_by: int
    currency_code: Literal["EUR"] = "EUR"


class GroupExpense(Expense):
    """Group Expense Model."""

    group_id: int
