import pygame
from pygame.math import Vector2
from utils.stage import Stage, WIDTH
from physics.colliders import CircleCollider, PolygonCollider

class PlatformManager:

    circles = []
    polys = []

    @classmethod
    def initialize(cls):
        cls.polys.append(PolygonCollider(Vector2(200, 550), [
            Vector2(100, 0), Vector2(50, 70), Vector2(-50, 70), Vector2(-100, 0), Vector2(0, -70)
        ]))
        cls.circles.append(CircleCollider(Vector2(WIDTH / 2, 600), 100))

    @classmethod
    def draw(cls):
        for c in cls.circles:
            pygame.draw.circle(Stage.stage, (255, 255, 255), c.pos, c.radius)

        for p in cls.polys:
            pygame.draw.polygon(Stage.stage, (255, 0, 0), p.verts)
