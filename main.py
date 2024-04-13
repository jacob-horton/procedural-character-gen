'''
the main script
'''
import pygame
from game.config import RESOLUTION
from game.run import run
from game.render_update import render

# pygame setup
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
running = True

run(screen, clock, render)
