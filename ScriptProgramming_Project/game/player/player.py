from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from pyre.components import Script, Transform
from pyre.inputs import Input
from pyre.time import Time

if TYPE_CHECKING:
    from pyre.entities import Entity


class Player(Script):
    def __init__(self) -> None:
        super().__init__()

        self.m_input = Input.GetInstance()

        self.m_moveSpeed: float = 50.0
        self.m_rotSpeed: float = 25.0

        self.m_turrent = None

    def Awake(self):
        pass

    def Start(self):
        pass

    def Update(self) -> None:
        dt = Time.delta

        if self.m_input.GetKey(pygame.K_w):
            self.MoveForward(self.m_parent, dt)
        if self.m_input.GetKey(pygame.K_a):
            self.RotateLeft(self.m_parent, dt)
        if self.m_input.GetKey(pygame.K_s):
            self.MoveBackward(self.m_parent, dt)
        if self.m_input.GetKey(pygame.K_d):
            self.RotateRight(self.m_parent, dt)
        if self.m_input.GetKey(pygame.K_q):
            self.RotateLeft(self.m_turrent, dt)
        if self.m_input.GetKey(pygame.K_e):
            self.RotateRight(self.m_turrent, dt)

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def MoveForward(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponent(Transform)

        newPos = transform.m_localPos + (transform.GetForwardVec() * self.m_moveSpeed * dt)
        transform.SetPosition(newPos)

    def MoveBackward(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponent(Transform)

        newPos = transform.m_localPos + (-transform.GetForwardVec() * self.m_moveSpeed * dt)
        transform.SetPosition(newPos)

    def RotateLeft(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponent(Transform)

        newRot = transform.m_localRot - self.m_rotSpeed * dt
        transform.SetRotation(newRot)

    def RotateRight(self, entity: "Entity", dt: float) -> None:
        from pyre.components import Transform

        transform = entity.GetComponent(Transform)

        newRot = transform.m_localRot + self.m_rotSpeed * dt
        transform.SetRotation(newRot)