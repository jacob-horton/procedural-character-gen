from dataclasses import dataclass
import pygame

# Attenuation
# (percent) * (attenuation) ^ depth
# 1 = none
# <1 = decrease probability with depth
# >1 = increase probability with depth


@dataclass
class Gene:
    # blob->limb locus
    limb_on_blob_percent: float
    limb_on_blob_attenuation: float

    blob_on_limb_percent: float
    blob_on_limb_attenuation: float

    limb_on_limb_percent: float
    limb_on_limb_attempts: int  # Number of attempts to add a limb to the end of another (can have multiple branch off)
    limb_on_limb_attenuation: float

    blob_on_blob_percent: float
    blob_on_blob_attenuation: float

    eye_on_blob_percent: float
    eye_on_blob_attenuation: float

    eye_on_limb_percent: float
    eye_on_limb_attenuation: float

    eye_size: float
    eye_size_variation: float

    limb_length: float
    limb_length_variation: float
    limb_length_attenuation: float

    limb_width: float
    limb_width_change: float  # Difference between start and end width of limb
    limb_width_variation: float
    limb_width_attenuation: float
    limb_width_growth_rate: float  # e.g. 1.05 is a good value

    limb_off_blob_angle_variation: float
    limb_off_limb_angle_variation: float

    blob_size_attenuation: float
    blob_initial_randomness: float
    blob_repulsion: float
    blob_node_count: int

    primary_base_colour: pygame.Color
    secondary_base_colour: pygame.Color
    colour_variation: float
    primary_colour_percentage: float
