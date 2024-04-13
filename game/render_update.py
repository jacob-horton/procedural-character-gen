import pygame
from body.node import RESOLUTION, Circle, Node
from body.algo.body_generator import GrowthGenerator, RootNode
import numpy as np

from body.polygon import Polygon

THICKNESS = 10

gg = GrowthGenerator(seed=None)
root_circle = Circle(Node(0,0,0), np.zeros(2), THICKNESS)
root_node = RootNode(root_circle.node, gg, n=30, initial_distance=10)
print(gg.points)

def render(screen: pygame.Surface, space: bool):
    root_circle.draw(screen)
    centre = np.array(RESOLUTION) / 2
    for i in gg.points:
        Circle(Node(*i), centre, THICKNESS).draw(screen)

    polygon = Polygon.from_3d_points(np.array(gg.points))
    polygon.translation = centre
    polygon.draw(screen, pygame.Color(50, 180, 255))

    if space:
        gg.grow(repulsion=10)
        print(gg.points)
