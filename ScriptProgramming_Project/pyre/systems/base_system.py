from abc import ABC, abstractmethod

from pyre.components import BaseComponent


class BaseSystem(ABC):
    @abstractmethod
    def Register(self, comp: BaseComponent) -> None:
        pass

    @abstractmethod
    def Unregister(self, comp: BaseComponent) -> None:
        pass

    def Update(self, dt: float) -> None:
        pass