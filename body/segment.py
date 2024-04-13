from dataclasses import dataclass

import pygame

from node import Node


@dataclass
class Segment:
    start: Node
    end: Node
    width: int

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        # TODO: cap the ends
        pygame.draw.line(screen, color, self.start.project(), self.end.project(), self.width)
