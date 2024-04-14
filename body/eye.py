from dataclasses import dataclass
import pygame
from pygame import Vector2, Vector3
from body.gene import ENV_RANDOM as random

from algo.projection import ZOOM, predefined_projection


@dataclass
class Eye:
    parent_offset: Vector3
    radius: float

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        projected = predefined_projection(self.parent_offset + global_offset)
        radius = self.radius / ZOOM.x * 3

        pygame.draw.circle(screen, "white", projected, radius)

        pupil_offset = (pygame.mouse.get_pos() - projected).normalize() * radius * 0.5
        twitch_offset = Vector2(random.random(), random.random()) * radius * 0.2

        pygame.draw.circle(
            screen, "black", projected + pupil_offset + twitch_offset, radius * 0.3
        )
