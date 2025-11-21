from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components.colliders import BaseCollider

if TYPE_CHECKING:
    from pyre.components import Transform


class BoxCollider(BaseCollider):
    def __init__(self, *, offset: pygame.Vector2 | None = None, size: pygame.Vector2 | None = None) -> None:
        super().__init__(offset=offset)

        self.m_size: pygame.Vector2 = size if size is not None else None

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)

        transform.m_onPositionChanged.Add(self.UpdatePosition)
        transform.m_onPositionChanged.Add(self.UpdateBounds)
        transform.m_onRotationChanged.Add(self.UpdatePosition)
        transform.m_onRotationChanged.Add(self.UpdateBounds)
        transform.m_onScaleChanged.Add(self.UpdatePosition)
        transform.m_onScaleChanged.Add(self.UpdateBounds)

        self.UpdatePosition()
        self.UpdateBounds()

    def Uninit(self) -> None:
        super().Uninit()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)

        transform.m_onPositionChanged.Remove(self.UpdatePosition)
        transform.m_onPositionChanged.Remove(self.UpdateBounds)
        transform.m_onRotationChanged.Remove(self.UpdatePosition)
        transform.m_onRotationChanged.Remove(self.UpdateBounds)
        transform.m_onScaleChanged.Remove(self.UpdatePosition)
        transform.m_onScaleChanged.Remove(self.UpdateBounds)

    def UpdatePosition(self) -> None:
        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)
        self.m_worldPos = transform.m_worldPos + self.m_offset

    def UpdateBounds(self) -> None:
        from pyre.components.transform import Transform
        from pyre.components import Sprite

        transform = self.m_parent.GetComponent(Transform)
        sprite = self.m_parent.GetComponent(Sprite)

        if self.m_size is None:
            if sprite:
                textureSize = pygame.Vector2(sprite.m_originalTexture.get_size())
                self.m_size = textureSize.elementwise() * transform.m_worldScale.elementwise()
            else:
                self.m_size = pygame.Vector2(1, 1)

    def DrawBounds(self, surface: pygame.Surface) -> None:
        from pyre.components.transform import Transform
        from pyre.utils.math_utils import ERectPoints, GetRotatedRectCorners

        transform = self.m_parent.GetComponent(Transform)

        corners = GetRotatedRectCorners(
            self.m_worldPos,
            self.m_size,
            transform.m_worldRot,
            ERectPoints.CENTER,
        )

        points = []
        for corner in corners:
            points.append((corner.x, corner.y))

        pygame.draw.polygon(surface, (255, 0, 0), points, 1)