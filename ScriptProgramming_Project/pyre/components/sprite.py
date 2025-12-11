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
        spriteKey: str,
        layer: int = 0,
    ) -> None:
        super().__init__()

        self.m_spriteKey: str = spriteKey
        self.m_layer: int = layer

        self.m_transform: "Transform" | None = None
        self.m_surface: pygame.Surface | None = None
        self._m_scaledSurface: pygame.Surface | None = None

    def _Init(self) -> None:
        super()._Init()

        from pyre.components import Transform
        from pyre.components.colliders import BaseCollider
        from pyre.managers import SpriteManager

        self.m_transform = self.m_parent.GetComponentByType(Transform)
        self.m_surface = SpriteManager.GetInstance().GetSprite(self.m_spriteKey)

        if not self.m_transform:
            raise RuntimeError("Component without Transform found!")

        self.m_transform.m_onRotationChanged.Add(self._UpdateRotation)
        self.m_transform.m_onScaleChanged.Add(self._UpdateScale)

        for collider in self.m_parent.GetComponentsByType(BaseCollider):
            collider.m_sprite = self

        self._UpdateScale()
        self._UpdateRotation()

    def _Uninit(self) -> None:
        from pyre.components.colliders import BaseCollider

        if self.m_transform:
            self.m_transform.m_onRotationChanged.Remove(self._UpdateRotation)
            self.m_transform.m_onScaleChanged.Remove(self._UpdateScale)

        for collider in self.m_parent.GetComponentsByType(BaseCollider):
            collider.m_sprite = None

        self.m_transform = None

        super()._Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def Destroy(self) -> None:
        super().Destroy()

    def SetSprite(self, spriteKey: str) -> None:
        self.m_spriteKey = spriteKey

        self._UpdateScale()
        self._UpdateRotation()

    def _UpdateRotation(self) -> None:
        if self.m_transform is None:
            return

        if self.m_surface is None:
            return

        self.m_surface = pygame.transform.rotate(self._m_scaledSurface, -self.m_transform.m_worldRot)

    def _UpdateScale(self) -> None:
        if self.m_transform is None:
            return

        from pyre.managers import SpriteManager

        originalSurface = SpriteManager.GetInstance().GetSprite(self.m_spriteKey)

        if originalSurface is None:
            return

        surfaceSize = pygame.Vector2(originalSurface.get_size())
        scaledSize = surfaceSize.elementwise() * self.m_transform.m_worldScale.elementwise()

        self._m_scaledSurface = pygame.transform.scale(originalSurface, scaledSize)
        self.m_surface = self._m_scaledSurface