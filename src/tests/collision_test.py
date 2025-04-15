import unittest
from physics.colliders import CircleCollider, PolygonCollider
from physics.collisionhandler import CollisionHandler
from pygame.math import Vector2
import math

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.c1 = CircleCollider(Vector2(500, 500), 100)
        self.c2 = CircleCollider(Vector2(650, 500), 100)
        self.poly = PolygonCollider(Vector2(650, 500), [Vector2(math.cos(2 * math.pi / 5 * i), math.sin(2 * math.pi / 5 * i)) * 100 for i in range(5)])

    def test_circle_circle_collision(self):
        v = CollisionHandler.circle_circle(self.c1, self.c2)
        self.assertNotEqual(v, None)

    def test_circle_poly_collision(self):
        v = CollisionHandler.circle_polygon(self.c1, self.poly)
        self.assertNotEqual(v, None)
