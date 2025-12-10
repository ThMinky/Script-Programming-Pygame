from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.command import Command

if TYPE_CHECKING:
    from pyre.entities import Entity


class RotateLeftCmd(Command):
    def __init__(self, rotSpeed: float) -> None:
        self.m_rotSpeed = rotSpeed

    def Execute(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponentByType(Transform)

        newRot = transform.m_localRot - self.m_rotSpeed * dt
        transform.SetRotation(newRot)