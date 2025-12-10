import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pygame

from pyre.display import Window
from pyre.managers import InputManager, SystemManager
from pyre.systems import RenderSystem, ScriptSystem
from pyre.time import Time

from scene import Scene

# ///////////////////////////////////////////////////////////////////////////
# Init
pygame.init()

window = Window(width=1280, height=768, title="BlastField")

inputMgr = InputManager().GetInstance()
systemMgr = SystemManager.GetInstance()

renderSys = systemMgr.GetSystemInstanceByType(RenderSystem)
scriptSys = systemMgr.GetSystemInstanceByType(ScriptSystem)

currentScene = Scene()

# ///////////////////////////////////////////////////////////////////////////

running = True
while running:
    Time.Update()

    inputMgr.Update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if InputManager.GetInstance().GetKeyDown(pygame.K_c):
        renderSys.m_debugColliders = not renderSys.m_debugColliders

    if InputManager.GetInstance().GetKeyDown(pygame.K_v):
        renderSys.m_debugFPS = not renderSys.m_debugFPS

    scriptSys.Update()

    window.m_surface.fill((0, 0, 0))

    renderSys.Render(window.m_surface)

    pygame.display.flip()