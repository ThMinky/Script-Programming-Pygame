import pygame

from pyre.components.colliders import BaseCollider


class BoxCollider(BaseCollider):
    def __init__(self, *, offset: pygame.Vector2 | None = None, size: pygame.Vector2 | None = None) -> None:
        super().__init__(offset=offset)

        self.m_size: pygame.Vector2 | None = size if size is not None else None

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
        if self.m_size is None:
            if self.m_sprite:
                self.m_size = pygame.Vector2(self.m_sprite.m_texture.get_size())
            else:
                self.m_size = pygame.Vector2(1, 1)

    def DrawBounds(self, surface: pygame.Surface) -> None:
        from pyre.utils.math_utils import ERectPivots, GetRotatedRectCorners

        if not self.m_transform:
            return

        corners = GetRotatedRectCorners(
            self.m_worldPos,
            self.m_size,
            self.m_transform.m_worldRot,
            ERectPivots.CENTER,
        )

        points = []
        for corner in corners:
            points.append((corner.x, corner.y))

        pygame.draw.polygon(surface, (255, 0, 0), points, 1)