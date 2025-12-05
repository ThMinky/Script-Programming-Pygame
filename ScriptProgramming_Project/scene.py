from enum import IntEnum

import math
import random

import pygame

# Engine
from pyre.components import Sprite, Transform
from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider
from pyre.entities import Entity
from pyre.managers import SpriteManager

# Project
from project.player.player_script import PlayerScript


class ELayers(IntEnum):
    TILE = 0
    DECOR = 1
    INTERACT = 2
    ENTITY = 3
    UI = 4


class Scene:
    def __init__(self):
        self.m_player: Entity | None = None

        self.m_baseRoot: Entity | None = None
        self.m_base: list[Entity] = []

        self.m_map: list[Entity] = []
        self.m_decor: list[Entity] = []

        self.m_enemiesBasic: list[Entity] = []
        self.m_enemiesElite: list[Entity] = []

        # Register Sprites
        # //////////////////////////////////////////////////
        self.spriteMng = SpriteManager.GetInstance()

        # Tiles
        self.spriteMng.RegisterSprite("0", "resources/tiles/sand.png")
        self.spriteMng.RegisterSprite("1", "resources/tiles/road_hor.png")
        self.spriteMng.RegisterSprite("2", "resources/tiles/road_ver.png")
        self.spriteMng.RegisterSprite("3", "resources/tiles/road_corner_ur.png")
        self.spriteMng.RegisterSprite("4", "resources/tiles/road_corner_ul.png")
        self.spriteMng.RegisterSprite("5", "resources/tiles/road_corner_dr.png")
        self.spriteMng.RegisterSprite("6", "resources/tiles/road_corner_dl.png")
        self.spriteMng.RegisterSprite("7", "resources/tiles/road_cross_r.png")
        self.spriteMng.RegisterSprite("8", "resources/tiles/road_r_cross_r.png")
        self.spriteMng.RegisterSprite("9", "resources/tiles/road_split_l.png")
        self.spriteMng.RegisterSprite("10", "resources/tiles/road_split_u.png")
        self.spriteMng.RegisterSprite("11", "resources/tiles/road_split_r.png")
        self.spriteMng.RegisterSprite("12", "resources/tiles/road_split_d.png")

        # Tank Hulls / Turrets
        self.spriteMng.RegisterSprite("darkTankHull", "resources/tanks/tank_hull_dark.png")
        self.spriteMng.RegisterSprite("darkTankTurret", "resources/tanks/tank_turret_dark.png")

        # Auto Turret Stand / Head
        self.spriteMng.RegisterSprite("autoTurretHead", "resources/autoTurret/auto_turret_head.png")
        self.spriteMng.RegisterSprite("autoTurretStand", "resources/autoTurret/auto_turret_stand.png")

        # Ammo Wire / Barrel
        self.spriteMng.RegisterSprite("ammoWire", "resources/autoTurret/ammo_wire.png")
        self.spriteMng.RegisterSprite("ammoBarrel", "resources/autoTurret/ammo_barrel.png")

        # Sand Bag
        self.spriteMng.RegisterSprite("sandbag", "resources/decor/sandbag.png")

        # Bushs / Twigs / Leafs
        self.spriteMng.RegisterSprite("bush", "resources/decor/bush.png")
        self.spriteMng.RegisterSprite("twigs", "resources/decor/twigs.png")
        self.spriteMng.RegisterSprite("leaf", "resources/decor/leaf.png")

        # //////////////////////////////////////////////////

        self.m_map = self.CreateMap("map.txt", (64, 64))

        self.m_decor = self.CreateDecor(45, 75)

        self.m_base = self.CreateBase(pygame.Vector2(640, 384))

        self.m_player = self.CreatePlayer(pygame.Vector2(200, 200))

    def CreateMap(self, path: str, tileSize: tuple[int, int]) -> list[Entity]:
        self.tiles: list[Entity] = []
        self.mapData = self._LoadMapFromFile(path)

        for i in range(len(self.mapData)):
            for j in range(len(self.mapData[i])):
                tileId = self.mapData[i][j]

                posX = j * tileSize[0] + tileSize[0] / 2
                posY = i * tileSize[1] + tileSize[1] / 2

                tile = Entity(localPos=pygame.Vector2(posX, posY))
                tile.AddComponent(
                    Sprite(
                        surface=self.spriteMng.GetSprite(tileId),
                        layer=ELayers.TILE,
                    )
                )
                self.tiles.append(tile)

        return self.tiles

    def CreateDecor(self, minRadius: int, maxRadius: int) -> list[Entity]:
        decorEntities: list[Entity] = []

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
                    surface=self.spriteMng.GetSprite("bush"),
                    layer=ELayers.DECOR,
                )
            )
            decorEntities.append(bush)

            twigCount = random.randint(1, 2)
            for _ in range(twigCount):
                offset = randomOffset()
                twig = Entity(localPos=bushPos + offset)
                twig.AddComponent(
                    Sprite(
                        surface=self.spriteMng.GetSprite("twigs"),
                        layer=ELayers.DECOR,
                    )
                )
                decorEntities.append(twig)

            leafCount = random.randint(1, 3)
            for _ in range(leafCount):
                offset = randomOffset()
                leaf = Entity(localPos=bushPos + offset)
                leaf.AddComponent(
                    Sprite(
                        surface=self.spriteMng.GetSprite("leaf"),
                        layer=ELayers.DECOR,
                    )
                )
                decorEntities.append(leaf)

        return decorEntities

    def CreateBase(self, center: pygame.Vector2) -> list:
        baseEntities: list[Entity] = []

        # Root
        baseRoot = Entity(localPos=center)
        baseRoot.AddComponent(BoxCollider(size=pygame.Vector2(130, 130)))
        self.m_baseRoot = baseRoot
        baseEntities.append(baseRoot)

        baseTransform = baseRoot.GetComponentByType(Transform)

        # Offsets
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

        # Ammo Barrel
        ammoBarrel = Entity(parentTransform=baseTransform)
        ammoBarrel.AddComponent(
            Sprite(
                surface=self.spriteMng.GetInstance().GetSprite("ammoBarrel"),
                layer=ELayers.INTERACT,
            )
        )
        baseEntities.append(ammoBarrel)

        # Ammo Wires
        for pos, rot, scale in wireOffsets:
            ammoWire = Entity(
                parentTransform=baseTransform,
                localPos=pos,
                localRot=rot,
                localScale=scale,
            )
            ammoWire.AddComponent(
                Sprite(
                    surface=self.spriteMng.GetSprite("ammoWire"),
                    layer=ELayers.ENTITY,
                )
            )
            baseEntities.append(ammoWire)

        # Turret Stands / Turret Heads
        for off in turretOffsets:
            # Turret Stand
            turretStand = Entity(
                localPos=off,
                parentTransform=baseTransform,
            )
            turretStand.AddComponent(
                Sprite(
                    surface=self.spriteMng.GetSprite("autoTurretStand"),
                    layer=ELayers.ENTITY,
                )
            )
            baseEntities.append(turretStand)

            # Turret Head
            turretHead = Entity(parentTransform=turretStand.GetComponentByType(Transform))
            turretHead.AddComponent(Sprite(surface=self.spriteMng.GetSprite("autoTurretHead")))
            baseEntities.append(turretHead)

        # Sandbags
        for pos, rot in sandbagOffsets:
            sandbag = Entity(
                localPos=pos,
                localRot=rot,
                parentTransform=baseTransform,
            )
            sandbag.AddComponent(
                Sprite(
                    surface=self.spriteMng.GetSprite("sandbag"),
                    layer=ELayers.INTERACT,
                )
            )
            baseEntities.append(sandbag)

    def CreatePlayer(self, pos: pygame.Vector2) -> Entity:
        hull = Entity(localPos=pos)
        hull.AddComponent(
            Sprite(
                surface=self.spriteMng.GetSprite("darkTankHull"),
                layer=ELayers.ENTITY,
            )
        )
        hull.AddComponent(BoxCollider())
        hull.AddComponent(PlayerScript())

        turret = Entity(
            parentTransform=hull.GetComponentByType(Transform),
            localPos=pygame.Vector2(0, 5),
            localRot=180
        )
        turret.AddComponent(Sprite(surface=self.spriteMng.GetSprite("darkTankTurret")))

        hull.GetComponentByType(PlayerScript).m_turrent = turret

        return hull

    def _LoadMapFromFile(self, path) -> list[list[str]]:
        mapData: list[list[str]] = []

        with open(path, "r") as file:
            for line in file:
                row = line.strip().split()
                mapData.append(row)

        return mapData