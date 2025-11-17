import os

import pygame

from pyre import Game


os.chdir(os.path.dirname(os.path.abspath(__file__)))

game = Game()
game.Init(1280, 720, "BlastField")

game.Loop()

game.Uninit()