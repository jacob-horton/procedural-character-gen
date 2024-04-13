from dataclasses import dataclass

import pygame
from pygame import Vector3

from body.algo.projection import predefined_projection


@dataclass
class Segment:
    start: Vector3
    end: Vector3
    width: int

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        # TODO: cap the ends
        start = predefined_projection(self.start)
        end = predefined_projection(self.end)
        pygame.draw.line(screen, color, start, end, self.width)
