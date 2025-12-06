import pygame


RECT_CORNER_OFFSETS_FROM_CENTER: list[pygame.Vector2] = [
    pygame.Vector2(-0.5, -0.5),
    pygame.Vector2(0.5, -0.5),
    pygame.Vector2(0.5, 0.5),
    pygame.Vector2(-0.5, 0.5),
]


def GetRotatedRectVerticesWorldPos(worldPos: pygame.Vector2, size: pygame.Vector2, angleDeg: float) -> list[pygame.Vector2]:
    from pyre.utils.math_utils import RotatePointAroundPivot

    rotatedVertices = []
    for offset in RECT_CORNER_OFFSETS_FROM_CENTER:
        rotatedVertex = RotatePointAroundPivot(worldPos + size.elementwise() * offset.elementwise(), worldPos, angleDeg)
        rotatedVertices.append(rotatedVertex)

    return rotatedVertices


def GetNormalizedRectNormals(vertices: list[pygame.Vector2]) -> list[pygame.Vector2]:
    normals = []

    edge1 = vertices[1] - vertices[0]
    normal1 = pygame.Vector2(edge1.y, -edge1.x).normalize()
    normals.append(normal1)

    edge2 = vertices[2] - vertices[1]
    normal2 = pygame.Vector2(edge2.y, -edge2.x).normalize()
    normals.append(normal2)

    return normals