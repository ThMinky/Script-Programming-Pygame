import pygame

from pyre.command import Command


class ToggleFpsDebug(Command):
    __instance = None

    def __new__(cls) -> "ToggleFpsDebug":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "m_renderSys"):
            from pyre.managers import SystemManager
            from pyre.systems import RenderSystem

            self.m_renderSys = SystemManager.GetInstance().GetSystemInstanceByType(RenderSystem)

    @staticmethod
    def GetInstance() -> "ToggleFpsDebug":
        if ToggleFpsDebug.__instance is None:
            ToggleFpsDebug()
        return ToggleFpsDebug.__instance

    def Execute(self) -> None:
        if self.m_renderSys:
            self.m_renderSys.m_debugFPS = not self.m_renderSys.m_debugFPS
