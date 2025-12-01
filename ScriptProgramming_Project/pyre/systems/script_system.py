from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pyre.components import Script


class ScriptSystem:
    __instance = None

    def __new__(cls) -> "ScriptSystem":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_scripts"):
            self._m_scripts: list["Script"] = []
            self._m_to_add: list["Script"] = []
            self._m_to_remove: list["Script"] = []
            self._m_pending_starts: list[Script] = []

    @staticmethod
    def GetInstance() -> "ScriptSystem":
        if ScriptSystem.__instance is None:
            ScriptSystem()
        return ScriptSystem.__instance

    def Register(self, script: "Script") -> None:
        from pyre.components.scripts import BaseScript

        if isinstance(script, BaseScript):
            if script not in self._m_to_add:
                if script not in self._m_scripts:
                    self._m_to_add.append(script)

    def Unregister(self, script: "Script") -> None:
        from pyre.components import Script

        if isinstance(script, Script):
            if script not in self._m_to_remove:
                self._m_to_remove.append(script)

    def Update(self) -> None:
        self._FlushChanges()

        for script in self._m_scripts:
            script.Update()

    def _FlushChanges(self):
        for script in self._m_to_add:
            script.Awake()
            self._m_pending_starts.append(script)

        self._m_scripts.extend(self._m_to_add)
        self._m_to_add.clear()

        for script in self._m_pending_starts:
            if script.m_enabled:
                script.Start()
        self._m_pending_starts.clear()

        for script in self._m_to_remove:
            if script in self._m_scripts:
                self._m_scripts.remove(script)
        self._m_to_remove.clear()