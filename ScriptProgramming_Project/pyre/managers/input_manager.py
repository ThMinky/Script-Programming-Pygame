import pygame


class InputManager:
    __instance = None

    def __new__(cls) -> "InputManager":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_mousePos"):
            self._mousePos: pygame.Vector2 = pygame.Vector2(0, 0)

            self._keysHeld: dict[int, bool] = {}
            self._keysPressed: set[int] = set()
            self._keysReleased: set[int] = set()

    @staticmethod
    def GetInstance() -> "InputManager":
        if InputManager.__instance is None:
            InputManager()
        return InputManager.__instance

    def Update(self) -> None:
        self._keysPressed.clear()
        self._keysReleased.clear()

        for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEMOTION]):
            if event.type == pygame.KEYDOWN:
                self._keysHeld[event.key] = True
                self._keysPressed.add(event.key)
            elif event.type == pygame.KEYUP:
                self._keysHeld[event.key] = False
                self._keysReleased.add(event.key)
            elif event.type == pygame.MOUSEMOTION:
                self._mousePos.update(event.pos)

    def GetKey(self, key: int) -> bool:
        return self._keysHeld.get(key, False)

    def GetKeyDown(self, key: int) -> bool:
        return key in self._keysPressed

    def GetKeyUp(self, key: int) -> bool:
        return key in self._keysReleased

    def GetMousePosition(self) -> pygame.Vector2:
        return self._mousePos.copy()