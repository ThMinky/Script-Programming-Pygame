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


def GetRectCornersWorldPos(worldPos: pygame.Vector2, size: pygame.Vector2) -> list[pygame.Vector2]:
    corners = []
    for offset in RECT_CORNER_OFFSETS_FROM_CENTER:
        corner = worldPos + (size.elementwise() * offset.elementwise())
        corners.append(corner)

    return corners


def GetRotatedRectCornersWorldPos(
    worldPos: pygame.Vector2, size: pygame.Vector2, angleDeg: float, pivotPosition: ERectPivots
) -> list[pygame.Vector2]:
    from pyre.utils.math_utils import RotatePointAroundPivot

    corners = []
    for offset in RECT_CORNER_OFFSETS_FROM_CENTER:
        corner = worldPos + (size.elementwise() * offset.elementwise())
        corners.append(corner)

    pivot = worldPos + (size.elementwise() * RECT_PIVOT_OFFSETS_FROM_CENTER[pivotPosition].elementwise())

    rotatedCorners = []
    for corner in corners:
        rotatedCorners.append(RotatePointAroundPivot(corner, pivot, angleDeg))

    return rotatedCorners