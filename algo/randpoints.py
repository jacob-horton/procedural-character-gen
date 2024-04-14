# generate nodes close by randomly
import random

from pygame import Vector3


def distribute_points(
    n: int, initial_distance: float, random_state: random.Random = random.Random(None)
):
    mkpt = lambda: Vector3(
        [(random_state.random() * 2 - 1) * initial_distance for _ in range(3)]
    )
    """'
    def make_point():
        r: list[float] = []
        for _ in range(3):
            # from [-1, 1)
            x = (random_state.random()*2-1)
            # from [-10, 10)
            x *= initial_distance
            # offset to root +- 10
            r.append(x)
        return Vector3(r)
    """
    point_list = [mkpt() for _ in range(n)]
    return point_list
