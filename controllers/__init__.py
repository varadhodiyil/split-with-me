"""Controllers."""
from typing import Literal

from .friends import FriendController, FriendsController
from .groups import GroupController, GroupsController
from .profile import ProfileController

CONTROLLERS: [tuple[Literal, type[ProfileController]]] = [
    ("profile", ProfileController, None),
    ("groups", GroupsController, None),
    ("group", GroupController, "/<group_id:int>"),
    ("friends", FriendsController, None),
    ("friend", FriendController, "/<friend_id:int>"),
]
