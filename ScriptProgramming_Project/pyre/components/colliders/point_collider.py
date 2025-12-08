import pygame

from pyre.components.colliders import BaseCollider


class PointCollider(BaseCollider):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
    ) -> None:
        super().__init__(offset=offset)

    def _Init(self) -> None:
        super()._Init()

        self.m_transform.m_onPositionChanged.Add(self.UpdatePosition)

        self.UpdatePosition()

    def _Uninit(self) -> None:
        if self.m_transform:
            self.m_transform.m_onPositionChanged.Remove(self.UpdatePosition)

        super()._Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdatePosition(self) -> None:
        super().UpdatePosition()

    def UpdateBounds(self) -> None:
        pass

    def DrawBounds(self, surface: pygame.Surface) -> None:
        surface.set_at((int(self.m_worldPos.x), int(self.m_worldPos.y)), (255, 0, 0))