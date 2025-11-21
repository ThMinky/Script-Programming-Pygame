from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.commands.command import Command

if TYPE_CHECKING:
    from pyre.entities import Entity


class MoveForward(Command):
    def __init__(self) -> None:
        pass

    def Execute(self, entity: "Entity", dt: float) -> None:
        pass