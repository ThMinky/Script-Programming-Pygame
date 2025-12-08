from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar

import pygame

if TYPE_CHECKING:
    from pyre.components import BaseComponent, Transform


T = TypeVar("T", bound="BaseComponent")


class Entity:
    def __init__(
        self,
        *,
        localPos: pygame.Vector2 | None = None,
        localRot: float = 0,
        localScale: pygame.Vector2 | None = None,
        parentTransform: "Transform" | None = None,
    ) -> None:
        self.m_comps: list["BaseComponent"] = []

        from pyre.components import Transform

        self.AddComponent(
            Transform(
                localPos=localPos,
                localRot=localRot,
                localScale=localScale,
                parentTransform=parentTransform,
            )
        )

    def AddComponent(self, comp: "BaseComponent") -> None:
        from pyre.components import Transform

        if isinstance(comp, Transform):
            if self.GetComponentByType(Transform):
                return

        comp.m_parent = self
        comp._Init()
        self.m_comps.append(comp)

    def RemoveComponent(self, comp: "BaseComponent") -> None:
        from pyre.components import Transform

        if isinstance(comp, Transform):
            return

        if comp in self.m_comps:
            comp._Uninit()
            self.m_comps.remove(comp)

    def RemoveComponentsByType(self, compType: type[T]) -> None:
        from pyre.components import Transform

        if compType is Transform:
            return

        toRemove: list[T] = []
        for comp in self.m_comps:
            if isinstance(comp, compType):
                toRemove.append(comp)

        for comp in toRemove:
            comp._Uninit()
            self.m_comps.remove(comp)

    def GetComponentByType(self, compType: Type[T]) -> T | None:
        for comp in self.m_comps:
            if isinstance(comp, compType):
                return comp
        return None

    def GetComponentsByType(self, compType: Type[T]) -> list[T]:
        results: list[T] = []
        for comp in self.m_comps:
            if isinstance(comp, compType):
                results.append(comp)
        return results

    def Destroy(self) -> None:
        for comp in reversed(list(self.m_comps)):
            comp._Uninit()

        self.m_comps.clear()