from dataclasses import dataclass
import random

import pygame
from pygame import Vector3
from algo.randpoints import distribute_points
from body.body import BodyPart
from algo.projection import predefined_projection
from body.gene import Gene
from graphics.line import draw_line


@dataclass
class Segment:
    start: Vector3
    end: Vector3
    width: int

    def draw(
        self,
        screen: pygame.Surface,
        global_offset: Vector3,
        color: pygame.Color | str = "black",
    ):
        start = predefined_projection(self.start + global_offset)
        end = predefined_projection(self.end + global_offset)
        draw_line(screen, color, start, end, self.width, end_scale=0.7)


class Limb(BodyPart):
    """
    Limbs are linear sequences of 3D vectors which are projected into the
    2D plane and rendered as segments (lines joining sequential points).
        The limb will extend outwards equal to the offset of the point it was created from in that point.
        You can
    """

    def __init__(
        self,
        gene: Gene,
        parent: BodyPart,
        parent_offset: Vector3,
        # hyperparameters
        thickness: int = 50,
        initial_length: float = 10,
        angle_variation: float = 0.1,
        color: pygame.Color | None = None,
    ):
        self.thickness = thickness
        self.growth_rate = gene.limb_growth_rate

        p = distribute_points(1, angle_variation)[0]
        movement_vector = parent_offset.normalize() + p
        super().__init__(
            gene, [movement_vector * initial_length], parent_offset, color=color
        )
        self.append_to(parent)

    def append_to(self, parent: BodyPart):
        parent.children.append(self)

    def grow(self, depth, all_children):
        self.points[0] *= self.growth_rate
        self.growth_rate = 1 + ((self.growth_rate - 1) * 0.99)

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset + self.parent_offset

        Segment(
            self.parent_offset, self.parent_offset + self.points[0], self.thickness
        ).draw(screen, global_offset, self.color)

        for i in self.children:
            i.draw(screen, global_pos)
