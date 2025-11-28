import pygame

from pyre.commands.command import Command


class ToggleFpsDebug(Command):
    __instance = None

    @staticmethod
    def GetInstance() -> "ToggleFpsDebug":
        if ToggleFpsDebug.__instance is None:
            ToggleFpsDebug()
        return ToggleFpsDebug.__instance

    def __init__(self) -> None:
        if ToggleFpsDebug.__instance is not None:
            return

        ToggleFpsDebug.__instance = self
        from pyre.managers.system_manager import SystemManager
        from pyre.systems import RenderSystem

        self.m_renderSys = SystemManager.GetInstance().GetSystemInstance(RenderSystem)

    def Execute(self) -> None:
        if self.m_renderSys:
            self.m_renderSys.m_debugFPS = not self.m_renderSys.m_debugFPS
