import pygame


class Window:
    __instance = None

    def __new__(cls, *args, **kwargs) -> "Window":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
        self,
        *,
        width: int,
        height: int,
        title: str,
    ) -> None:

        if not hasattr(self, "m_width"):
            self.m_width = width
            self.m_height = height
            self.m_title = title

            self.m_surface = None

    @staticmethod
    def GetInstance() -> "Window":
        if Window.__instance is None:
            Window()
        return Window.__instance

    def Init(self) -> None:
        self.m_surface = pygame.display.set_mode((self.m_width, self.m_height))
        pygame.display.set_caption(self.m_title)