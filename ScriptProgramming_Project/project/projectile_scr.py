from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components import Transform
from pyre.components.colliders import BaseCollider
from pyre.components.scripts import MonoScript
from pyre.managers import SoundManager

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from scene import Scene


class ProjectileScr(MonoScript):
    def __init__(
        self,
        *,
        dmg: float,
        speed: float,
        dir: pygame.Vector2,
    ) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

        # Caches
        self.m_transform: "Transform" | None = None
        self.m_collider: "BaseCollider" | None = None

        # Vars
        self.m_dmg: float = dmg
        self.m_speed: float = speed
        self.m_dir: pygame.Vector2 = dir

    def Start(self) -> None:
        self.m_transform = self.m_parent.GetComponentByType(Transform)
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

    def Update(self) -> None:
        from pyre import Time
        
        newPos = self.m_transform.m_worldPos + self.m_speed * self.m_dir * Time.deltaTime
        self.m_transform.SetPosition(newPos)

        collision = self.m_collider.GetCollision()
        if collision:
            target = collision.m_parent

            for script in target.GetComponentsByType(MonoScript):
                if isinstance(script, IDamagable):
                    script.TakeDamage(self.m_dmg)
                    break

            SoundManager.GetInstance().PlaySound("projImpact")

            if self.m_parent in self.m_scene.m_projectiles:
                self.m_scene.m_projectiles.remove(self.m_parent)

            self.m_parent.Destroy()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()