from __future__ import annotations
from typing import TYPE_CHECKING, Type, TypeVar, Optional
import warnings

if TYPE_CHECKING:
    from pyre.components import BaseComponent
    from pyre.systems import (
        BaseSystem,
        TransformSystem,
        RenderSystem,
        CollisionSystem,
        MovementSystem,
    )


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
            warnings.warn(
                "Attempted to create another instance of SystemManager (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return

        SystemManager.__instance = self
        self.transformSys: TransformSystem = None
        self.renderSys: RenderSystem = None
        self.collisionSys: CollisionSystem = None
        self.movementSys: MovementSystem = None

        self.m_componentsToSystems: dict[Type["BaseComponent"], "BaseSystem"] = {}
        self.m_systemsToClasses: dict[Type["BaseSystem"], "BaseSystem"] = {}

    def Init(self) -> None:
        from pyre.components import Transform, Sprite, Movement
        from pyre.components.colliders import BaseCollider
        from pyre.systems import (
            TransformSystem,
            RenderSystem,
            CollisionSystem,
            MovementSystem,
        )

        self.transformSys = TransformSystem.GetInstance()
        self.renderSys = RenderSystem.GetInstance()
        self.collisionSys = CollisionSystem.GetInstance()
        self.movementSys = MovementSystem.GetInstance()

        self.m_componentsToSystems = {
            Transform: self.transformSys,
            Sprite: self.renderSys,
            BaseCollider: self.collisionSys,
            Movement: self.movementSys,
        }

        self.m_systemsToClasses = {
            TransformSystem: self.transformSys,
            RenderSystem: self.renderSys,
            CollisionSystem: self.collisionSys,
            MovementSystem: self.movementSys,
        }

    def GetSystemInstanceForComponent(
        self, comp: "BaseComponent"
    ) -> "BaseSystem" | None:
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