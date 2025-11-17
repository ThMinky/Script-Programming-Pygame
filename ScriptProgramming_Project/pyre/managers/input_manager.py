import warnings

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
            warnings.warn(
                "Attempted to create another instance of InputManager (singleton violation)",
                category=UserWarning,
                stacklevel=2,
            )
            return

        InputManager.__instance = self
        self.m_heldKeys: dict[str, bool] = {}
        self.m_singlePressKeys: set[str] = set()
        self.m_pressedThisFrame: set[str] = set()
        self.m_quit: bool = False

    def Init(self) -> None:
        self.m_heldKeys = {
            "W": False,
            "A": False,
            "S": False,
            "D": False,
            "Q": False,
            "E": False,
        }
        self.m_singlePressKeys = {"C", "SPACE"}
        self.m_pressedThisFrame = set()
        self.m_quit = False

    def Update(self) -> None:
        self.m_pressedThisFrame.clear()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.m_quit = True
            elif event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key).upper()
                if key_name in self.m_singlePressKeys:
                    self.m_pressedThisFrame.add(key_name)

        keys = pygame.key.get_pressed()
        for key in self.m_heldKeys:
            self.m_heldKeys[key] = keys[getattr(pygame, f"K_{key.lower()}")]

    def IsKeyHeld(self, key: str) -> bool:
        return self.m_heldKeys.get(key.upper(), False)

    def IsKeyPressed(self, key: str) -> bool:
        return key.upper() in self.m_pressedThisFrame

    def QuitRequested(self) -> bool:
        return self.m_quit