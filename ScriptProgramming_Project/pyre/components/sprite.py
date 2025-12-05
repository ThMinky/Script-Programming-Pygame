from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Transform


class Sprite(BaseComponent):
    def __init__(
        self,
        *,
        surface: pygame.Surface,
        layer: int = 0,
    ) -> None:
        super().__init__()

        self.m_surface: pygame.Surface = surface
        self.m_layer: int = layer

        self.m_transform: "Transform" | None = None
        self._m_scaledSurface: pygame.Surface = self.m_surface.copy()
        self._m_originalSurface: pygame.Surface = self.m_surface.copy()

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform
        from pyre.components.colliders import BaseCollider

        self.m_transform = self.m_parent.GetComponentByType(Transform)

        if not self.m_transform:
            return

        self.m_transform.m_onRotationChanged.Add(self.UpdateRotation)
        self.m_transform.m_onScaleChanged.Add(self.UpdateScale)

        for collider in self.m_parent.GetComponentsByType(BaseCollider):
            collider.m_sprite = self

        self.UpdateScale()
        self.UpdateRotation()

    def Uninit(self) -> None:
        from pyre.components.colliders import BaseCollider

        if not self.m_transform:
            return

        self.m_transform.m_onRotationChanged.Remove(self.UpdateRotation)
        self.m_transform.m_onScaleChanged.Remove(self.UpdateScale)

        for collider in self.m_parent.GetComponentsByType(BaseCollider):
            collider.m_sprite = None

        self.m_transform = None

        super().Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def Destroy(self) -> None:
        super().Destroy()

    def UpdateRotation(self) -> None:
        if not self.m_transform:
            return

        self.m_surface = pygame.transform.rotate(self._m_scaledSurface, -self.m_transform.m_worldRot)

    def UpdateScale(self) -> None:
        if not self.m_transform:
            return

        surfaceSize = pygame.Vector2(self._m_originalSurface.get_size())
        scaledSize = surfaceSize.elementwise() * self.m_transform.m_worldScale.elementwise()

        self._m_scaledSurface = pygame.transform.scale(self._m_originalSurface, scaledSize)
        self.m_surface = self._m_scaledSurface