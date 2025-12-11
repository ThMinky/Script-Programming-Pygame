from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.components import BaseComponent

if TYPE_CHECKING:
    from pyre.components import Sprite
    from pyre.managers import AnimationData
    from pyre.timer import Timer


class AnimatedSprite(BaseComponent):
    def __init__(
        self,
        *,
        animationKey: str,
    ) -> None:
        super().__init__()

        self.m_animationKey: str = animationKey
        self.m_animation: "AnimationData" | None = None
        self.m_frameIndex: int = 0
        self.m_finished: bool = False

        self.m_sprite: "Sprite" | None = None

        self.m_timer: "Timer" | None = None

    def _Init(self) -> None:
        super()._Init()

        from pyre.components import Sprite
        from pyre.managers import AnimationManager
        from pyre.timer import Timer

        self.m_animation = AnimationManager.GetInstance().GetAnimation(self.m_animationKey)

        if self.m_animation is None:
            raise RuntimeError(f"Animation '{self.m_animationKey}' not found")

        self.m_sprite = self.m_parent.GetComponentByType(Sprite)

        if self.m_sprite is None:
            raise RuntimeError("AnimatedSprite requires a Sprite component")

        self.m_timer = Timer(self.m_animation.frameTime)

        self._ApplyFrame(0)

    def _Uninit(self) -> None:
        self.m_animation = None
        self.m_sprite = None

        super()._Uninit()

    def Enable(self) -> None:
        super().Enable()

    def Disable(self) -> None:
        super().Disable()

    def Destroy(self) -> None:
        super().Destroy()

    def SetAnimation(self, key: str, reset: bool = True) -> None:
        from pyre.managers import AnimationManager

        anim = AnimationManager.GetInstance().GetAnimation(key)

        if anim is None:
            raise RuntimeError(f"Animation '{key}' not found")

        if self.m_animationKey == key and not reset:
            return

        self.m_animationKey = key
        self.m_animation = anim
        self.m_frameIndex = 0
        self.m_finished = False

        self.m_timer = Timer(anim.frameTime)

        self._ApplyFrame(0)

    def Advance(self) -> None:
        if self.m_animation is None:
            return

        if self.m_sprite is None:
            return

        if not self.m_timer.Tick():
            return

        self.m_timer.Reset()
        self.m_frameIndex += 1

        if self.m_frameIndex >= len(self.m_animation.frames):
            if self.m_animation.loop:
                self.m_frameIndex = 0
            else:
                self.m_finished = True
                return

        self._ApplyFrame(self.m_frameIndex)

    def _ApplyFrame(self, frameIndex: int) -> None:
        frameKey = self.m_animation.frames[frameIndex]
        self.m_sprite.SetSprite(frameKey)