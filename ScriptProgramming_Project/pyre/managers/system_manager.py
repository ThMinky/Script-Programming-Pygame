from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar, Optional

if TYPE_CHECKING:
    from pyre.components import BaseComponent
    from pyre.systems import BaseSystem, RenderSystem, CollisionSystem


T = TypeVar("T", bound="BaseSystem")


class SystemManager:
    __instance = None

    @staticmethod
    def GetInstance() -> "SystemManager":
        if SystemManager.__instance is None:
            SystemManager()
        return SystemManager.__instance

    def __init__(self) -> None:
        if SystemManager.__instance is not None:
            return

        SystemManager.__instance = self
        self.renderSys: RenderSystem = None
        self.collisionSys: CollisionSystem = None

        self.m_componentsToSystems: dict[Type["BaseComponent"], "BaseSystem"] = {}
        self.m_systemsToClasses: dict[Type["BaseSystem"], "BaseSystem"] = {}

    def Init(self) -> None:
        from pyre.components import Sprite
        from pyre.components.colliders import BaseCollider
        from pyre.systems import RenderSystem, CollisionSystem

        self.renderSys = RenderSystem.GetInstance()
        self.collisionSys = CollisionSystem.GetInstance()

        self.m_componentsToSystems = {
            Sprite: self.renderSys,
            BaseCollider: self.collisionSys,
        }

        self.m_systemsToClasses = {
            RenderSystem: self.renderSys,
            CollisionSystem: self.collisionSys,
        }

    def GetSystemInstanceForComponent(self, comp: "BaseComponent") -> "BaseSystem" | None:
        for compType, system in self.m_componentsToSystems.items():
            if isinstance(comp, compType):
                return system
        return None

    def GetSystemInstance(self, systemType: type[T]) -> Optional[T]:
        system = self.m_systemsToClasses.get(systemType)
        if isinstance(system, systemType):
            return system
        else:
            return None