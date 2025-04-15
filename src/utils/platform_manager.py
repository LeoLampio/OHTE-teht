import math
import random
from pygame.math import Vector2, clamp
from utils.time import Time
from utils.stage import Stage
from physics.colliders import CircleCollider, PolygonCollider
from physics.collisionhandler import CollisionHandler
from entities.player import Player
from entities.platform import Platform

# Generates and updates Platform objects

class PlatformManager:
    current_platforms: list[Platform] = []

    # Generation variables
    __y_range = Vector2(100, 400)
    __x_range = Vector2(100, 600)
    __size_range = Vector2(20, 120)

    __prev_pos = Vector2(0, 0)
    __current_dist = 0
    __current_size = 0

    @classmethod
    def begin(cls):
        cls.__prev_pos = Vector2(Stage.WIDTH / 2, Stage.HEIGHT * 0.8)
        circle = CircleCollider(cls.__prev_pos.copy(), 100)
        start_platform = Platform(True, circle, (0, 200, 100))
        cls.current_platforms.append(start_platform)

        cls.__set_values()
        while (cls.__can_generate()):
            cls.generate()

    @classmethod
    def __can_generate(cls) -> bool:
        return cls.__prev_pos.y + Stage.Offset.y + cls.__current_size >= cls.__current_dist

    @classmethod
    def __set_values(cls):
        cls.__current_dist = random.randint(cls.__y_range.x, cls.__y_range.y)
        cls.__current_size = random.randint(cls.__size_range.x, cls.__size_range.y)

    @classmethod
    def __get_pos(cls) -> Vector2:
        dx = random.randint(cls.__x_range.x, cls.__x_range.y)
        x = random.randint(cls.__prev_pos.x - dx, cls.__prev_pos.x + dx)
        x = clamp(x, 0, Stage.WIDTH)
        return Vector2(x, cls.__prev_pos.y)

    @classmethod
    def generate(cls):
        cls.destroy()

        if (not cls.__can_generate()):
            return
        
        cls.__prev_pos.y -= cls.__current_dist

        if (random.random() < 0.5):
            cls.__create_circle()
        else:
            cls.__create_polygon()
        
        cls.__prev_pos.x = cls.current_platforms[-1].coll.pos.x
        cls.__set_values()        

    @classmethod
    def destroy(cls):
        if (cls.current_platforms[0].coll.pos.y + Stage.Offset.y > Stage.HEIGHT + cls.__size_range.y):
            cls.current_platforms.pop(0)

    @classmethod
    def __create_circle(cls):
        circle = CircleCollider(cls.__get_pos(), cls.__current_size)
        cls.current_platforms.append(Platform(True, circle, (255, 255, 255)))

    @classmethod
    def __create_polygon(cls):
        vs = []
        n = random.randint(3, 8)
        for i in range(n):
            v_norm = Vector2(math.cos(math.pi * 2 / n * i), math.sin(math.pi * 2 / n * i))
            vs.append(v_norm * cls.__current_size)
        poly = PolygonCollider(cls.__get_pos(), vs)
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
        info = CollisionHandler.circle_collision(Player.instance.coll, c.coll)
        if (info is not None):
            Player.instance.controller.add_to_buffer(info)

    # Check player collision against a moving platform
    @classmethod
    def __dynamic_check(cls, c: Platform):
        info = CollisionHandler.circle_collision(Player.instance.coll, c.coll)
        if (info is not None):
            info.inherited_offset = c.vel * Time.dt
            Player.instance.controller.add_to_buffer(info)

    @classmethod
    def render(cls):
        for c in cls.current_platforms:
            c.draw()
