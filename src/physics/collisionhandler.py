import math
from pygame.math import Vector2
from physics.colliders import Collider, CircleCollider, PolygonCollider

# A datatype holding information relating to collisions between colliders

class CollisionInfo:
    def __init__(self, normal: Vector2, overlap: float, point: Vector2):
        self.normal = normal
        self.overlap = overlap
        self.point = point

    # Resolve collision fully
    def get_offset_out(self):
        return self.normal * (self.overlap + Collider.SkinWidth)
    
    # Keep the colliders barely touching
    def get_offset_in(self):
        return self.normal * (self.overlap - Collider.SkinWidth)

# A helper class to compute collisions

class CollisionHandler:
    @classmethod
    def circle_collision(cls, circ: CircleCollider, other: Collider) -> CollisionInfo:
        if (isinstance(other, CircleCollider)):
            return cls.circle_circle(circ, other)
        return cls.circle_polygon(circ, other)

    @classmethod
    def circle_circle(cls, c1: CircleCollider, c2: CircleCollider) -> CollisionInfo:
        if (not Collider.overlap(c1.bounds, c2.bounds)):
            return None

        d2 = Vector2.length_squared(c1.pos - c2.pos)
        radii = c1.radius + c2.radius

        # avoid expensive square root
        if (radii**2 < d2):
            return None
        
        d = math.sqrt(d2)
        n = (c1.pos - c2.pos) / d
        return CollisionInfo(n, radii - d, c1.pos - n * (d - c2.radius))
    
    @classmethod
    def circle_polygon(cls, c: CircleCollider, p: PolygonCollider):
        # broad phase
        if (not Collider.overlap(c.bounds, p.bounds)):
            return None
        
        # circle center in polygon
        if (cls.point_in_polygon(p, c.pos)):
            return None # Unimplemented

        # Go over edges
        for i in range(p.degree):
            v0 = p.vertices[i]
            v1 = p.vertices[(i + 1) % p.degree]
            n = p.normals[i]
            l = cls.point_line_segment_dist(v0, v1, c.pos)
            if (l < 0 or l > c.radius):
                continue
            return CollisionInfo(n, c.radius - l, c.pos - n * l)
        
        # Go over vertices
        for v in p.vertices:
            if (cls.point_in_circle(c, v)):
                return CollisionInfo(Vector2.normalize(c.pos - v), c.radius - Vector2.length(c.pos - v), v)

        # no collision
        return None

    @classmethod
    def point_in_polygon(cls, p: PolygonCollider, v: Vector2) -> bool:
        for i in range(p.degree):
            if (Vector2.dot(p.vertices[i] - v, p.normals[i]) < 0):
                return False
        return True

    @classmethod
    def point_in_circle(cls, c: CircleCollider, v: Vector2) -> bool:
        return Vector2.length_squared(v - c.pos) < c.radius_squared
    
    @classmethod
    def point_line_segment_dist(cls, p0: Vector2, p1: Vector2, v: Vector2) -> float:
        p01 = p1 - p0
        t = Vector2.dot(p01, v - p0) / Vector2.length_squared(p01)
        if (t < 0 or t > 1):
            return -1
        line_point = p0 * (1 - t) + p1 * t
        return Vector2.length(v - line_point)
