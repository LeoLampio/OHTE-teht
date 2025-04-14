import pygame
from pygame.math import Vector2
from utils.time import Time
from physics.colliders import Collider, CircleCollider
from physics.collisionhandler import CollisionHandler
from entities.player import PlayerController

# Represents a platform object, which can be static or have a constant, unchanging velocity
# Platforms are kinematic and thus only interact with the player

class Platform:
    def __init__(self, static: bool, collider: Collider, color: tuple):
        self.is_static = static
        self.vel = Vector2(0, 0)

        self.coll = collider
        self.__color = color
    
    def move(self):
        self.coll.pos += self.vel * Time.dt

    def set_velocity(self, new_vel: Vector2):
        self.vel = new_vel
        self.is_static = self.vel == Vector2(0, 0)

    def draw(self, surf):
        if (isinstance(self.coll, CircleCollider)):
            pygame.draw.circle(surf, self.__color, self.coll.pos, self.coll.radius)
        else:
            pygame.draw.polygon(surf, self.__color, self.coll.Vertices)

# Generates and updates Platform objects

class PlatformManager:
    current_platforms: list[Platform] = []

    @classmethod
    def generate(cls):
        circle = CircleCollider(Vector2(600, 1000), 100)
        cls.current_platforms.append(Platform(True, circle, (255, 255, 255)))

    @classmethod
    def update(cls):
        for c in cls.current_platforms:
            if (c.is_static):
                cls.__static_check(c)
            else:
                c.move()
                cls.__dynamic_check(c)

    @classmethod
    def __static_check(cls, c: Platform):
        info = CollisionHandler.circle_collision(PlayerController.instance.coll, c.coll)
        if (info is not None):
            PlayerController.instance.collision_response(info)

    @classmethod
    def __dynamic_check(cls, c: Platform):
        info = CollisionHandler.circle_collision(PlayerController.instance.coll, c.coll)
        if (info is not None):
            PlayerController.instance.collision_response(info)

    @classmethod
    def draw(cls, surf):
        for c in cls.current_platforms:
            c.draw(surf)
