import pygame

from pyre.window import Window
from pyre.managers import SystemManager, InputManager
from pyre.entities import Entity
from pyre.components import BaseComponent, Transform, Sprite, Movement
from pyre.components.colliders import BaseCollider, BoxCollider, CircleCollider
from pyre.systems import TransformSystem, RenderSystem, CollisionSystem, MovementSystem
from pyre.commands import (
    MoveForward,
    MoveBackward,
    RotateHullLeft,
    RotateHullRight,
    RotateTurretLeft,
    RotateTurretRight,
    ToggleColliderDebug,
)


class Game:
    def __init__(self) -> None:
        self.m_window = None

        # Managers
        self.m_inputManager = None
        self.m_systemManager = None

        # Systems
        self.m_transformSystem = None
        self.m_collisionSystem = None
        self.m_renderSystem = None

        self.m_clock = pygame.time.Clock()

        self.m_running = False

    def Init(self, width: int, height: int, title: str) -> None:
        # ///////////////////////////////////////////////////////////////////////////
        # Initialization
        _, failed = pygame.init()
        if failed > 0:
            raise RuntimeError(f"Pygame failed to initialize {failed} module(s)")

        # ///////////////////////////////////////////////////////////////////////////
        # Window Setup
        self.m_window = Window(width, height, title)
        self.m_window.Init()

        # ///////////////////////////////////////////////////////////////////////////
        # Managers Setup
        self.m_inputManager = InputManager().GetInstance()
        self.m_inputManager.Init()

        self.m_systemManager = SystemManager.GetInstance()
        self.m_systemManager.Init()
        # ///////////////////////////////////////////////////////////////////////////
        # Systems Setup
        self.m_transformSystem = self.m_systemManager.GetSystemInstance(TransformSystem)
        self.m_collisionSystem = self.m_systemManager.GetSystemInstance(CollisionSystem)
        self.m_renderSystem = self.m_systemManager.GetSystemInstance(RenderSystem)

        # ///////////////////////////////////////////////////////////////////////////
        # Player Setup
        self.m_tankBody = Entity(
            localPos=pygame.Vector2(500, 500),
            localScale=pygame.Vector2(0.40, 0.40),
        )
        self.m_tankBody.AddComponent(
            Sprite(texturePath="resources/tanks/type_a/01_hull.png")
        )
        self.m_tankBody.AddComponent(BoxCollider())
        self.m_tankBody.AddComponent(Movement(moveSpeed=50, rotSpeed=25))

        self.m_tankTurret = Entity(
            parentTransform=self.m_tankBody.GetComponent(Transform),
        )
        self.m_tankTurret.AddComponent(
            Sprite(
                texturePath="resources/tanks/type_a/01_turret.png",
                pivot=pygame.Vector2(50, 170),
            )
        )
        self.m_tankTurret.AddComponent(BoxCollider())
        self.m_tankTurret.AddComponent(Movement(moveSpeed=0, rotSpeed=20))

        # ///////////////////////////////////////////////////////////////////////////
        # Commands Setup
        self.m_keyCommands = {
            "W": MoveForward(self.m_tankBody),
            "A": RotateHullLeft(self.m_tankBody),
            "S": MoveBackward(self.m_tankBody),
            "D": RotateHullRight(self.m_tankBody),
            "Q": RotateTurretLeft(self.m_tankTurret),
            "E": RotateTurretRight(self.m_tankTurret),
            "C": ToggleColliderDebug(),
        }

    def Loop(self) -> None:
        self.m_running = True

        while self.m_running:
            # Update
            dt = self.m_clock.tick(60) / 1000.0

            self.m_inputManager.Update()
            self.m_transformSystem.Update(dt)
            self.m_collisionSystem.Update(dt)

            # Logic
            if self.m_inputManager.QuitRequested():
                self.m_running = False

            if self.m_inputManager.IsKeyHeld("W"):
                self.m_keyCommands["W"].Execute(dt)
            if self.m_inputManager.IsKeyHeld("A"):
                self.m_keyCommands["A"].Execute(dt)
            if self.m_inputManager.IsKeyHeld("S"):
                self.m_keyCommands["S"].Execute(dt)
            if self.m_inputManager.IsKeyHeld("D"):
                self.m_keyCommands["D"].Execute(dt)
            if self.m_inputManager.IsKeyHeld("Q"):
                self.m_keyCommands["Q"].Execute(dt)
            if self.m_inputManager.IsKeyHeld("E"):
                self.m_keyCommands["E"].Execute(dt)

            if self.m_inputManager.IsKeyPressed("C"):
                self.m_keyCommands["C"].Execute()

            # Render
            self.m_renderSystem.Render(self.m_window.Get())

            pygame.display.flip()
            self.m_window.m_surface.fill("black")

    def Uninit(self) -> None:
        pygame.quit()