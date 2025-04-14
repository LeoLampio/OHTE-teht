from pygame.math import Vector2
from pygame.rect import Rect

# Base type for all colliders

class Collider:
    SkinWidth = 1

    def __init__(self, pos: Vector2):
        self.pos = pos
        self._bounds = None
    
    @property
    def Bounds(self):
        return Rect(self._bounds.left + self.pos.x - 3, self._bounds.top + self.pos.y - 3, 
                    self._bounds.width + 6, self._bounds.height + 6)
    
    @classmethod
    def overlap(cls, bounds1: Rect, bounds2: Rect) -> bool:
        return bounds1.right > bounds2.left and bounds1.bottom > bounds2.top and bounds1.left < bounds2.right and bounds1.top < bounds2.bottom

# A radial collider around a given position

class CircleCollider(Collider):
    def __init__(self, pos, radius):
        super().__init__(pos)
        self.__radius = max(1, radius)
        self.__r2 = self.__radius**2
        self._bounds = Rect(-self.__radius, -self.__radius, self.__radius * 2, self.__radius * 2)
    
    @property
    def R(self):
        return self.__radius
    @property
    def R2 (self):
        return self.__r2

# A convex polygon collider defined by a set of vertices

class PolygonCollider(Collider):    
    def __init__(self, pos: Vector2, vertex_array: list):
        """
        pos = world space position\n
        vertex_array = list of vertices relative to pos
        """
        super().__init__(pos)
        if (len(vertex_array) < 3):
            raise Exception("A polygon must have a minimum of 3 vertices!")
        
        self.__vertices = vertex_array
        self.__vert_count = len(vertex_array)
        self.__check_convex()
        self.__compute_bounds()
        self.__compute_normals()
        self.__compute_centroid()

    @property
    def Vertices(self):
        return [v + self.pos for v in self.__vertices]
    @property
    def N(self):
        return self.__vert_count

    @property
    def Is_clockwise(self):
        return self.__clockwise
    @property
    def Normals(self):
        return self.__normals
    @property
    def Centroid(self):
        return self.__centroid + self.pos

    def __check_convex(self):
        sign = Vector2.cross(self.__vertices[-1] - self.__vertices[0], 
                             self.__vertices[1] - self.__vertices[0])
        for i in range(1, self.__vert_count):
            if (sign * Vector2.cross(self.__vertices[i - 1] - self.__vertices[i], 
                    self.__vertices[(i + 1) % self.__vert_count] - self.__vertices[i]) < 0):
                raise Exception("Polygon Collider only supports convex polygons!")
        self.__clockwise = sign < 0
    
    def __compute_bounds(self):
        _min = Vector2(self.__vertices[0].x, self.__vertices[0].y)
        _max = Vector2(self.__vertices[0].x, self.__vertices[0].y)
        for v in self.__vertices:
            if (_min.x > v.x):
                _min.x = v.x
            elif (_max.x < v.x):
                _max.x = v.x
            if (_min.y > v.y):
                _min.y = v.y
            elif (_max.y < v.y):
                _max.y = v.y
        self._bounds = Rect(_min.x, _min.y, _max.x - _min.x, _max.y - _min.y)

    def __compute_normals(self):
        self.__normals = []
        for i in range(self.__vert_count):
            v0 = self.__vertices[i]
            v1 = self.__vertices[(i + 1) % self.__vert_count]
            v01 = Vector2.normalize(v1 - v0)
            self.__normals.append(Vector2(v01.y, -v01.x) if self.__clockwise 
                                else Vector2(-v01.y, v01.x))

    def __compute_centroid(self):
        _sum = Vector2(0, 0)
        for v in self.__vertices:
            _sum += v
        self.__centroid = _sum / self.__vert_count
