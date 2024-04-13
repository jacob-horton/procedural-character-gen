''' do maths'''
from dataclasses import dataclass
import pygame
import numpy as np

from body.algo.projection import predefined_projection

RESOLUTION = (32, 32)

class Node:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    # replace
    def project(self):
        return predefined_projection(np.array([self.x, self.y, self.z]))

    
    def ortho_heat(self):
        if self.z > 0:
            color = pygame.Color(max(0, min(int(self.z), 255)), 0, 0, 0)
        else:
            color = pygame.Color(0, max(0, min(int(abs(self.z)), 255)), 0, 0)
        return ((self.x, self.y), color)

@dataclass
class Circle:
    # do better w subclass
    node: Node
    translation: np.ndarray
    radius: float

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        # p, c = self.node.ortho_heat()
        point = self.node.project()
        pygame.draw.circle(screen, color, list(point + self.translation), self.radius)
