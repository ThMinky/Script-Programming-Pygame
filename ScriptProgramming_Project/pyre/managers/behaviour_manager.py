from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyre.behaviours import Behaviour


class BehaviourManager:
    __instance = None

    @staticmethod
    def GetInstance() -> "BehaviourManager":
        if BehaviourManager.__instance is None:
            BehaviourManager()
        return BehaviourManager.__instance

    def __init__(self) -> None:
        if BehaviourManager.__instance is not None:
            return

        BehaviourManager.__instance = self
        self._m_behaviours: list["Behaviour"] = []
        self._m_to_add: set["Behaviour"] = ()
        self._m_to_remove: set["Behaviour"] = ()

    def Register(self, behaviour: "Behaviour") -> None:
        from pyre.behaviours import Behaviour

        if isinstance(behaviour, Behaviour):
            if behaviour not in self._m_to_add:
                if behaviour not in self._m_behaviours:
                    self._m_to_add.append(behaviour)

    def Unregister(self, behaviour: "Behaviour") -> None:
        from pyre.behaviours import Behaviour

        if isinstance(behaviour, Behaviour):
            if behaviour not in self._m_to_remove:
                self._m_to_remove.append(behaviour)

    def Update(self) -> None:
        self._FlushChanges()

        for behaviour in self._m_behaviours:
            behaviour.Update()

    def _FlushChanges(self):
        for behaviour in self._m_to_remove:
            if behaviour in self._m_behaviours:
                self._m_behaviours.remove(behaviour)
        self._m_to_remove.clear()

        self._m_behaviours.extend(self._m_to_add)
        self._m_to_add.clear()