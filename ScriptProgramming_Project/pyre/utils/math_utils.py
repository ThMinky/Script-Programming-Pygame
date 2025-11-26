from enum import Enum, auto

import math
import pygame


class ERectPivots(Enum):
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_LEFT = auto()
    TOP_CENTER = auto()
    RIGHT_CENTER = auto()
    BOTTOM_CENTER = auto()
    LEFT_CENTER = auto()
    CENTER = auto()


RECT_PIVOT_OFFSETS_FROM_CENTER: dict[ERectPivots, pygame.Vector2] = {
    ERectPivots.TOP_LEFT: pygame.Vector2(-0.5, -0.5),
    ERectPivots.TOP_RIGHT: pygame.Vector2(0.5, -0.5),
    ERectPivots.BOTTOM_RIGHT: pygame.Vector2(0.5, 0.5),
    ERectPivots.BOTTOM_LEFT: pygame.Vector2(-0.5, 0.5),
    ERectPivots.TOP_CENTER: pygame.Vector2(0, -0.5),
    ERectPivots.RIGHT_CENTER: pygame.Vector2(0.5, 0),
    ERectPivots.BOTTOM_CENTER: pygame.Vector2(0, 0.5),
    ERectPivots.LEFT_CENTER: pygame.Vector2(-0.5, 0),
    ERectPivots.CENTER: pygame.Vector2(0, 0),
}

RECT_CORNER_OFFSETS_FROM_CENTER: list[pygame.Vector2] = [
    pygame.Vector2(-0.5, -0.5),
    pygame.Vector2(0.5, -0.5),
    pygame.Vector2(0.5, 0.5),
    pygame.Vector2(-0.5, 0.5),
]


def GetRectCorners(
    worldPos: pygame.Vector2,
    size: pygame.Vector2,
) -> list[pygame.Vector2]:

    corners = []
    for offset in RECT_CORNER_OFFSETS_FROM_CENTER:
        corner = worldPos + (size.elementwise() * offset.elementwise())
        corners.append(corner)

    return corners


def GetRotatedRectCorners(
    worldPos: pygame.Vector2,
    size: pygame.Vector2,
    angleDeg: float,
    pivotType: ERectPivots,
) -> list[pygame.Vector2]:

    corners = []
    for offset in RECT_CORNER_OFFSETS_FROM_CENTER:
        corner = worldPos + (size.elementwise() * offset.elementwise())
        corners.append(corner)

    pivot = worldPos + (size.elementwise() * RECT_PIVOT_OFFSETS_FROM_CENTER[pivotType].elementwise())

    rotatedCorners = []
    for corner in corners:
        rotatedCorners.append(RotatePointAroundPivot(corner, pivot, angleDeg))

    return rotatedCorners


def RotatePointAroundPivot(point: pygame.Vector2, pivot: pygame.Vector2, angleDeg: float) -> pygame.Vector2:
    rad = math.radians(angleDeg)

    xTranslate = point.x - pivot.x
    yTranslate = point.y - pivot.y

    xRot = xTranslate * math.cos(rad) - yTranslate * math.sin(rad)
    yRot = xTranslate * math.sin(rad) + yTranslate * math.cos(rad)

    return pygame.Vector2(xRot + pivot.x, yRot + pivot.y)