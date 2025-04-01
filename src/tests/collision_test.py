import unittest
from physics.colliders import CircleCollider
from physics.collisionhandler import CollisionHandler
from pygame.math import Vector2

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.c1 = CircleCollider(Vector2(500, 500), 100)
        self.c2 = CircleCollider(Vector2(650, 500), 100)

    def test_circle_circle_collision(self):
        v = CollisionHandler.circle_circle(self.c1, self.c2)
        self.assertNotEqual(v, None)