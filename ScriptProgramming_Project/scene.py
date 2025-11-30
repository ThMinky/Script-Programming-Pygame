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
        SpriteManager.GetInstance().RegisterSprite("body", "resources/tanks/type_a/01_hull.png")
        SpriteManager.GetInstance().RegisterSprite("turret","resources/tanks/type_a/01_turret.png")
        
        # To Do fix Sprite

        self.playerTankBody = Entity(localPos=pygame.Vector2(500, 500), localScale=pygame.Vector2(0.4, 0.4))
        self.playerTankBody.AddComponent(Sprite(texturePath="resources/tanks/type_a/01_hull.png"))
        self.playerTankBody.AddComponent(BoxCollider())
        self.playerTankBody.AddComponent(PlayerScript())

        self.playerTankTurret = Entity(parentTransform=self.playerTankBody.GetComponentByType(Transform))
        self.playerTankTurret.AddComponent(Sprite(texturePath="resources/tanks/type_a/01_turret.png"))
        self.playerTankTurret.AddComponent(LineCollider())

        player_script = self.playerTankBody.GetComponentByType(PlayerScript)
        player_script.m_turrent = self.playerTankTurret