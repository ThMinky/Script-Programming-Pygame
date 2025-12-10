from __future__ import annotations
from typing import TYPE_CHECKING

import weakref

from pyre.components import Transform
from pyre.components.scripts import MonoScript
from pyre.entities import Entity
from pyre.systems import RenderSystem
from pyre.utils.math_utils import GetAngleFromDirVector
from pyre.timer import Timer

from project.interfaces import IDamagable

if TYPE_CHECKING:
    from project.base import BaseScr
    from scene import Scene


class AutoTurretScr(MonoScript):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None # Auto assign
        self.m_baseScr: "BaseScr" | None = None # Auto assign

        self.m_targetRef: weakref.ref["Entity"] | None = None

        # Caches
        self.m_tr: "Transform" | None = None

        # Timers
        self.m_reloadCooldown: float = 2.5
        self.m_reloadTimer = Timer(self.m_reloadCooldown)

        # Vars
        self.m_dmg: float = 1
        self.m_range: float = 100

    def Start(self) -> None:
        # Caches
        self.m_tr = self.m_parent.GetComponentByType(Transform)

    def Update(self) -> None:
        self.Gizmo()

        self.m_reloadTimer.Tick()

        self.GetClosestTarget()
        self.LookAtTarget()
        self.Shoot()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def GetClosestTarget(self) -> None:
        if self.m_targetRef is not None:
            return

        enemyTransforms: list["Transform"] = []

        for enemy in self.m_scene.m_enemies.copy():
            enemyTransforms.append(enemy.GetComponentByType(Transform))

        if len(enemyTransforms) == 0:
            self.m_targetRef = None
            return

        enemyTransforms.sort(key=lambda tr: self.m_tr.m_worldPos.distance_squared_to(tr.m_worldPos))

        closest = enemyTransforms[0]

        if self.m_tr.m_worldPos.distance_squared_to(closest.m_worldPos) <= self.m_range**2:
            self.m_targetRef = weakref.ref(enemyTransforms[0].m_parent)
            return

        self.m_targetRef = None

    def LookAtTarget(self):
        if self.m_targetRef is None:
            return

        if self.m_targetRef() is None:
            self.m_targetRef = None
            return

        targetTransform = self.m_targetRef().GetComponentByType(Transform)

        if targetTransform is None:
            self.m_targetRef = None
            return

        dirVec = (targetTransform.m_worldPos - self.m_tr.m_worldPos).normalize()
        rot = GetAngleFromDirVector(dirVec)
        self.m_tr.SetRotation(rot - self.m_tr.m_parentTransform.m_worldRot)

    def Shoot(self):
        if self.m_targetRef is None:
            return

        if self.m_targetRef() is None:
            self.m_targetRef = None
            return

        if self.m_reloadTimer.m_flag:
            for script in self.m_targetRef().GetComponentsByType(MonoScript):
                if isinstance(script, IDamagable):
                    script.TakeDamage(self.m_dmg)

                    self.m_reloadTimer.Reset()
                    break

    def Gizmo(self) -> None:
        RenderSystem.GetInstance().DebugCircle(self.m_tr.m_worldPos, self.m_range, (255, 255, 0))