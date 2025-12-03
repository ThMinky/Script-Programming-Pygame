from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

import pygame

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Sprite, Transform


class BaseCollider(BaseComponent, ABC):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
    ) -> None:
        super().__init__()

        self.m_offset: pygame.Vector2 = offset if offset is not None else pygame.Vector2(0, 0)

        self.m_worldPos: pygame.Vector2 = pygame.Vector2(0, 0)
        self.m_sprite: "Sprite" | None = None
        self.m_transform: "Transform" | None = None

    def Init(self) -> None:
        super().Init()

        from pyre.components import Sprite, Transform

        self.m_sprite = self.m_parent.GetComponentByType(Sprite)
        self.m_transform = self.m_parent.GetComponentByType(Transform)

    def Uninit(self) -> None:
        self.m_transform = None
        self.m_sprite = None

        super().Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def UpdatePosition(self) -> None:
        if not self.m_transform:
            return

        self.m_worldPos = self.m_transform.m_worldPos + self.m_offset.rotate(self.m_transform.m_worldRot)

    @abstractmethod
    def UpdateBounds(self) -> None:
        pass

    @abstractmethod
    def DrawBounds(self, surface: pygame.Surface) -> None:
        pass