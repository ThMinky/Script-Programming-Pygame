import math

import pygame

from pyre.components.colliders import BaseCollider


class BoxCollider(BaseCollider):
    def __init__(
        self,
        *,
        offset: pygame.Vector2 | None = None,
        size: pygame.Vector2 | None = None
    ) -> None:
        super().__init__(offset=offset)

        self.m_size: pygame.Vector2 = size if size is not None else None

    def Init(self) -> None:
        super().Init()

    def Uninit(self) -> None:
        super().Uninit()

    def DirtyUpdate(self) -> None:
        super().DirtyUpdate()

        from pyre.components import Transform, Sprite

        transformComp = self.m_parent.GetComponent(Transform)
        spriteComp = self.m_parent.GetComponent(Sprite)

        if self.m_size is None:
            if spriteComp:
                textureSize = pygame.Vector2(spriteComp.m_originalTexture.get_size())
                self.m_size = textureSize.elementwise() * transformComp.m_worldScale.elementwise()
            else:
                self.m_size = pygame.Vector2(1, 1)
        
        self.m_isDirty = False

    def DrawBounds(self, surface: pygame.Surface) -> None:
        rect = pygame.Rect(
            int(self.m_worldPos.x),
            int(self.m_worldPos.y),
            int(self.m_size.x),
            int(self.m_size.y),
        )

        pygame.draw.rect(surface, (255, 0, 0), rect, 1)

    def GetRotatedCorners(self) -> list[pygame.Vector2]:
        from pyre.components import Transform

        w, h = self.m_size.x / 2, self.m_size.y / 2
        localCorners = [
            pygame.Vector2(-w, -h),
            pygame.Vector2(w, -h),
            pygame.Vector2(w, h),
            pygame.Vector2(-w, h),
        ]

        angleRad = math.radians(self.m_parent.GetComponent(Transform).m_worldRot)
        cosA = math.cos(angleRad)
        sinA = math.sin(angleRad)

        rotatedCorners = []
        for corner in localCorners:
            rotatedX = corner.x * cosA - corner.y * sinA
            rotatedY = corner.x * sinA + corner.y * cosA

            worldCorner = pygame.Vector2(rotatedX, rotatedY) + self.m_worldPos
            rotatedCorners.append(worldCorner)

        return rotatedCorners