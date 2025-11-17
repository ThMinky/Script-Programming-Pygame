import pygame

from pyre.components import BaseComponent


class Sprite(BaseComponent):
    def __init__(
        self, *, texturePath: str, layer: int = 0, pivot: pygame.Vector2 | None = None
    ) -> None:
        super().__init__()
        self.m_texture: pygame.Surface = pygame.image.load(texturePath).convert_alpha()
        self.m_originalTexture: pygame.Surface = self.m_texture.copy()
        self.m_layer: int = layer
        self.m_size: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_pivot: pygame.Vector2 | None = None
        self.m_isDirty: bool = True

    def Init(self) -> None:
        super().Init()

    def Uninit(self) -> None:
        super().Uninit()

    def DirtyUpdate(self, transformComp) -> None:
        if not self.m_isDirty:
            return

        textureSize = pygame.Vector2(self.m_originalTexture.get_size())
        scaledSize = (
            textureSize.elementwise() * transformComp.m_worldScale.elementwise()
        )

        self.m_texture = pygame.transform.smoothscale(
            self.m_originalTexture, scaledSize
        )
        self.m_size = scaledSize
        self.m_isDirty = False