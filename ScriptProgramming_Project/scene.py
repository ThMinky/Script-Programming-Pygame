from enum import IntEnum

import math
import random

import pygame

# Engine
from pyre.components import Sprite, Transform
from pyre.components.colliders import BoxCollider, LineCollider
from pyre.entities import Entity
from pyre.managers import SpriteManager

# Project
from project.enemies import BasicEnemy, BossTag, EnemySpawner, HellspotEnemy, KamikazeEnemy
from project.player.player_script import PlayerScript
from project import Base
from project import Blocker
from project import Projectile


class ELayers(IntEnum):
    TILE = 0
    DECOR = 1
    INTERACT = 2
    ENTITY = 3
    UI = 4


class Scene:
    def __init__(self):
        self.m_mapTiles: list["Entity"] = []
        self.m_mapBounds: list["Entity"] = []
        self.m_mapDecors: list["Entity"] = []

        self.m_baseRoot: "Entity" | None = None
        self.m_player: "Entity" | None = None

        self.m_enemySpawner: "Entity" | None = None
        self.m_enemies: list["Entity"] = []

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
        SpriteManager.GetInstance().RegisterSprite("explodeBarrelSize", "resources/decor/explode_barrel_side.png")

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

        SpriteManager.GetInstance().RegisterSprite("hellspot", "resources/tanks/tank_hull_kamikaze.png")

        SpriteManager.GetInstance().RegisterSprite("projectile", "resources/tanks/tank_projectile.png")

        # //////////////////////////////////////////////////

        self.m_mapTiles = self.CreateMap("map.txt", (64, 64))
        self.m_mapBounds = self.CreateMapBounds(1280, 768)
        self.m_mapDecors = self.CreateDecor(45, 75)

        self.m_baseRoot = self.CreateBase(pygame.Vector2(640, 384))
        self.m_player = self.CreatePlayer(pygame.Vector2(450, 450))

        # self.CreateBasicEnemy(pygame.Vector2(1280, 384), 90)

        self.m_enemySpawner = self.CreateEnemySpawner()

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
        topBound.AddComponent(Blocker())
        bounds.append(topBound)

        leftBound = Entity(localPos=pygame.Vector2((thickness / 2) - 10, mapHeight / 2))
        leftBound.AddComponent(BoxCollider(size=pygame.Vector2(thickness, mapHeight)))
        leftBound.AddComponent(Blocker())
        bounds.append(leftBound)

        bottomBound = Entity(localPos=pygame.Vector2(mapWidth / 2, (mapHeight - thickness / 2) + 9))
        bottomBound.AddComponent(BoxCollider(size=pygame.Vector2(mapWidth, thickness)))
        bottomBound.AddComponent(Blocker())
        bounds.append(bottomBound)

        rightBound = Entity(localPos=pygame.Vector2((mapWidth - thickness / 2) + 9, mapHeight / 2))
        rightBound.AddComponent(BoxCollider(size=pygame.Vector2(thickness, mapHeight)))
        rightBound.AddComponent(Blocker())
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
        baseRoot.AddComponent(Base())
        baseRoot.AddComponent(Blocker())

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
        hull.AddComponent(PlayerScript())

        barrel = Entity(
            localPos=pygame.Vector2(0, -5),
            parentTransform=hull.GetComponentByType(Transform),
        )
        barrel.AddComponent(Sprite(spriteKey="sandTankBarrel"))

        hull.GetComponentByType(PlayerScript).m_barrel = barrel
        hull.GetComponentByType(PlayerScript).m_scene = self

        return hull

    def CreateEnemySpawner(self) -> "Entity":
        enemySpawner = Entity()
        enemySpawner.AddComponent(EnemySpawner())

        enemySpawner.GetComponentByType(EnemySpawner).m_scene = self

        return enemySpawner

    def CreateBasicEnemy(self, pos: pygame.Vector2, rot: float) -> None:
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
        hull.AddComponent(BasicEnemy())
        hull.AddComponent(Blocker())

        barrel = Entity(
            localPos=pygame.Vector2(0, -5),
            parentTransform=hull.GetComponentByType(Transform),
        )
        barrel.AddComponent(Sprite(spriteKey="darkTankBarrel"))

        hull.GetComponentByType(BasicEnemy).m_barrelTransform = barrel.GetComponentByType(Transform)
        hull.GetComponentByType(BasicEnemy).m_scene = self

        self.m_enemies.append(hull)

        return hull

    def CreateHellspotEnemy(self, pos: pygame.Vector2, rot: float) -> None:
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
        hull.AddComponent(BoxCollider())
        hull.AddComponent(HellspotEnemy())
        hull.AddComponent(BossTag())
        hull.AddComponent(Blocker())

        hull.GetComponentByType(HellspotEnemy).m_scene = self

        self.m_enemies.append(hull)

        return hull

    def CreateKamikazeEnemy(self, pos: pygame.Vector2, rot: float) -> None:
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
        hull.AddComponent(KamikazeEnemy())
        hull.AddComponent(BossTag())
        hull.AddComponent(Blocker())

        hull.GetComponentByType(KamikazeEnemy).m_scene = self

        self.m_enemies.append(hull)

        return hull

    def CreateProjectile(self, dmg: int, speed: int, senderTransform: "Transform"):
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
        projectile.AddComponent(Projectile(dmg, speed, senderTransform.GetForwardVec()))

    def _LoadMapFromFile(self, path) -> list[list[str]]:
        mapData: list[list[str]] = []

        with open(path, "r") as file:
            for line in file:
                row = line.strip().split()
                mapData.append(row)

        return mapData