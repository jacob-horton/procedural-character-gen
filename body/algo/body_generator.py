# from perlin_noise import PerlinNoise
import random
import numpy as np
from typing import Any
from body.node import Node

class RootNode:
    def __init__(self, node: Node, gg: 'GrowthGenerator', n: int = 3, initial_distance: int = 10):
        self.gg = gg
        self.pos = (node.x, node.y, node.z)
        self.points = gg.make_points(self, n, initial_distance)


class GrowthGenerator:
    def __init__(self, seed: Any = None):
        self.SEED = seed
        self.RANDOM_STATE = random.Random(self.SEED)
        self.points: list[Any] = []

    # generate nodes close by randomly
    def make_points(self, root: RootNode, n: int, initial_distance: int):
        def mk_pt():
            r = []
            for i in range(3):
                print(i, root.pos[i])
                # from [-1, 1)
                x = (self.RANDOM_STATE.random()*2-1)
                # from [-10, 10)
                x *= initial_distance
                # offset to root +- 10
                x += root.pos[i]
                print(x)
                r.append(x)
            return np.array(r)
        
        point_list = np.array([mk_pt() for _ in range(n)])
        print(point_list)
        self.points += list(point_list)
        return point_list

    def grow(self, rate: int = 10, repulsion: float = 0.1):
        print('GROW')
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
            movement_vec = np.array(point, dtype=float)
            print(f'{index=}, {movement_vec=}')
            # find the vector from this to the nearest neighbouring node
            nearest_neighbour_vector = None
            for neighbour in self.points:
                if np.array_equal(point, neighbour): continue
                if nearest_neighbour_vector is None:
                    nearest_neighbour_vector = point - neighbour
                    continue
                neighbour_vector = point - neighbour
                if np.linalg.norm(neighbour_vector) < np.linalg.norm(nearest_neighbour_vector):
                    nearest_neighbour_vector = neighbour_vector
            if nearest_neighbour_vector is None:
                raise Exception("nearest neighbour was none")
            # add the movement vector to a weighted nearest neighbour vector (nnv)
            movement_vec += nearest_neighbour_vector * repulsion
            print(f'{movement_vec=}')
            self.points[index] = point + (movement_vec/np.linalg.norm(movement_vec)) * rate
