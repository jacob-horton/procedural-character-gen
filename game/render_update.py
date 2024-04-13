import pygame
from pygame import Vector3
from body.node import RESOLUTION, Circle
from body.algo.body_generator import Creature, Blob

from body.polygon import Polygon

THICKNESS = 10
centre = RESOLUTION / 2
DIFF = 400

gg = Creature(seed=None)
root_node_left = Blob(Vector3(-DIFF//2, 0, 0), gg, n=40, initial_distance=10)
root_node_right  = Blob(Vector3(DIFF//2, 0, 0), gg, n=20, initial_distance=10)

print(root_node_left.points, root_node_right.points, gg.points)
def render(screen: pygame.Surface, space: bool):
    for i in gg.points:
        Circle(i, centre, THICKNESS).draw(screen)

    for i in (root_node_left, root_node_right):
        polygon = Polygon.from_3d_points(i.points)
        polygon.pos = centre
        polygon.draw(screen, pygame.Color(50, 180, 255))

    if space:
        gg.grow(repulsion=10)
        print(root_node_left.points, root_node_right.points, gg.points)
