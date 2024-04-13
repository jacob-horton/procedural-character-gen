import pygame
from body.node import Circle, Node
from body.algo.body_generator import GrowthGenerator

THICKNESS = 10
root = Circle(Node(0, 0, 0), THICKNESS)
gg = GrowthGenerator(root, n=10, seed=None, initial_distance=10)
print(gg.point_list)

def render(screen: pygame.Surface, space: bool):
    root.draw(screen)
    for i in gg.point_list:
        Circle(Node(*i), THICKNESS).draw(screen)
    if space:
        gg.grow(repulsion=10)
        print(gg.point_list)