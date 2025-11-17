import pygame


class Window:
    def __init__(self, width: int, height: int, title: str) -> None:
        self.m_width = width
        self.m_height = height
        self.m_title = title

        self.m_surface = None

    def Init(self) -> None:
        self.m_surface = pygame.display.set_mode((self.m_width, self.m_height))
        self.m_surface.fill("black")
        pygame.display.set_caption(self.m_title)

    def Get(self) -> pygame.Surface:
        return self.m_surface