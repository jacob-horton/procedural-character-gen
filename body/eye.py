from dataclasses import dataclass
import random
import pygame
from pygame import Vector2, Vector3

from body.algo.projection import predefined_projection

@dataclass
class Eye:
    pos: Vector3
    radius: float

    def draw(self, screen: pygame.Surface):
        projected = predefined_projection(self.pos)

        pygame.draw.circle(
            screen,
            "white",
            projected,
            self.radius
        )

        pupil_offset = (pygame.mouse.get_pos() - projected).normalize() * self.radius * 0.5
        twitch_offset = Vector2(random.random(), random.random()) * self.radius * 0.2

        pygame.draw.circle(
            screen,
            "black",
            projected + pupil_offset + twitch_offset,
            self.radius * 0.3
        )
