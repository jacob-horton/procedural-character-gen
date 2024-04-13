import pygame
from body.node import RESOLUTION, Circle, Node
from body.algo.body_generator import GrowthGenerator
import numpy as np

from body.polygon import Polygon

THICKNESS = 10
root = Circle(Node(0, 0, 0), np.zeros(2), THICKNESS)
gg = GrowthGenerator(root, n=50, seed=None, initial_distance=10)
print(gg.point_list)

def render(screen: pygame.Surface, space: bool):
    root.draw(screen)
    centre = np.array(RESOLUTION) / 2
    for i in gg.point_list:
        Circle(Node(*i), centre, THICKNESS).draw(screen)

    polygon = Polygon.from_3d_points(np.array(gg.point_list))
    polygon.translation = centre
    polygon.draw(screen, pygame.Color(50, 180, 255))

    if space:
        gg.grow(repulsion=10)
        print(gg.point_list)
