import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame

# Engine
from pyre.display import Window
from pyre.managers import InputManager, SystemManager
from pyre.systems import RenderSystem, ScriptSystem
from pyre.time import Time


# Project
from project.debug import ToggleCollidersDebug, ToggleFpsDebug

# Scene
from scene import Scene

# ///////////////////////////////////////////////////////////////////////////
# Init
pygame.init()
window = Window(1280, 768, "BlastField")
window.Init()
clock = pygame.time.Clock()

systemManager = SystemManager.GetInstance()
systemManager.Init()

renderSystem = systemManager.GetSystemInstanceByType(RenderSystem)
scriptSystem = systemManager.GetSystemInstanceByType(ScriptSystem)

currentScene = Scene()

# ///////////////////////////////////////////////////////////////////////////

running = True
while running:
    InputManager.GetInstance().Update()
    Time.Update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if InputManager.GetInstance().GetKeyDown(pygame.K_c):
        ToggleCollidersDebug().GetInstance().Execute()

    if InputManager.GetInstance().GetKeyDown(pygame.K_v):
        ToggleFpsDebug().GetInstance().Execute()

    scriptSystem.Update()

    window.m_surface.fill((0, 0, 0))

    renderSystem.Render(window.m_surface)

    pygame.display.flip()