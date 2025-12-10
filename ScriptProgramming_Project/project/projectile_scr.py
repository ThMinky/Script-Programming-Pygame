import pygame

from pyre.components import Transform
from pyre.components.colliders import BaseCollider
from pyre.components.scripts import MonoScript
from pyre import Time

from project.interfaces import IDamagable


class ProjectileScr(MonoScript):
    def __init__(
        self,
        *,
        dmg: int,
        speed: int,
        dir: pygame.Vector2,
    ) -> None:
        super().__init__()

        # Caches
        self.m_transform: "Transform" | None = None
        self.m_collider: "BaseCollider" | None = None

        # Vars
        self.m_dmg: int = dmg
        self.m_speed: int = speed
        self.m_dir: pygame.Vector2 = dir

    def Start(self) -> None:
        self.m_transform = self.m_parent.GetComponentByType(Transform)
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

    def Update(self) -> None:
        newPos = self.m_transform.m_worldPos + self.m_speed * self.m_dir * Time.deltaTime
        self.m_transform.SetPosition(newPos)

        collision = self.m_collider.GetCollision()
        if collision:
            target = collision.m_parent

            for script in target.GetComponentsByType(MonoScript):
                if isinstance(script, IDamagable):
                    script.TakeDamage(self.m_dmg)
                    break

            self.m_parent.Destroy()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass