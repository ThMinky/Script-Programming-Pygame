from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def Execute(self, *args, **kwargs) -> None:
        pass