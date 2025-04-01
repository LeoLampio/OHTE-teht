from pygame.math import Vector2
from pygame.rect import Rect

skin_width = 1

class Collider:
    def __init__(self, pos: Vector2):
        self.pos = pos
        self.bounds = None

class CircleCollider(Collider):
    def __init__(self, pos, radius):
        super().__init__(pos)
        self.bounds = Rect(-radius, -radius, radius * 2, radius * 2)
        self.radius = radius
        self.r2 = radius**2

class PolygonCollider(Collider):
    pass