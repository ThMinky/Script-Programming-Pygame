from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.commands.command import Command

if TYPE_CHECKING:
    from pyre.entities import Entity


class MoveBackward(Command):
    def __init__(self, entity: "Entity") -> None:
        self.m_entity: "Entity" = entity

        from pyre.managers.system_manager import SystemManager
        from pyre.systems.movement_system import MovementSystem

        self.m_movementSys = SystemManager.GetInstance().GetSystemInstance(
            MovementSystem
        )

    def Execute(self, dt: float) -> None:
        self.m_movementSys.MoveBackward(self.m_entity, dt)