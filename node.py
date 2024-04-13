''' do maths'''
from dataclasses import dataclass
import pygame
import numpy as np

from projection import predefined_projection

RESOLUTION = (1280, 720)
center = (RESOLUTION[0]/2, RESOLUTION[1]/2)

class Node:
    def __init__(self, x: float, y: float, z: float):
        self.x = x + center[0]
        self.y = y + center[1]
        self.z = z

    # replace
    def project(self):
        projected = predefined_projection(np.array([self.x, self.y, self.z]))

        return [projected[0], projected[1]]
    
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
    radius: float

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        p, c = self.node.ortho_heat()
        pygame.draw.circle(screen, c, p, self.radius)
