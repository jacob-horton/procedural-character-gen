# from perlin_noise import PerlinNoise
import random
import numpy as np
from typing import Any

# Returns array of points
def circle_randomiser_body_generator(radius: float, variability: float, n_points: int = 16) -> np.ndarray:
    noise = PerlinNoise(octaves=2, seed=random.randrange(1000))

    points = np.zeros(n_points)
    for i in range(n_points):
        frac = float(i) / float(n_points)
        mag = radius + variability * noise(frac)
        angle = frac * 2 * np.pi
        points[i] = np.ones(4)
    
    pass

class GrowthGenerator:
    def __init__(self, root: Any, n: int = 3, seed: Any = None, initial_distance: int = 10):
        self.SEED = seed
        self.RANDOM_STATE = random.Random(self.SEED)
        # generate nodes close by randomly
        r = lambda: np.array([round((self.RANDOM_STATE.random()*2-1)*initial_distance) for _ in range(3)]) 
        self.point_list = [r() for _ in range(n)]

    def grow(self, rate: int = 10, repulsion: float = 0.1):
        for index, point in enumerate(self.point_list):
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
            for neighbour in self.point_list:
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
            self.point_list[index] = point + (movement_vec/np.linalg.norm(movement_vec)) * rate
