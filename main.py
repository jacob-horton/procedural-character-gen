'''
the main script
'''
import pygame
import game
from node import Node, Circle, RESOLUTION
from body_generator import GrowthGenerator

# pygame setup
pygame.init()
screen = pygame.display.set_mode(RESOLUTION)
clock = pygame.time.Clock()
running = True

THICKNESS = 10
root = Circle(Node(0, 0, 0), THICKNESS)
gg = GrowthGenerator(root, n=10, seed=None, initial_distance=10)
print(gg.point_list)

def render(space: bool):
    root.draw(screen)
    for i in gg.point_list:
        Circle(Node(*i), THICKNESS).draw(screen)
    if space:
        gg.grow(repulsion=10)
        print(gg.point_list)

game.run(screen, clock, render)