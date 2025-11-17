from __future__ import annotations
from typing import TYPE_CHECKING
import warnings

from pyre.systems import BaseSystem

if TYPE_CHECKING:
    from pyre.components import BaseComponent, Transform


class TransformSystem(BaseSystem):
    __instance = None

    def GetInstance() -> "TransformSystem":
        if TransformSystem.__instance is None:
            TransformSystem()
        return TransformSystem.__instance

    def __init__(self) -> None:
        if TransformSystem.__instance is not None:
            warnings.warn(
                "Attempted to create another instance of TransformSystem (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return

        TransformSystem.__instance = self
        self.m_comps: list["Transform"] = []

    def Register(self, comp: "BaseComponent") -> None:
        from pyre.components import Transform

        if isinstance(comp, Transform):
            if comp not in self.m_comps:
                self.m_comps.append(comp)

    def Unregister(self, comp: "BaseComponent") -> None:
        if comp in self.m_comps:
            self.m_comps.remove(comp)

    def Update(self, dt) -> None:
        super().Update(dt)

        for transform in self.m_comps:
            if transform.m_parentTransform is None:
                self._UpdateHierarchy(transform)

    def _UpdateHierarchy(self, transformComp: "Transform") -> None:
        if not transformComp.m_isStatic:
            transformComp.UpdateWorldTransform()
        for child in transformComp.m_childrenTransforms:
            self._UpdateHierarchy(child)