import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame

# Engine
from pyre.display import Window
from pyre.managers import SystemManager
from pyre.systems import RenderSystem, ScriptSystem
from pyre.inputs import Input
from pyre.time import Time


# Scene
from scene import Scene

# ///////////////////////////////////////////////////////////////////////////
# Init
pygame.init()
window = Window(1280, 720, "BlastField")
window.Init()
clock = pygame.time.Clock()

systemManager = SystemManager.GetInstance()
systemManager.Init()

renderSystem = systemManager.GetSystemInstance(RenderSystem)
scriptSystem = systemManager.GetSystemInstance(ScriptSystem)

currentScene = Scene()

# ///////////////////////////////////////////////////////////////////////////

running = True
while running:
    Input.GetInstance().Update()
    Time.Update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    scriptSystem.Update()

    window.GetSurface().fill((0, 0, 0))

    RenderSystem.GetInstance().Render(window.GetSurface())

    pygame.display.flip()