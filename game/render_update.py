import pygame
from pygame import Vector3
from body.algo.creature import Creature

THICKNESS = 10
DIFF = 50

gg = Creature(seed=None)
gg.create_blob(Vector3(-DIFF//2, 0, 0))
gg.create_blob(Vector3(DIFF//2, 0, 0))

def render(screen: pygame.Surface, space: bool):
    gg.render(screen)

    if space:
        gg.grow(repulsion=10)
