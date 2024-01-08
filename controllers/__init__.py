"""Controllers."""
from typing import Literal

from .profile import ProfileController
from .groups import GroupsController
from .groups import GroupController

CONTROLLERS: [tuple[Literal, type[ProfileController]]] = [
    ("profile", ProfileController, None),
    ("groups", GroupsController, None),
    ("group", GroupController, "/<group_id:int>"),
]
