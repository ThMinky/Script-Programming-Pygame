import pygame

from pyre.components.colliders import BaseCollider


class LineCollider(BaseCollider):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
        length: float | None = None,
    ) -> None:
        super().__init__(offset=offset)

        self.m_length: float | None = length if length is not None else None

        self.m_startPoint: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_endPoint: pygame.Vector2 = pygame.Vector2(0, 0)

    def _Init(self) -> None:
        super()._Init()

        self.m_transform.m_onPositionChanged.Add(self.UpdatePosition)
        self.m_transform.m_onPositionChanged.Add(self.UpdateBounds)

        self.UpdatePosition()
        self.UpdateBounds()

    def _Uninit(self) -> None:
        if self.m_transform:
            self.m_transform.m_onPositionChanged.Remove(self.UpdatePosition)
            self.m_transform.m_onPositionChanged.Remove(self.UpdateBounds)

        super()._Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdatePosition(self) -> None:
        super().UpdatePosition()

    def UpdateBounds(self) -> None:
        if not self.m_transform:
            return

        if self.m_length is None:
            if self.m_sprite:
                self.m_length = self.m_sprite.m_surface.get_size()[1]
            else:
                self.m_length = 1.0

        self.m_startPoint = self.m_worldPos + (-self.m_transform.GetForwardVec() * (self.m_length / 2))
        self.m_endPoint = self.m_worldPos + (self.m_transform.GetForwardVec() * (self.m_length / 2))

    def DrawBounds(self, surface) -> None:
        pygame.draw.line(surface, (255, 0, 0), self.m_startPoint, self.m_endPoint, 1)