''' do maths'''
from dataclasses import dataclass
import pygame
from pygame import Vector3

from body.algo.projection import predefined_projection

@dataclass
class Circle:
    node: Vector3
    radius: float

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        point = predefined_projection(self.node)
        pygame.draw.circle(screen, color, point, self.radius)
