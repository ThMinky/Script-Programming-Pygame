from __future__ import annotations
from typing import TYPE_CHECKING

import math

import pygame

from .rect_utils import GetRotatedRectVerticesWorldPos, GetNormalizedRectNormals

if TYPE_CHECKING:
    from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider


# //////////////////////////////////////////////////
# All collision functions support:
# - Axis-Aligned Bounding Boxes (AABB)
# - Oriented Bounding Boxes (OBB)
# - Only for convex shapes!
# //////////////////////////////////////////////////


# //////////////////////////////////////////////////
# Box
def BoxBox(first: "BoxCollider", second: "BoxCollider") -> bool:
    verticesFirst = GetRotatedRectVerticesWorldPos(first.m_worldPos, first.m_size, first.m_transform.m_worldRot)
    verticesSecond = GetRotatedRectVerticesWorldPos(second.m_worldPos, second.m_size, second.m_transform.m_worldRot)

    normals = GetNormalizedRectNormals(verticesFirst) + GetNormalizedRectNormals(verticesSecond)

    for normal in normals:
        minA, maxA = _ProjectPointsOnNormal(verticesFirst, normal)
        minB, maxB = _ProjectPointsOnNormal(verticesSecond, normal)

        if maxA < minB or minA > maxB:
            return False

    return True


def BoxCircle(first: "BoxCollider", second: "CircleCollider") -> bool:
    verticesFirst = GetRotatedRectVerticesWorldPos(first.m_worldPos, first.m_size, first.m_transform.m_worldRot)

    normals = GetNormalizedRectNormals(verticesFirst)

    for normal in normals:
        minA, maxA = _ProjectPointsOnNormal(verticesFirst, normal)

        centerProj = second.m_worldPos.dot(normal)
        minB = centerProj - second.m_radius
        maxB = centerProj + second.m_radius

        if maxA < minB or minA > maxB:
            return False

    return True


def BoxLine(first: "BoxCollider", second: "LineCollider") -> bool:
    verticesFirst = GetRotatedRectVerticesWorldPos(first.m_worldPos, first.m_size, first.m_transform.m_worldRot)
    verticesSecond: list[pygame.Vector2] = [second.m_startPoint, second.m_endPoint]

    normals = GetNormalizedRectNormals(verticesFirst)

    for normal in normals:
        minA, maxA = _ProjectPointsOnNormal(verticesFirst, normal)
        minB, maxB = _ProjectPointsOnNormal(verticesSecond, normal)

        if maxA < minB or minA > maxB:
            return False

    return True


def BoxPoint(first: "BoxCollider", second: "PointCollider") -> bool:
    verticesFirst = GetRotatedRectVerticesWorldPos(first.m_worldPos, first.m_size, first.m_transform.m_worldRot)

    normals = GetNormalizedRectNormals(verticesFirst)

    for normal in normals:
        minA, maxA = _ProjectPointsOnNormal(verticesFirst, normal)

        centerProj = second.m_worldPos.dot(normal)

        if maxA < centerProj or minA > centerProj:
            return False

    return True


# //////////////////////////////////////////////////


# //////////////////////////////////////////////////
# Circle
def CircleBox(first: "CircleCollider", second: "BoxCollider") -> bool:
    return BoxCircle(second, first)


def CircleCircle(first: "CircleCollider", second: "CircleCollider") -> bool:
    distance = (first.m_worldPos - second.m_worldPos).length_squared()

    if distance <= math.pow(first.m_radius + second.m_radius, 2):
        return True
    return False


def CircleLine(first: "CircleCollider", second: "LineCollider") -> bool:
    ab = second.m_endPoint - second.m_startPoint
    ap = first.m_worldPos - second.m_startPoint

    t = max(0, min(1, ab.dot(ap) / ab.length_squared()))

    distance = (ap - (ab * t)).length_squared()

    if distance <= math.pow(first.m_radius, 2):
        return True
    return False


def CirclePoint(first: "CircleCollider", second: "PointCollider") -> bool:
    distance = (first.m_worldPos - second.m_worldPos).length_squared()

    if distance <= math.pow(first.m_radius, 2):
        return True
    return False


# //////////////////////////////////////////////////


# //////////////////////////////////////////////////
# Line
def LineBox(first: "LineCollider", second: "BoxCollider") -> bool:
    return BoxLine(second, first)


def LineCircle(first: "LineCollider", second: "CircleCollider") -> bool:
    return CircleLine(second, first)


def LineLine(first: "LineCollider", second: "LineCollider") -> bool:
    line1 = first.m_endPoint - first.m_startPoint
    line2 = second.m_endPoint - second.m_startPoint

    cross = line1.cross(line2)

    if cross == 0:
        return False

    delta = second.m_startPoint - first.m_startPoint

    t = delta.cross(line2) / cross
    u = delta.cross(line1) / cross

    if 0 <= t <= 1 and 0 <= u <= 1:
        return True
    return False


def LinePoint(first: "LineCollider", second: "PointCollider") -> bool:
    ab = first.m_endPoint - first.m_startPoint
    ap = second.m_worldPos - first.m_startPoint

    t = max(0, min(1, ab.dot(ap) / ab.length_squared()))

    distance = (ap - (ab * t)).length_squared()

    if distance <= 1:
        return True
    return False


# //////////////////////////////////////////////////


# //////////////////////////////////////////////////
# Point
def PointBox(first: "PointCollider", second: "BoxCollider") -> bool:
    return BoxPoint(second, first)


def PointCircle(first: "PointCollider", second: "CircleCollider") -> bool:
    return CirclePoint(second, first)


def PointLine(first: "PointCollider", second: "LineCollider") -> bool:
    return LinePoint(second, first)


def PointPoint(first: "PointCollider", second: "PointCollider") -> bool:
    if int(first.m_worldPos.x) == int(second.m_worldPos.x) and int(first.m_worldPos.y) == int(second.m_worldPos.y):
        return True
    return False


# //////////////////////////////////////////////////


def _ProjectPointsOnNormal(points: list[pygame.Vector2], normal: pygame.Vector2) -> tuple[float, float]:
    projections = []

    for point in points:
        proj = point.dot(normal)
        projections.append(proj)

    return min(projections), max(projections)