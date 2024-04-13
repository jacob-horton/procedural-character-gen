import pygame
from pygame import Vector3
from body.node import RESOLUTION, Circle
from body.algo.body_generator import GrowthGenerator, RootNode

from body.polygon import Polygon

THICKNESS = 10
centre = RESOLUTION / 2

gg = GrowthGenerator(seed=None)
root_circle = Circle(Vector3(0,0,0), centre, THICKNESS)
root_node = RootNode(root_circle.node, gg, n=30, initial_distance=10)

def render(screen: pygame.Surface, space: bool):
    root_circle.draw(screen)
    for i in gg.points:
        Circle(i, centre, THICKNESS).draw(screen)

    polygon = Polygon.from_3d_points(gg.points)
    polygon.pos = centre
    polygon.draw(screen, pygame.Color(50, 180, 255))

    if space:
        gg.grow(repulsion=10)
