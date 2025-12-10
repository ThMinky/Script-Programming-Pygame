from __future__ import annotations
from typing import TYPE_CHECKING

from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from pyre.components import BaseComponent


class BaseSystem(ABC):
    @abstractmethod
    def Register(self, comp: "BaseComponent") -> None:
        pass

    @abstractmethod
    def Unregister(self, comp: "BaseComponent") -> None:
        pass