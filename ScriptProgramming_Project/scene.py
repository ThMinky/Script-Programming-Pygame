import pygame

# Engine
from pyre.components import Sprite, Transform
from pyre.components.colliders import BoxCollider, CircleCollider, LineCollider, PointCollider
from pyre.entities import Entity

# Game
from project.player.player_script import PlayerScript


class Scene:
    def __init__(self):
        self.m_entities: list[Entity] = []

        self.playerTankBody = Entity(localPos=pygame.Vector2(500, 500), localScale=pygame.Vector2(0.4, 0.4))
        self.playerTankBody.AddComponent(Sprite(texturePath="resources/tanks/type_a/01_hull.png"))
        self.playerTankBody.AddComponent(BoxCollider())
        self.playerTankBody.AddComponent(PlayerScript())

        self.m_entities.append(self.playerTankBody)

        self.playerTankTurret = Entity(parentTransform=self.playerTankBody.GetComponent(Transform))
        self.playerTankTurret.AddComponent(Sprite(texturePath="resources/tanks/type_a/01_turret.png"))
        self.playerTankTurret.AddComponent(LineCollider())

        self.m_entities.append(self.playerTankTurret)

        player_script = self.playerTankBody.GetComponent(PlayerScript)
        player_script.m_turrent = self.playerTankTurret