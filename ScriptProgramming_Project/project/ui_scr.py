import globals

from pyre.components.scripts import MonoScript
from pyre.time import Time


class UIScr(MonoScript):
    __instance = None

    def __new__(cls, *args, **kwargs) -> "UIScr":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        super().__init__()

        from pyre.systems.render_system import RenderSystem

        if not hasattr(self, "m_playerHp"):
            # Vars
            self.m_playerHp: float = 3
            self.m_playerAmmo: int = 1

            self.m_baseHp: float = 10
            self.m_baseAmmo: int = 12

            self.m_timer_start = 3 * 60 + 6
            self.m_timer_current = self.m_timer_start

            RenderSystem.GetInstance().m_uiScr = self

    @staticmethod
    def GetInstance() -> "UIScr":
        if UIScr.__instance is None:
            UIScr()
        return UIScr.__instance

    def Start(self):
        pass

    def Update(self):
        if self.m_timer_current <= 0:
            globals.won = True
            globals.running = False

        self.m_timer_current -= Time.deltaTime

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def Destroy(self):
        super().Destroy()