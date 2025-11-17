from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyre.entities import Entity


class BaseComponent:
    def __init__(self) -> None:
        self.m_parent: "Entity" = None

    def Init(self) -> None:
        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceForComponent(self)

        if system:
            system.Register(self)

    def Uninit(self) -> None:
        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceForComponent(self)

        if system:
            system.Unregister(self)