from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent, Sprite, Transform


class RenderSystem(BaseSystem):
    __instance = None

    def __new__(cls) -> "RenderSystem":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_sprites"):
            self._m_sprites: list["Sprite"] = []
            self._m_to_add: set["Sprite"] = set()
            self._m_to_remove: set["Sprite"] = set()
            self._m_sorted: bool = False
            self.m_debugColliders: bool = False
            self.m_debugFPS: bool = False

    @staticmethod
    def GetInstance() -> "RenderSystem":
        if RenderSystem.__instance is None:
            RenderSystem()
        return RenderSystem.__instance

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components import Sprite

        if isinstance(comp, Sprite):
            self._m_to_add.add(comp)
            self._m_sorted = False

    def Unregister(self, comp: "BaseComponent") -> None:
        from pyre.components import Sprite

        if isinstance(comp, Sprite):
            self._m_to_remove.add(comp)

    def Render(self, surface: pygame.Surface) -> None:
        from pyre.components import Transform
        from pyre.components.colliders import BaseCollider

        self._FlushChanges()

        if not self._m_sorted:
            self._SortSprites()

        for sprite in self._m_sprites:
            transform = sprite.m_parent.GetComponentByType(Transform)

            rotatedSprite = pygame.transform.rotate(sprite.m_sprite, -transform.m_worldRot)

            rect = rotatedSprite.get_rect(center=transform.m_worldPos)

            surface.blit(rotatedSprite, rect.topleft)

            if self.m_debugColliders:
                colliders = sprite.m_parent.GetComponentsByType(BaseCollider)
                for collider in colliders:
                    collider.DrawBounds(surface)

        if self.m_debugFPS:
            from pyre.time import Time

            Time.DrawFPS(surface)

    def _FlushChanges(self) -> None:
        self._m_sprites.extend(self._m_to_add)
        self._m_to_add.clear()

        for sprite in self._m_to_remove:
            if sprite in self._m_sprites:
                self._m_sprites.remove(sprite)

    def _SortSprites(self) -> None:
        from pyre.components import Transform

        for sprite in self._m_sprites:
            transform = sprite.m_parent.GetComponentByType(Transform)

            if transform.m_parentTransform is None:
                self._AssignHierarchyLayer(transform)

        self._m_sprites.sort(key=lambda s: s.m_layer)
        self._m_sorted = True

    def _AssignHierarchyLayer(self, transform: "Transform", baseLayer: int = 0) -> None:
        from pyre.components import Sprite

        sprite = transform.m_parent.GetComponentByType(Sprite)
        currentLayer = baseLayer

        if sprite:
            if sprite.m_layer == 0:
                sprite.m_layer = baseLayer + 1
                currentLayer = baseLayer + 1
            else:
                currentLayer = sprite.m_layer + 1

        for child in transform.m_childrenTransforms:
            self._AssignHierarchyLayer(child, currentLayer)