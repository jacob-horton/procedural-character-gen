import numpy as np
import matplotlib.pyplot as plt

def get_top_most(points: np.ndarray) -> np.ndarray:
    max_y = points[0][1]
    top_most = points[0]

    for point in points[1:]:
        if point[1] > max_y:
            max_y = point[1]
            top_most = point


    return top_most


# Points = array of (x, y)
def gift_wrap(points: np.ndarray) -> np.ndarray:
    current = get_top_most(points)
    hull = [current]
    prev_diff = np.array([1, 0])

    # Loop until we get back to start
    while True:
        if len(hull) > 1 and np.array_equal(current, hull[0]):
            break

        # Max dot product = min angle between the vectors
        max_dot = None
        max_point = None

        for point in points:
            # Skip if checking against itself
            if any([np.array_equal(p, point) for p in hull[1:]]):
                continue

            diff = point - current
            diff /= np.linalg.norm(diff)
            dot = np.dot(diff, prev_diff)

            if max_dot is None or dot > max_dot:
                max_dot = dot
                max_point = point

        if max_point is None:
            print("UH OH")
            exit(1)
            
        prev_diff = max_point - hull[-1]
        prev_diff /= np.linalg.norm(prev_diff)

        hull.append(max_point)
        current = max_point

    return np.array(hull[:-1])


points = np.array([
    [0, 5],
    [0.5, 3.5],
    [2, 5.5],
    [2, 4],
    [2.5, 2.5],
    [2, 0],
    [3.5, 4.5],
    [3.5, 3.5],
    [5.5, 2],
    [5.5, 5],
])
hull = gift_wrap(points)



plt.scatter(points.swapaxes(0,1)[0], points.swapaxes(0,1)[1])
plt.plot(hull.swapaxes(0,1)[0], hull.swapaxes(0,1)[1])
plt.show()

