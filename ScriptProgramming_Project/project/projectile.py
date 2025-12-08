import pygame

# Engine
from pyre.components import Transform
from pyre.components.colliders import BaseCollider
from pyre.components.scripts import BaseScript
from pyre import Time

# Project
from project.interfaces import IDamagable


class Projectile(BaseScript):
    def __init__(
        self,
        dmg: int,
        speed: int,
        dir: pygame.Vector2,
    ):
        super().__init__()

        self.m_transform: "Transform" | None = None
        self.m_collider: "BaseCollider" | None = None

        self.m_dmg: int = dmg
        self.m_speed: int = speed
        self.m_dir: pygame.Vector2 = dir

    def Start(self):
        self.m_transform = self.m_parent.GetComponentByType(Transform)
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

    def Update(self):
        dt = Time.deltaTime

        newPos = self.m_transform.m_worldPos + self.m_dir * self.m_speed * dt
        self.m_transform.SetPosition(newPos)

        collision = self.m_collider.GetCollision()
        if collision:
            target = collision.m_parent

            for script in target.GetComponentsByType(BaseScript):
                if isinstance(script, IDamagable):
                    script.TakeDamage(self.m_dmg)
                    break

            print("Collided!")

            self.m_parent.Destroy()

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass