from dataclasses import dataclass

import pygame


@dataclass
class SoundData:
    sound: pygame.mixer.Sound
    path: str


class SoundManager:
    __instance = None

    def __new__(cls) -> "SoundManager":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_sounds"):
            self._m_sounds: dict[str, SoundData] = {}

    @staticmethod
    def GetInstance() -> "SoundManager":
        if SoundManager.__instance is None:
            SoundManager()
        return SoundManager.__instance

    def RegisterSound(self, key: str, path: str) -> None:
        if key in self._m_sounds:
            return

        sound = None
        for _, soundData in self._m_sounds.items():
            if soundData.path == path:
                sound = soundData.sound
                break

        if not sound:
            sound = pygame.mixer.Sound(path)

        self._m_sounds[key] = SoundData(
            sound=sound,
            path=path,
        )

    def GetSound(self, key: str) -> pygame.mixer.Sound | None:
        if key in self._m_sounds:
            return self._m_sounds[key].sound
        return None

    def UnregisterSound(self, key: str) -> None:
        if key not in self._m_sounds:
            return

        del self._m_sounds[key]

    def PlaySound(self, key: str, loops: int = 0, maxtime: int = 0, fade_ms: int = 0) -> None:
        sound = self.GetSound(key)

        if sound:
            if maxtime == 0:
                maxtime = int(sound.get_length() * 1000)

            sound.play(loops=loops, maxtime=maxtime, fade_ms=fade_ms)
