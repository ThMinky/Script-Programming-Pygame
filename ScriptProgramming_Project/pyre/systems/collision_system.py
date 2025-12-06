from __future__ import annotations
from typing import TYPE_CHECKING, Callable

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

    def DetectCollision(self, collider: "BaseCollider") -> "BaseCollider" | None:
        for other in self.m_colliders:
            if other is collider:
                continue

            func = self._GetCollisionFunc(collider, other)
            if func:
                if func(collider, other):
                    return other

        return None

    def DetectCollisions(self, collider: "BaseCollider") -> list["BaseCollider"]:
        collisions: list["BaseCollider"] = []

        for other in self.m_colliders:
            if other is collider:
                continue

            func = self._GetCollisionFunc(collider, other)
            if func:
                if func(collider, other):
                    collisions.append(other)

        return collisions

    def _GetCollisionFunc(self, a: "BaseCollider", b: "BaseCollider") -> Callable[["BaseCollider", "BaseCollider"], bool] | None:
        from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider
        from pyre.utils.collision_utils import (
            BoxBox, BoxCircle, BoxLine, BoxPoint,
            CircleBox, CircleCircle, CircleLine, CirclePoint,
            LineBox, LineCircle, LineLine, LinePoint,
            PointBox, PointCircle, PointLine, PointPoint,
        )

        colliderTypesToFunc = {
            (BoxCollider, BoxCollider): BoxBox,
            (BoxCollider, CircleCollider): BoxCircle,
            (BoxCollider, LineCollider): BoxLine,
            (BoxCollider, PointCollider): BoxPoint,
            (CircleCollider, BoxCollider): CircleBox,
            (CircleCollider, CircleCollider): CircleCircle,
            (CircleCollider, LineCollider): CircleLine,
            (CircleCollider, PointCollider): CirclePoint,
            (LineCollider, BoxCollider): LineBox,
            (LineCollider, CircleCollider): LineCircle,
            (LineCollider, LineCollider): LineLine,
            (LineCollider, PointCollider): LinePoint,
            (PointCollider, BoxCollider): PointBox,
            (PointCollider, CircleCollider): PointCircle,
            (PointCollider, LineCollider): PointLine,
            (PointCollider, PointCollider): PointPoint,
        }

        return colliderTypesToFunc.get((type(a), type(b)), None)