import math
from pygame.math import Vector2
from physics.colliders import Collider, CircleCollider, PolygonCollider

# A datatype holding information relating to collisions between colliders

class CollisionInfo:
    def __init__(self, normal: Vector2, overlap: float, point: Vector2):
        self.normal = normal
        self.overlap = overlap
        self.point = point

    def get_offset_out(self):
        return self.normal * (self.overlap + Collider.SkinWidth)
    def get_offset_in(self):
        return self.normal * (self.overlap - Collider.SkinWidth)

# A helper class to compute collisions

class CollisionHandler:
    @classmethod
    def circle_collision(cls, circ: CircleCollider, other: Collider) -> CollisionInfo:
        if (type(other) is CircleCollider):
            return cls.circle_circle(circ, other)
        return cls.circle_polygon(circ, other)

    @classmethod
    def circle_circle(cls, c1: CircleCollider, c2: CircleCollider) -> CollisionInfo:
        if (not Collider.overlap(c1.Bounds, c2.Bounds)):
            return None

        d2 = Vector2.length_squared(c1.pos - c2.pos)
        radii = c1.R + c2.R

        if (radii**2 < d2):
            return None
        
        d = math.sqrt(d2)
        n = (c1.pos - c2.pos) / d
        return CollisionInfo(n, radii - d, c1.pos - n * (d - c2.R))
    
    @classmethod
    def circle_polygon(cls, c: CircleCollider, p: PolygonCollider):
        if (not Collider.overlap(c.Bounds, p.Bounds)):
            return None
        
        # circle center in polygon
        if (cls.point_in_polygon(p, c.pos)):
            return None # Unimplemented

        # Go over edges
        for i in range(p.N):
            v0 = p.Vertices[i]
            v1 = p.Vertices[(i + 1) % p.N]
            n = p.Normals[i]
            l = cls.point_line_segment_dist(v0, v1, c.pos)
            if (l < 0 or l > c.R):
                continue
            return CollisionInfo(n, c.R - l, c.pos - n * l)
        
        # Go over vertices
        for v in p.Vertices:
            if (cls.point_in_circle(c, v)):
                return CollisionInfo(Vector2.normalize(c.pos - v), 
                                     c.R - Vector2.length(c.pos - v), v)

        return None

    @classmethod
    def point_in_polygon(cls, p: PolygonCollider, v: Vector2) -> bool:
        for i in range(p.N):
            if (Vector2.dot(p.Vertices[i] - v, p.Normals[i]) < 0):
                return False
        return True

    @classmethod
    def point_in_circle(cls, c: CircleCollider, v: Vector2) -> bool:
        return Vector2.length_squared(v - c.pos) < c.R2
    
    @classmethod
    def point_line_segment_dist(cls, p0: Vector2, p1: Vector2, v: Vector2) -> float:
        p01 = p1 - p0
        t = Vector2.dot(p01, v - p0) / Vector2.length_squared(p01)
        if (t < 0 or t > 1):
            return -1
        line_point = p0 * (1 - t) + p1 * t
        return Vector2.length(v - line_point)
