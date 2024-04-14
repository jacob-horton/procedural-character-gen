import pygame
from pygame import Vector3
from body.algo.creature import Creature
import random

THICKNESS = 10

gg = Creature(seed=None)
torso = gg.body.create_blob(Vector3(0, 0, 0), n=20, growth_rate=2, repulsion=2)
neck = torso.create_limb(random.choice(torso.points))
head = neck.create_blob(random.choice(neck.points), n=6, growth_rate=1, repulsion=1.5)

def render(screen: pygame.Surface, space: bool):
    gg.draw(screen, Vector3())
    if space:
        print('SPACE')
        gg.grow()
