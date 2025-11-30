from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar, cast

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
        self._m_collisionSys: "CollisionSystem" | None = None
        self._m_renderSys: "RenderSystem" | None = None
        self._m_scriptSys: "ScriptSystem" | None = None

        self._m_componentsToSystems: dict[Type["BaseComponent"], "BaseSystem"] = {}
        self._m_typesToSystems: dict[Type["BaseSystem"], "BaseSystem"] = {}

    def Init(self) -> None:
        from pyre.components import Sprite
        from pyre.components.scripts import BaseScript
        from pyre.components.colliders import BaseCollider
        from pyre.systems import CollisionSystem, RenderSystem, ScriptSystem

        self._m_collisionSys = CollisionSystem.GetInstance()
        self._m_renderSys = RenderSystem.GetInstance()
        self._m_scriptSys = ScriptSystem.GetInstance()

        self._m_componentsToSystems = {
            BaseScript: self._m_scriptSys,
            Sprite: self._m_renderSys,
            BaseCollider: self._m_collisionSys,
        }

        self._m_typesToSystems = {
            CollisionSystem: self._m_collisionSys,
            RenderSystem: self._m_renderSys,
            ScriptSystem: self._m_scriptSys,
        }

    def GetSystemInstanceByComponent(self, comp: "BaseComponent") -> T | None:
        for compType, system in self._m_componentsToSystems.items():
            if isinstance(comp, compType):
                return system
        return None

    def GetSystemInstanceByType(self, systemType: type[T]) -> T | None:
        system = self._m_typesToSystems.get(systemType)
        return cast(T | None, system)