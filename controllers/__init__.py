"""Controllers."""
from typing import Literal

from .profile import ProfileController

CONTROLLERS: [tuple[Literal, type[ProfileController]]] = [
    ("profile", ProfileController),
]
