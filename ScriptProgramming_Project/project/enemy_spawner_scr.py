from __future__ import annotations
from typing import TYPE_CHECKING

from collections import deque

from dataclasses import dataclass

import random

import pygame

from pyre.components.scripts import MonoScript
from pyre.timer import Timer

if TYPE_CHECKING:
    from scene import Scene


@dataclass
class Spawns:
    spawnPos: pygame.Vector2
    spawnRot: float
    spawnLocationType: str
    isLocked: bool
    targetDest: pygame.Vector2


class EnemySpawnerScr(MonoScript):
    def __init__(self) -> None:
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None

        # Timers
        self.m_basicEnemySpawnTimer: "Timer" | None = None
        self.m_bossEnemySpawnTimer: "Timer" | None = None

        # Vars
        self.m_roadSpawns: list["Spawns"] = []
        self.m_cornerSpawns: list["Spawns"] = []
        self.m_bossQueue: deque[tuple[str, str]] = deque()

    def Start(self) -> None:
        self.m_basicEnemySpawnTimer = Timer(8)
        self.m_bossEnemySpawnTimer = Timer(30)

        self.m_spawns: list["Spawns"] = [
            Spawns(pygame.Vector2(640, -50), 0, "road", False, pygame.Vector2(0, 0)),  # Top
            Spawns(pygame.Vector2(1330, 384), 90, "road", False, pygame.Vector2(0, 0)),  # Right
            Spawns(pygame.Vector2(640, 803), 180, "road", False, pygame.Vector2(0, 0)),  # Bottom
            Spawns(pygame.Vector2(-50, 384), -90, "road", False, pygame.Vector2(0, 0)),  # Left
            Spawns(pygame.Vector2(-35, -35), -45, "corner", False, pygame.Vector2(45, 45)),  # Top-left
            Spawns(pygame.Vector2(1315, -35), 45, "corner", False, pygame.Vector2(1235, 45)),  # Top-right
            Spawns(pygame.Vector2(1315, 803), 135, "corner", False, pygame.Vector2(1235, 733)),  # Bottom-right
            Spawns(pygame.Vector2(-35, 803), -135, "corner", False, pygame.Vector2(45, 733)),  # Bottom-left
        ]

    def Update(self) -> None:
        if self.m_basicEnemySpawnTimer.Tick():
            self.SpawnBasicEnemy()
            self.m_basicEnemySpawnTimer.Reset()

        if self.m_bossEnemySpawnTimer.Tick():
            self.SpawnBossEnemy()
            self.m_bossEnemySpawnTimer.Reset()

    def OnEnable(self) -> None:
        pass

    def OnDisable(self) -> None:
        pass

    def SpawnBasicEnemy(self) -> None:
        freeSpawns = []
        for spawn in self.m_spawns:
            if not spawn.isLocked and spawn.spawnLocationType == "road":
                freeSpawns.append(spawn)

        if len(freeSpawns) > 0:
            randSpawn: "Spawns" = random.choice(freeSpawns)
            randSpawn.isLocked = True
            self.m_scene.CreateGruntEnemy(randSpawn.spawnPos, randSpawn.spawnRot, randSpawn)

    def SpawnBossEnemy(self) -> None:
        bossType = random.choice(["hellspot", "kamikaze"])
        requiredSpawnType: str

        if bossType == "hellspot":
            requiredSpawnType = "corner"
        else:
            requiredSpawnType = "road"

        freeSpawns = []
        for spawn in self.m_spawns:
            if not spawn.isLocked and spawn.spawnLocationType == requiredSpawnType:
                freeSpawns.append(spawn)

        if len(freeSpawns) > 0:
            randSpawn: "Spawns" = random.choice(freeSpawns)
            randSpawn.isLocked = True

            if bossType == "hellspot":
                self.m_scene.CreateHellspotEnemy(randSpawn.spawnPos, randSpawn.spawnRot, randSpawn)
            else:
                self.m_scene.CreateKamikazeEnemy(randSpawn.spawnPos, randSpawn.spawnRot, randSpawn)