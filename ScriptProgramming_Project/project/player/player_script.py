from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

# Engine
from pyre.components import Transform
from pyre.components.colliders import BaseCollider
from pyre.components.scripts import BaseScript
from pyre.entities import Entity
from pyre.managers import InputManager
from pyre.time import Time

# Project
from project.interfaces import IDamagable
from project.player.move_commands import MoveBackward, MoveForward, RotateLeft, RotateRight
from project.blocker import Blocker

if TYPE_CHECKING:
    from scene import Scene


class PlayerScript(BaseScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        self.m_hp: int = 3

        self.m_transform: "Transform" | None = None
        self.m_collider: "BaseCollider" | None = None

        self.m_barrel: "Entity" | None = None
        self.m_scene: "Scene" | None = None

        self.m_shootCooldown: float = 2.8
        self.m_timer: float = self.m_shootCooldown
        self.m_canShoot: bool = True

        self.m_projDmg: int = 2
        self.m_projSpeed: int = 750

        self.m_hullMoveSpeed: int = 120
        self.m_hullRotSpeed: int = 50
        self.m_barrelRotSpeed: int = 35

        self.m_cmd_moveForward: "MoveForward" | None = None
        self.m_cmd_rotHullLeft: "RotateLeft" | None = None
        self.m_cmd_moveBackward: "MoveBackward" | None = None
        self.m_cmd_rotHullRight: "RotateRight" | None = None
        self.m_cmd_rotTurretLeft: "RotateLeft" | None = None
        self.m_cmd_rotTurretRight: "RotateRight" | None = None

    def Start(self) -> None:
        self.m_transform = self.m_parent.GetComponentByType(Transform)
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

        self.m_cmd_moveForward = MoveForward(self.m_hullMoveSpeed)
        self.m_cmd_rotHullLeft = RotateLeft(self.m_hullRotSpeed)
        self.m_cmd_moveBackward = MoveBackward(self.m_hullMoveSpeed)
        self.m_cmd_rotHullRight = RotateRight(self.m_hullRotSpeed)
        self.m_cmd_rotTurretLeft = RotateLeft(self.m_barrelRotSpeed)
        self.m_cmd_rotTurretRight = RotateRight(self.m_barrelRotSpeed)

    def Update(self) -> None:
        isMoving = False
        oldPos = self.m_transform.m_worldPos

        # Timer
        if not self.m_canShoot:
            self.m_timer -= Time.deltaTime

            if self.m_timer <= 0:
                self.m_canShoot = True
                self.m_timer = self.m_shootCooldown

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
            if self.m_canShoot:
                self.Shoot()

                self.m_canShoot = False

        # Check for Blockers
        collisions = self.m_collider.GetCollisions()
        for other in collisions:
            if other.m_parent.GetComponentByType(Blocker):
                self.m_transform.SetPosition(oldPos)
                break

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def TakeDamage(self, amount: int) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:
            self.m_parent.Destroy()

    def Shoot(self) -> None:
        self.m_scene.CreateProjectile(self.m_projDmg, self.m_projSpeed, self.m_barrel.GetComponentByType(Transform))