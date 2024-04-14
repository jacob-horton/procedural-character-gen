from dataclasses import dataclass
import random

import pygame
from pygame import Vector3
from algo.randpoints import distribute_points
from body.body import BodyPart, NewPart
from algo.projection import ZOOM, predefined_projection
from body.eye import Eye
from body.gene import Gene
from graphics.line import draw_line
import body.gene as gene


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
        angle_variation: float = 1.0,
        color: pygame.Color | None = None,
    ):
        self.thickness = thickness
        self.growth_rate = gene.limb_growth_rate

        p = distribute_points(1, angle_variation)[0]
        movement_vector = parent_offset.normalize() + p
        super().__init__(
            gene,
            [movement_vector * initial_length],
            parent_offset,
            color=color,
        )
        self.append_to(parent)

    def append_to(self, parent: BodyPart):
        parent.children.append(self)

    def grow(self, depth, all_children):
        self.points[0] *= self.growth_rate
        self.growth_rate = 1 + ((self.growth_rate - 1) * 0.95)
        # spawn blob
        chance = (
            self.gene.blob_on_limb_percent * self.gene.blob_on_limb_attenuation**depth
        )
        if gene.RANDOM.random() * 100 < chance:
            return NewPart("Blob", self.points[0])

        for point in self.points:
            chance = (
                self.gene.limb_on_limb_percent
                * self.gene.limb_on_limb_attenuation**depth
            ) / len(self.points)
            if gene.RANDOM.random() * 100 < chance:
                return NewPart("Limb", point)

            if (
                gene.RANDOM.random() * 100
                < self.gene.eye_on_limb_percent
                * self.gene.eye_on_limb_attenuation**depth
            ):
                if any([e.parent_offset == point for e in self.eyes]):
                    continue

                size = (
                    self.gene.eye_size
                    + self.gene.eye_size_variation * gene.RANDOM.random()
                )
                self.eyes.append(Eye(point, size))

    def draw_self(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset + self.parent_offset
        draw_line(
            screen,
            self.color,
            predefined_projection(global_pos),
            predefined_projection(global_pos + self.points[0]),
            self.thickness,
            end_scale=0.8,
        )
