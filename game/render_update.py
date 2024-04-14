import pygame
from pygame import Vector3
import body
import random

THICKNESS = 10

gg = body.Creature()
torso = body.Blob(gg.body, Vector3(), growth_rate=1.5)
neck = body.Limb(torso, random.choice(torso.points))
joint = body.Limb(neck, neck.points[0], angle_variation=1)
head = body.Blob(joint, joint.points[0])
"""
torso = gg.body.create_blob(Vector3(0, 0, 0), n=20, growth_rate=2, repulsion=2)
neck = torso.create_limb(random.choice(torso.points))
head = neck.create_blob(random.choice(neck.points), n=6, growth_rate=1, repulsion=1.5)
neck2 = head.create_limb(random.choice(head.points))
head2 = neck2.create_blob(random.choice(neck.points), n=6, growth_rate=1, repulsion=1.5)
"""


def render(screen: pygame.Surface, space: bool):
    gg.draw(screen, Vector3())
    if space:
        print("SPACE")
        [gg.grow() for _ in range(5)]
