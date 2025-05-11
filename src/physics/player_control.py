import pygame
from pygame.math import Vector2
from utils.data.time import Time
from utils.game_state import GameStateHandler
from utils.data.statistics import DeathType
from physics.collisionhandler import CollisionInfo
from entities.entity import Entity

# Handles player movement and response to physics

class PlayerController:
    def __init__(self, entity: Entity):
        """Component, which transforms keyboard input to physics movement."""
        # parent
        self.entity = entity

        # state variables
        self.__input = 0
        self.__jump_pressed = False
        self.__is_grounded = False
        self.__can_jump = False

        # movement variables
        self.__max_speed = 300
        self.__accel = self.__max_speed / 0.15
        self.__friction = 1 / 10
        self.__initialize_gravity()

        # vel (world space), surface_vel (surface space)
        self.vel = Vector2(0, 0)
        self.__surface_vel = Vector2(0, 0)

        # collision variables
        self.collision_point = None
        self.__collision_buffer: list[CollisionInfo] = []
        self.in_collision_with = None
    
    # Compute required gravity & jump_force using parabola math
    def __initialize_gravity(self):
        max_jump_height = 300
        max_jump_time = 1.2
        self.__terminal_vel = 1500

        time_to_apex = max_jump_time / 2
        self.__gravity = 2 * max_jump_height / (time_to_apex**2)
        self.__jump_force = 2 * max_jump_height / time_to_apex
    
    # Player loop
    def update(self):
        if (self.__is_grounded):
            self.__grounded_update()
        else:
            self.__midair_update()
        
        self.__is_grounded = False

# - - - - Ground Update - - - -

    def __grounded_update(self):
        # transformation from world to surface space
        self.__surface_vel = self.entity.world_to_obj(self.vel)

        self.__read_input()
        self.__apply_horizontal_accel()
        self.__apply_friction()
        self.__clamp_velocity()
        self.__handle_jumping()
        
        # transformation from surface to world space
        self.vel = self.entity.obj_to_world(self.__surface_vel)

    # Horizontal input: arrow keys, A and D
    # Jump: space
    def __read_input(self):
        self.__input = 0
        keys = pygame.key.get_pressed()

        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.__input -= 1
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            self.__input += 1
        
        self.__jump_pressed = keys[pygame.K_SPACE]

    # Accelerate when input exists
    def __apply_horizontal_accel(self):
        if (self.__input == 0):
            return
        self.__surface_vel.x += self.__input * self.__accel * Time.dt
    
    # Decelerate the player
    def __apply_friction(self):
        self.__surface_vel.x *= (1 - self.__friction)
    
    def __clamp_velocity(self):
        # the speed of the player should not exceed max_speed
        self.__surface_vel.x = pygame.math.clamp(self.__surface_vel.x, -self.__max_speed, self.__max_speed)

        # if the speed is very small => default to zero
        if (abs(self.__surface_vel.x) < 5):
            self.__surface_vel.x = 0

    # The player may only jump if grounded when the space bar is pressed
    # The can_jump variable prevents the player from jumping multiple times with the same space bar press
    def __handle_jumping(self):
        if (not self.__jump_pressed and self.__is_grounded):
            self.__can_jump = True
        
        if (self.__jump_pressed and self.__can_jump):
            self.__can_jump = False
            self.__surface_vel.y = self.__jump_force * self.__jump_force_multiplier()

    # The jump_force (initial y-velocity) is not constant
    # The more the player jumps in the direction of gravity, the less force is applied
    def __jump_force_multiplier(self):
        # difference is a number in range [-1, 1]
        difference = Vector2.dot(self.entity.up, Vector2(0, -1))
        # [-1, 1] -> [0, 1]
        difference = (difference + 1) / 2
        # the multiplier should be non zero
        return max(difference, 0.1)

# - - - - Midair Update - - - -

    def __midair_update(self):
        # reset surface_vel since player is airborne
        self.__surface_vel = Vector2(0, 0)
        self.__apply_gravity()

    def __apply_gravity(self):
        # apply downwards acceleration always in the direction of the positive y-axis
        self.vel.y += self.__gravity * Time.dt
        # make sure the player doesn't accelerate too much
        self.vel.y = min(self.vel.y, self.__terminal_vel)

# - - - - Collision Logic - - - -

    # Add per update cycle data to the collision buffer
    def add_to_buffer(self, data: CollisionInfo):
        self.__collision_buffer.append(data)

    # Respond to collisions with surfaces (platforms)
    def collision_response(self):
        # no collisions
        if (len(self.__collision_buffer) == 0):
            self.collision_point = None
            return
        
        # trivial collision
        if (len(self.__collision_buffer) == 1):
            self.__collision_resolve(self.__collision_buffer[0])
            return
        
        # are you forced between a rock and a hard place?
        if (self.is_squished()):
            GameStateHandler.on_gameover(DeathType.SQUISH)
            return
        
        # just push the player out of collision if stationary
        if (self.vel == Vector2(0, 0)):
            for c in self.__collision_buffer:
                self.entity.coll.pos += c.get_offset_out()
            return

        # find the ideal collision
        diff = Vector2.dot(self.vel, self.__collision_buffer[0].normal)
        index = 0
        for i in range(1, len(self.__collision_buffer)):
            other = Vector2.dot(self.vel, self.__collision_buffer[i].normal)
            if (other < diff):
                diff = other
                index = i

        self.__collision_resolve(self.__collision_buffer[index])

    def is_squished(self) -> bool:
        for c in self.__collision_buffer:
            if (c.overlap > 10):
                return True
        return False

    def __collision_resolve(self, info: CollisionInfo):
        # resolve collision (technically not); make the player stick to the collider
        self.entity.translate(info.get_offset_in() + info.inherited_offset)

        # change basis
        self.entity.up = info.normal
        self.entity.right = Vector2(-info.normal.y, info.normal.x)

        # remove all vertical velocity upon collision with a surface
        self.vel = Vector2.dot(self.vel, self.entity.right) * self.entity.right

        self.collision_point = info.point
        self.__is_grounded = True

        # reset buffer
        self.__collision_buffer.clear()
