from dataclasses import dataclass, field


@dataclass
class AnimationData:
    key: str
    frameTime: float
    loop: bool
    frames: list[str] = field(default_factory=list)


class AnimationManager:
    __instance = None

    def __new__(cls) -> "AnimationManager":
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        if not hasattr(self, "_m_animations"):
            self._m_animations: dict[str, AnimationData] = {}

    @staticmethod
    def GetInstance() -> "AnimationManager":
        if AnimationManager.__instance is None:
            AnimationManager()
        return AnimationManager.__instance

    def RegisterAnimation(self, key: str, frames: list[str], frameTime: float, loop: bool = False) -> None:
        if key in self._m_animations:
            return

        self._m_animations[key] = AnimationData(
            key=key,
            frameTime=frameTime,
            loop=loop,
            frames=frames,
        )

    def GetAnimation(self, key: str) -> AnimationData | None:
        if key in self._m_animations:
            return self._m_animations[key]
        return None

    def UnregisterAnimation(self, key: str) -> None:
        if key not in self._m_animations:
            return

        del self._m_animations[key]