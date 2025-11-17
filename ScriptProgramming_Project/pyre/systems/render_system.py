from __future__ import annotations
import math
from typing import TYPE_CHECKING
import warnings

import pygame

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent, Transform, Sprite


class RenderSystem(BaseSystem):
    __instance = None

    @staticmethod
    def GetInstance() -> "RenderSystem":
        if RenderSystem.__instance is None:
            RenderSystem()
        return RenderSystem.__instance

    def __init__(self) -> None:
        if RenderSystem.__instance is not None:
            warnings.warn(
                "Attempted to create another instance of RenderSystem (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return
        else:
            RenderSystem.__instance = self
            self.m_comps: list["Sprite"] = []
            self.m_sorted: bool = False
            self.m_debugColliders: bool = True

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components import Sprite

        if isinstance(comp, Sprite):
            if comp not in self.m_comps:
                self.m_comps.append(comp)
                self.m_sorted = False

    def Unregister(self, comp: "BaseComponent") -> None:
        if comp in self.m_comps:
            self.m_comps.remove(comp)

    def Update(self, dt: float) -> None:
        super().Update(dt)

    def Render(self, surface: pygame.Surface) -> None:
        from pyre.components import Transform
        from pyre.components.colliders import BaseCollider

        if not self.m_sorted:
            self._SortSprites()

        for sprite in self.m_comps:
            transformComp = sprite.m_parent.GetComponent(Transform)
            if sprite.m_isDirty:
                sprite.DirtyUpdate(transformComp)

            rect = self._CalcPivot(sprite, transformComp)

            rotatedSprite = pygame.transform.rotate(
                sprite.m_texture, -transformComp.m_worldRot
            )

            surface.blit(rotatedSprite, rect.topleft)

            if self.m_debugColliders:
                colliders = sprite.m_parent.GetComponents(BaseCollider)
                for collider in colliders:
                    collider.DrawBounds(surface)

    def _SortSprites(self) -> None:
        from pyre.components import Transform
        
        for sprite in self.m_comps:
            transformComp = sprite.m_parent.GetComponent(Transform)
            if transformComp.m_parentTransform is None:
                self._AssignHierarchyLayer(transformComp)

        self.m_comps.sort(key=lambda s: s.m_layer)
        self.m_sorted = True

    def _AssignHierarchyLayer(
        self, transformComp: "Transform", baseLayer: int = 0
    ) -> None:
        from pyre.components import Sprite

        spriteComp = transformComp.m_parent.GetComponent(Sprite)
        currentLayer = baseLayer

        if spriteComp:
            if spriteComp.m_layer == 0:
                spriteComp.m_layer = baseLayer + 1
                currentLayer = baseLayer + 1
            else:
                currentLayer = spriteComp.m_layer + 1

        for child in transformComp.m_childrenTransforms:
            self._AssignHierarchyLayer(child, currentLayer)

    def _CalcPivot(self, sprite: Sprite, transformComp) -> pygame.Rect:
        # Rotate the sprite surface
        rotated_sprite = pygame.transform.rotate(sprite.m_texture, -transformComp.m_worldRot)

        if sprite.m_pivot is None:
            # Default: rotate around center
            rect = rotated_sprite.get_rect(center=transformComp.m_worldPos)
            return rect

        # Custom pivot
        sprite_size = pygame.Vector2(sprite.m_texture.get_size())
        pivot = sprite.m_pivot

        # Vector from pivot to center
        offset = sprite_size / 2 - pivot

        # Rotate the offset
        angle_rad = math.radians(transformComp.m_worldRot)
        rotated_offset = pygame.Vector2(
            offset.x * math.cos(angle_rad) - offset.y * math.sin(angle_rad),
            offset.x * math.sin(angle_rad) + offset.y * math.cos(angle_rad)
        )

        # Create rect with top-left adjusted so pivot aligns with world position
        rect = rotated_sprite.get_rect()
        rect.topleft = transformComp.m_worldPos - rotated_offset
        return rect
