from typing import Callable, Any


class Event:
    def __init__(self) -> None:
        self._m_listeners: list[Callable[..., Any]] = []

    def Add(self, callback: Callable[..., Any]) -> None:
        if callback not in self._m_listeners:
            self._m_listeners.append(callback)

    def Remove(self, callback: Callable[..., Any]) -> None:
        if callback in self._m_listeners:
            self._m_listeners.remove(callback)

    def Fire(self, *args, **kwargs) -> None:
        for listener in self._m_listeners:
            listener(*args, **kwargs)