from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyre.entities import Entity


class BaseComponent:
    def __init__(self) -> None:
        self.m_parent: "Entity" | None = None
        self.m_enabled: bool = True

    def Init(self) -> None:
        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceByComponent(self)

        if system:
            system.Register(self)

    def Uninit(self) -> None:
        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceByComponent(self)

        if system:
            system.Unregister(self)

    def Enable(self) -> None:
        if self.m_enabled:
            return

        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceByComponent(self)

        if system:
            system.Register(self)

        self.m_enabled = True

    def Disable(self) -> None:
        if not self.m_enabled:
            return

        from pyre.managers.system_manager import SystemManager

        system = SystemManager.GetInstance().GetSystemInstanceByComponent(self)

        if system:
            system.Unregister(self)

        self.m_enabled = False

    def Destroy(self) -> None:
        self.m_parent.RemoveComponent(self)