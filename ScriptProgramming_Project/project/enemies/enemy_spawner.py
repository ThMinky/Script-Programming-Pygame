from __future__ import annotations
from typing import TYPE_CHECKING

from dataclasses import dataclass

import random

import pygame

from pyre.components.scripts import BaseScript
from pyre.timer import Timer

if TYPE_CHECKING:
    from scene import Scene


@dataclass
class Spawns:
    pos: pygame.Vector2
    rot: float
    spawnType: str
    isLocked: bool = False


class EnemySpawner(BaseScript):
    def __init__(self):
        super().__init__()

        # Refs
        self.m_scene: "Scene" | None = None

        self.m_basicEnemySpawnTimer: "Timer" | None = None
        self.m_bossEnemySpawnTimer: "Timer" | None = None

        self.m_spawns: list["Spawns"] = []

    def Start(self):
        self.m_basicEnemySpawnTimer = Timer(8)
        self.m_bossEnemySpawnTimer = Timer(30)

        self.m_spawns: list["Spawns"] = [
            Spawns(pygame.Vector2(640, 0), 0, "road"),  # Top -90
            Spawns(pygame.Vector2(1280, 384), 90, "road"),  # Right 179
            Spawns(pygame.Vector2(640, 768), 180, "road"),  # Bottom 90
            Spawns(pygame.Vector2(0, 384), -90, "road"),  # Left - 179
            Spawns(pygame.Vector2(0, 0), -45, "corner"),  # Top-left
            Spawns(pygame.Vector2(1280, 0), 45, "corner"),  # Top-right
            Spawns(pygame.Vector2(1280, 768), 135, "corner"),  # Bottom-right
            Spawns(pygame.Vector2(0, 768), -135, "corner"),  # Bottom-left
        ]

    def Update(self):
        if self.m_basicEnemySpawnTimer.Tick():
            self.SpawnBasicEnemy()
            self.m_basicEnemySpawnTimer.Reset()

        if self.m_bossEnemySpawnTimer.Tick():
            self.SpawnBossEnemy()
            self.m_bossEnemySpawnTimer.Reset()

    def OnEnable(self):
        pass

    def OnDisable(self):
        pass

    def SpawnBasicEnemy(self):
        freeSpawns = []
        for spawn in self.m_spawns:
            if not spawn.isLocked:
                freeSpawns.append(spawn)

        randSpawn: "Spawns" = random.choice(freeSpawns)
        randSpawn.isLocked = True
        self.m_scene.CreateBasicEnemy(randSpawn.pos, randSpawn.rot)

    def SpawnBossEnemy(self):
        bossType = random.choice(["hellspot", "kamikaze"])

        if bossType == "hellspot":
            requiredType = "road"
        else:
            requiredType = "corner"

        freeSpawns = []
        for spawn in self.m_spawns:
            if not spawn.isLocked and spawn.spawnType == requiredType:
                freeSpawns.append(spawn)

        randSpawn: "Spawns" = random.choice(freeSpawns)
        randSpawn.isLocked = True

        if bossType == "hellspot":
            self.m_scene.CreateHellspotEnemy(randSpawn.pos, randSpawn.rot)
        else:
            self.m_scene.CreateKamikazeEnemy(randSpawn.pos, randSpawn.rot)