from pyre.command import Command


class ToggleCollidersDebug(Command):
    __instance = None

    def __new__(cls) -> "ToggleCollidersDebug":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "m_renderSys"): 
            from pyre.managers import SystemManager
            from pyre.systems import RenderSystem

            self.m_renderSys = SystemManager.GetInstance().GetSystemInstanceByType(RenderSystem)

    @staticmethod
    def GetInstance() -> "ToggleCollidersDebug":
        if ToggleCollidersDebug.__instance is None:
            ToggleCollidersDebug()
        return ToggleCollidersDebug.__instance

    def Execute(self) -> None:
        if self.m_renderSys:
            self.m_renderSys.m_debugColliders = not self.m_renderSys.m_debugColliders