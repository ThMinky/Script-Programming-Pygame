from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Transform


class Sprite(BaseComponent):
    def __init__(self, *, texturePath: str, layer: int = 0) -> None:
        super().__init__()

        self.m_texture: pygame.Surface = pygame.image.load(texturePath).convert_alpha()
        self.m_originalTexture: pygame.Surface = self.m_texture.copy()
        self.m_layer: int = layer

        self.m_transform: "Transform" | None = None

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform
        from pyre.components.colliders import BaseCollider

        self.m_transform = self.m_parent.GetComponent(Transform)

        self.m_transform.m_onScaleChanged.Add(self.UpdateScale)

        for collider in self.m_parent.GetComponents(BaseCollider):
            collider.m_sprite = self

        self.UpdateScale()

    def Uninit(self) -> None:
        from pyre.components.colliders import BaseCollider

        self.m_transform.m_onScaleChanged.Remove(self.UpdateScale)

        for collider in self.m_parent.GetComponents(BaseCollider):
            collider.m_sprite = None

        self.m_transform = None

        super().Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdateScale(self) -> None:
        textureSize = pygame.Vector2(self.m_originalTexture.get_size())
        scaledSize = textureSize.elementwise() * self.m_transform.m_worldScale.elementwise()

        self.m_texture = pygame.transform.smoothscale(self.m_originalTexture, scaledSize)