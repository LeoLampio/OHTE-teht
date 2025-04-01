from gamemanager import *

from physics.colliders import CircleCollider

class PlatformManager:
    obj = CircleCollider(Vector2(Width / 2, 600), 100)

    @classmethod
    def draw(cls):
        pygame.draw.circle(Stage.stage, (255, 255, 255), cls.obj.pos, cls.obj.radius)