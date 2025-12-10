from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

from pyre.components import Transform
from pyre.components.scripts import MonoScript
from pyre.utils.math_utils import GetAngleFromDirVector
from pyre.time import Time
from pyre.timer import Timer

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from project.enemy_spawner_scr import Spawns
    from scene import Scene


class HellspotScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign
        self.m_spawnPoint: "Spawns" | None = None  # Auto assign

        self.m_playerTrRef: weakref.ref["Transform"] | None = None

        # Caches
        self.m_tr: "Transform" | None = None
        self.m_lazerLTr: "Transform" | None = None  # Auto assign
        self.m_lazerRTr: "Transform" | None = None  # Auto assign

        # Timers
        self.m_lockDuration: float = 3
        self.m_lockTimer: "Timer" = Timer(self.m_lockDuration)

        self.m_reloadCooldown: float = 7
        self.m_reloadTimer: "Timer" = Timer(self.m_reloadCooldown, flag=True)

        # Vars
        self.m_hp: float = 6
        self.m_moveSpeed: float = 15

        self.m_blastDmg: float = 100
        self.m_blastRadius: float = 75
        self.m_timeToImpact: float = 4

        self.m_onPosition = False

    def Start(self) -> None:
        # Refs
        if self.m_scene.m_player is not None:
            self.m_playerTrRef = weakref.ref(self.m_scene.m_player.GetComponentByType(Transform))

        # Caches
        self.m_tr = self.m_parent.GetComponentByType(Transform)

    def Update(self) -> None:
        if not self.m_onPosition:
            self.MoveTowardsMarkingPos()
            return

        self.m_reloadTimer.Tick()

        self.LockTarget()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()

    def LockTarget(self) -> None:
        if self.m_playerTrRef is None:
            return

        if self.m_playerTrRef() is None:
            return

        if self.m_reloadTimer.m_flag:
            if self.m_lockTimer.m_flag:
                self.CallAirStrike()
                self.m_lockTimer.Reset()
                self.m_reloadTimer.Reset()
            else:
                self.m_lockTimer.Tick()
                self.Gizmo()

        self.RotateLazers()

    def RotateLazers(self) -> None:
        if self.m_playerTrRef is None:
            return

        if self.m_playerTrRef() is None:
            return

        dirVec = (self.m_playerTrRef().m_worldPos - self.m_tr.m_worldPos).normalize()
        rot = GetAngleFromDirVector(dirVec)
        self.m_lazerLTr.SetRotation(rot - self.m_tr.m_worldRot)
        self.m_lazerRTr.SetRotation(rot - self.m_tr.m_worldRot)

    def CallAirStrike(self) -> None:
        self.m_scene.CreateBlastArea(self.m_blastDmg, self.m_playerTrRef().m_worldPos, self.m_blastRadius, self.m_timeToImpact)

    def MoveTowardsMarkingPos(self) -> None:
        if self.m_onPosition:
            return

        dirVec = (self.m_spawnPoint.targetDest - self.m_tr.m_worldPos).normalize()
        newPos = self.m_tr.m_localPos + dirVec * self.m_moveSpeed * Time.deltaTime
        self.m_tr.SetPosition(newPos)

        if self.m_tr.m_worldPos.distance_squared_to(self.m_spawnPoint.targetDest) <= 1:
            self.m_onPosition = True

    def TakeDamage(self, amount: float) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:
            if self.m_spawnPoint is not None:
                self.m_spawnPoint.isLocked = False

            if self.m_parent in self.m_scene.m_enemies:
                self.m_scene.m_enemies.remove(self.m_parent)

            self.m_parent.Destroy()

    def Gizmo(self) -> None:
        from pyre.systems import RenderSystem
        
        if self.m_playerTrRef is None:
            return

        if self.m_playerTrRef() is None:
            return

        startL = (int(self.m_lazerLTr.m_worldPos.x), int(self.m_lazerLTr.m_worldPos.y))
        endL = (int(self.m_playerTrRef().m_worldPos.x), int(self.m_playerTrRef().m_worldPos.y))

        startR = (int(self.m_lazerRTr.m_worldPos.x), int(self.m_lazerRTr.m_worldPos.y))
        endR = (int(self.m_playerTrRef().m_worldPos.x), int(self.m_playerTrRef().m_worldPos.y))

        RenderSystem.GetInstance().DebugLine(startL, endL)
        RenderSystem.GetInstance().DebugLine(startR, endR)