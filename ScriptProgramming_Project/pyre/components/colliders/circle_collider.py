import pygame

from pyre.components.colliders import BaseCollider


class CircleCollider(BaseCollider):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
        radius: float | None = None,
    ) -> None:
        super().__init__(offset=offset)

        self.m_radius: float | None = radius if radius is not None else None

    def Init(self) -> None:
        super().Init()

        if not self.m_transform:
            return

        self.m_transform.m_onPositionChanged.Add(self.UpdatePosition)
        self.m_transform.m_onPositionChanged.Add(self.UpdateBounds)

        self.UpdatePosition()
        self.UpdateBounds()

    def Uninit(self) -> None:
        if not self.m_transform:
            super().Uninit()
            return

        self.m_transform.m_onPositionChanged.Remove(self.UpdatePosition)
        self.m_transform.m_onPositionChanged.Remove(self.UpdateBounds)

        super().Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdatePosition(self) -> None:
        super().UpdatePosition()

    def UpdateBounds(self) -> None:
        if self.m_radius is None:
            if self.m_sprite:
                textureSize = pygame.Vector2(self.m_sprite.m_texture.get_size())
                self.m_radius = (
                    max(
                        (
                            textureSize.x,
                            textureSize.y,
                        )
                    )
                    / 2
                )
            else:
                self.m_radius = 1.0

    def DrawBounds(self, surface: pygame.Surface) -> None:
        pygame.draw.circle(surface, (255, 0, 0), (self.m_worldPos.x, self.m_worldPos.y), self.m_radius, 1)