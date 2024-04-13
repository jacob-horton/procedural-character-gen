''' do maths'''
from dataclasses import dataclass
import pygame
from pygame import Vector2, Vector3

from body.algo.projection import predefined_projection

RESOLUTION = Vector2(1280, 720)

@dataclass
class Circle:
    node: Vector3
    offset: Vector2
    radius: float

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        point = predefined_projection(self.node) + self.offset
        pygame.draw.circle(screen, color, point, self.radius)
