import random
from pygame import Vector3
import pygame

from algo.avgvec import avg_vec2s, avg_vec3s
from algo.gift_wrapping import gift_wrap
from algo.projection import predefined_projection
from algo.randpoints import distribute_points
from body.body import BodyPart
from body.eye import Eye


class Blob(BodyPart):
    """
    The parent point chosen becomes the offset for the child (as always).
    The points that make up the blob are generated randomly (with initial_distance multiplier)
    It will be grown by the root Creature according to its rate and repulsion.
    """

    def __init__(
        self,
        parent: BodyPart,
        parent_offset: Vector3,
        n: int = 10,
        initial_distance: int = 10,
        growth_rate: float = 2,
        repulsion: float = 1,
    ):
        # hyperparameters
        self.repulsion = repulsion
        self.growth_rate = growth_rate
        self.n = n
        self.initial_distance = initial_distance
        # rendering
        points = distribute_points(self.n, self.initial_distance)
        self.parent_offset = random.choice(parent.points)
        self.append_to(parent)
        super().__init__(points, parent_offset)

    def append_to(self, parent: BodyPart):
        parent.children.append(self)

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        print(f"I, {self}, am drawing!")
        global_pos = global_offset + self.parent_offset
        for i in self.children:
            i.draw(screen, global_pos)

        projected = [predefined_projection(p + global_pos) for p in self.points]
        hull = gift_wrap(projected)

        avg = avg_vec2s(hull)

        for i in range(len(hull)):
            triangle = [avg, hull[i], hull[(i + 1) % len(hull)]]
            pygame.draw.polygon(
                screen,
                self.color + pygame.Color(i * 10, i * 10, i * 10),
                triangle,
            )

        # for point in projected:
        #     pygame.draw.circle(screen, "black", point, 5)

        Eye(avg_vec3s(self.points), 20).draw(screen, global_pos)
