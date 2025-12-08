from __future__ import annotations
from typing import TYPE_CHECKING

import math

import pygame

# Engine
from pyre.components import Transform
from pyre.components.scripts import BaseScript
from pyre.systems import RenderSystem
from pyre.utils.math_utils import GetAngleFromDirVector
from pyre.time import Time
from pyre.timer import Timer

# Project
from project.interfaces import IDamagable

if TYPE_CHECKING:
    from scene import Scene


class BasicEnemy(BaseScript, IDamagable):
    def __init__(self):
        super().__init__()

        self.m_hp: int = 4

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

        self.m_transform: "Transform" | None = None
        self.m_barrelTransform: "Transform" | None = None  # Auto assign

        self.m_baseTransform: "Transform" | None = None
        self.m_playerTransform: "Transform" | None = None

        # Targeting
        self.m_lockedTarget: "Transform" | None = None

        # Timers
        self.m_lockDuration: float = 1.5
        self.m_lockTimer: "Timer" = Timer(self.m_lockDuration)

        self.m_reloadCooldown: float = 2.5
        self.m_reloadTimer: "Timer" = Timer(self.m_reloadCooldown, flag=True)

        # Movement
        self.m_hullMoveSpeed = 20
        self.m_moveSpeed = self.m_hullMoveSpeed

        # Ranges
        self.m_playerAttackRange: float = 300
        self.m_baseAttackRange: float = 125

        # Projectiles
        self.m_projDmg: int = 1
        self.m_projSpeed: int = 500

    def Start(self):
        self.m_transform = self.m_parent.GetComponentByType(Transform)

        self.m_baseTransform = self.m_scene.m_baseRoot.GetComponentByType(Transform)
        self.m_playerTransform = self.m_scene.m_player.GetComponentByType(Transform)

    def Update(self):
        if self.m_lockedTarget is not None:
            self.HandleTargeting(self.m_lockedTarget)
            return

        if self.m_transform.m_worldPos.distance_squared_to(self.m_baseTransform.m_worldPos) < self.m_baseAttackRange**2:
            self.m_lockedTarget = self.m_baseTransform
            return

        if self.m_transform.m_worldPos.distance_squared_to(self.m_playerTransform.m_worldPos) < self.m_playerAttackRange**2:
            self.m_lockedTarget = self.m_playerTransform
            return

        self.MoveTowards(self.m_baseTransform)
        self.RotateBarrel(self.m_baseTransform)

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

    def HandleTargeting(self, target: "Transform") -> None:
        if self.m_reloadTimer.m_flag:
            if self.m_lockTimer.m_flag:
                self.Shoot()
                self.m_lockTimer.Reset()
                self.m_reloadTimer.Reset()
                self.m_lockedTarget = None
            else:
                self.m_lockTimer.Tick()
                self.RotateBarrel(target)
                self.Mark(self.m_lockedTarget)
        else:
            self.m_reloadTimer.Tick()
            self.RotateBarrel(target)

    def MoveTowards(self, targetTransform: "Transform") -> None:
        dirVec = (targetTransform.m_worldPos - self.m_transform.m_worldPos).normalize()
        newPos = self.m_transform.m_localPos + dirVec * self.m_moveSpeed * Time.deltaTime
        self.m_transform.SetPosition(newPos)

    def RotateBarrel(self, targetTransform: "Transform") -> None:
        dirVec = (targetTransform.m_worldPos - self.m_transform.m_worldPos).normalize()
        rot = GetAngleFromDirVector(dirVec)
        self.m_barrelTransform.SetRotation(rot - self.m_transform.m_worldRot)

    def Mark(self, targetTransform: "Transform") -> None:
        rs = RenderSystem.GetInstance()
        start = (int(self.m_barrelTransform.m_worldPos.x), int(self.m_barrelTransform.m_worldPos.y))
        end = (int(targetTransform.m_worldPos.x), int(targetTransform.m_worldPos.y))

        rs.DebugLine(start, end)

    def Shoot(self) -> None:
        self.m_scene.CreateProjectile(self.m_projDmg, self.m_projSpeed, self.m_barrelTransform)