import math
import random
from pygame.math import Vector2
from utils.data.time import Time
from utils.gui.camera import Camera
from physics.colliders import CircleCollider, PolygonCollider
from physics.collisionhandler import CollisionHandler
from entities.player import Player
from entities.platform import Platform

# Generates and updates Platform objects

class PlatformManager:
    """Stores & updates platforms and controls their procedural generation."""
    current_platforms: list[Platform] = []

    # Static Platform Variables
    static_dist = 200
    next_static_bottom = 0

    # Dynamic Platform Variables
    spawn_delay = 2.5
    spawn_timer = 0

    start_platform_color = (0, 200, 100)
    static_platform_color = (200, 200, 50)
    dynamic_platform_color = (50, 200, 200)

# Control Methods

    # Ran at the beginning of a game
    @classmethod
    def begin(cls):
        start_platform_coll = CircleCollider(Vector2(Camera.horizontal_center(), Camera.bottom() - 150), 100)
        start_platform = Platform(True, start_platform_coll, cls.start_platform_color)
        cls.current_platforms.append(start_platform)

        cls.next_static_bottom = start_platform_coll.bounds.top - cls.static_dist

    @classmethod
    def update(cls):
        cls.__generate()
        cls.__unload()
        cls.__update_platforms()

    @classmethod
    def reset(cls):
        cls.static_dist = 200
        cls.spawn_timer = 0
        cls.current_platforms.clear()

    @classmethod
    def draw(cls):
        for c in cls.current_platforms:
            c.draw()

# Generation Methods

    # Is the player high enough for the next static platform to appear
    @classmethod
    def __spawn_next_static(cls) -> bool:
        return Camera.top() < cls.next_static_bottom
    
    # Is it time to spawn the next dynamic platform
    @classmethod
    def __spawn_next_dynamic(cls) -> bool:
        return cls.spawn_timer > cls.spawn_delay
    
    # The distance between static platforms increases as the player gets higher
    @classmethod
    def __increase_difficulty(cls):
        cls.static_dist += 100

    # Generate platforms, if possible
    @classmethod
    def __generate(cls):
        while (cls.__spawn_next_static()):
            cls.__create_static()
            cls.__increase_difficulty()

        cls.spawn_timer += Time.dt
        if (cls.__spawn_next_dynamic()):
            cls.spawn_timer = 0
            cls.__create_dynamic()
    
    # Create a static platform
    @classmethod
    def __create_static(cls):
        size = random.randint(25, 150)

        if (random.random() < 0.5):
            x = random.randint(size, Camera.right() - size)
            y = cls.next_static_bottom - size
            coll = CircleCollider(Vector2(x, y), size)
        else:
            verts = []
            n = random.randint(3, 8)
            offset_angle = random.random() * math.pi / 2
            for i in range(n):
                angle = math.pi * 2 / n * i + offset_angle
                v_norm = Vector2(math.cos(angle), math.sin(angle))
                verts.append(v_norm * size)
            coll = PolygonCollider(Vector2(0, 0), verts)
            x = random.randint(-1 * coll.bounds.left, Camera.right() - coll.bounds.right)
            y = cls.next_static_bottom - coll.bounds.bottom
            coll.pos = Vector2(x, y)
        
        platform = Platform(True, coll, cls.static_platform_color)
        cls.current_platforms.append(platform)
        cls.next_static_bottom = coll.bounds.top - cls.static_dist

    # Create a dynamic platform
    @classmethod
    def __create_dynamic(cls):
        left_side = random.random() < 0.5
        size = random.randint(25, 150)
        x_vel = random.randint(50, 200) * (1 if left_side else -1)

        if (random.random() < 0.5):
            x = -size if left_side else Camera.right() + size
            y = random.randint(Camera.top() + size, Camera.bottom() - size)
            coll = CircleCollider(Vector2(x, y), size)
        else:
            verts = []
            n = random.randint(3, 8)
            offset_angle = random.random() * math.pi / 2
            for i in range(n):
                angle = math.pi * 2 / n * i + offset_angle
                v_norm = Vector2(math.cos(angle), math.sin(angle))
                verts.append(v_norm * size)
            coll = PolygonCollider(Vector2(0, 0), verts)
            x = coll.bounds.left if left_side else Camera.right() + coll.bounds.right
            y = random.randint(Camera.top() + coll.bounds.top, Camera.bottom() + coll.bounds.bottom)
            coll.pos = Vector2(x, y)
        
        platform = Platform(False, coll, cls.dynamic_platform_color)
        platform.vel = Vector2(x_vel, 0)
        cls.current_platforms.append(platform)

    # Go over platforms to see if any are due for deletion
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
    
    # Can this platform be deleted
    @classmethod
    def __unload_platform(cls, index: int) -> bool:
        p = cls.current_platforms[index]

        if (p.coll.bounds.top > Camera.bottom()):
            return True
        
        if (p.is_static):
            return False

        if (p.vel.x > 0 and p.coll.bounds.left > Camera.right()):
            return True
        if (p.vel.x < 0 and p.coll.bounds.right < 0):
            return True
        return False

# Platform Updating

    # Move dynamic platforms & check collision against player
    @classmethod
    def __update_platforms(cls):
        for c in cls.current_platforms:
            if (not c.is_static):
                c.move()
            
            info = CollisionHandler.circle_collision(Player.instance.coll, c.coll)
            if (info is not None):
                info.inherited_offset = Vector2(0, 0) if c.is_static else c.vel * Time.dt
                Player.instance.controller.add_to_buffer(info)
