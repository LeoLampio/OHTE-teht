import math
from pygame.math import Vector2
import pygame
from utils.time import Time
from utils.stage import Stage, HEIGHT
from physics.colliders import CircleCollider, skin_width
from physics.collisionhandler import CollisionHandler, CollisionInfo
from entities.platformmanager import PlatformManager

class PlayerController:

    def __init__(self, startpos: Vector2):
        self.input = 0
        self.jump_pressed = False
        self.is_grounded = False
        self.can_jump = False

        self.speed = 300
        self.accel = self.speed / 0.5
        self.drag = 1 / 40

        self.initialize_gravity()

        self.surface_normal = Vector2(0, 0)
        self.jump_dir = Vector2(0, -1)
        self.move_dir = Vector2(1, 0)

        self.vel = Vector2(0, 0)
        self.surface_vel = Vector2(0, 0)

        self.coll = CircleCollider(startpos, 30)
        self.last_collision_point = Vector2(0, -1000)
    
    def initialize_gravity(self):
        max_jump_height = 300
        max_jump_time = 1.2
        self.terminal_vel = 1500

        time_to_apex = max_jump_time / 2
        self.gravity = 2 * max_jump_height / (time_to_apex**2)
        self.jump_force = 2 * max_jump_height / time_to_apex

    def update(self):
        if (self.is_grounded):
            self.jump_dir = self.surface_normal
            self.move_dir = Vector2(-self.surface_normal.y, self.surface_normal.x)
            self.surface_vel = Vector2(
                Vector2.dot(self.move_dir, self.vel), Vector2.dot(self.jump_dir, self.vel))

            self.read_input()
            self.check_jump()
            self.apply_horizontal_accel()
        else:
            self.apply_gravity()

        self.move()
        self.handle_collision()

    def read_input(self):
        self.input = 0
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.input -= 1
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.input += 1
        
        self.jump_pressed = keys[pygame.K_SPACE]

    def apply_gravity(self):
        self.vel.y += self.gravity * Time.dt
        self.vel.y = min(self.vel.y, self.terminal_vel)

    def apply_horizontal_accel(self):
        if (self.input == 0):
            if (self.surface_vel.x == 0):
                return
            self.surface_vel.x -= math.copysign(1, self.surface_vel.x) * self.accel * Time.dt
        else:
            self.surface_vel.x += self.input * self.accel * Time.dt

        self.surface_vel.x *= (1 - self.drag)

        self.surface_vel.x = pygame.math.clamp(self.surface_vel.x, -self.speed, self.speed)
        if (abs(self.surface_vel.x) < 5):
            self.surface_vel.x = 0

    def check_jump(self):
        if (not self.jump_pressed and not self.can_jump):
            self.can_jump = True
        
        if (self.is_grounded and self.jump_pressed and self.can_jump):
            self.can_jump = False
            self.surface_vel.y = self.jump_force * max(
                (Vector2.dot(self.surface_normal, Vector2(0, -1)) + 1) / 2, 0.1)

    def move(self):
        if (self.is_grounded):
            self.vel = self.surface_vel.x * self.move_dir + self.surface_vel.y * self.jump_dir
        
        self.coll.pos += self.vel * Time.dt

    # Does not take into consideration collision with multiple colliders at the same time
    def handle_collision(self):
        self.is_grounded = False
        self.floor_collision()

        for c in PlatformManager.circles:
            info = CollisionHandler.circle_circle(self.coll, c)
            if (info is None):
                continue
            self.collision_response(info)
        
        for p in PlatformManager.polys:
            info = CollisionHandler.circle_polygon(self.coll, p)
            if (info is None):
                continue
            self.collision_response(info)

    def collision_response(self, info: CollisionInfo):
        self.coll.pos += info.normal * (info.overlap - skin_width)
        self.last_collision_point = info.point
        self.surface_normal = info.normal

        tangent = Vector2(-info.normal.y, info.normal.x)
        self.vel = Vector2.dot(tangent, self.vel) * tangent
        self.is_grounded = True

    def floor_collision(self):
        if (self.coll.pos.y + self.coll.radius > HEIGHT):
            self.coll.pos.y = HEIGHT - self.coll.radius
            self.surface_normal = Vector2(0, -1)
            self.last_collision_point = Vector2(self.coll.pos.x, self.coll.pos.y + self.coll.radius)
            self.vel.y = 0
            self.is_grounded = True

    def draw(self):
        pygame.draw.circle(Stage.stage, (255, 0, 0), self.coll.pos, self.coll.radius)
        pygame.draw.circle(Stage.stage, (0, 255, 0), self.last_collision_point, 5)
