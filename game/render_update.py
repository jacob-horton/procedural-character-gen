import pygame
from pygame import Vector3
from body.algo.creature import Creature

THICKNESS = 10
DIFF = 50

gg = Creature(seed=None)
gg.create_blob(Vector3(-DIFF//2, 0, 0), n=20, growth_rate=10, repulsion=2)
gg.create_blob(Vector3(DIFF//2, 0, 0), n=6, growth_rate=5, repulsion=-1)

def render(screen: pygame.Surface, space: bool):
    gg.render(screen, Vector3())
    if space:
        gg.grow()
