from typing import Any
from pygame import Vector3, Surface
from algo.avgvec import avg_vec3s
from body.blob import Blob
from body.body import BodyPart
from body.limb import *


class Creature:
    def __init__(self, seed: Any = None, parent_offset: Vector3 = Vector3()):
        self.SEED = seed
        self.body = BodyPart([Vector3()], parent_offset)

    def grow(self):
        # Flatten hierarchy.
        all_children: list[BodyPart] = []

        def helper(child_list: list[BodyPart]):
            for i in child_list:
                all_children.append(i)
                helper(i.children)

        helper(self.body.children)

        print(all_children)
        for bp in all_children:
            if isinstance(bp, Limb):
                print(bp.growth_rate)
                bp.points[0] *= bp.growth_rate
                bp.growth_rate = 1 + ((bp.growth_rate - 1) * 0.99)
                print(bp.growth_rate)
                continue
            if isinstance(bp, Blob):
                for point in bp.points:
                    """
                    Each of the nodes can be considered a vector from (0,0,0), which is the root node.
                    We can increase the magnitude of this vector to make them further away, so we do this each step with mods:
                    1. Add deviation to this vector (inc by random small amnts)
                    2.1. Calculate the vectors for the other non-root nodes to this
                    2.2. Find the smallest one and weight it (decrease its size)
                    2.3. Add them together to make it move away from the closest node
                    3. Hope that translates well.
                    """
                    # move further
                    movement_vec = point + bp.parent_offset
                    # find the vector from this to the nearest neighbouring node
                    nearest_neighbour_vector = None
                    for other in all_children:
                        for n in other.points:
                            neighbour = n + other.parent_offset
                            # are we comparing point with offset to neighbour with same offset here?
                            if point == neighbour:
                                continue

                            if nearest_neighbour_vector is None:
                                nearest_neighbour_vector = point + neighbour
                                continue

                            neighbour_vector = point - neighbour
                            if (
                                neighbour_vector.magnitude_squared()
                                < nearest_neighbour_vector.magnitude_squared()
                            ):
                                nearest_neighbour_vector = neighbour_vector

                    if nearest_neighbour_vector is None:
                        raise Exception("nearest neighbour was none")

                    # add the movement vector to a weighted nearest neighbour vector (nnv)
                    movement_vec += nearest_neighbour_vector * bp.repulsion
                    point += movement_vec.normalize() * bp.growth_rate

                centre = avg_vec3s(bp.points)
                for point in bp.points:
                    point -= centre

    def draw(self, screen: Surface, global_offset: Vector3):
        global_pos = global_offset + self.body.parent_offset
        for child in self.body.children:
            child.draw(screen, global_pos)
