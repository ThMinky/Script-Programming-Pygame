from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

from pyre.components import Transform
from pyre.components.scripts import MonoScript
from pyre.systems import RenderSystem
from pyre.utils.math_utils import GetAngleFromDirVector
from pyre.time import Time
from pyre.timer import Timer

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from project.enemy_spawner_scr import Spawns
    from scene import Scene


class GruntScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None # Auto assign
        self.m_spawnPoint: "Spawns" | None = None # Auto assign

        self.m_baseTrRef: weakref.ref["Transform"] | None = None
        self.m_playerTrRef: weakref.ref["Transform"] | None = None
        self.m_currentTargetTrRef: weakref.reef["Transform"] | None = None

        # Caches
        self.m_tr: "Transform" | None = None
        self.m_barrelTr: "Transform" | None = None # Auto assign

        # Timers
        self.m_lockDuration: float = 1.5
        self.m_lockTimer: "Timer" = Timer(self.m_lockDuration)

        self.m_reloadCooldown: float = 2.5
        self.m_reloadTimer: "Timer" = Timer(self.m_reloadCooldown, flag=True)

        # Vars
        self.m_hp: float = 4
        self.m_moveSpeed: float = 20

        self.m_projDmg: float = 1
        self.m_projSpeed: float = 500

        self.m_AttackRangeToBase: float = 125
        self.m_AttackRangeToPlayer: float = 250

    def Start(self) -> None:
        # Refs
        if self.m_scene.m_baseRoot is not None:
            self.m_baseTrRef = weakref.ref(self.m_scene.m_baseRoot.GetComponentByType(Transform))

        if self.m_scene.m_player is not None:
            self.m_playerTrRef = weakref.ref(self.m_scene.m_player.GetComponentByType(Transform))

        # Caches
        self.m_tr = self.m_parent.GetComponentByType(Transform)

    def Update(self) -> None:
        self.m_reloadTimer.Tick()

        self.GetClosestTarget()

        if self.m_currentTargetTrRef is not None:
            if self.m_currentTargetTrRef() is not None:
                self.LockTarget()
                return

        self.MoveTowardsBase()
        self.m_lockTimer.Reset()

    def Enable(self) -> None:
        pass

    def Disable(self) -> None:
        pass

    def GetClosestTarget(self) -> None:
        if self.m_currentTargetTrRef is not None:
            return

        if self.m_baseTrRef is not None:
            if self.m_baseTrRef() is not None:
                if self.m_tr.m_worldPos.distance_squared_to(self.m_baseTrRef().m_worldPos) < self.m_AttackRangeToBase**2:
                    self.m_currentTargetTrRef = self.m_baseTrRef
                    return

        if self.m_playerTrRef is not None:
            if self.m_playerTrRef() is not None:
                if self.m_tr.m_worldPos.distance_squared_to(self.m_playerTrRef().m_worldPos) < self.m_AttackRangeToPlayer**2:
                    self.m_currentTargetTrRef = self.m_playerTrRef
                    return

        self.m_currentTargetTrRef = None

    def LockTarget(self) -> None:
        if self.m_currentTargetTrRef is None:
            return

        if self.m_currentTargetTrRef() is None:
            self.m_currentTargetTrRef = None
            return

        if self.m_reloadTimer.m_flag:
            if self.m_lockTimer.m_flag:
                self.Shoot()
                self.m_lockTimer.Reset()
                self.m_reloadTimer.Reset()
                self.m_currentTargetTrRef = None
            else:
                self.m_lockTimer.Tick()
                self.Gizmo()

        self.RotateBarrel()

    def RotateBarrel(self) -> None:
        if self.m_currentTargetTrRef is None:
            self.m_barrelTr.SetRotation(0)
            return

        if self.m_currentTargetTrRef() is None:
            self.m_currentTargetTrRef = None
            self.m_barrelTr.SetRotation(0)
            return

        dirVec = (self.m_currentTargetTrRef().m_worldPos - self.m_tr.m_worldPos).normalize()
        rot = GetAngleFromDirVector(dirVec)
        self.m_barrelTr.SetRotation(rot - self.m_tr.m_worldRot)

    def Shoot(self) -> None:
        self.m_scene.CreateProjectile(self.m_projDmg, self.m_projSpeed, self.m_barrelTr)

    def MoveTowardsBase(self) -> None:
        if self.m_baseTrRef is None:
            return

        if self.m_baseTrRef() is None:
            self.m_baseTrRef = None
            return

        dirVec = (self.m_baseTrRef().m_worldPos - self.m_tr.m_worldPos).normalize()
        newPos = self.m_tr.m_localPos + dirVec * self.m_moveSpeed * Time.deltaTime
        self.m_tr.SetPosition(newPos)

    def TakeDamage(self, amount: float) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:

            if self.m_spawnPoint is not None:
                self.m_spawnPoint.isLocked = False

            if self.m_parent in self.m_scene.m_enemies:
                self.m_scene.m_enemies.remove(self.m_parent)

            self.m_parent.Destroy()

    def Gizmo(self) -> None:
        if self.m_currentTargetTrRef is None:
            return

        if self.m_currentTargetTrRef() is None:
            self.m_currentTargetTrRef = None
            return

        start = (int(self.m_barrelTr.m_worldPos.x), int(self.m_barrelTr.m_worldPos.y))
        end = (int(self.m_currentTargetTrRef().m_worldPos.x), int(self.m_currentTargetTrRef().m_worldPos.y))

        RenderSystem.GetInstance().DebugLine(start, end)