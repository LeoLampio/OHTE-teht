import pygame
from pygame.surface import Surface
from entities.player import PlayerController
from entities.platforms import PlatformManager

# Handle Drawing & Window Properties

class Stage:
    WIDTH = 0
    HEIGHT = 0
    __offset = 0

    def __init__(self, surf: Surface):
        self.__stage = surf
        Stage.WIDTH = surf.get_width()
        Stage.HEIGHT = surf.get_height()

    def draw(self):
        self.__stage.fill((0, 0, 0))

        PlatformManager.draw(self.__stage)
        PlayerController.instance.draw(self.__stage)

        pygame.display.flip()
