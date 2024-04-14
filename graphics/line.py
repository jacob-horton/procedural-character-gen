import pygame
from pygame import Vector2

from algo.projection import ZOOM


def draw_line(
    screen: pygame.Surface,
    color: pygame.Color | str,
    start: Vector2,
    end: Vector2,
    width: float,
    start_scale: float = 1.0,
    end_scale: float = 1.0,
):
    width = width / ZOOM.x * 3
    perp = (end - start).normalize().rotate(90)
    ws = width * start_scale
    we = width * end_scale

    quad = [
        start + perp * ws / 2,
        start - perp * ws / 2,
        end - perp * we / 2,
        end + perp * we / 2,
    ]

    pygame.draw.polygon(screen, color, quad)
    pygame.draw.circle(screen, color, start, ws / 2)
    pygame.draw.circle(screen, color, end, we / 2)
