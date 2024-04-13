import numpy as np

def project_point(point: np.ndarray, transformation_matrix: np.ndarray):
    left = -2
    right = 2
    bottom = -2
    up = 2
    near = 0
    far = 4


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

    point4d = np.append(point, 1)
    projected = convert_to_left_handed @ scale_matrix @ centre_matrix @ transformation_matrix @ point4d

    return projected[:2]


def generate_transformation_matrix(scale_factor: int, rotation: np.ndarray, translation: np.ndarray):
    translation_matrix = np.array([
        [1,0,0,translation[0]],
        [0,1,0,translation[1]],
        [0,0,1,translation[2]],
        [0,0,0,1],
    ])

    scaling_matrix = np.array([
        [scale_factor,0,0,0],
        [0,scale_factor,0,0],
        [0,0,scale_factor,0],
        [0,0,0,1],
    ])

    x_rot = np.array([
        [1, 0, 0, 0],
        [0, np.cos(rotation[0]), np.sin(rotation[0]), 0],
        [0, -np.sin(rotation[0]), np.cos(rotation[0]), 0],
        [0, 0, 0, 1],
    ])

    y_rot = np.array([
        [np.cos(rotation[1]), 0, -np.sin(rotation[1]), 0],
        [0, 1, 0, 0],
        [np.sin(rotation[1]), 0, np.cos(rotation[1]), 0],
        [0, 0, 0, 1],
    ])

    z_rot = np.array([
        [np.cos(rotation[0]), -np.sin(rotation[0]), 0, 0],
        [np.sin(rotation[0]), np.cos(rotation[0]), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    return scaling_matrix @ translation_matrix @ x_rot @ y_rot @ z_rot


predefined_transform_matrix = generate_transformation_matrix(1, np.array([np.radians(20), np.radians(45), 0]), np.zeros(3))
def predefined_projection(point: np.ndarray):
    return project_point(point, predefined_transform_matrix)
    
