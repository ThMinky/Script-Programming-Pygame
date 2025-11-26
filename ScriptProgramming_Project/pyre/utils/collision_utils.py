from __future__ import annotations
from typing import TYPE_CHECKING

import math

import pygame

if TYPE_CHECKING:
    from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider


# //////////////////////////////////////////////////
# Box
def BoxBox(first: "BoxCollider", second: "BoxCollider") -> bool:
    pass


def BoxCircle(first: "BoxCollider", second: "CircleCollider") -> bool:
    pass


def BoxLine(first: "BoxCollider", second: "LineCollider") -> bool:
    pass


def BoxPoint(first: "BoxCollider", second: "PointCollider") -> bool:
    pass


# //////////////////////////////////////////////////


# //////////////////////////////////////////////////
# Circle
def CircleCircle(first: "CircleCollider", second: "CircleCollider") -> bool:
    distance = (first.m_worldPos - second.m_worldPos).length_squared()

    if distance <= math.pow(first.m_radius + second.m_radius, 2):
        return True
    return False


def CircleBox(first: "CircleCollider", second: "BoxCollider") -> bool:
    pass


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
def LineLine(first: "LineCollider", second: "LineCollider") -> bool:
    pass


def LineBox(first: "LineCollider", second: "BoxCollider") -> bool:
    pass


def LineCircle(first: "LineCollider", second: "CircleCollider") -> bool:
    ab = first.m_endPoint - first.m_startPoint
    ap = second.m_worldPos - first.m_startPoint

    t = max(0, min(1, ab.dot(ap) / ab.length_squared()))

    distance = (ap - (ab * t)).length_squared()

    if distance <= math.pow(second.m_radius, 2):
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
def PointPoint(first: "PointCollider", second: "PointCollider") -> bool:
    if int(first.m_worldPos.x) == int(second.m_worldPos.x) and int(first.m_worldPos.y) == int(second.m_worldPos.y):
        return True
    return False


def PointBox(first: "PointCollider", second: "BoxCollider") -> bool:
    pass


def PointCircle(first: "PointCollider", second: "CircleCollider") -> bool:
    distance = (first.m_worldPos - second.m_worldPos).length_squared()

    if distance <= math.pow(second.m_radius, 2):
        return True
    return False


def PointLine(first: "PointCollider", second: "LineCollider") -> bool:
    ab = second.m_endPoint - second.m_startPoint
    ap = first.m_worldPos - second.m_startPoint

    t = max(0, min(1, ab.dot(ap) / ab.length_squared()))

    distance = (ap - (ab * t)).length_squared()

    if distance <= 1:
        return True
    return False


# //////////////////////////////////////////////////