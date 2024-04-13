''' do maths'''
from dataclasses import dataclass

@dataclass
class Node:
    x: float
    y: float
    z: float

@dataclass
class Sphere(Node):
    radius: float

