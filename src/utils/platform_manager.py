import math
import random
from pygame.math import Vector2
from utils.data.time import Time
from utils.gui.stage import Stage
from physics.colliders import CircleCollider, PolygonCollider
from physics.collisionhandler import CollisionHandler
from entities.player import Player
from entities.platform import Platform

# Generates and updates Platform objects

class PlatformManager:
    current_platforms: list[Platform] = []

    # Static platforms occasionally
        # Distance between them increases the higher the player climbs
    # Mostly dynamic platforms
        # Sideways movement
        # Spawn either left or right, move to the other side and get destroyed

    # Static Platform Variables
    dist_to_next = 200
    next_y = 0

    # Dynamic Platform Variables
    spawn_delay = 3
    spawn_timer = 0

    start_platform_color = (0, 200, 100)
    static_platform_color = (200, 200, 50)
    dynamic_platform_color = (50, 200, 200)

# Control Methods

    @classmethod
    def begin(cls):
        start_platform_coll = CircleCollider(Vector2(Stage.WIDTH / 2, Stage.bottom() - 150), 100)
        start_platform = Platform(True, start_platform_coll, cls.start_platform_color)
        cls.current_platforms.append(start_platform)

        cls.next_y = start_platform_coll.bounds.top - cls.dist_to_next

    @classmethod
    def update(cls):
        cls.__generate()
        cls.__unload()
        cls.__update_platforms()

    @classmethod
    def reset(cls):
        cls.dist_to_next = 200
        cls.spawn_timer = 0
        cls.current_platforms.clear()

    @classmethod
    def draw(cls):
        for c in cls.current_platforms:
            c.draw()

# Generation Methods

    @classmethod
    def __spawn_next_static(cls) -> bool:
        return Stage.top() < cls.next_y
    
    @classmethod
    def __spawn_next_dynamic(cls) -> bool:
        return cls.spawn_timer > cls.spawn_delay
    
    @classmethod
    def __increase_difficulty(cls):
        cls.dist_to_next += 100

    @classmethod
    def __generate(cls):
        while (cls.__spawn_next_static()):
            cls.__create_static()
            cls.__increase_difficulty()

        cls.spawn_timer += Time.dt
        if (cls.__spawn_next_dynamic()):
            cls.spawn_timer = 0
            cls.__create_dynamic()
    
    @classmethod
    def __create_static(cls):
        if (random.random() < 0.5):
            r = random.randint(25, 150)
            x = random.randint(r, Stage.WIDTH - r)
            coll = CircleCollider(Vector2(x, cls.next_y - r), r)
        else:
            vs = []
            n = random.randint(3, 8)
            size = random.randint(25, 150)
            offset_angle = random.random() * math.pi / 2
            for i in range(n):
                angle = math.pi * 2 / n * i + offset_angle
                v_norm = Vector2(math.cos(angle), math.sin(angle))
                vs.append(v_norm * size)
            coll = PolygonCollider(Vector2(0, 0), vs)
            x = random.randint(-coll.bounds.left, Stage.WIDTH - coll.bounds.right)
            coll.pos = Vector2(x, cls.next_y - coll.bounds.bottom)
        
        platform = Platform(True, coll, cls.static_platform_color)
        cls.current_platforms.append(platform)
        cls.next_y = coll.bounds.top - cls.dist_to_next

    @classmethod
    def __create_dynamic(cls):
        x_vel = random.randint(25, 150)

        if (random.random() < 0.5):
            r = random.randint(25, 150)
            y = random.randint(Stage.top() + r, Stage.bottom() - r)
            x = 0
            if (random.random() < 0.5):
                x = -r
            else:
                x = Stage.WIDTH + r
                x_vel *= -1
            coll = CircleCollider(Vector2(x, y), r)
        else:
            vs = []
            n = random.randint(3, 8)
            size = random.randint(25, 150)
            offset_angle = random.random() * math.pi / 2
            for i in range(n):
                angle = math.pi * 2 / n * i + offset_angle
                v_norm = Vector2(math.cos(angle), math.sin(angle))
                vs.append(v_norm * size)
            coll = PolygonCollider(Vector2(0, 0), vs)
            y = random.randint(Stage.top() + coll.bounds.top, Stage.bottom() + coll.bounds.bottom)
            x = 0
            if (random.random() < 0.5):
                x = -coll.bounds.right
            else:
                x = Stage.WIDTH - coll.bounds.left
                x_vel *= -1
            coll.pos = Vector2(x, y)
        
        platform = Platform(False, coll, cls.dynamic_platform_color)
        platform.vel = Vector2(x_vel, 0)
        cls.current_platforms.append(platform)

    @classmethod
    def __unload(cls):
        n = len(cls.current_platforms)
        i = 0
        while (i < n):
            if (cls.__unload_platform(i)):
                cls.current_platforms.pop(i)
                n -= 1
                continue
            i += 1
    
    @classmethod
    def __unload_platform(cls, index: int) -> bool:
        p = cls.current_platforms[index]

        if (p.is_static):
            if (p.coll.bounds.top > Stage.bottom()):
                return True
            return False
        
        if (p.vel.x > 0 and p.coll.bounds.left > Stage.WIDTH):
            return True
        if (p.vel.x < 0 and p.coll.bounds.right < 0):
            return True
        return False

# Platform Updating

    @classmethod
    def __update_platforms(cls):
        for c in cls.current_platforms:
            if (not c.is_static):
                c.move()
            
            info = CollisionHandler.circle_collision(Player.instance.coll, c.coll)
            if (info is not None):
                info.inherited_offset = Vector2(0, 0) if c.is_static else c.vel * Time.dt
                Player.instance.controller.add_to_buffer(info)
