from pygame.math import Vector2
from physics.colliders import Collider
from entities.entity import Entity
from utils.data.time import Time

class Platform(Entity):
    def __init__(self, is_static: bool, collider: Collider, color: tuple):
        super().__init__(collider, color)
        self.is_static = is_static
        self.vel = Vector2(0, 0)
    
    def move(self):
        self.translate(self.vel * Time.dt)
