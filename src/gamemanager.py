import pygame
from pygame.math import Vector2
from utils.stage import Stage
from utils.time import Time
from entities.platforms import PlatformManager
from entities.player import PlayerController

# Manages Game States & Updating

class GameManager:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Hello World!")
        self.window = Stage(pygame.display.set_mode((1200, 1000)))
        self.clock = pygame.time.Clock()

        self.player = PlayerController(Vector2(600, 500), 30)
        PlatformManager.generate()

        self.load_content()

    def load_content(self):

        self.update()

    def update(self):
        while (True):
            Time.update(self.clock)
            self.check_events()
            
            self.player.update()
            PlatformManager.update()

            self.window.draw()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    self.on_exit()

    def on_exit(self):
        exit()