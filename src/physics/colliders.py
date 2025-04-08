from pygame.math import Vector2
from pygame.rect import Rect

skin_width = 1

class Collider:
    def __init__(self, pos: Vector2):
        self.pos = pos
        self._bounds = None
    
    @property
    def bounds(self):
        return Rect(self._bounds.left + self.pos.x - 3, self._bounds.top + self.pos.y - 3, 
                    self._bounds.width + 6, self._bounds.height + 6)

class CircleCollider(Collider):
    def __init__(self, pos, radius):
        super().__init__(pos)
        self._bounds = Rect(-radius, -radius, radius * 2, radius * 2)
        self.radius = radius
        self.r2 = radius**2

class PolygonCollider(Collider):
    """Specifically a Convex Polygon."""
    
    def __init__(self, pos, vertex_array: list):
        """pos: relative to world space 
        / / vertex_array: contains the positions of the vertices relative to the origin (not pos).
        """
        super().__init__(pos)
        if (len(vertex_array) < 3):
            raise Exception("A polygon must have a minimum of 3 vertices!")
        
        self.vertices = vertex_array
        self.vert_count = len(vertex_array)
        self.check_convex()
        self.compute_bounds()
        self.compute_normals()
        self.compute_centroid()

    @property
    def verts(self):
        return [v + self.pos for v in self.vertices]

    def check_convex(self):
        sign = Vector2.cross(self.vertices[-1] - self.vertices[0], 
                             self.vertices[1] - self.vertices[0])
        for i in range(1, self.vert_count):
            if (sign * Vector2.cross(self.vertices[i - 1] - self.vertices[i], 
                self.vertices[(i + 1) % self.vert_count] - self.vertices[i]) < 0):
                raise Exception("Polygon Collider only supports convex polygons!")
        self.clockwise = sign < 0
    
    def compute_bounds(self):
        _min = Vector2(self.vertices[0].x, self.vertices[0].y)
        _max = Vector2(self.vertices[0].x, self.vertices[0].y)
        for v in self.vertices:
            if (_min.x > v.x):
                _min.x = v.x
            elif (_max.x < v.x):
                _max.x = v.x
            if (_min.y > v.y):
                _min.y = v.y
            elif (_max.y < v.y):
                _max.y = v.y
        self._bounds = Rect(_min.x, _min.y, _max.x - _min.x, _max.y - _min.y)

    def compute_normals(self):
        self.normals = []
        for i in range(self.vert_count):
            v0 = self.vertices[i]
            v1 = self.vertices[(i + 1) % self.vert_count]
            v01 = Vector2.normalize(v1 - v0)
            self.normals.append(Vector2(v01.y, -v01.x) if self.clockwise 
                                else Vector2(-v01.y, v01.x))

    def compute_centroid(self):
        _sum = Vector2(0, 0)
        for v in self.vertices:
            _sum += v
        self.centroid = _sum / self.vert_count
