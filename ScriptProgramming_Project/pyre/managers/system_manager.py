from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar, Optional, cast

if TYPE_CHECKING:
    from pyre.components import BaseComponent
    from pyre.systems import BaseSystem, CollisionSystem, RenderSystem, ScriptSystem

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
        self.m_collisionSys: Optional[CollisionSystem] = None
        self.m_renderSys: Optional[RenderSystem] = None
        self.m_scriptSys: Optional[ScriptSystem] = None

        self.m_componentsToSystems: dict[Type["BaseComponent"], "BaseSystem"] = {}
        self.m_systemsToClasses: dict[Type["BaseSystem"], "BaseSystem"] = {}

    def Init(self) -> None:
        from pyre.components import Script, Sprite
        from pyre.components.colliders import BaseCollider
        from pyre.systems import CollisionSystem, RenderSystem, ScriptSystem

        self.m_collisionSys = CollisionSystem.GetInstance()
        self.m_renderSys = RenderSystem.GetInstance()
        self.m_scriptSys = ScriptSystem.GetInstance()

        self.m_componentsToSystems = {
            Script: self.m_scriptSys,
            Sprite: self.m_renderSys,
            BaseCollider: self.m_collisionSys,
        }

        self.m_systemsToClasses = {
            CollisionSystem: self.m_collisionSys,
            RenderSystem: self.m_renderSys,
            ScriptSystem: self.m_scriptSys,
        }

    def GetSystemInstanceForComponent(self, comp: "BaseComponent") -> Optional[BaseSystem]:
        for compType, system in self.m_componentsToSystems.items():
            if isinstance(comp, compType):
                return system
        return None

    def GetSystemInstance(self, systemType: type[T]) -> Optional[T]:
        return cast(Optional[T], self.m_systemsToClasses.get(systemType))