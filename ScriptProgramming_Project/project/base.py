# Engine
from pyre.components.scripts import BaseScript

# Project
from project.interfaces import IDamagable


class Base(BaseScript, IDamagable):
    def __init__(self):
        super().__init__()

        self.m_hp: int = 20

    def Start(self):
        pass

    def Update(self):
        pass

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def TakeDamage(self, amount: int) -> None:
        self.m_hp -= amount

        if self.m_hp <= 0:
            self.m_parent.Destroy()