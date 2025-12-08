import pygame

from pyre.components.colliders import BaseCollider


class BoxCollider(BaseCollider):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
        size: pygame.Vector2 | None = None,
    ) -> None:
        super().__init__(offset=offset)

        self.m_size: pygame.Vector2 | None = size if size is not None else None

    def _Init(self) -> None:
        super()._Init()

        self.m_transform.m_onPositionChanged.Add(self.UpdatePosition)
        self.m_transform.m_onScaleChanged.Add(self.UpdateBounds)

        self.UpdatePosition()
        self.UpdateBounds()

    def _Uninit(self) -> None:
        if self.m_transform:
            self.m_transform.m_onPositionChanged.Remove(self.UpdatePosition)
            self.m_transform.m_onScaleChanged.Remove(self.UpdateBounds)

        super()._Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdatePosition(self) -> None:
        super().UpdatePosition()

    def UpdateBounds(self) -> None:
        if self.m_size is None:
            if self.m_sprite:
                self.m_size = pygame.Vector2(self.m_sprite.m_surface.get_size())
            else:
                self.m_size = pygame.Vector2(1, 1)

    def DrawBounds(self, surface: pygame.Surface) -> None:
        from pyre.utils.rect_utils import GetRotatedRectVerticesWorldPos

        if not self.m_transform:
            return

        corners = GetRotatedRectVerticesWorldPos(
            self.m_worldPos,
            self.m_size,
            self.m_transform.m_worldRot,
        )

        points = []
        for corner in corners:
            points.append((corner.x, corner.y))

        pygame.draw.polygon(surface, (255, 0, 0), points, 1)