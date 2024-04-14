from pygame import Vector2, Vector3


def avg_vec3s(vecs: list[Vector3]) -> Vector3:
    sum = Vector3()

    for vec in vecs:
        sum += vec
    return sum / len(vecs)


def avg_vec2s(vecs: list[Vector2]) -> Vector2:
    sum = Vector2()

    for vec in vecs:
        sum += vec

    return sum / len(vecs)
