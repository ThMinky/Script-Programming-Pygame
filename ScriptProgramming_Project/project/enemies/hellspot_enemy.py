from pyre.components.scripts import BaseScript


class HellspotEnemy(BaseScript):
    def __init__(self):
        super().__init__()

        self.m_hp: int = 6

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

            if self.m_parent in self.m_scene.m_enemies:
                self.m_scene.m_enemies.remove(self.m_parent)

            self.m_parent.Destroy()