from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent
    from pyre.components.colliders import BaseCollider


class CollisionSystem(BaseSystem):
    __instance = None

    def __new__(cls) -> "CollisionSystem":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "m_colliders"):
            self.m_colliders: list["BaseCollider"] = []

    @staticmethod
    def GetInstance() -> "CollisionSystem":
        if CollisionSystem.__instance is None:
            CollisionSystem()
        return CollisionSystem.__instance

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components.colliders import BaseCollider

        if isinstance(comp, BaseCollider):
            if comp not in self.m_colliders:
                self.m_colliders.append(comp)

    def Unregister(self, comp: "BaseComponent") -> None:
        from pyre.components.colliders import BaseCollider

        if isinstance(comp, BaseCollider):
            if comp in self.m_colliders:
                self.m_colliders.remove(comp)