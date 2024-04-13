'''
the main script
'''
import pygame
import game
from node import Node, Circle, RESOLUTION
import random

# pygame setup
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
running = True

SEED = None
RANDOM_STATE = random.Random(SEED)
r = RANDOM_STATE.random
randnode = lambda: Node(*(round((r()*2-1)*100) for _ in range(3)))

THICKNESS = 10
root = Circle(Node(0, 0, 0), THICKNESS)
def render():
    a,b,c = (Circle(randnode(), THICKNESS) for _ in range(3))
    root.draw(screen)
    a.draw(screen, "red")
    b.draw(screen, "green")
    c.draw(screen, "blue")


game.run(screen, clock, render)