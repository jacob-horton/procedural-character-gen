import random
import pygame
from pygame import Vector3

SEED = None
RANDOM_STATE = random.Random(SEED)


class BodyPart:
    def __init__(
        self,
        points: list[Vector3],
        parent_offset: Vector3,
        color: pygame.Color | None = None,
    ):
        self.children: list["BodyPart"] = []
        self.points = points
        self.parent_offset = parent_offset

        if color is None:
            color = pygame.Color(
                random.randrange(256), random.randrange(256), random.randrange(256)
            )
        self.color = color

    def append_to(self, parent: "BodyPart"): ...

    def __repr__(self):
        return f"<{self.__class__} with {len(self.children)}>"

    def draw(self, screen: pygame.Surface, global_offset: Vector3): ...

    """
    def create_limb(self, point: Vector3):
        limb = Limb(point, [point], color=self.color)
        self.children.append(limb)
        return limb
    
    def create_blob(self, point: Vector3, n: int = 20, initial_distance: int = 10, growth_rate: float = 10, repulsion: float = 1):
        points = make_points(n, initial_distance)
        blob = Blob(point, points, growth_rate, repulsion)
        self.children.append(blob)
        return blob
    """
