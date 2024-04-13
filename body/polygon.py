from dataclasses import dataclass
import pygame
from pygame import Vector3, Vector2

from body.algo.projection import predefined_projection
from body.algo.gift_wrapping import gift_wrap

@dataclass
class Polygon:
    points: list[Vector2]
    pos: Vector2

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        pygame.draw.polygon(
            screen,
            color,
            [p + self.pos for p in self.points]
        )

    @staticmethod
    def from_3d_points(points: list[Vector3]) -> 'Polygon':
        points_2d = [predefined_projection(p) for p in points]
        hull = gift_wrap(points_2d)
        return Polygon(hull, Vector2())
