from pygame.math import Vector2
import math
from physics.colliders import CircleCollider

class CollisionInfo:
    def __init__(self, normal: Vector2, overlap: float, point: Vector2):
        self.normal = normal
        self.overlap = overlap
        self.point = point

class CollisionHandler:
    @classmethod
    def circle_circle(cls, c1: CircleCollider, c2: CircleCollider) -> CollisionInfo:
        d2 = Vector2.length_squared(c1.pos - c2.pos)
        radii = c1.radius + c2.radius

        if (radii**2 < d2):
            return None
        
        d = math.sqrt(d2)
        n = (c1.pos - c2.pos) / d
        return CollisionInfo(n, radii - d, c1.pos - n * (d - c2.radius))
    
    @classmethod
    def circle_polygon(cls):
        pass