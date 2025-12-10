from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyre.components.scripts import MonoScript


class ScriptSystem:
    __instance = None

    def __new__(cls) -> "ScriptSystem":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_scripts"):
            self._m_scripts: list["MonoScript"] = []
            self._m_to_add: list["MonoScript"] = []
            self._m_to_remove: list["MonoScript"] = []
            self._m_pending_starts: list["MonoScript"] = []

    @staticmethod
    def GetInstance() -> "ScriptSystem":
        if ScriptSystem.__instance is None:
            ScriptSystem()
        return ScriptSystem.__instance

    def Register(self, script: "MonoScript") -> None:
        from pyre.components.scripts import MonoScript

        if isinstance(script, MonoScript):
            if script not in self._m_to_add:
                if script not in self._m_scripts:
                    self._m_to_add.append(script)

    def Unregister(self, script: "MonoScript") -> None:
        from pyre.components.scripts import MonoScript

        if isinstance(script, MonoScript):
            if script not in self._m_to_remove:
                self._m_to_remove.append(script)

    def Update(self) -> None:
        self._FlushChanges()

        for script in self._m_scripts:
            script.Update()

    def _FlushChanges(self):
        for script in self._m_to_add:
            self._m_scripts.append(script)
            if not getattr(script, "_m_started", False):
                self._m_pending_starts.append(script)
        self._m_to_add.clear()

        for script in self._m_pending_starts:
            script.Start()
            script._m_started = True
        self._m_pending_starts.clear()

        for script in self._m_to_remove:
            if script in self._m_scripts:
                self._m_scripts.remove(script)
        self._m_to_remove.clear()