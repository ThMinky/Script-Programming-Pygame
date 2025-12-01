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
        sprite: pygame.Surface,
        layer: int = 0,
    ) -> None:
        super().__init__()

        self.m_sprite: pygame.Surface = sprite
        self.m_layer: int = layer

        self.m_transform: "Transform" | None = None
        self._m_originalSprite: pygame.Surface = self.m_sprite.copy()

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform
        from pyre.components.colliders import BaseCollider

        self.m_transform = self.m_parent.GetComponentByType(Transform)

        if not self.m_transform:
            return

        self.m_transform.m_onScaleChanged.Add(self.UpdateScale)

        for collider in self.m_parent.GetComponentsByType(BaseCollider):
            collider.m_sprite = self

        self.UpdateScale()

    def Uninit(self) -> None:
        from pyre.components.colliders import BaseCollider

        if not self.m_transform:
            return

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

    def UpdateScale(self) -> None:
        if not self.m_transform:
            return

        textureSize = pygame.Vector2(self._m_originalSprite.get_size())
        scaledSize = textureSize.elementwise() * self.m_transform.m_worldScale.elementwise()

        self.m_sprite = pygame.transform.smoothscale(self._m_originalSprite, scaledSize)