from __future__ import annotations
from typing import TYPE_CHECKING
import warnings

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.entities import Entity
    from pyre.components import BaseComponent, Movement


class MovementSystem(BaseSystem):
    __instance = None

    @staticmethod
    def GetInstance() -> "MovementSystem":
        if MovementSystem.__instance is None:
            MovementSystem()
        return MovementSystem.__instance

    def __init__(self) -> None:
        if MovementSystem.__instance is not None:
            warnings.warn(
                "Attempted to create another instance of MovementSystem (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return
        else:
            MovementSystem.__instance = self

    def Register(self, comp: "BaseComponent") -> None:
        pass

    def Unregister(self, comp: "BaseComponent") -> None:
        pass

    def Update(self, dt: float) -> None:
        super().Update(dt)

    def MoveForward(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform, Movement

        transform = entity.GetComponent(Transform)
        movement = entity.GetComponent(Movement)

        if movement:
            transform.m_localPos += (
                transform.GetForwardVec() * movement.m_moveSpeed * dt
            )

    def MoveBackward(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform, Movement

        transform = entity.GetComponent(Transform)
        movement = entity.GetComponent(Movement)

        if movement:
            transform.m_localPos += (
                -transform.GetForwardVec() * movement.m_moveSpeed * dt
            )

    def RotateLeft(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform, Movement

        transform = entity.GetComponent(Transform)
        movement = entity.GetComponent(Movement)

        if movement:
            transform.m_localRot -= movement.m_rotSpeed * dt

    def RotateRight(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform, Movement

        transform = entity.GetComponent(Transform)
        movement = entity.GetComponent(Movement)

        if movement:
            transform.m_localRot += movement.m_rotSpeed * dt