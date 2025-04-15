from pygame.math import Vector2
from physics.colliders import Collider
from entities.entity import Entity
from utils.time import Time

class Platform(Entity):
    def __init__(self, static: bool, collider: Collider, color: tuple):
        super().__init__(collider, color)
        self.is_static = static
        self.vel = Vector2(0, 0)
    
    def move(self):
        self.translate(self.vel * Time.dt)

    def set_velocity(self, new_vel: Vector2):
        self.vel = new_vel
        self.is_static = self.vel == Vector2(0, 0)
