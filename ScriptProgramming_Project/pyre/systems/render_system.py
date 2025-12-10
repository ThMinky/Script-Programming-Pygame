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
            self.m_sprites: list["Sprite"] = []
            self._m_to_add: set["Sprite"] = set()
            self._m_to_remove: set["Sprite"] = set()
            self._m_sorted: bool = False
            self.m_debugColliders: bool = False
            self.m_debugFPS: bool = False

            # Enemy Marking
            self.m_debugDrawQueue: list[tuple] = []

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

        self._FlushChanges()

        if not self._m_sorted:
            self._SortSprites()

        for sprite in self.m_sprites:
            transform = sprite.m_parent.GetComponentByType(Transform)

            if not transform:
                continue

            rect = sprite.m_surface.get_rect(center=transform.m_worldPos)

            surface.blit(sprite.m_surface, rect.topleft)

        if self.m_debugColliders:
            from pyre.systems.collision_system import CollisionSystem

            for collider in CollisionSystem.GetInstance().m_colliders:
                collider.DrawBounds(surface)

        if self.m_debugFPS:
            from pyre.time import Time

            Time.DrawFPS(surface)

        # Enemy Marking
        for item in self.m_debugDrawQueue:
            if item[0] == "line":
                _, start, end, color, width = item
                pygame.draw.line(surface, color, start, end, width)
            elif item[0] == "circle":
                _, center, radius, color, width = item
                pygame.draw.circle(surface, color, center, radius, width)

        self.m_debugDrawQueue.clear()

    def _FlushChanges(self) -> None:
        self.m_sprites.extend(self._m_to_add)
        self._m_to_add.clear()

        for sprite in self._m_to_remove:
            if sprite in self.m_sprites:
                self.m_sprites.remove(sprite)

    def _SortSprites(self) -> None:
        visitedRoots: set["Transform"] = set()

        for sprite in self.m_sprites:
            rootTransform = self._GetTopMostTransform(sprite)

            if rootTransform in visitedRoots:
                continue
            visitedRoots.add(rootTransform)

            self._AssignHierarchyLayer(rootTransform)

        self.m_sprites.sort(key=lambda s: s.m_layer)
        self._m_sorted = True

    def _GetTopMostTransform(self, sprite: "Sprite") -> "Transform":
        from pyre.components import Transform

        transform = sprite.m_parent.GetComponentByType(Transform)

        if transform:
            while transform.m_parentTransform is not None:
                transform = transform.m_parentTransform
            return transform

    def _AssignHierarchyLayer(self, transform: "Transform", baseLayer: int = 0) -> None:
        from pyre.components import Sprite

        sprite = transform.m_parent.GetComponentByType(Sprite)

        if sprite:
            if transform.m_parentTransform:
                if sprite.m_layer == 0:
                    sprite.m_layer = baseLayer + 1
                    baseLayer += 1
                else:
                    baseLayer = sprite.m_layer + 1
            else:
                baseLayer = sprite.m_layer + 1

        for child in transform.m_childrenTransforms:
            self._AssignHierarchyLayer(child, baseLayer)

    # Enemy Marking
    def DebugLine(self, start, end, color=(255, 0, 0), width=1):
        self.m_debugDrawQueue.append(("line", start, end, color, width))

    def DebugCircle(self, center, radius, color=(255, 0, 0), width=1):
        self.m_debugDrawQueue.append(("circle", center, radius, color, width))