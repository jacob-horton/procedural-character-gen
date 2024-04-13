# from perlin_noise import PerlinNoise
import random
from typing import Any

from pygame import Vector3

class Blob:
    def __init__(self, node: Vector3, gg: 'Creature', n: int = 3, initial_distance: int = 10):
        self.gg = gg
        self.pos = (node.x, node.y, node.z)
        self.points = gg.make_points(self, n, initial_distance)


class Creature:
    def __init__(self, seed: Any = None):
        self.SEED = seed
        self.RANDOM_STATE = random.Random(self.SEED)
        self.points: list[Vector3] = []

    # generate nodes close by randomly
    def make_points(self, root: Blob, n: int, initial_distance: int):
        def mk_pt():
            r = []
            for i in range(3):
                # from [-1, 1)
                x = (self.RANDOM_STATE.random()*2-1)
                # from [-10, 10)
                x *= initial_distance
                # offset to root +- 10
                x += root.pos[i]
                r.append(x)

            return Vector3(r)
        
        point_list = [mk_pt() for _ in range(n)]
        self.points += point_list
        return point_list

    def grow(self, rate: float = 10, repulsion: float = 0.1):
        for index, point in enumerate(self.points):
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
            movement_vec = point.copy()
            # find the vector from this to the nearest neighbouring node
            nearest_neighbour_vector = None
            for neighbour in self.points:
                if point == neighbour: continue

                if nearest_neighbour_vector is None:
                    nearest_neighbour_vector = point - neighbour
                    continue

                neighbour_vector = point - neighbour
                if neighbour_vector.magnitude_squared() < nearest_neighbour_vector.magnitude_squared():
                    nearest_neighbour_vector = neighbour_vector

            if nearest_neighbour_vector is None:
                raise Exception("nearest neighbour was none")

            # add the movement vector to a weighted nearest neighbour vector (nnv)
            movement_vec += nearest_neighbour_vector * repulsion
            point += (movement_vec.normalize()) * rate
