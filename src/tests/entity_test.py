import unittest
from entities.entity import Entity
from physics.colliders import CircleCollider
from pygame.math import Vector2

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.e = Entity(CircleCollider(Vector2(500, 500), 100), (0, 0, 0))
        self.e.right = Vector2.normalize(Vector2(1, 1))
        self.e.up = Vector2.normalize(Vector2(1, -1))

    def test_world_to_obj(self):
        v = self.e.world_to_obj(Vector2(1, 0))
        self.assertEqual(v, Vector2.normalize(Vector2(1, 1)))

    def test_obj_to_world(self):
        v = self.e.obj_to_world(Vector2(1, 0))
        self.assertEqual(v, self.e.right)