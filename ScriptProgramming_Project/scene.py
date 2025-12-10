from __future__ import annotations

from enum import IntEnum

import weakref

import math
import random

import pygame

from pyre.components import Sprite, Transform
from pyre.components.colliders import BoxCollider, LineCollider
from pyre.entities import Entity
from pyre.managers import SoundManager, SpriteManager

from project.base import AutoTurretScr, BaseScr
from project.enemies import GruntScr, HellspotScr, KamikazeScr
from project.player.player_scr import PlayerScr
from project.tags import BlockerTag
from project.ammo_box_scr import AmmoBoxScr
from project.blast_area_scr import BlastAreaScr
from project.enemy_spawner_scr import Spawns, EnemySpawnerScr
from project.projectile_scr import ProjectileScr
from project.ui_scr import UIScr


class ELayers(IntEnum):
    TILE = 0
    DECOR = 1
    INTERACT = 2
    ENTITY = 3


class Scene:
    def __init__(self):
        self.m_mapTiles: list["Entity"] = []
        self.m_mapBounds: list["Entity"] = []
        self.m_mapDecors: list["Entity"] = []

        self.m_baseRoot: "Entity" | None = None
        self.m_player: "Entity" | None = None

        self.m_enemySpawner: "Entity" | None = None
        self.m_enemies: list["Entity"] = []

        self.m_projectiles: list["Entity"] = []
        self.m_blastAreas: list["Entity"] = []

        self.m_ammoBoxes: list["Entity"] = []

        self.m_ui: "Entity" | None = None

        # Register Sprites
        # //////////////////////////////////////////////////

        # Map Tiles
        SpriteManager.GetInstance().RegisterSprite("0", "resources/tiles/sand.png")
        SpriteManager.GetInstance().RegisterSprite("1", "resources/tiles/road_hor.png")
        SpriteManager.GetInstance().RegisterSprite("2", "resources/tiles/road_ver.png")
        SpriteManager.GetInstance().RegisterSprite("3", "resources/tiles/road_corner_ur.png")
        SpriteManager.GetInstance().RegisterSprite("4", "resources/tiles/road_corner_ul.png")
        SpriteManager.GetInstance().RegisterSprite("5", "resources/tiles/road_corner_dr.png")
        SpriteManager.GetInstance().RegisterSprite("6", "resources/tiles/road_corner_dl.png")
        SpriteManager.GetInstance().RegisterSprite("7", "resources/tiles/road_cross_r.png")
        SpriteManager.GetInstance().RegisterSprite("8", "resources/tiles/road_r_cross_r.png")
        SpriteManager.GetInstance().RegisterSprite("9", "resources/tiles/road_split_l.png")
        SpriteManager.GetInstance().RegisterSprite("10", "resources/tiles/road_split_u.png")
        SpriteManager.GetInstance().RegisterSprite("11", "resources/tiles/road_split_r.png")
        SpriteManager.GetInstance().RegisterSprite("12", "resources/tiles/road_split_d.png")

        # Decors
        SpriteManager.GetInstance().RegisterSprite("bush", "resources/decor/bush.png")
        SpriteManager.GetInstance().RegisterSprite("twigs", "resources/decor/twigs.png")
        SpriteManager.GetInstance().RegisterSprite("leaf", "resources/decor/leaf.png")

        SpriteManager.GetInstance().RegisterSprite("sandbag", "resources/decor/sandbag.png")

        SpriteManager.GetInstance().RegisterSprite("explodeBarrelTop", "resources/decor/explode_barrel_top.png")
        SpriteManager.GetInstance().RegisterSprite("explodeBarrelSide", "resources/decor/explode_barrel_side.png")

        # Base
        SpriteManager.GetInstance().RegisterSprite("autoTurretHead", "resources/autoTurret/auto_turret_head.png")
        SpriteManager.GetInstance().RegisterSprite("autoTurretStand", "resources/autoTurret/auto_turret_stand.png")

        SpriteManager.GetInstance().RegisterSprite("ammoWire", "resources/autoTurret/ammo_wire.png")
        SpriteManager.GetInstance().RegisterSprite("ammoBarrel", "resources/autoTurret/ammo_barrel.png")

        # Tank Hulls / Barrels / Projectiles
        SpriteManager.GetInstance().RegisterSprite("sandTankHull", "resources/tanks/tank_hull_sand.png")
        SpriteManager.GetInstance().RegisterSprite("sandTankBarrel", "resources/tanks/tank_barrel_sand.png")

        SpriteManager.GetInstance().RegisterSprite("darkTankHull", "resources/tanks/tank_hull_dark.png")
        SpriteManager.GetInstance().RegisterSprite("darkTankBarrel", "resources/tanks/tank_barrel_dark.png")

        SpriteManager.GetInstance().RegisterSprite("hellspot", "resources/tanks/tank_hull_hellspot.png")
        SpriteManager.GetInstance().RegisterSprite("lazerL", "resources/tanks/tank_lazer_left.png")
        SpriteManager.GetInstance().RegisterSprite("lazerR", "resources/tanks/tank_lazer_right.png")

        SpriteManager.GetInstance().RegisterSprite("kamikaze", "resources/tanks/tank_hull_kamikaze.png")

        SpriteManager.GetInstance().RegisterSprite("projectile", "resources/tanks/tank_projectile.png")

        # Ammo Box
        SpriteManager.GetInstance().RegisterSprite("ammoBox", "resources/autoTurret/ammo_box.png")

        # //////////////////////////////////////////////////

        # Register Sounds
        # //////////////////////////////////////////////////

        SoundManager.GetInstance().RegisterSound("explosion", "resources/sounds/explosion.wav")
        SoundManager.GetInstance().RegisterSound("pickupAmmo", "resources/sounds/pickup_ammo.wav")
        SoundManager.GetInstance().RegisterSound("projImpact", "resources/sounds/proj_impact.wav")
        SoundManager.GetInstance().RegisterSound("tankFire", "resources/sounds/tank_fire.wav")
        SoundManager.GetInstance().RegisterSound("turretFire", "resources/sounds/turret_fire.wav")

        # //////////////////////////////////////////////////

        self.m_mapTiles = self.CreateMap("map.txt", (64, 64))
        self.m_mapBounds = self.CreateMapBounds(1280, 768)
        self.m_mapDecors = self.CreateDecor(45, 75)

        self.m_baseRoot = self.CreateBase(pygame.Vector2(640, 384))
        self.m_player = self.CreatePlayer(pygame.Vector2(450, 450))

        self.m_enemySpawner = self.CreateEnemySpawner()

        self.m_ui = self.CreateUI()

    def CreateMap(self, path: str, tileSize: tuple[int, int]) -> list["Entity"]:
        self.tiles: list["Entity"] = []
        self.mapData = self._LoadMapFromFile(path)

        for i in range(len(self.mapData)):
            for j in range(len(self.mapData[i])):
                tileId = self.mapData[i][j]

                posX = j * tileSize[0] + tileSize[0] / 2
                posY = i * tileSize[1] + tileSize[1] / 2

                tile = Entity(localPos=pygame.Vector2(posX, posY))
                tile.AddComponent(
                    Sprite(
                        spriteKey=tileId,
                        layer=ELayers.TILE,
                    )
                )
                self.tiles.append(tile)

        return self.tiles

    def CreateMapBounds(self, mapWidth: int, mapHeight: int, thickness: int = 10) -> list["Entity"]:
        bounds: list["Entity"] = []

        topBound = Entity(localPos=pygame.Vector2(mapWidth / 2, (thickness / 2) - 10))
        topBound.AddComponent(BoxCollider(size=pygame.Vector2(mapWidth, thickness)))
        topBound.AddComponent(BlockerTag())
        bounds.append(topBound)

        leftBound = Entity(localPos=pygame.Vector2((thickness / 2) - 10, mapHeight / 2))
        leftBound.AddComponent(BoxCollider(size=pygame.Vector2(thickness, mapHeight)))
        leftBound.AddComponent(BlockerTag())
        bounds.append(leftBound)

        bottomBound = Entity(localPos=pygame.Vector2(mapWidth / 2, (mapHeight - thickness / 2) + 9))
        bottomBound.AddComponent(BoxCollider(size=pygame.Vector2(mapWidth, thickness)))
        bottomBound.AddComponent(BlockerTag())
        bounds.append(bottomBound)

        rightBound = Entity(localPos=pygame.Vector2((mapWidth - thickness / 2) + 9, mapHeight / 2))
        rightBound.AddComponent(BoxCollider(size=pygame.Vector2(thickness, mapHeight)))
        rightBound.AddComponent(BlockerTag())
        bounds.append(rightBound)

        return bounds

    def CreateDecor(self, minRadius: int, maxRadius: int) -> list["Entity"]:
        decors: list["Entity"] = []

        bushPositions: list[pygame.Vector2] = [
            pygame.Vector2(260, 85),
            pygame.Vector2(300, 250),
            pygame.Vector2(500, 240),
            pygame.Vector2(800, 85),
            pygame.Vector2(950, 70),
            pygame.Vector2(950, 260),
            pygame.Vector2(1125, 250),
            pygame.Vector2(1050, 520),
            pygame.Vector2(820, 510),
            pygame.Vector2(800, 675),
            pygame.Vector2(440, 550),
            pygame.Vector2(220, 520),
            pygame.Vector2(130, 675),
        ]

        def randomOffset() -> pygame.Vector2:
            angle = random.uniform(0, 6.28)
            dist = random.uniform(minRadius, maxRadius)
            return pygame.Vector2(math.cos(angle) * dist, math.sin(angle) * dist)

        for bushPos in bushPositions:
            bush = Entity(localPos=bushPos)
            bush.AddComponent(
                Sprite(
                    spriteKey="bush",
                    layer=ELayers.DECOR,
                )
            )
            decors.append(bush)

            twigCount = random.randint(1, 2)
            for _ in range(twigCount):
                offset = randomOffset()
                twig = Entity(localPos=bushPos + offset)
                twig.AddComponent(
                    Sprite(
                        spriteKey="twigs",
                        layer=ELayers.DECOR,
                    )
                )
                decors.append(twig)

            leafCount = random.randint(1, 3)
            for _ in range(leafCount):
                offset = randomOffset()
                leaf = Entity(localPos=bushPos + offset)
                leaf.AddComponent(
                    Sprite(
                        spriteKey="leaf",
                        layer=ELayers.DECOR,
                    )
                )
                decors.append(leaf)

        return decors

    def CreateBase(self, center: pygame.Vector2) -> "Entity":
        baseRoot = Entity(localPos=center)
        baseRoot.AddComponent(BoxCollider(size=pygame.Vector2(130, 130)))
        baseRoot.AddComponent(BaseScr())
        baseRoot.AddComponent(BlockerTag())

        baseRoot.GetComponentByType(BaseScr).m_scene = self

        baseRootTransform = baseRoot.GetComponentByType(Transform)

        wireOffsets: list[tuple[pygame.Vector2, float, pygame.Vector2]] = [
            (pygame.Vector2(-25, -15), -50, pygame.Vector2(0.85, 0.85)),
            (pygame.Vector2(25, -15), 50, pygame.Vector2(0.85, 0.85)),
            (pygame.Vector2(20, 20), 150, pygame.Vector2(0.85, 0.85)),
            (pygame.Vector2(-20, 20), -150, pygame.Vector2(0.85, 0.85)),
        ]

        turretOffsets: list[pygame.Vector2] = [
            pygame.Vector2(-32, -32),
            pygame.Vector2(32, -32),
            pygame.Vector2(32, 32),
            pygame.Vector2(-32, 32),
        ]

        sandbagOffsets: tuple[list[pygame.Vector2], float] = [
            (pygame.Vector2(-32, -62), 0),
            (pygame.Vector2(32, -62), 0),
            (pygame.Vector2(62, -32), 90),
            (pygame.Vector2(62, 32), 90),
            (pygame.Vector2(32, 62), 0),
            (pygame.Vector2(-32, 62), 0),
            (pygame.Vector2(-62, 32), 90),
            (pygame.Vector2(-62, -32), 90),
        ]

        ammoBarrel = Entity(parentTransform=baseRootTransform)
        ammoBarrel.AddComponent(
            Sprite(
                spriteKey="ammoBarrel",
                layer=ELayers.DECOR,
            )
        )

        for pos, rot, scale in wireOffsets:
            ammoWire = Entity(
                parentTransform=baseRootTransform,
                localPos=pos,
                localRot=rot,
                localScale=scale,
            )
            ammoWire.AddComponent(
                Sprite(
                    spriteKey="ammoWire",
                    layer=ELayers.DECOR,
                )
            )

        for off in turretOffsets:
            turretStand = Entity(
                localPos=off,
                parentTransform=baseRootTransform,
            )
            turretStand.AddComponent(
                Sprite(
                    spriteKey="autoTurretStand",
                    layer=ELayers.ENTITY,
                )
            )

            turretHead = Entity(parentTransform=turretStand.GetComponentByType(Transform))
            turretHead.AddComponent(Sprite(spriteKey="autoTurretHead"))
            turretHead.AddComponent(AutoTurretScr())

            turretHead.GetComponentByType(AutoTurretScr).m_baseScr = baseRoot.GetComponentByType(BaseScr)
            turretHead.GetComponentByType(AutoTurretScr).m_scene = self

        for pos, rot in sandbagOffsets:
            sandbag = Entity(
                localPos=pos,
                localRot=rot,
                parentTransform=baseRootTransform,
            )
            sandbag.AddComponent(
                Sprite(
                    spriteKey="sandbag",
                    layer=ELayers.DECOR,
                )
            )

        return baseRoot

    def CreatePlayer(self, pos: pygame.Vector2) -> "Entity":
        hull = Entity(localPos=pos)
        hull.AddComponent(
            Sprite(
                spriteKey="sandTankHull",
                layer=ELayers.ENTITY,
            )
        )
        hull.AddComponent(BoxCollider())
        hull.AddComponent(PlayerScr())

        barrel = Entity(
            localPos=pygame.Vector2(0, -5),
            parentTransform=hull.GetComponentByType(Transform),
        )
        barrel.AddComponent(Sprite(spriteKey="sandTankBarrel"))

        hull.GetComponentByType(PlayerScr).m_barrel = barrel
        hull.GetComponentByType(PlayerScr).m_scene = self

        return hull

    def CreateEnemySpawner(self) -> "Entity":
        enemySpawner = Entity()
        enemySpawner.AddComponent(EnemySpawnerScr())

        enemySpawner.GetComponentByType(EnemySpawnerScr).m_scene = self

        return enemySpawner

    def CreateGruntEnemy(self, pos: pygame.Vector2, rot: float, spawnRef: "Spawns" | None = None) -> None:
        hull = Entity(
            localPos=pos,
            localRot=rot,
        )
        hull.AddComponent(
            Sprite(
                spriteKey="darkTankHull",
                layer=ELayers.ENTITY,
            )
        )
        hull.AddComponent(BoxCollider())
        hull.AddComponent(GruntScr())
        hull.AddComponent(BlockerTag())

        barrel = Entity(
            localPos=pygame.Vector2(0, -5),
            parentTransform=hull.GetComponentByType(Transform),
        )
        barrel.AddComponent(Sprite(spriteKey="darkTankBarrel"))

        hull.GetComponentByType(GruntScr).m_scene = self
        hull.GetComponentByType(GruntScr).m_spawnPoint = spawnRef
        hull.GetComponentByType(GruntScr).m_barrelTr = barrel.GetComponentByType(Transform)

        self.m_enemies.append(hull)

    def CreateHellspotEnemy(self, pos: pygame.Vector2, rot: float, spawnRef: "Spawns" | None = None) -> None:
        hull = Entity(
            localPos=pos,
            localRot=rot,
        )
        hull.AddComponent(
            Sprite(
                spriteKey="hellspot",
                layer=ELayers.ENTITY,
            )
        )
        hull.AddComponent(BoxCollider(size=pygame.Vector2(50, 54)))
        hull.AddComponent(HellspotScr())
        hull.AddComponent(BlockerTag())

        lazerL = Entity(
            localPos=pygame.Vector2(10, 0),
            parentTransform=hull.GetComponentByType(Transform),
        )
        lazerL.AddComponent(Sprite(spriteKey="lazerL"))

        lazerR = Entity(
            localPos=pygame.Vector2(-10, 0),
            parentTransform=hull.GetComponentByType(Transform),
        )
        lazerR.AddComponent(Sprite(spriteKey="lazerR"))

        hull.GetComponentByType(HellspotScr).m_scene = self
        hull.GetComponentByType(HellspotScr).m_spawnPoint = spawnRef
        hull.GetComponentByType(HellspotScr).m_lazerLTr = lazerL.GetComponentByType(Transform)
        hull.GetComponentByType(HellspotScr).m_lazerRTr = lazerR.GetComponentByType(Transform)

        self.m_enemies.append(hull)

    def CreateKamikazeEnemy(self, pos: pygame.Vector2, rot: float, spawnRef: "Spawns" | None = None) -> None:
        hull = Entity(
            localPos=pos,
            localRot=rot,
        )
        hull.AddComponent(
            Sprite(
                spriteKey="kamikaze",
                layer=ELayers.ENTITY,
            )
        )
        hull.AddComponent(BoxCollider())
        hull.AddComponent(KamikazeScr())
        hull.AddComponent(BlockerTag())

        explodeBarrelTop = Entity(
            localPos=pygame.Vector2(0, -15),
            parentTransform=hull.GetComponentByType(Transform),
        )
        explodeBarrelTop.AddComponent(Sprite(spriteKey="explodeBarrelTop"))

        explodeBarrelSide = Entity(
            localPos=pygame.Vector2(0, 15),
            localRot=90,
            parentTransform=hull.GetComponentByType(Transform),
        )
        explodeBarrelSide.AddComponent(Sprite(spriteKey="explodeBarrelSide"))

        hull.GetComponentByType(KamikazeScr).m_scene = self
        hull.GetComponentByType(KamikazeScr).m_spawnPoint = spawnRef

        self.m_enemies.append(hull)

    def CreateProjectile(self, dmg: float, speed: float, senderTransform: "Transform") -> None:
        projSpawnOffset = senderTransform.GetForwardVec() * 40
        projSpawnPoint = senderTransform.m_worldPos + projSpawnOffset

        projectile = Entity(
            localPos=projSpawnPoint,
            localRot=senderTransform.m_worldRot,
        )
        projectile.AddComponent(
            Sprite(
                spriteKey="projectile",
                layer=ELayers.ENTITY,
            )
        )
        projectile.AddComponent(LineCollider())
        projectile.AddComponent(
            ProjectileScr(
                dmg=dmg,
                speed=speed,
                dir=senderTransform.GetForwardVec(),
            )
        )

        projectile.GetComponentByType(ProjectileScr).m_scene = self

        self.m_projectiles.append(projectile)

    def CreateBlastArea(self, dmg: float, center: pygame.Vector2, radius: float, countdown: float) -> None:
        blastArea = Entity()
        blastArea.AddComponent(
            BlastAreaScr(
                dmg=dmg,
                center=center,
                radius=radius,
                countdown=countdown,
            )
        )

        blastArea.GetComponentByType(BlastAreaScr).m_scene = self

        self.m_blastAreas.append(blastArea)

    def CreateAmmoBox(self, pos: pygame.Vector2) -> None:
        ammoBox = Entity(localPos=pos)
        ammoBox.AddComponent(
            Sprite(
                spriteKey="ammoBox",
                layer=2,
            )
        )
        ammoBox.AddComponent(BoxCollider())
        ammoBox.AddComponent(AmmoBoxScr())

        if self.m_baseRoot is not None:
            baseScr = self.m_baseRoot.GetComponentByType(BaseScr)
            ammoBox.GetComponentByType(AmmoBoxScr).m_baseScrRef = weakref.ref(baseScr)

    def CreateUI(self) -> "Entity":
        ui = Entity()
        ui.AddComponent(UIScr())

        return ui

    def _LoadMapFromFile(self, path) -> list[list[str]]:
        mapData: list[list[str]] = []

        with open(path, "r") as file:
            for line in file:
                row = line.strip().split()
                mapData.append(row)

        return mapData