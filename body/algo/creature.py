import random
from typing import Any

from pygame import Vector3, Surface
import pygame
from body.algo.gift_wrapping import gift_wrap
from body.algo.projection import predefined_projection
from body.eye import Eye

class Blob:
    def __init__(self, parent_offset: Vector3, points: list[Vector3], growth_rate: float, repulsion: float):
        self.parent_offset = parent_offset
        self.points = points
        self.repulsion = repulsion
        self.growth_rate = growth_rate

    def draw(self, screen: pygame.Surface, global_offset: Vector3, color: pygame.Color):
        global_pos = global_offset + self.parent_offset
        projected = [predefined_projection(p + global_pos) for p in self.points]
        hull = gift_wrap(projected)
        pygame.draw.polygon(
            screen,
            color,
            hull,
        )

        for point in projected:
            pygame.draw.circle(screen, "black", point, 5)

        Eye(Vector3(), 20).draw(screen, global_pos)


class Creature:
    def __init__(self, seed: Any = None, parent_offset = Vector3()):
        self.SEED = seed
        self.RANDOM_STATE = random.Random(self.SEED)
        self.blobs: list[Blob] = []
        self.parent_offset = parent_offset

    def create_blob(self, parent_offset: Vector3, n: int = 20, initial_distance: int = 10, growth_rate: float = 10, repulsion: float = 1):
        points = self.make_points(n, initial_distance)
        self.blobs.append(Blob(parent_offset, points, growth_rate, repulsion))

    # generate nodes close by randomly
    def make_points(self, n: int, initial_distance: int):
        def mk_pt():
            r: list[float] = []
            for _ in range(3):
                # from [-1, 1)
                x = (self.RANDOM_STATE.random()*2-1)
                # from [-10, 10)
                x *= initial_distance
                # offset to root +- 10
                r.append(x)

            return Vector3(r)
        
        point_list = [mk_pt() for _ in range(n)]
        return point_list

    def grow(self):
        # Loop through all blobs to grow them
        for blob in self.blobs:
            for point in blob.points:
                '''
                Each of the nodes can be considered a vector from (0,0,0), which is the root node.
                We can increase the magnitude of this vector to make them further away, so we do this each step with mods:
                1. Add deviation to this vector (inc by random small amnts)
                2.1. Calculate the vectors for the other non-root nodes to this
                2.2. Find the smallest one and weight it (decrease its size)
                2.3. Add them together to make it move away from the closest node
                3. Hope that translates well.
                '''
                # move further
                movement_vec = point + blob.parent_offset
                # find the vector from this to the nearest neighbouring node
                nearest_neighbour_vector = None
                for other_blob in self.blobs:
                    for n in other_blob.points:
                        neighbour = n + other_blob.parent_offset
                        if point == neighbour: continue

                        if nearest_neighbour_vector is None:
                            nearest_neighbour_vector = point + neighbour
                            continue

                        neighbour_vector = point - neighbour
                        if neighbour_vector.magnitude_squared() < nearest_neighbour_vector.magnitude_squared():
                            nearest_neighbour_vector = neighbour_vector

                if nearest_neighbour_vector is None:
                    raise Exception("nearest neighbour was none")

                # add the movement vector to a weighted nearest neighbour vector (nnv)
                movement_vec += nearest_neighbour_vector * blob.repulsion
                point += movement_vec.normalize() * blob.growth_rate

    def render(self, screen: Surface, global_offset: Vector3):
        for blob in self.blobs:
            blob.draw(screen, global_offset + self.parent_offset, pygame.Color(255,0,100))
