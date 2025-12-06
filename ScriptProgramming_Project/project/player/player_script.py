from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

# Engine
from pyre.components import Transform
from pyre.components.scripts import BaseScript
from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider
from pyre.managers import InputManager
from pyre.time import Time

# Project
from .move_commands import MoveBackward, MoveForward, RotateLeft, RotateRight

if TYPE_CHECKING:
    from pyre.entities import Entity


class PlayerScript(BaseScript):
    def __init__(self) -> None:
        super().__init__()

        self.m_input = InputManager.GetInstance()

        self.m_hullMoveSpeed: float = 75.0
        self.m_hullRotSpeed: float = 50.0
        self.m_barrelRotSpeed: float = 35.0

        self.m_barrel = None

        self.m_cmd_moveForward = MoveForward(self.m_hullMoveSpeed)
        self.m_cmd_rotHullLeft = RotateLeft(self.m_hullRotSpeed)
        self.m_cmd_moveBackward = MoveBackward(self.m_hullMoveSpeed)
        self.m_cmd_rotHullRight = RotateRight(self.m_hullRotSpeed)
        self.m_cmd_rotTurretLeft = RotateLeft(self.m_barrelRotSpeed)
        self.m_cmd_rotTurretRight = RotateRight(self.m_barrelRotSpeed)

    def Awake(self):
        pass

    def Start(self):
        pass

    def Update(self) -> None:
        moving = False

        if self.m_input.GetKey(pygame.K_w):
            self.m_cmd_moveForward.Execute(self.m_parent, Time.deltaTime)
            moving = True
        if self.m_input.GetKey(pygame.K_s):
            self.m_cmd_moveBackward.Execute(self.m_parent, Time.deltaTime)
            moving = True

        if moving:
            if self.m_input.GetKey(pygame.K_a):
                self.m_cmd_rotHullLeft.Execute(self.m_parent, Time.deltaTime)
            if self.m_input.GetKey(pygame.K_d):
                self.m_cmd_rotHullRight.Execute(self.m_parent, Time.deltaTime)

        if self.m_input.GetKey(pygame.K_q):
            self.m_cmd_rotTurretLeft.Execute(self.m_barrel, Time.deltaTime)
        if self.m_input.GetKey(pygame.K_e):
            self.m_cmd_rotTurretRight.Execute(self.m_barrel, Time.deltaTime)

        # print(self.m_parent.GetComponentByType(Transform).m_worldPos, end="\r", flush=True)

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass