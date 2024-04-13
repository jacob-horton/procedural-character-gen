from perlin_noise import PerlinNoise
import random
import numpy as np


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

