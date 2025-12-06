import math

import pygame


def RotatePointAroundPivot(point: pygame.Vector2, pivot: pygame.Vector2, angleDeg: float) -> pygame.Vector2:
    rad = math.radians(angleDeg)

    xTranslate = point.x - pivot.x
    yTranslate = point.y - pivot.y

    xRot = xTranslate * math.cos(rad) - yTranslate * math.sin(rad)
    yRot = xTranslate * math.sin(rad) + yTranslate * math.cos(rad)

    xInvTranslate = xRot + pivot.x
    yInvTranslate = yRot + pivot.y

    return pygame.Vector2(xInvTranslate, yInvTranslate)