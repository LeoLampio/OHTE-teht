from pygame.math import Vector2
from physics.colliders import Collider

# Base class for all game objects

class Entity:
    def __init__(self, collider: Collider, color: tuple):
        self.coll = collider
        self.right = Vector2(1, 0)
        self.up = Vector2(0, -1)
        self.color = color

    # Move entity in world space
    def translate(self, translation: Vector2):
        self.coll.pos += translation

    # Convert a direction vector from world space tp object space
    def world_to_obj(self, v: Vector2) -> Vector2:
        return Vector2(Vector2.dot(self.right, v), Vector2.dot(self.up, v))

    # Convert a direction vector from object space tp world space
    def obj_to_world(self, v: Vector2) -> Vector2:
        return v.x * self.right + v.y * self.up

    def draw(self):
        self.coll.draw_coll(self.color)
