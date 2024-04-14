import numpy as np
from typing import Any
from pygame import Vector2, Vector3

from game.config import RESOLUTION

NDArray = np.ndarray[float, np.dtype[Any]]

# TODO: class for these values (zoom should be single float)
ROT = Vector3(20, 45, 0)
ZOOM = Vector3(1, 1, 1) * 3.0


def project_point(point: Vector3, transformation_matrix: NDArray) -> Vector3:
    bottom = -100 * ZOOM.y
    up = 100 * ZOOM.y
    left = bottom * RESOLUTION.x / RESOLUTION.y
    right = up * RESOLUTION.x / RESOLUTION.y
    near = 0
    far = 200 * ZOOM.x

    mid_x = (left + right) / 2
    mid_y = (bottom + up) / 2
    mid_z = (-near - far) / 2

    centre_matrix = np.array(
        [
            [1, 0, 0, -mid_x],
            [0, 1, 0, -mid_y],
            [0, 0, 1, -mid_z],
            [0, 0, 0, 1],
        ]
    )

    scale_x = 2.0 / (right - left)
    scale_y = 2.0 / (up - bottom)
    scale_z = 2.0 / (far - near)

    scale_matrix = np.array(
        [
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, 0],
            [0, 0, 0, 1],
        ]
    )

    convert_to_left_handed = np.array(
        [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, -1, 0],
            [0, 0, 0, 1],
        ]
    )

    point4d = np.append(np.array(point), 1)
    projected = (
        convert_to_left_handed
        @ scale_matrix
        @ centre_matrix
        @ transformation_matrix
        @ point4d
    )

    # Convert to
    return Vector3(*projected[:3])


def to_screen_space(point: Vector3) -> Vector2:
    return ((point.xy.elementwise() + 1).elementwise() * RESOLUTION.elementwise()) / 2


def generate_transformation_matrix(
    scale_factor: int, rotation: Vector3, translation: Vector3
) -> NDArray:
    translation_matrix = np.array(
        [
            [1, 0, 0, translation.x],
            [0, 1, 0, translation.y],
            [0, 0, 1, translation.z],
            [0, 0, 0, 1],
        ]
    )

    scaling_matrix = np.array(
        [
            [scale_factor, 0, 0, 0],
            [0, scale_factor, 0, 0],
            [0, 0, scale_factor, 0],
            [0, 0, 0, 1],
        ]
    )

    x_rot = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(rotation.x), np.sin(rotation.x), 0],
            [0, -np.sin(rotation.x), np.cos(rotation.x), 0],
            [0, 0, 0, 1],
        ]
    )

    y_rot = np.array(
        [
            [np.cos(rotation.y), 0, -np.sin(rotation.y), 0],
            [0, 1, 0, 0],
            [np.sin(rotation.y), 0, np.cos(rotation.y), 0],
            [0, 0, 0, 1],
        ]
    )

    z_rot = np.array(
        [
            [np.cos(rotation.z), -np.sin(rotation.z), 0, 0],
            [np.sin(rotation.z), np.cos(rotation.z), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )

    return scaling_matrix @ translation_matrix @ x_rot @ y_rot @ z_rot


def predefined_projection(point: Vector3) -> Vector2:
    predefined_transform_matrix = generate_transformation_matrix(
        1, ROT * np.pi / 180, Vector3()
    )
    return to_screen_space(project_point(point, predefined_transform_matrix))


def predefined_projection_depth(point: Vector3) -> float:
    predefined_transform_matrix = generate_transformation_matrix(
        1, ROT * np.pi / 180, Vector3()
    )
    return project_point(point, predefined_transform_matrix).z
