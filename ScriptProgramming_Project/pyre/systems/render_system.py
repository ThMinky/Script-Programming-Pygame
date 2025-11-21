from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent, Sprite, Transform


class RenderSystem(BaseSystem):
    __instance = None

    @staticmethod
    def GetInstance() -> "RenderSystem":
        if RenderSystem.__instance is None:
            RenderSystem()
        return RenderSystem.__instance

    def __init__(self) -> None:
        if RenderSystem.__instance is not None:
            return

        RenderSystem.__instance = self
        self._m_sprites: list["Sprite"] = []
        self._m_to_add: set["Sprite"] = set()
        self._m_to_remove: set["Sprite"] = set()
        self._m_sorted: bool = False
        self.m_debugColliders: bool = True

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
        super().Update()

        from pyre.components import Transform
        from pyre.components.colliders import BaseCollider

        self._FlushChanges()

        if not self._m_sorted:
            self._SortSprites()

        for sprite in self._m_sprites:
            transform = sprite.m_parent.GetComponent(Transform)

            rotatedSprite = pygame.transform.rotate(sprite.m_texture, -transform.m_worldRot)

            rect = rotatedSprite.get_rect(center=transform.m_worldPos)

            surface.blit(rotatedSprite, rect.topleft)

            if self.m_debugColliders:
                colliders = sprite.m_parent.GetComponents(BaseCollider)
                for collider in colliders:
                    collider.DrawBounds(surface)

    def _FlushChanges(self) -> None:
        for sprite in self._m_to_remove:
            if sprite in self._m_sprites:
                self._m_sprites.remove(sprite)

        self._m_sprites.extend(self._m_to_add)
        self._m_to_add.clear()

    def _SortSprites(self) -> None:
        from pyre.components import Transform

        for sprite in self._m_sprites:
            transform = sprite.m_parent.GetComponent(Transform)
            if transform.m_parentTransform is None:
                self._AssignHierarchyLayer(transform)

        self._m_sprites.sort(key=lambda s: s.m_layer)
        self._m_sorted = True

    def _AssignHierarchyLayer(self, transform: "Transform", baseLayer: int = 0) -> None:
        from pyre.components import Sprite

        sprite = transform.m_parent.GetComponent(Sprite)
        currentLayer = baseLayer

        if sprite:
            if sprite.m_layer == 0:
                sprite.m_layer = baseLayer + 1
                currentLayer = baseLayer + 1
            else:
                currentLayer = sprite.m_layer + 1

        for child in transform.m_childrenTransforms:
            self._AssignHierarchyLayer(child, currentLayer)