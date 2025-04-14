import pygame
from pygame.math import Vector2
from utils.time import Time
from physics.colliders import CircleCollider
from physics.collisionhandler import CollisionInfo

# Handles player movement and response to physics

class PlayerController:
    instance: "PlayerController" = None

    def __init__(self, startpos: Vector2, radius: float):
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

        # surface basis vectors
        self.__jump_axis = Vector2(0, -1)
        self.__move_axis = Vector2(1, 0)

        # vel (world space), surface_vel (surface space)
        self.vel = Vector2(0, 0)
        self.__surface_vel = Vector2(0, 0)

        # collision variables
        self.coll = CircleCollider(startpos, radius)
        self.__last_collision_point = Vector2(0, -1000)

        # singleton
        PlayerController.instance = self
    
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

        self.__move()
        self.__is_grounded = False

# - - - - Ground Update - - - -

    def __grounded_update(self):
        # transformation from world to surface space
        self.__surface_vel = Vector2(Vector2.dot(self.__move_axis, self.vel), Vector2.dot(self.__jump_axis, self.vel))

        self.__read_input()
        self.__apply_horizontal_accel()
        self.__apply_friction()
        self.__clamp_velocity()
        self.__handle_jumping()
        
        # transformation from surface to world space
        self.vel = self.__surface_vel.x * self.__move_axis + self.__surface_vel.y * self.__jump_axis

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

    def __apply_horizontal_accel(self):
        if (self.__input == 0):
            return
        
        # accelerate when input exists
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
        return max((Vector2.dot(self.__jump_axis, Vector2(0, -1)) + 1) / 2, 0.1)

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

# - - - - Other Methods - - - -

    # Move the player in world space
    def __move(self):
        self.coll.pos += self.vel * Time.dt

    # Respond to collisions with surfaces (platforms)
    def collision_response(self, info: CollisionInfo, inherited_offset: Vector2 = Vector2(0, 0)):
        # resolve collision (technically not); make the player stick to the collider
        self.coll.pos += info.get_offset_in() + inherited_offset

        # change basis
        self.__jump_axis = info.normal
        self.__move_axis = Vector2(-info.normal.y, info.normal.x)

        # remove all vertical velocity upon collision with a surface
        self.vel = Vector2.dot(self.vel, self.__move_axis) * self.__move_axis

        self.__last_collision_point = info.point
        self.__is_grounded = True

    # Draw the player's collider on screen
    def draw(self, surf):
        pygame.draw.circle(surf, (255, 0, 0), self.coll.pos, self.coll.radius)
        pygame.draw.circle(surf, (0, 255, 0), self.__last_collision_point, 5)
