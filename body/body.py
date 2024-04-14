import random
import pygame
from pygame import Vector3

from body.gene import Gene

SEED = None
RANDOM_STATE = random.Random(SEED)


class BodyPart:
    def __init__(
        self,
        gene: Gene,
        points: list[Vector3],
        parent_offset: Vector3,
        color: pygame.Color | None = None,
    ):
        self.gene = gene
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

    def grow(self, all_children: list[tuple["BodyPart", int]]): ...

    def draw(self, screen: pygame.Surface, global_offset: Vector3): ...
