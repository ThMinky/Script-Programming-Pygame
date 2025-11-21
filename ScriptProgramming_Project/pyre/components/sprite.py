from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Transform


class Sprite(BaseComponent):
    def __init__(self, *, texturePath: str, layer: int = 0, pivot: pygame.Vector2 | None = None) -> None:
        super().__init__()

        self.m_texture: pygame.Surface = pygame.image.load(texturePath).convert_alpha()
        self.m_originalTexture: pygame.Surface = self.m_texture.copy()
        self.m_layer: int = layer

        self.m_size: pygame.Vector2 = pygame.Vector2(0, 0)

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)
        
        transform.m_onScaleChanged.Add(self.UpdateScale)

        self.UpdateScale()

    def Uninit(self) -> None:
        super().Uninit()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)
        
        transform.m_onScaleChanged.Remove(self.UpdateScale)

    def UpdateScale(self) -> None:
        from pyre.components import Transform

        transform = self.m_parent.GetComponent(Transform)

        textureSize = pygame.Vector2(self.m_originalTexture.get_size())
        scaledSize = textureSize.elementwise() * transform.m_worldScale.elementwise()

        self.m_texture = pygame.transform.smoothscale(self.m_originalTexture, scaledSize)
        self.m_size = scaledSize