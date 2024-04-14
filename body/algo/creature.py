import random
from typing import Any

from pygame import Vector2, Vector3, Surface
import pygame
from body.algo.gift_wrapping import gift_wrap
from body.algo.projection import predefined_projection
from body.eye import Eye
from body.segment import Segment

SEED = None
RANDOM_STATE = random.Random(SEED)

# generate nodes close by randomly
def make_points(n: int, initial_distance: int):
    def mk_pt():
        r: list[float] = []
        for _ in range(3):
            # from [-1, 1)
            x = (RANDOM_STATE.random()*2-1)
            # from [-10, 10)
            x *= initial_distance
            # offset to root +- 10
            r.append(x)
        return Vector3(r)
    
    point_list = [mk_pt() for _ in range(n)]
    return point_list

class BodyPart:
    def __init__(self, points: list[Vector3], parent_offset: Vector3):
        self.children: list['BodyPart'] = []
        self.points = points
        self.parent_offset = parent_offset
    
    def create_limb(self, point: Vector3):
        '''
        The limb will extend outwards equal to the offset of the point it was created from in that point.
        You can 
        '''
        limb = Limb(point, [point])
        self.children.append(limb)
        return limb
    
    def create_blob(self, point: Vector3, n: int = 20, initial_distance: int = 10, growth_rate: float = 10, repulsion: float = 1):
        '''
        The parent point chosen becomes the offset for the child (as always).
        The points that make up the blob are generated randomly (with initial_distance multiplier)
        It will be grown by the root Creature according to its rate and repulsion.
        '''
        points = make_points(n, initial_distance)
        blob = Blob(point, points, growth_rate, repulsion)
        self.children.append(blob)
        return blob
    
    def __repr__(self):
        return f"<{self.__class__} with {len(self.children)}>"
    
    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        ...

def avg_vec3s(vecs: list[Vector3]) -> Vector3:
    sum = Vector3()

    for vec in vecs:
        sum += vec

    return sum / len(vecs)


def avg_vec2s(vecs: list[Vector2]) -> Vector2:
    sum = Vector2()

    for vec in vecs:
        sum += vec

    return sum / len(vecs)

class Blob(BodyPart):
    def __init__(self, parent_offset: Vector3, points: list[Vector3], growth_rate: float, repulsion: float, color: pygame.Color | None = None):
        self.repulsion = repulsion
        self.growth_rate = growth_rate
        super().__init__(points, parent_offset)

        if color is None:
            color = pygame.Color(random.randrange(256), random.randrange(256), random.randrange(256))
        self.color = color

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        print(f"I, {self}, am drawing!")
        global_pos = global_offset + self.parent_offset
        projected = [predefined_projection(p + global_pos) for p in self.points]
        hull = gift_wrap(projected)

        avg = avg_vec2s(hull)

        for i in range(len(hull)):
            triangle = [avg, hull[i], hull[(i+1)%len(hull)]]
            pygame.draw.polygon(
                screen,
                self.color + pygame.Color(i*10, i*10, i*10),
                triangle,
            )

        for point in projected:
            pygame.draw.circle(screen, "black", point, 5)

        Eye(avg_vec3s(self.points), 20).draw(screen, global_pos)
        for i in self.children:
            i.draw(screen, global_pos)


class Creature: 
    def __init__(self, seed: Any = None, parent_offset: Vector3 = Vector3()):
        self.SEED = seed
        self.body = BodyPart([Vector3()], parent_offset)

    def grow(self):
        # Flatten hierarchy.
        all_children: list[BodyPart] = []
        def helper(child_list: list[BodyPart]):
            for i in child_list:
                all_children.append(i)
                helper(i.children)
        helper(self.body.children)

        print(all_children)
        for bp in all_children:
            if not isinstance(bp, Blob):
                continue
            for point in bp.points:
                '''
                Each of the nodes can be considered a vector from (0,0,0), which is the root node.
                We can increase the magnitude of this vector to make them further away, so we do this each step with mods:
                1. Add deviation to this vector (inc by random small amnts)
                2.1. Calculate the vectors for the other non-root nodes to this
                2.2. Find the smallest one and weight it (decrease its size)
                2.3. Add them together to make it move away from the closest node
                3. Hope that translates well.
                '''
                # move further
                movement_vec = point + bp.parent_offset
                # find the vector from this to the nearest neighbouring node
                nearest_neighbour_vector = None
                for other in all_children:
                    for n in other.points:
                        neighbour = n + other.parent_offset
                        # are we comparing point with offset to neighbour with same offset here?
                        if point == neighbour: continue

                        if nearest_neighbour_vector is None:
                            nearest_neighbour_vector = point + neighbour
                            continue

                        neighbour_vector = point - neighbour
                        if neighbour_vector.magnitude_squared() < nearest_neighbour_vector.magnitude_squared():
                            nearest_neighbour_vector = neighbour_vector

                if nearest_neighbour_vector is None:
                    raise Exception("nearest neighbour was none")

                # add the movement vector to a weighted nearest neighbour vector (nnv)
                movement_vec += nearest_neighbour_vector * bp.repulsion
                point += movement_vec.normalize() * bp.growth_rate

            centre = avg_vec3s(bp.points)
            for point in bp.points:
                point -= centre

    def draw(self, screen: Surface, global_offset: Vector3):
        global_pos = global_offset + self.body.parent_offset
        for child in self.body.children:
            child.draw(screen, global_pos)

class Limb(BodyPart):
    '''
    Limbs are linear sequences of 3D vectors which are projected into the
    2D plane and rendered as segments (lines joining sequential points).
    '''
    def __init__(self, parent_offset: Vector3, points: list[Vector3], thickness: int = 50):
        self.thickness = thickness
        super().__init__(points, parent_offset)
    
    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset+self.parent_offset
        Segment(
            self.parent_offset, 
            self.parent_offset+self.points[0],
            self.thickness
        ).draw(screen, global_offset)
        for i in self.children:
            i.draw(screen, global_pos)
