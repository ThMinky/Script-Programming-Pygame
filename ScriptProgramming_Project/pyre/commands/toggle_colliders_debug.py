from pyre.commands.command import Command


class ToggleCollidersDebug(Command):
    __instance = None

    @staticmethod
    def GetInstance() -> "ToggleCollidersDebug":
        if ToggleCollidersDebug.__instance is None:
            ToggleCollidersDebug()
        return ToggleCollidersDebug.__instance

    def __init__(self) -> None:
        if ToggleCollidersDebug.__instance is not None:
            return
        
        ToggleCollidersDebug.__instance = self
        from pyre.managers.system_manager import SystemManager
        from pyre.systems import RenderSystem

        self.m_renderSys = SystemManager.GetInstance().GetSystemInstance(RenderSystem)

    def Execute(self) -> None:
        if self.m_renderSys:
            self.m_renderSys.m_debugColliders = not self.m_renderSys.m_debugColliders