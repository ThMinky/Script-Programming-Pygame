from dataclasses import dataclass

import pygame


@dataclass
class SpriteData:
    surface: pygame.Surface
    path: str


class SpriteManager:
    __instance = None

    def __new__(cls) -> "SpriteManager":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_sprites"):
            self._m_sprites: dict[str, SpriteData] = {}

    @staticmethod
    def GetInstance() -> "SpriteManager":
        if SpriteManager.__instance is None:
            SpriteManager()
        return SpriteManager.__instance

    def RegisterSprite(self, key: str, path: str) -> None:
        if key in self._m_sprites:
            return

        surface = None
        for _, spriteData in self._m_sprites.items():
            if spriteData.path == path:
                surface = spriteData.surface
                break

        if not surface:
            surface = pygame.image.load(path).convert_alpha()

        self._m_sprites[key] = SpriteData(
            surface=surface,
            path=path,
        )

    def GetSprite(self, key: str) -> pygame.Surface | None:
        if key in self._m_sprites:
            return self._m_sprites[key].surface
        return None

    def UnregisterSprite(self, key: str) -> None:
        if key not in self._m_sprites:
            return

        del self._m_sprites[key]