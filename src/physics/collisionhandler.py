import math
from pygame.math import Vector2
from physics.colliders import CircleCollider, PolygonCollider

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
    def circle_polygon(cls, c: CircleCollider, p: PolygonCollider):
        if (not (c.bounds.right > p.bounds.left and c.bounds.bottom > p.bounds.top
                and c.bounds.left < p.bounds.right and c.bounds.top < p.bounds.bottom)):
            return None
        
        # circle center in polygon
        if (cls.point_in_polygon(p, c.pos)):
            pass

        # Go over edges
        for i in range(p.vert_count):
            v0 = p.verts[i]
            v1 = p.verts[(i + 1) % p.vert_count]
            n = p.normals[i]
            l = cls.point_line_segment_dist(v0, v1, c.pos)
            if (l < 0 or l > c.radius):
                continue
            return CollisionInfo(n, c.radius - l, c.pos - n * l)
        
        # Go over vertices
        for v in p.verts:
            if (cls.point_in_circle(c, v)):
                return CollisionInfo(Vector2.normalize(c.pos - v), 
                                     c.radius - Vector2.length(c.pos - v), v)

        return None

    @classmethod
    def point_in_polygon(cls, p: PolygonCollider, v: Vector2) -> bool:
        for i in range(p.vert_count):
            if (Vector2.dot(p.verts[i] - v, p.normals[i]) < 0):
                return False
        return True

    @classmethod
    def point_in_circle(cls, c: CircleCollider, v: Vector2) -> bool:
        return Vector2.length_squared(v - c.pos) < c.r2
    
    @classmethod
    def point_line_segment_dist(cls, p0: Vector2, p1: Vector2, v: Vector2) -> float:
        p01 = p1 - p0
        t = Vector2.dot(p01, v - p0) / Vector2.length_squared(p01)
        if (t < 0 or t > 1):
            return -1
        line_point = p0 * (1 - t) + p1 * t
        return Vector2.length(v - line_point)
