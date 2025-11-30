import pygame


class InputManager:
    __instance = None

    @staticmethod
    def GetInstance() -> "InputManager":
        if InputManager.__instance is None:
            InputManager()
        return InputManager.__instance

    def __init__(self) -> None:
        if InputManager.__instance is not None:
            return

        InputManager.__instance = self
        self._keys_held: dict[int, bool] = {}
        self._keys_pressed: set[int] = set()
        self._keys_released: set[int] = set()

    def Update(self) -> None:
        self._keys_pressed.clear()
        self._keys_released.clear()

        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP]):
            if event.type == pygame.KEYDOWN:
                self._keys_held[event.key] = True
                self._keys_pressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self._keys_held[event.key] = False
                self._keys_released.add(event.key)

    def GetKey(self, key: int) -> bool:
        return self._keys_held.get(key, False)

    def GetKeyDown(self, key: int) -> bool:
        return key in self._keys_pressed

    def GetKeyUp(self, key: int) -> bool:
        return key in self._keys_released