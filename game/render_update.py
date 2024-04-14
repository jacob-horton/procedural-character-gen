import pygame
from pygame import Vector3
import body
import random

from body.gene import Gene, GROWSCALE

THICKNESS = 10

gg = body.Creature(Gene())
body.Blob(gg.body.gene.copy(), gg.body, gg.body.parent_offset)


def render(screen: pygame.Surface, space: bool):
    gg.draw(screen, Vector3())
    if space:
        [gg.grow() for _ in range(GROWSCALE)]
