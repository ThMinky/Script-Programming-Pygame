from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components.colliders import BaseCollider

if TYPE_CHECKING:
    from pyre.components import Transform


class CircleCollider(BaseCollider):
    def __init__(self, *, offset: pygame.Vector2 | None = None, radius: float | None = None) -> None:
        super().__init__(offset=offset)

        self.m_radius: float = radius if radius is not None else None

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)

        transform.m_onPositionChanged.Add(self.UpdatePosition)
        transform.m_onPositionChanged.Add(self.UpdateBounds)
        transform.m_onScaleChanged.Add(self.UpdateBounds)

        self.UpdatePosition()
        self.UpdateBounds()

    def Uninit(self) -> None:
        super().Uninit()

        from pyre.components.transform import Transform

        transform = self.m_parent.GetComponent(Transform)

        transform.m_onPositionChanged.Remove(self.UpdatePosition)
        transform.m_onPositionChanged.Remove(self.UpdateBounds)
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

        if self.m_radius is None:
            if sprite:
                textureSize = pygame.Vector2(sprite.m_originalTexture.get_size())
                self.m_radius = (
                    max(
                        (
                            textureSize.x * transform.m_worldScale.x,
                            textureSize.y * transform.m_worldScale.y,
                        )
                    )
                    / 2
                )
            else:
                self.m_radius = 1.0

    def DrawBounds(self, renderer: pygame.Surface) -> None:
        pygame.draw.circle(
            renderer,
            (255, 0, 0),
            (self.m_worldPos.x, self.m_worldPos.y),
            self.m_radius,
            1,
        )