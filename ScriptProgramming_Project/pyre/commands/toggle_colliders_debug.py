from pyre.commands.command import Command


class ToggleCollidersDebug(Command):
    def __init__(self) -> None:
        from pyre.managers.system_manager import SystemManager
        from pyre.systems import RenderSystem

        self.m_renderSys = SystemManager.GetInstance().GetSystemInstance(RenderSystem)

    def Execute(self) -> None:
        if self.m_renderSys:
            self.m_renderSys.m_debugColliders = not self.m_renderSys.m_debugColliders