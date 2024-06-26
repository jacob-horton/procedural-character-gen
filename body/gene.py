from dataclasses import dataclass
import pygame
import random, sys
from copy import copy

# Attenuation
# (percent) * (attenuation) ^ depth
# 0 (instant kill) - 1 (no change with depth) - x (coefficient applied depth times)
# <1 = decrease probability with depth
# >1 = increase probability with depth

# the genetic determinance affects whether events can happen or not
GEN_SEED = random.randrange(sys.maxsize)
GEN_RANDOM = random.Random(GEN_SEED)
# the environmental determinance affects how likely events are to happen
ENV_SEED = random.randrange(sys.maxsize)
ENV_RANDOM = random.Random(ENV_SEED)
# skip render cycles
GROWSCALE = 5

r_attenuation = lambda: ENV_RANDOM.random() * 0.85
gauss = ENV_RANDOM.gauss


def norm(mean: float = 1, sd: float = 1, low=0, upp=100):
    r = low - 1
    while r < low or r > upp:
        r = gauss(mean, sd)
    return r


@dataclass
class Gene:

    # blob -> limb
    limb_on_blob_percent: float = norm(15, 10, 0, 100) / GROWSCALE
    limb_on_blob_attenuation: float = r_attenuation()
    # blob hyperparams
    blob_initial_randomness: float = gauss(10, 5)
    blob_repulsion: float = gauss(1, 0.1)
    blob_node_count: int = round(norm(15, 2, 5, 30))

    # limb -> blob
    blob_on_limb_percent: float = norm(50, 10, 0, 100) / GROWSCALE
    blob_on_limb_attenuation: float = r_attenuation() / 0.85

    # limb hyperparams
    limb_growth_rate: float = norm(1.1, 0.02, 1, 2)

    eye_on_blob_percent: float = norm(0.1, 0.05)
    eye_on_blob_attenuation: float = r_attenuation()

    eye_on_limb_percent: float = norm(0.3, 0.5)
    eye_on_limb_attenuation: float = r_attenuation()

    eye_size: float = norm(20, 10, 5, 40)
    eye_size_variation: float = norm(10, 3, 0, 20)

    limb_on_limb_percent: float = norm(4, 2, 0, 100) / GROWSCALE
    limb_on_limb_attenuation: float = r_attenuation() * 0.6

    colour = pygame.Vector3(
        GEN_RANDOM.randrange(256), GEN_RANDOM.randrange(256), GEN_RANDOM.randrange(256)
    )
    """

    blob_on_blob_percent: float
    blob_on_blob_attenuation: float

    limb_length_variation: float
    limb_length_attenuation: float

    limb_width: float
    limb_width_change: float  # Difference between start and end width of limb
    limb_width_variation: float
    limb_width_attenuation: float
    limb_width_growth_rate: float  # e.g. 1.05 is a good value

    limb_off_blob_angle_variation: float
    limb_off_limb_angle_variation: float


    primary_base_colour: pygame.Color
    secondary_base_colour: pygame.Color
    colour_variation: float
    primary_colour_percentage: float
    """

    def copy(self):
        new_gene = copy(self)
        new_gene.colour += pygame.Vector3(
            GEN_RANDOM.random() * gauss(0, 50),
            GEN_RANDOM.random() * gauss(0, 50),
            GEN_RANDOM.random() * gauss(0, 50),
        )
        return new_gene

    def __repr__(self):
        return "\n".join([f" - {k} = {v}" for k, v in self.__dict__.items()])
