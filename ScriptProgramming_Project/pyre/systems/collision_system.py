from __future__ import annotations
from typing import TYPE_CHECKING
import warnings

from click import password_option
import pygame

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent
    from pyre.components.colliders import BaseCollider


class CollisionSystem(BaseSystem):
    __instance = None

    @staticmethod
    def GetInstance() -> "CollisionSystem":
        if CollisionSystem.__instance is None:
            CollisionSystem()
        return CollisionSystem.__instance

    def __init__(self) -> None:
        if CollisionSystem.__instance is not None:
            warnings.warn(
                "Attempted to create another instance of CollisionSystem (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return

        CollisionSystem.__instance = self
        self.m_comps: list["BaseCollider"] = []

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components.colliders import BaseCollider

        if isinstance(comp, BaseCollider):
            if comp not in self.m_comps:
                self.m_comps.append(comp)

    def Unregister(self, comp: "BaseComponent") -> None:
        if comp in self.m_comps:
            self.m_comps.remove(comp)

    def Update(self, dt) -> None:
        super().Update(dt)

        from pyre.components import Transform, Sprite
        from pyre.components.colliders import BoxCollider, CircleCollider

        for collider in self.m_comps:
            transformComp = collider.m_parent.GetComponent(Transform)
            if collider.m_isDirty:
                collider.DirtyUpdate()

            if isinstance(collider, BoxCollider):
                collider.m_worldPos = (
                    transformComp.m_worldPos - collider.m_size / 2 + collider.m_offset
                )
            elif isinstance(collider, CircleCollider):
                collider.m_worldPos = transformComp.m_worldPos + collider.m_offset