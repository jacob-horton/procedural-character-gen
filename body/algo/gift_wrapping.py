from pygame import Vector2 

def get_top_most(points: list[Vector2]) -> Vector2:
    max_y = points[0].y
    top_most = points[0]

    for point in points[1:]:
        if point.y > max_y:
            max_y = point.y
            top_most = point


    return top_most


# Points = array of (x, y)
def gift_wrap(points: list[Vector2]) -> list[Vector2]:
    current = get_top_most(points)
    hull = [current]
    prev_diff = Vector2(1, 0)

    # Loop until we get back to start
    while True:
        if len(hull) > 1 and current == hull[0]:
            break

        # Max dot product = min angle between the vectors
        max_dot = None
        max_point = None

        for point in points:
            # Skip if checking against itself
            if any([p == point for p in hull[1:]]) or point == current:
                continue

            print(hull)
            print(current)
            print(point)
            diff = (point - current).normalize()
            dot = diff.dot(prev_diff)

            if max_dot is None or dot > max_dot:
                max_dot = dot
                max_point = point

        if max_point is None:
            print("UH OH")
            exit(1)
            
        print('here')
        prev_diff = max_point - hull[-1]
        prev_diff /= prev_diff.magnitude()

        hull.append(max_point)
        current = max_point

    return hull[:-1]
