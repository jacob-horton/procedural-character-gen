from dataclasses import dataclass
import pygame
import numpy as np

from body.algo.projection import predefined_projection
from body.algo.gift_wrapping import gift_wrap

@dataclass
class Polygon:
    # [[x1, y1], [x2, y2], ...]
    points: np.ndarray
    translation: np.ndarray

    def draw(self, screen: pygame.Surface, color: pygame.Color | str = "black"):
        pygame.draw.polygon(
            screen,
            color,
            [p + self.translation for p in self.points]
        )

    @staticmethod
    def from_3d_points(points: np.ndarray) -> 'Polygon':
        points_2d = np.array([predefined_projection(p) for p in points])
        hull = gift_wrap(points_2d)
        return Polygon(hull, np.zeros(2))
