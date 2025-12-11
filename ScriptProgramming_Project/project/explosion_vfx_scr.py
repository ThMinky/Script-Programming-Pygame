from __future__ import annotations
from typing import TYPE_CHECKING

from pyre.components import AnimatedSprite
from pyre.components.scripts import MonoScript

if TYPE_CHECKING:
    from scene import Scene


class ExplosionVFXScr(MonoScript):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None  # Auto assign

    def Start(self) -> None:
        pass

    def Update(self) -> None:
        anim_comp = self.m_parent.GetComponentByType(AnimatedSprite)
        if not anim_comp:
            return

        anim_comp.Advance()

        if anim_comp.m_finished:

            if self.m_parent in self.m_scene.m_vfx:
                self.m_scene.m_vfx.remove(self.m_parent)

            self.m_parent.Destroy()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def Destroy(self) -> None:
        super().Destroy()
