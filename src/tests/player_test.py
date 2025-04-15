import unittest
from entities.player import Player
from physics.collisionhandler import CollisionInfo
from pygame.math import Vector2

class TestCollision(unittest.TestCase):
    def setUp(self):
        self.player = Player(Vector2(500, 500), 100)
        self.info = CollisionInfo(Vector2(1, 0), 5, Vector2(0, 0))

    def test_collision_response(self):
        self.player.controller.add_to_buffer(self.info)
        self.player.controller.collision_response()
        self.assertEqual(self.player.coll.pos, Vector2(504, 500))