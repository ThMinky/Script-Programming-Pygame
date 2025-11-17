from __future__ import annotations
import math
from typing import TYPE_CHECKING

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Transform


class Transform(BaseComponent):
    def __init__(
        self,
        *,
        localPos: pygame.Vector2 | None = None,
        localRot: float = 0.0,
        localScale: pygame.Vector2 | None = None,
        parentTransform: "Transform" | None = None,
        isStatic: bool = False,
    ) -> None:
        super().__init__()

        self.m_localPos: pygame.Vector2 = (
            localPos if localPos is not None else pygame.Vector2(0, 0)
        )
        self.m_localRot: float = localRot
        self.m_localScale: pygame.Vector2 = (
            localScale if localScale is not None else pygame.Vector2(1, 1)
        )

        self.m_worldPos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_worldRot: float = 0.0
        self.m_worldScale: pygame.Vector2 = pygame.Vector2(1, 1)

        self.m_parentTransform: "Transform" = parentTransform
        self.m_childrenTransforms: list["Transform"] = []

        self.m_isStatic = isStatic

    def Init(self) -> None:
        super().Init()

        if self.m_parentTransform:
            if self not in self.m_parentTransform.m_childrenTransforms:
                self.m_parentTransform.m_childrenTransforms.append(self)

    def Uninit(self) -> None:
        super().Uninit()

        if self.m_parentTransform:
            if self in self.m_parentTransform.m_childrenTransforms:
                self.m_parentTransform.m_childrenTransforms.remove(self)
            self.m_parentTransform = None

    def GetForwardVec(self) -> pygame.Vector2:
        rad = math.radians(self.m_worldRot - 90)
        return pygame.Vector2(math.cos(rad), math.sin(rad))

    def GetRightVec(self) -> pygame.Vector2:
        rad = math.radians(self.m_worldRot)
        return pygame.Vector2(math.cos(rad), math.sin(rad))

    def SetScale(self, newScale: pygame.Vector2) -> None:
        if newScale == self.m_localScale:
            return

        self.m_localScale = newScale
        self._MarkDirtyScale()

    def _MarkDirtyScale(self) -> None:
        from pyre.components import Sprite
        from pyre.components.colliders import BaseCollider

        spriteComp = self.m_parent.GetComponent(Sprite)
        if spriteComp:
            spriteComp.m_isDirty = True

        colliderComps = self.m_parent.GetComponents(BaseCollider)
        for collider in colliderComps:
            collider.m_isDirty = True

        for child in self.m_childrenTransforms:
            child._MarkDirtyScale()

    def UpdateWorldTransform(self) -> None:
        self.m_localRot %= 360

        if self.m_parentTransform:
            updatedLocalPos = (
                self.m_localPos.elementwise()
                * self.m_parentTransform.m_worldScale.elementwise()
            ).rotate(self.m_parentTransform.m_worldRot)

            self.m_worldPos = updatedLocalPos + self.m_parentTransform.m_worldPos
            self.m_worldRot = self.m_localRot + self.m_parentTransform.m_worldRot
            self.m_worldScale = (
                self.m_localScale.elementwise()
                * self.m_parentTransform.m_worldScale.elementwise()
            )
        else:
            self.m_worldPos = self.m_localPos
            self.m_worldRot = self.m_localRot
            self.m_worldScale = self.m_localScale

        self.m_worldRot %= 360