from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.commands.command import Command

if TYPE_CHECKING:
    from pyre.entities import Entity


class MoveForward(Command):
    def __init__(self, moveSpeed: float) -> None:
        self.m_moveSpeed = moveSpeed

    def Execute(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponentByType(Transform)

        newPos = transform.m_localPos + (transform.GetForwardVec() * self.m_moveSpeed * dt)
        transform.SetPosition(newPos)