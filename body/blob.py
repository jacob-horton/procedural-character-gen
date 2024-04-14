import random
from pygame import Vector3
import pygame

from algo.avgvec import avg_vec2s, avg_vec3s
from algo.gift_wrapping import gift_wrap
from algo.projection import predefined_projection
from algo.randpoints import distribute_points
from body.body import BodyPart
from body.eye import Eye
from body.gene import Gene


class Blob(BodyPart):
    """
    The parent point chosen becomes the offset for the child (as always).
    The points that make up the blob are generated randomly (with initial_distance multiplier)
    It will be grown by the root Creature according to its rate and repulsion.
    """

    def __init__(
        self,
        gene: Gene,
        parent: BodyPart,
        parent_offset: Vector3,
        n: int = 10,
        initial_distance: int = 10,
        growth_rate: float = 2,
        repulsion: float = 1,
    ):
        # hyperparameters
        self.repulsion = repulsion
        self.growth_rate = growth_rate
        self.n = n
        self.initial_distance = initial_distance
        # rendering
        points = distribute_points(self.n, self.initial_distance)
        self.parent_offset = random.choice(parent.points)
        self.append_to(parent)
        super().__init__(gene, points, parent_offset)

    def append_to(self, parent: BodyPart):
        parent.children.append(self)

    def grow(self, all_children):
        """
        Each of the nodes can be considered a vector from (0,0,0), which is the root node.
        We can increase the magnitude of this vector to make them further away, so we do this each step with mods:
        1. Add deviation to this vector (inc by random small amnts)
        2.1. Calculate the vectors for the other non-root nodes to this
        2.2. Find the smallest one and weight it (decrease its size)
        2.3. Add them together to make it move away from the closest node
        3. Hope that translates well.
        """
        for point in self.points:
            # move further
            movement_vec = point + self.parent_offset
            # find the vector from this to the nearest neighbouring node
            nearest_neighbour_vector = None
            for other, depth in all_children:
                for n in other.points:
                    neighbour = n + other.parent_offset
                    # are we comparing point with offset to neighbour with same offset here?
                    if point == neighbour:
                        continue

                    if nearest_neighbour_vector is None:
                        nearest_neighbour_vector = point + neighbour
                        continue

                    neighbour_vector = point - neighbour
                    if (
                        neighbour_vector.magnitude_squared()
                        < nearest_neighbour_vector.magnitude_squared()
                    ):
                        nearest_neighbour_vector = neighbour_vector

            if nearest_neighbour_vector is None:
                raise Exception("nearest neighbour was none")

            # add the movement vector to a weighted nearest neighbour vector (nnv)
            movement_vec += nearest_neighbour_vector * self.repulsion
            point += movement_vec.normalize() * self.growth_rate

        centre = avg_vec3s(self.points)
        for point in self.points:
            point -= centre

    def draw(self, screen: pygame.Surface, global_offset: Vector3):
        global_pos = global_offset + self.parent_offset
        for i in self.children:
            i.draw(screen, global_pos)

        projected = [predefined_projection(p + global_pos) for p in self.points]
        hull = gift_wrap(projected)

        avg = avg_vec2s(hull)

        for i in range(len(hull)):
            triangle = [avg, hull[i], hull[(i + 1) % len(hull)]]
            pygame.draw.polygon(
                screen,
                self.color + pygame.Color(i * 10, i * 10, i * 10),
                triangle,
            )

        # for point in projected:
        #     pygame.draw.circle(screen, "black", point, 5)

        Eye(avg_vec3s(self.points), 20).draw(screen, global_pos)
