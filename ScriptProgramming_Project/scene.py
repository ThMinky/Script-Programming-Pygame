import pygame

# Engine
from pyre.components import Sprite, Transform
from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider
from pyre.entities import Entity
from pyre.managers import SpriteManager

# Game
from project.player.player_script import PlayerScript


class Scene:
    def __init__(self):
        SpriteManager.GetInstance().RegisterSprite("0", "resources/tile_sand.png")
        SpriteManager.GetInstance().RegisterSprite("1", "resources/roads/tile_road_hor.png")
        SpriteManager.GetInstance().RegisterSprite("2", "resources/roads/tile_road_ver.png")
        SpriteManager.GetInstance().RegisterSprite("3", "resources/roads/tile_road_corner_ur.png")
        SpriteManager.GetInstance().RegisterSprite("4", "resources/roads/tile_road_corner_ul.png")
        SpriteManager.GetInstance().RegisterSprite("5", "resources/roads/tile_road_corner_dr.png")
        SpriteManager.GetInstance().RegisterSprite("6", "resources/roads/tile_road_corner_dl.png")
        SpriteManager.GetInstance().RegisterSprite("7", "resources/roads/tile_road_cross_r.png")
        SpriteManager.GetInstance().RegisterSprite("8", "resources/roads/tile_road_r_cross_r.png")
        SpriteManager.GetInstance().RegisterSprite("9", "resources/roads/tile_road_split_l.png")
        SpriteManager.GetInstance().RegisterSprite("10", "resources/roads/tile_road_split_u.png")
        SpriteManager.GetInstance().RegisterSprite("11", "resources/roads/tile_road_split_r.png")
        SpriteManager.GetInstance().RegisterSprite("12", "resources/roads/tile_road_split_d.png")

        # Loading Map
        self.tiles = self.LoadMapFromFile("map.txt")

        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[i])):
                tileId = self.tiles[i][j]

                posX = j * 64 + 64 / 2
                posY = i * 64 + 64 / 2

                tile = Entity(localPos=pygame.Vector2(posX, posY))
                tile.AddComponent(Sprite(surface=SpriteManager.GetInstance().GetSprite(tileId), layer=0))

        SpriteManager.GetInstance().RegisterSprite("body", "resources/tankBody_dark_outline.png")
        SpriteManager.GetInstance().RegisterSprite("turret", "resources/tankDark_barrel2_outline.png")

        self.playerTankBody = Entity(
            localPos=pygame.Vector2(500, 500),
            localScale=pygame.Vector2(0.5, 0.5),
        )
        self.playerTankBody.AddComponent(
            Sprite(
                surface=SpriteManager().GetInstance().GetSprite("body"),
                layer=5,
            )
        )
        self.playerTankBody.AddComponent(BoxCollider())
        self.playerTankBody.AddComponent(PlayerScript())

        self.playerTankTurret = Entity(
            parentTransform=self.playerTankBody.GetComponentByType(Transform),
            localPos=pygame.Vector2(0, 10),
            localRot=180,
        )
        self.playerTankTurret.AddComponent(Sprite(surface=SpriteManager().GetInstance().GetSprite("turret")))
        self.playerTankTurret.AddComponent(
            LineCollider(
                length=40,
                offset=pygame.Vector2(0, 15),
            )
        )

        player_script = self.playerTankBody.GetComponentByType(PlayerScript)
        player_script.m_turrent = self.playerTankTurret

    def LoadMapFromFile(self, path) -> list:
        mapData = []

        with open(path, "r") as file:
            for line in file:
                row = line.strip().split()
                mapData.append(row)

        return mapData