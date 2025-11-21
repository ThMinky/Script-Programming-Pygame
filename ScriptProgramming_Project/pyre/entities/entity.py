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
        comp.m_parent = self
        comp.Init()
        self.m_comps.append(comp)

    def RemoveComponent(self, comp: "BaseComponent") -> None:
        from pyre.components import Transform

        if comp in self.m_comps:
            if not isinstance(comp, Transform):
                comp.Uninit()
                self.m_comps.remove(comp)

    def GetComponent(self, compType: Type[T]) -> Optional[T]:
        for comp in self.m_comps:
            if isinstance(comp, compType):
                return comp
        return None

    def GetComponents(self, compType: Type[T]) -> list[T]:
        temp = []
        for comp in self.m_comps:
            if isinstance(comp, compType):
                temp.append(comp)
        return temp