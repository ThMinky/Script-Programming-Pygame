from abc import ABC, abstractmethod
import math

import pygame

from pyre.components import BaseComponent


class BaseCollider(BaseComponent, ABC):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
    ) -> None:
        super().__init__()

        self.m_offset: pygame.Vector2 = (
            offset if offset is not None else pygame.Vector2(0, 0)
        )
        self.m_worldPos: pygame.Vector2 = None
        self.m_isDirty: bool = True

    def Init(self) -> None:
        super().Init()

    def Uninit(self) -> None:
        super().Uninit()

    def DirtyUpdate(self) -> None:
        pass

    @abstractmethod
    def DrawBounds(self, surface: pygame.Surface) -> None:
        pass