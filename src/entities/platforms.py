import math
import random
from pygame.math import Vector2
from utils.time import Time
from utils.stage import Stage
from physics.colliders import Collider, CircleCollider, PolygonCollider
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

    def draw(self):
        if (isinstance(self.coll, CircleCollider)):
            Stage.draw_circle(self.coll.pos, self.coll.radius, self.__color)
        else:
            Stage.draw_polygon(self.coll.vertices, self.__color)

# Generates and updates Platform objects

class PlatformManager:
    current_platforms: list[Platform] = []
    __platform_dist = 350
    __last_y = 0
    __max_rad = 100

    @classmethod
    def begin(cls):
        cls.__last_y = Stage.HEIGHT * 0.8
        circle = CircleCollider(Vector2(Stage.WIDTH / 2, cls.__last_y), 100)
        start_platform = Platform(True, circle, (0, 200, 100))
        cls.current_platforms.append(start_platform)

        while (cls.__last_y + cls.__max_rad >= cls.__platform_dist):
            cls.generate()

    @classmethod
    def generate(cls):
        if (cls.__last_y + Stage.Offset.y + cls.__max_rad < cls.__platform_dist):
            return
        
        cls.__last_y -= cls.__platform_dist
        if (random.random() < 0.5):
            cls.__create_circle()
        else:
            cls.__create_polygon()

    @classmethod
    def destroy(cls):
        if (cls.current_platforms[0].coll.pos.y + Stage.Offset.y > Stage.HEIGHT + cls.__max_rad):
            cls.current_platforms.pop(0)

    @classmethod
    def __create_circle(cls):
        pos = Vector2(random.randint(cls.__max_rad, Stage.WIDTH - cls.__max_rad), cls.__last_y)
        circle = CircleCollider(pos, cls.__max_rad)
        cls.current_platforms.append(Platform(True, circle, (255, 255, 255)))

    @classmethod
    def __create_polygon(cls):
        vs = []
        n = random.randint(3, 8)
        for i in range(n):
            v_norm = Vector2(math.cos(math.pi * 2 / n * i), math.sin(math.pi * 2 / n * i))
            vs.append(v_norm * cls.__max_rad)
        pos = Vector2(random.randint(cls.__max_rad, Stage.WIDTH - cls.__max_rad), cls.__last_y)
        poly = PolygonCollider(pos, vs)
        cls.current_platforms.append(Platform(True, poly, (255, 255, 255)))

    @classmethod
    def update(cls):
        for c in cls.current_platforms:
            if (c.is_static):
                cls.__static_check(c)
            else:
                c.move()
                cls.__dynamic_check(c)

    # Check player collision against a non moving platform
    @classmethod
    def __static_check(cls, c: Platform):
        info = CollisionHandler.circle_collision(PlayerController.instance.coll, c.coll)
        if (info is not None):
            PlayerController.instance.collision_response(info)

    # Check player collision against a moving platform
    @classmethod
    def __dynamic_check(cls, c: Platform):
        info = CollisionHandler.circle_collision(PlayerController.instance.coll, c.coll)
        if (info is not None):
            PlayerController.instance.collision_response(info, c.vel * Time.dt)

    @classmethod
    def draw(cls):
        for c in cls.current_platforms:
            c.draw()
