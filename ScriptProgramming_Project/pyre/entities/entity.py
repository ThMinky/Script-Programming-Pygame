from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar, Optional

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
        comp.Init()
        self.m_comps.append(comp)

    def RemoveComponent(self, comp: "BaseComponent") -> None:
        from pyre.components import Transform

        if isinstance(comp, Transform):
            return

        if comp in self.m_comps:
            comp.Uninit()
            self.m_comps.remove(comp)

    def RemoveComponentByType(self, compType: type["BaseComponent"]) -> None:
        from pyre.components import Transform

        if compType is Transform:
            return

        for comp in self.m_comps:
            if isinstance(comp, compType):
                comp.Uninit()
                self.m_comps.remove(comp)
                break

    def RemoveComponentsByType(self, compType: type["BaseComponent"]) -> None:
        from pyre.components import Transform

        if compType is Transform:
            return

        temp: list["BaseComponent"] = []
        for comp in self.m_comps:
            if isinstance(comp, compType):
                temp.append(comp)

        for comp in temp:
            comp.Uninit()
            self.m_comps.remove(comp)

    def GetComponentByType(self, compType: Type[T]) -> Optional[T]:
        for comp in self.m_comps:
            if isinstance(comp, compType):
                return comp
        return None

    def GetComponentsByType(self, compType: Type[T]) -> list[T]:
        temp: list["BaseComponent"] = []
        for comp in self.m_comps:
            if isinstance(comp, compType):
                temp.append(comp)
        return temp

    def DestroyRecursively(self):
        from pyre.components import Transform

        transform = self.GetComponentByType(Transform)

        if not transform:
            self._Destroy()
            return

        for child in list(transform.m_childrenTransforms):
            childEntity = child.m_parent
            childEntity.DestroyRecursively()

        self._Destroy()

    def _Destroy(self):
        for comp in list(self.m_comps):
            comp.Uninit()

        self.m_comps.clear()