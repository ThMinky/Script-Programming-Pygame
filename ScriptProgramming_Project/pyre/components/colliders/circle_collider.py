import pygame

from pyre.components.colliders import BaseCollider


class CircleCollider(BaseCollider):
    def __init__(
        self, *, offset: pygame.Vector2 | None = None, radius: float | None = None
    ) -> None:
        super().__init__(offset=offset)

        self.m_radius: float = radius if radius is not None else None

    def Init(self) -> None:
        super().Init()

    def Uninit(self) -> None:
        super().Uninit()

    def DirtyUpdate(self) -> None:
        super().DirtyUpdate()

        from pyre.components import Transform, Sprite

        transformComp = self.m_parent.GetComponent(Transform)
        spriteComp = self.m_parent.GetComponent(Sprite)

        if self.m_radius is None:
            if spriteComp:
                textureSize = pygame.Vector2(spriteComp.m_originalTexture.get_size())
                self.m_radius = (
                    max(
                        (
                            textureSize.x * transformComp.m_worldScale.x,
                            textureSize.y * transformComp.m_worldScale.y,
                        )
                    )
                    / 2
                )
            else:
                self.m_radius = 1.0

        self.m_isDirty = False

    def DrawBounds(self, renderer: pygame.Surface) -> None:
        pygame.draw.circle(
            renderer,
            (255, 0, 0),
            (self.m_worldPos.x, self.m_worldPos.y),
            self.m_radius,
            1,
        )