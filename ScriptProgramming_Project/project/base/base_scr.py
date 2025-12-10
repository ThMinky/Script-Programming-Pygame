from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.components.scripts import MonoScript

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from scene import Scene


class BaseScr(MonoScript, IDamagable):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None # Auto assign

        # Vars
        self.m_hp: float = 20
        
        self.m_autoTurretAmmo: int = 16

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        pass

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def TakeDamage(self, amount: float) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:

            self.m_scene.m_baseRoot = None

            self.m_parent.Destroy()