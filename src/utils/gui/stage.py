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
    def left(cls):
        return -int(Stage.Offset.x)
    
    @classmethod
    def right(cls):
        return int(cls.WIDTH - Stage.Offset.x)
    
    @classmethod
    def top(cls):
        return -int(Stage.Offset.y)
    
    @classmethod
    def bottom(cls):
        return int(Stage.HEIGHT - Stage.Offset.y)

    @classmethod
    def draw_ui_element(cls, surf: Surface, pos: tuple):
        cls.__stage.blit(surf, pos)

    @classmethod
    def draw_background(cls):
        cls.__stage.fill(cls.__back_col)

    @classmethod
    def draw_custom_background(cls, bg: tuple):
        cls.__stage.fill(bg)

    @classmethod
    def draw_circle(cls, pos: Vector2, radius: float, color: tuple):
        pygame.draw.circle(cls.__stage, color, pos + cls.Offset, radius)

    @classmethod
    def draw_polygon(cls, vertices: list, color: tuple):
        pygame.draw.polygon(cls.__stage, color, [v + cls.Offset for v in vertices])
