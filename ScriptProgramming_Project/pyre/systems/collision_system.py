from __future__ import annotations
from typing import TYPE_CHECKING

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
            return

        CollisionSystem.__instance = self
        self.m_comps: list["BaseCollider"] = []

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components.colliders import BaseCollider

        if isinstance(comp, BaseCollider):
            if comp not in self.m_comps:
                self.m_comps.append(comp)

    def Unregister(self, comp: "BaseComponent") -> None:
        from pyre.components.colliders import BaseCollider

        if isinstance(comp, BaseCollider):
            if comp in self.m_comps:
                self.m_comps.remove(comp)

     