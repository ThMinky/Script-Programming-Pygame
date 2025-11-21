import os

import pygame

from pyre.display import Window
from pyre.managers import SystemManager, InputManager


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ///////////////////////////////////////////////////////////////////////////
# ENGINE INIT
pygame.init()
window = pyre.display.Window(1280, 720, "BlastField")
clock = pygame.time.Clock()



# ///////////////////////////////////////////////////////////////////////////
