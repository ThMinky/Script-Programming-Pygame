from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

import pygame

# Engine
from pyre.components import Transform
from pyre.components.colliders import BaseCollider
from pyre.components.scripts import MonoScript
from pyre.entities import Entity
from pyre.managers import InputManager
from pyre.time import Time
from pyre.timer import Timer

# Project
from project.interfaces import IDamagable
from project.player.move_cmds import MoveBackwardCmd, MoveForwardCmd, RotateLeftCmd, RotateRightCmd
from project.tags import BlockerTag

if TYPE_CHECKING:
    from project.base import BaseScr
    from scene import Scene


class PlayerScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign
        self.m_barrel: "Entity" | None = None

        self.m_baseScrRef: weakref.ref["BaseScr"] | None = None  # Auto assign

        # Caches
        self.m_tr: "Transform" | None = None
        self.m_collider: "BaseCollider" | None = None

        # Timer
        self.m_reloadCooldown: float = 2.8
        self.m_reloadTimer: "Timer" = Timer(self.m_reloadCooldown, flag=True)

        # Vars
        self.m_hp: float = 3

        self.m_hullMoveSpeed: float = 125
        self.m_hullRotSpeed: float = 85
        self.m_barrelRotSpeed: float = 60

        self.m_projDmg: float = 2
        self.m_projSpeed: float = 750

        # Cmds
        self.m_cmd_moveForward: "MoveForwardCmd" = MoveForwardCmd(self.m_hullMoveSpeed)
        self.m_cmd_rotHullLeft: "RotateLeftCmd" = RotateLeftCmd(self.m_hullRotSpeed)
        self.m_cmd_moveBackward: "MoveBackwardCmd" = MoveBackwardCmd(self.m_hullMoveSpeed)
        self.m_cmd_rotHullRight: "RotateRightCmd" = RotateRightCmd(self.m_hullRotSpeed)
        self.m_cmd_rotTurretLeft: "RotateLeftCmd" = RotateLeftCmd(self.m_barrelRotSpeed)
        self.m_cmd_rotTurretRight: "RotateRightCmd" = RotateRightCmd(self.m_barrelRotSpeed)

    def Start(self) -> None:
        # Caches
        self.m_tr = self.m_parent.GetComponentByType(Transform)
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

    def Update(self) -> None:
        isMoving = False
        oldPos = self.m_tr.m_worldPos

        self.m_reloadTimer.Tick()

        # Move Hull
        if InputManager.GetInstance().GetKey(pygame.K_w):
            self.m_cmd_moveForward.Execute(self.m_parent, Time.deltaTime)
            isMoving = True
        if InputManager.GetInstance().GetKey(pygame.K_s):
            self.m_cmd_moveBackward.Execute(self.m_parent, Time.deltaTime)
            isMoving = True

        # Rotate Hull
        if isMoving:
            if InputManager.GetInstance().GetKey(pygame.K_a):
                self.m_cmd_rotHullLeft.Execute(self.m_parent, Time.deltaTime)
            if InputManager.GetInstance().GetKey(pygame.K_d):
                self.m_cmd_rotHullRight.Execute(self.m_parent, Time.deltaTime)

        # Rotate Barrel
        if InputManager.GetInstance().GetKey(pygame.K_q):
            self.m_cmd_rotTurretLeft.Execute(self.m_barrel, Time.deltaTime)
        if InputManager.GetInstance().GetKey(pygame.K_e):
            self.m_cmd_rotTurretRight.Execute(self.m_barrel, Time.deltaTime)

        # Shoot
        if InputManager.GetInstance().GetKeyDown(pygame.K_SPACE):
            if self.m_reloadTimer.m_flag:
                self.Shoot()

                self.m_reloadTimer.Reset()

        # Check for Blockers
        collisions = self.m_collider.GetCollisions()
        for other in collisions:
            if other.m_parent.GetComponentByType(BlockerTag):
                self.m_tr.SetPosition(oldPos)
                break

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def TakeDamage(self, amount: float) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:
            self.m_scene.m_player = None
            
            self.m_parent.Destroy()

    def Shoot(self) -> None:
        self.m_scene.CreateProjectile(self.m_projDmg, self.m_projSpeed, self.m_barrel.GetComponentByType(Transform))