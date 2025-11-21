from __future__ import annotations
from typing import TYPE_CHECKING

import math

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
    ) -> None:
        super().__init__()

        self.m_localPos: pygame.Vector2 = localPos if localPos is not None else pygame.Vector2(0, 0)
        self.m_localRot: float = localRot
        self.m_localScale: pygame.Vector2 = localScale if localScale is not None else pygame.Vector2(1, 1)

        self.m_worldPos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_worldRot: float = 0.0
        self.m_worldScale: pygame.Vector2 = pygame.Vector2(1, 1)

        self.m_parentTransform: "Transform" = parentTransform
        self.m_childrenTransforms: list["Transform"] = []

        from pyre.event import Event

        self.m_onPositionChanged: "Event" = Event()
        self.m_onRotationChanged: "Event" = Event()
        self.m_onScaleChanged: "Event" = Event()

    def Init(self) -> None:
        super().Init()

        self._UpdateWorldTransform()

        if self.m_parentTransform:
            if self not in self.m_parentTransform.m_childrenTransforms:
                self.m_parentTransform.m_childrenTransforms.append(self)

    def Uninit(self) -> None:
        super().Uninit()

        if self.m_parentTransform:
            if self in self.m_parentTransform.m_childrenTransforms:
                self.m_parentTransform.m_childrenTransforms.remove(self)
            self.m_parentTransform = None

    def SetPosition(self, newPos: pygame.Vector2) -> None:
        self.m_localPos = newPos
        self._UpdateWorldPosition()

    def SetRotation(self, newRot: float) -> None:
        self.m_localRot = newRot
        self._UpdateWorldRotation()

    def SetScale(self, newScale: pygame.Vector2) -> None:
        self.m_localScale = newScale
        self._UpdateWorldScale()

    def _UpdateWorldPosition(self):
        if self.m_parentTransform:
            self.m_worldPos = (self.m_localPos.elementwise() * self.m_parentTransform.m_worldScale.elementwise()).rotate(
                self.m_parentTransform.m_worldRot
            ) + self.m_parentTransform.m_worldPos
        else:
            self.m_worldPos = self.m_localPos

        for child in self.m_childrenTransforms:
            child._UpdateWorldPosition()

        self.m_onPositionChanged.Fire()

    def _UpdateWorldRotation(self):
        if self.m_parentTransform:
            self.m_worldRot = (self.m_localRot + self.m_parentTransform.m_worldRot) % 360
        else:
            self.m_worldRot = self.m_localRot % 360

        for child in self.m_childrenTransforms:
            child._UpdateWorldRotation()

        self.m_onRotationChanged.Fire()

    def _UpdateWorldScale(self):
        if self.m_parentTransform:
            self.m_worldScale = self.m_localScale.elementwise() * self.m_parentTransform.m_worldScale.elementwise()
        else:
            self.m_worldScale = self.m_localScale

        for child in self.m_childrenTransforms:
            child._UpdateWorldScale()

        self.m_onScaleChanged.Fire()

    def _UpdateWorldTransform(self):
        if self.m_parentTransform:
            self.m_worldPos = (self.m_localPos.elementwise() * self.m_parentTransform.m_worldScale.elementwise()).rotate(
                self.m_parentTransform.m_worldRot
            ) + self.m_parentTransform.m_worldPos
            self.m_worldRot = (self.m_localRot + self.m_parentTransform.m_worldRot) % 360
            self.m_worldScale = self.m_localScale.elementwise() * self.m_parentTransform.m_worldScale.elementwise()
        else:
            self.m_worldPos = self.m_localPos
            self.m_worldRot = self.m_localRot % 360
            self.m_worldScale = self.m_localScale

    def GetForwardVec(self) -> pygame.Vector2:
        rad = math.radians(self.m_worldRot - 90)
        return pygame.Vector2(math.cos(rad), math.sin(rad))

    def GetRightVec(self) -> pygame.Vector2:
        rad = math.radians(self.m_worldRot)
        return pygame.Vector2(math.cos(rad), math.sin(rad))