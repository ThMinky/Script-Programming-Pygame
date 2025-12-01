from dataclasses import dataclass

import pygame


@dataclass
class SpriteData:
    surface: pygame.Surface
    path: str


@dataclass
class SpriteSheetData:
    surfaces: list[pygame.Surface]
    spriteSize: tuple[int, int]
    sheetRowsCols: tuple[int, int]
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
            self._m_spriteSheets: dict[str, SpriteSheetData] = {}

    @staticmethod
    def GetInstance() -> "SpriteManager":
        if SpriteManager.__instance is None:
            SpriteManager()
        return SpriteManager.__instance

    # //////////////////////////////////////////////////
    # Sprite
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

    # //////////////////////////////////////////////////

    # //////////////////////////////////////////////////
    # Sprite Sheet
    def RegisterSpriteSheet(self, key: str, path: str, spriteSize: tuple[int, int]) -> None:
        if key in self._m_spriteSheets:
            return

        surfaces = []
        sheetRowsCols = ()
        for _, spriteSheetData in self._m_spriteSheets.items():
            if spriteSheetData.path == path:
                surfaces = spriteSheetData.surfaces
                sheetRowsCols = spriteSheetData.sheetRowsCols
                break

        if not surfaces:
            if surface.get_width() % spriteSize[0] != 0 or surface.get_height() % spriteSize[1] != 0:
                raise ValueError("Sprite size does not evenly divide the sheet")
            
            surface = pygame.image.load(path).convert_alpha()
            rows = surface.get_height() // spriteSize[1]
            cols = surface.get_width() // spriteSize[0]

            for row in range(rows):
                for col in range(cols):
                    rect = pygame.Rect(col * spriteSize[0], row * spriteSize[1], spriteSize[0], spriteSize[1])
                    surfaces.append(surface.subsurface(rect).copy())

            sheetRowsCols = rows, cols

        self._m_spriteSheets[key] = SpriteSheetData(
            surfaces=surfaces,
            spriteSize=spriteSize,
            sheetRowsCols=sheetRowsCols,
            path=path,
        )

    def GetSpriteSheet(self, key: str) -> list[pygame.Surface] | None:
        if key in self._m_spriteSheets:
            return self._m_spriteSheets[key].surfaces
        return None

    def UnregisterSpriteSheet(self, key: str) -> None:
        if key not in self._m_spriteSheets:
            return

        del self._m_spriteSheets[key]

    # //////////////////////////////////////////////////