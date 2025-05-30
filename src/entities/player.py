from pygame.math import Vector2
from entities.entity import Entity
from physics.player_control import PlayerController
from physics.colliders import CircleCollider
from utils.gui.stage import Stage
from utils.data.time import Time
from utils.gui.camera import Camera

# Player entity

class Player(Entity):
    # Singleton (only 1 player is allowed)
    instance: 'Player' = None

    def __init__(self, start_pos: Vector2, radius: float):
        super().__init__(CircleCollider(start_pos, radius), (255, 0, 0))
        self.controller = PlayerController(self)
        self.camera = Camera(self)

        Player.instance = self

    def update(self):
        self.controller.update()
        self.translate(self.controller.vel * Time.dt)

    def draw(self):
        super().draw()
        if (self.controller.collision_point is not None):
            Stage.draw_circle(self.controller.collision_point, 5, (0, 255, 0))
