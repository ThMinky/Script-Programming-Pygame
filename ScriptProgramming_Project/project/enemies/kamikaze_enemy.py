from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

# Engine
from pyre.components import Transform
from pyre.components.scripts import BaseScript
from pyre.systems import RenderSystem
from pyre.time import Time

if TYPE_CHECKING:
    from scene import Scene


class KamikazeEnemy(BaseScript):
    def __init__(self):
        super().__init__()

        self.m_hp: int = 8

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

        self.m_transform: "Transform" | None = None

        self.m_baseTransform: "Transform" | None = None
        self.m_playerTransform: "Transform" | None = None

        self.m_renderSys: "RenderSystem" | None = None

        # Movement
        self.m_hullMoveSpeed = 10

        # Ranges
        self.m_triggerRange: float = 150

    def Start(self):
        self.m_transform = self.m_parent.GetComponentByType(Transform)

        self.m_baseTransform = self.m_scene.m_baseRoot.GetComponentByType(Transform)
        self.m_playerTransform = self.m_scene.m_player.GetComponentByType(Transform)

        self.m_renderSys = RenderSystem.GetInstance()

    def Update(self):
        self.m_renderSys.DebugCircle(self.m_transform.m_worldPos, self.m_triggerRange)

        distToBase = self.m_transform.m_worldPos.distance_squared_to(self.m_baseTransform.m_worldPos)
        distToPlayer = self.m_transform.m_worldPos.distance_squared_to(self.m_playerTransform.m_worldPos)

        if distToBase <= self.m_triggerRange**2 or distToPlayer <= self.m_triggerRange**2:
            self.Explode()

        self.MoveTowards(self.m_baseTransform)

    def Enable(self):
        pass

    def Disable(self):
        pass

    def TakeDamage(self, amount: int) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:

            if self.m_parent in self.m_scene.m_enemies:
                self.m_scene.m_enemies.remove(self.m_parent)

            self.m_parent.Destroy()

    def MoveTowards(self, targetTransform: "Transform") -> None:
        dirVec = (targetTransform.m_worldPos - self.m_transform.m_worldPos).normalize()
        newPos = self.m_transform.m_localPos + dirVec * self.m_hullMoveSpeed * Time.deltaTime
        self.m_transform.SetPosition(newPos)

    def Explode(self) -> None:
        self.m_scene.CreateProjectile(self.m_projDmg, self.m_projSpeed, self.m_barrelTransform)