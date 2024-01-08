"""Expense Utils."""
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class GroupExpense(BaseModel):
    """Group Expense Model."""

    cost: float
    description: str
    details: str
    date: datetime
    currency_code: Literal["EUR"]
    group_id: int
    paid_by: int
