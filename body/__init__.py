from typing import Any
from pygame import Vector3, Surface
from algo.avgvec import avg_vec3s
from body.blob import Blob
from body.body import BodyPart
from body.limb import *
from gene import Gene


class Creature:
    def __init__(self, gene: Gene, parent_offset: Vector3 = Vector3()):
        self.body = BodyPart(gene, [Vector3()], parent_offset)

    def grow(self):
        # Flatten hierarchy.
        all_children: list[tuple[BodyPart, int]] = []

        def helper(child_list: list[BodyPart], depth=0):
            for i in child_list:
                all_children.append((i, depth))
                helper(i.children, depth + 1)

        helper(self.body.children, 0)
        print(all_children)
        for bp, depth in all_children:
            bp.grow(all_children)

    def draw(self, screen: Surface, global_offset: Vector3):
        global_pos = global_offset + self.body.parent_offset
        for child in self.body.children:
            child.draw(screen, global_pos)
