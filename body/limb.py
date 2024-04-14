from dataclasses import dataclass
import random

import pygame
from pygame import Vector3
from body.body import BodyPart
from algo.projection import predefined_projection


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
        # TODO: cap the ends
        start = predefined_projection(self.start + global_offset)
        end = predefined_projection(self.end + global_offset)
        pygame.draw.line(screen, color, start, end, self.width)


class Limb(BodyPart):
    """
    Limbs are linear sequences of 3D vectors which are projected into the
    2D plane and rendered as segments (lines joining sequential points).
        The limb will extend outwards equal to the offset of the point it was created from in that point.
        You can
    """

    def __init__(
        self,
        parent: BodyPart,
        parent_offset: Vector3,
        thickness: int = 50,
        color: pygame.Color | None = None,
    ):
        self.thickness = thickness
        super().__init__([parent_offset], parent_offset, color=color)
        self.append_to(parent)

    def append_to(self, parent: BodyPart):
        parent.children.append(self)

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset + self.parent_offset

        pygame.draw.circle(
            screen,
            self.color,
            predefined_projection(self.parent_offset),
            self.thickness / 2,
        )

        pygame.draw.circle(
            screen,
            self.color,
            predefined_projection(self.parent_offset + self.points[0]),
            self.thickness / 2,
        )

        Segment(
            self.parent_offset, self.parent_offset + self.points[0], self.thickness
        ).draw(screen, global_offset, self.color)

        for i in self.children:
            i.draw(screen, global_pos)
