import time

import pygame


class Time:
    deltaTime: float = 0.0
    timeSinceStart: float = 0.0
    frameCount: int = 0

    _last_time: float = time.time()

    @staticmethod
    def Update() -> None:
        now = time.time()
        Time.deltaTime = now - Time._last_time
        Time.timeSinceStart += Time.deltaTime
        Time._last_time = now
        Time.frameCount += 1

    @staticmethod
    def GetFPS() -> float:
        if Time.deltaTime > 0:
            return 1.0 / Time.deltaTime
        return 0.0

    @staticmethod
    def DrawFPS(surface: pygame.Surface) -> None:
        font = pygame.font.SysFont(None, 24)
        fpsText = font.render(f"FPS: {int(1 / Time.deltaTime)}", True, (255, 0, 0))
        surface.blit(fpsText, (7, 7))