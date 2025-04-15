import pygame
from pygame.math import Vector2
from pygame.surface import Surface

# Handle Drawing & Window Properties

class Stage:
    WIDTH = 0
    HEIGHT = 0
    Offset = Vector2(0, 0)

    __stage: Surface = None
    __back_col = (20, 0, 30)

    @classmethod
    def initialize(cls, surf: Surface):
        cls.__stage = surf
        cls.WIDTH = surf.get_width()
        cls.HEIGHT = surf.get_height()

    @classmethod
    def draw_background(cls):
        cls.__stage.fill(cls.__back_col)

    @classmethod
    def draw_circle(cls, pos: Vector2, radius: float, color: tuple):
        pygame.draw.circle(cls.__stage, color, pos + cls.Offset, radius)

    @classmethod
    def draw_polygon(cls, vertices: list, color: tuple):
        pygame.draw.polygon(cls.__stage, color, [v + cls.Offset for v in vertices])
