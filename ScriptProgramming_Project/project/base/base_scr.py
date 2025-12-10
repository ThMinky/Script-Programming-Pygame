from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.components.scripts import MonoScript
from pyre.managers import SoundManager

from project.interfaces import IDamagable
from project.ui_scr import UIScr

if TYPE_CHECKING:
    from scene import Scene


class BaseScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

        # Vars
        self.m_hp: float = 10

        self.m_autoTurretAmmo: int = 12

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        pass

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()

    def TakeDamage(self, amount: float) -> None:
        import globals

        UIScr.GetInstance().m_baseHp -= amount

        self.m_hp -= amount

        if self.m_hp <= 0:
            self.m_scene.m_baseRoot = None

            self.m_parent.Destroy()

            globals.won = False
            globals.running = False