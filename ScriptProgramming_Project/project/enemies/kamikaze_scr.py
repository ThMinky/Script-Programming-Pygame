from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

from pyre.components import Transform
from pyre.components.scripts import MonoScript
from pyre.managers import SoundManager
from pyre.time import Time

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from project.enemy_spawner_scr import Spawns
    from scene import Scene


class KamikazeScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign
        self.m_spawnPoint: "Spawns" | None = None  # Auto assign

        self.m_baseTrRef: weakref.ref["Transform"] | None = None
        self.m_playerTrRef: weakref.ref["Transform"] | None = None

        # Caches
        self.m_tr: "Transform" | None = None

        # Vars
        self.m_hp: float = 8
        self.m_moveSpeed: float = 8

        self.m_blastDmg: float = 100
        self.m_blastRadius: float = 100

        self.m_triggerRange: float = 100

    def Start(self) -> None:
        # Refs
        if self.m_scene.m_baseRoot is not None:
            self.m_baseTrRef = weakref.ref(self.m_scene.m_baseRoot.GetComponentByType(Transform))

        if self.m_scene.m_player is not None:
            self.m_playerTrRef = weakref.ref(self.m_scene.m_player.GetComponentByType(Transform))

        # Caches
        self.m_tr = self.m_parent.GetComponentByType(Transform)

    def Update(self) -> None:
        self.Gizmo()

        self.CheckForTargetsInTriggerRange()

        self.MoveTowardsBase()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self):
        super().Destroy()

    def CheckForTargetsInTriggerRange(self) -> None:
        if self.m_baseTrRef is not None:
            if self.m_baseTrRef() is not None:
                if self.m_tr.m_worldPos.distance_squared_to(self.m_baseTrRef().m_worldPos) <= self.m_triggerRange**2:
                    self.Detonate()
                    return

        if self.m_playerTrRef is not None:
            if self.m_playerTrRef() is not None:
                if self.m_tr.m_worldPos.distance_squared_to(self.m_playerTrRef().m_worldPos) <= self.m_triggerRange**2:
                    self.Detonate()
                    return

    def MoveTowardsBase(self) -> None:
        if self.m_baseTrRef is None:
            return

        if self.m_baseTrRef() is None:
            return

        dirVec = (self.m_baseTrRef().m_worldPos - self.m_tr.m_worldPos).normalize()
        newPos = self.m_tr.m_localPos + dirVec * self.m_moveSpeed * Time.deltaTime
        self.m_tr.SetPosition(newPos)

    def Detonate(self) -> None:
        self.m_scene.CreateBlastArea(self.m_blastDmg, self.m_tr.m_worldPos, self.m_blastRadius, 0)

    def TakeDamage(self, amount: float) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:

            SoundManager.GetInstance().PlaySound("explosion")

            if self.m_spawnPoint is not None:
                self.m_spawnPoint.isLocked = False

            if self.m_parent in self.m_scene.m_enemies:
                self.m_scene.m_enemies.remove(self.m_parent)

            self.m_parent.Destroy()

    def Gizmo(self) -> None:
        from pyre.systems import RenderSystem
        
        RenderSystem.GetInstance().DebugCircle(self.m_tr.m_worldPos, self.m_triggerRange, (255, 0, 0))