from __future__ import annotations

import weakref

import random

from pyre.components.colliders import BaseCollider
from pyre.components.scripts import MonoScript
from pyre.managers import SoundManager

from project.player.player_scr import PlayerScr
from project.base import BaseScr
from project.ui_scr import UIScr


class AmmoBoxScr(MonoScript):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_baseScrRef: weakref.ref["BaseScr"] | None = None  # Auto assign

        # Caches
        self.m_collider: "BaseCollider" | None = None

        # Vars
        self.m_ammoAmount: int = 0

    def Start(self) -> None:
        # Caches
        self.m_collider = self.m_parent.GetComponentByType(BaseCollider)

        # Vars
        self.m_ammoAmount = random.randint(2, 6)

    def Update(self) -> None:
        # Check for Player
        collisions = self.m_collider.GetCollisions()
        for other in collisions:
            if other.m_parent.GetComponentByType(PlayerScr):
                if self.m_baseScrRef is not None:
                    if self.m_baseScrRef() is not None:
                        UIScr.GetInstance().m_baseAmmo += self.m_ammoAmount

                        self.m_baseScrRef().m_autoTurretAmmo += self.m_ammoAmount

                SoundManager.GetInstance().PlaySound("pickupAmmo")

                self.m_parent.Destroy()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()