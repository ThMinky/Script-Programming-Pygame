from enum import Enum, auto

import math
import pygame


class ERectPoints(Enum):
    TOP_LEFT = auto()
    TOP_CENTER = auto()
    TOP_RIGHT = auto()
    RIGHT_CENTER = auto()
    BOTTOM_RIGHT = auto()
    BOTTOM_CENTER = auto()
    BOTTOM_LEFT = auto()
    LEFT_CENTER = auto()
    CENTER = auto()


RECT_PIVOT_OFFSETS = {
    ERectPoints.TOP_LEFT: (-0.5, -0.5),
    ERectPoints.TOP_CENTER: (0, -0.5),
    ERectPoints.TOP_RIGHT: (0.5, -0.5),
    ERectPoints.RIGHT_CENTER: (0.5, 0),
    ERectPoints.BOTTOM_RIGHT: (0.5, 0.5),
    ERectPoints.BOTTOM_CENTER: (0, 0.5),
    ERectPoints.BOTTOM_LEFT: (-0.5, 0.5),
    ERectPoints.CENTER: (0, 0),
}

RECT_CORNER_PATTERNS = {
    ERectPoints.TOP_LEFT: [
        (0, 0),
        (1, 0),
        (1, 1),
        (0, 1),
    ],
    ERectPoints.TOP_CENTER: [
        (-0.5, 0),
        (0.5, 0),
        (0.5, 1),
        (-0.5, 1),
    ],
    ERectPoints.TOP_RIGHT: [
        (-1, 0),
        (0, 0),
        (0, 1),
        (-1, 1),
    ],
    ERectPoints.RIGHT_CENTER: [
        (-1, -0.5),
        (0, -0.5),
        (0, 0.5),
        (-1, 0.5),
    ],
    ERectPoints.BOTTOM_RIGHT: [
        (-1, -1),
        (0, -1),
        (0, 0),
        (-1, 0),
    ],
    ERectPoints.BOTTOM_CENTER: [
        (-0.5, -1),
        (0.5, -1),
        (0.5, 0),
        (-0.5, 0),
    ],
    ERectPoints.BOTTOM_LEFT: [
        (0, -1),
        (1, -1),
        (1, 0),
        (0, 0),
    ],
    ERectPoints.CENTER: [
        (-0.5, -0.5),
        (0.5, -0.5),
        (0.5, 0.5),
        (-0.5, 0.5),
    ],
}


def GetRotatedRectCorners(
    worldPos: pygame.Vector2,
    size: pygame.Vector2,
    angleDeg: float,
    pivotType: ERectPoints,
) -> list[pygame.Vector2]:
    pivot = pygame.Vector2(
        worldPos.x + size.x * RECT_PIVOT_OFFSETS[pivotType][0],
        worldPos.y + size.y * RECT_PIVOT_OFFSETS[pivotType][1],
    )

    corners = []
    for x, y in RECT_CORNER_PATTERNS[pivotType]:
        corner = pygame.Vector2(worldPos.x + size.x * x, worldPos.y + size.y * y)
        corners.append(corner)

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