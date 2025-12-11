from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

import pygame

from pyre.components import Transform
from pyre.components.scripts import MonoScript
from pyre.entities import Entity
from pyre.managers import SoundManager
from pyre.time import Time

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from scene import Scene


class BlastAreaScr(MonoScript):
    def __init__(
        self,
        *,
        dmg: float,
        center: pygame.Vector2,
        radius: float,
        countdown: float,
    ) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

        self.m_baseTrRef: weakref.ref["Transform"] | None = None
        self.m_playerTrRef: weakref.ref["Transform"] | None = None

        # Vars
        self.m_dmg: float = dmg
        self.m_center: pygame.Vector2 = center
        self.m_radius: float = radius
        self.m_countdown: float = countdown

    def Start(self) -> None:
        if self.m_scene.m_baseRoot is not None:
            self.m_baseTrRef = weakref.ref(self.m_scene.m_baseRoot.GetComponentByType(Transform))

        if self.m_scene.m_player is not None:
            self.m_playerTrRef = weakref.ref(self.m_scene.m_player.GetComponentByType(Transform))

    def Update(self) -> None:
        self.Gizmo()
        
        if self.m_countdown <= 0:
            self.DealDmg()

        self.m_countdown -= Time.deltaTime

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()

    def DealDmg(self) -> None:
        SoundManager.GetInstance().PlaySound("explosion")
        
        toDmg: list["Entity"] = []

        baseTr = self.m_baseTrRef() if self.m_baseTrRef else None
        if baseTr is not None and baseTr.m_parent is not None:
            if self.m_center.distance_squared_to(baseTr.m_worldPos) <= self.m_radius**2:
                toDmg.append(baseTr.m_parent)

        playerTr = self.m_playerTrRef() if self.m_playerTrRef else None
        if playerTr is not None and playerTr.m_parent is not None:
            if self.m_center.distance_squared_to(playerTr.m_worldPos) <= self.m_radius**2:
                toDmg.append(playerTr.m_parent)

        for enemy in self.m_scene.m_enemies.copy():
            if enemy is None:
                continue

            enemyTr = enemy.GetComponentByType(Transform)
            if enemyTr is None:
                continue

            if self.m_center.distance_squared_to(enemyTr.m_worldPos) <= self.m_radius**2:
                toDmg.append(enemy)

        for entt in toDmg:
            if entt is None:
                continue

            for script in entt.GetComponentsByType(MonoScript):
                if isinstance(script, IDamagable):
                    script.TakeDamage(self.m_dmg)
                    break

        self.m_scene.CreateExplosionVFX(self.m_center, pygame.Vector2(2, 2))

        if self.m_parent in self.m_scene.m_blastAreas:
            self.m_scene.m_blastAreas.remove(self.m_parent)

        self.m_parent.Destroy()

    def Gizmo(self) -> None:
        from pyre.systems import RenderSystem
        
        RenderSystem.GetInstance().DebugCircle(self.m_center, self.m_radius, (255, 0, 0))