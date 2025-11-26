from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Transform, Sprite


class BaseCollider(BaseComponent, ABC):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
    ) -> None:
        super().__init__()

        self.m_offset: pygame.Vector2 = offset if offset is not None else pygame.Vector2(0, 0)

        self.m_worldPos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_transform: "Transform" | None = None
        self.m_sprite: "Sprite" | None = None

    def Init(self) -> None:
        super().Init()

        from pyre.components.transform import Transform

        self.m_transform = self.m_parent.GetComponent(Transform)

    def Uninit(self) -> None:
        self.m_transform = None
        self.m_sprite = None

        super().Uninit()

    def UpdatePosition(self) -> None:
        self.m_worldPos = self.transform.m_worldPos + self.m_offset

    @abstractmethod
    def UpdateBounds(self) -> None:
        pass

    @abstractmethod
    def DrawBounds(self, surface: pygame.Surface) -> None:
        pass