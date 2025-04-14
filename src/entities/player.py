import math
import pygame
from pygame.math import Vector2
from utils.time import Time
from physics.colliders import CircleCollider
from physics.collisionhandler import CollisionInfo

# Handles player movement and response to physics

class PlayerController:
    instance: "PlayerController" = None

    def __init__(self, startpos: Vector2, radius: float):
        self.__input = 0
        self.__jump_pressed = False
        self.__is_grounded = False
        self.__can_jump = False

        self.__max_speed = 300
        self.__accel = self.__max_speed / 0.5
        self.__friction = 1 / 40

        self.__initialize_gravity()

        self.__jump_axis = Vector2(0, -1)
        self.__move_axis = Vector2(1, 0)

        self.vel = Vector2(0, 0)
        self.__surface_vel = Vector2(0, 0)

        self.coll = CircleCollider(startpos, radius)
        self.__last_collision_point = Vector2(0, -1000)

        PlayerController.instance = self
    
    def __initialize_gravity(self):
        max_jump_height = 300
        max_jump_time = 1.2
        self.__terminal_vel = 1500

        time_to_apex = max_jump_time / 2
        self.__gravity = 2 * max_jump_height / (time_to_apex**2)
        self.__jump_force = 2 * max_jump_height / time_to_apex

    def update(self):
        if (self.__is_grounded):
            self.__grounded_update()
        else:
            self.__midair_update()

        self.__move()
        self.__is_grounded = False

# - - - - Ground Update - - - -

    def __grounded_update(self):
        self.__surface_vel = Vector2(Vector2.dot(self.__move_axis, self.vel), Vector2.dot(self.__jump_axis, self.vel))

        self.__read_input()
        self.__apply_horizontal_accel()
        self.__apply_friction()
        self.__clamp_velocity()
        self.__handle_jumping()

        self.vel = self.__surface_vel.x * self.__move_axis + self.__surface_vel.y * self.__jump_axis

    def __read_input(self):
        self.__input = 0
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.__input -= 1
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.__input += 1
        
        self.__jump_pressed = keys[pygame.K_SPACE]

    def __apply_horizontal_accel(self):
        if (self.__input != 0):
            self.__surface_vel.x += self.__input * self.__accel * Time.dt
            return
        
        if (self.__surface_vel.x == 0):
            return

        self.__surface_vel.x -= math.copysign(1, self.__surface_vel.x) * self.__accel * Time.dt
    
    def __apply_friction(self):
        self.__surface_vel.x *= (1 - self.__friction)
    
    def __clamp_velocity(self):
        self.__surface_vel.x = pygame.math.clamp(self.__surface_vel.x, -self.__max_speed, self.__max_speed)
        if (abs(self.__surface_vel.x) < 5):
            self.__surface_vel.x = 0

    def __handle_jumping(self):
        if (not self.__jump_pressed and self.__is_grounded):
            self.__can_jump = True
        
        if (self.__jump_pressed and self.__can_jump):
            self.__can_jump = False
            self.__surface_vel.y = self.__jump_force * self.__jump_force_multiplier()

    def __jump_force_multiplier(self):
        return max((Vector2.dot(self.__jump_axis, Vector2(0, -1)) + 1) / 2, 0.1)

# - - - - Midair Update - - - -

    def __midair_update(self):
        self.__surface_vel = Vector2(0, 0)
        self.__apply_gravity()

    def __apply_gravity(self):
        self.vel.y += self.__gravity * Time.dt
        self.vel.y = min(self.vel.y, self.__terminal_vel)

# - - - - Others - - - -

    def __move(self):
        self.coll.pos += self.vel * Time.dt

    def collision_response(self, info: CollisionInfo):
        self.coll.pos += info.get_offset_in()
        self.__last_collision_point = info.point

        self.__jump_axis = info.normal
        self.__move_axis = Vector2(-info.normal.y, info.normal.x)

        tangent = Vector2(-info.normal.y, info.normal.x)
        self.vel = Vector2.dot(tangent, self.vel) * tangent
        self.__is_grounded = True

    def draw(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), self.coll.pos, self.coll.radius)
        pygame.draw.circle(surf, (0, 255, 0), self.__last_collision_point, 5)
