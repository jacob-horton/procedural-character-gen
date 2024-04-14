from typing import Any, Literal, NamedTuple
import pygame
from pygame import Vector3
from algo.projection import predefined_projection_depth
from body.eye import Eye
from body.gene import Gene
from body.gene import ENV_RANDOM as random

NewPart = NamedTuple("NewPart", [("part", Literal["Limb", "Blob"]), ("point", Vector3)])


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
        self.eyes: list[Eye] = []
        self.color = pygame.Color([int(i) % 255 for i in self.gene.colour])

    def __repr__(self):
        return f"<{self.__class__} with {len(self.children)}>"

    def append_to(self, parent: "BodyPart"): ...

    def grow(
        self, depth: int, all_children: list[tuple["BodyPart", int]]
    ) -> NewPart | None: ...

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset + self.parent_offset
        depth = predefined_projection_depth(global_pos)
        render_items: list[Any] = [(depth, self)]

        for child in self.children:
            eye_global_pos = global_pos + child.parent_offset
            eye_depth = predefined_projection_depth(eye_global_pos)
            render_items.append((eye_depth, child))

        for eye in self.eyes:
            eye_global_pos = global_pos + eye.parent_offset
            eye_depth = predefined_projection_depth(eye_global_pos)
            render_items.append((eye_depth, eye))

        # Sort by depth, then render
        render_items.sort(key=lambda x: x[0])
        while len(render_items) > 0:
            item = render_items.pop()[1]

            if item is self:
                self.draw_self(screen, global_offset)
            else:
                item.draw(screen, self.get_child_offset(global_offset))

    def get_child_offset(self, global_offset: Vector3) -> Vector3:
        return self.parent_offset + global_offset

    def draw_self(self, screen: pygame.Surface, global_offset: Vector3): ...
