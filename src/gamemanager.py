import pygame
from pygame.math import Vector2
from utils.stage import Stage, HEIGHT, WIDTH
from utils.time import Time
from entities.platformmanager import PlatformManager
from entities.player import PlayerController

class GameManager:
    
    clock = None

    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Hello World!")
        Stage.stage = pygame.display.set_mode((WIDTH, HEIGHT))
        GameManager.clock = pygame.time.Clock()

        self.player = PlayerController(Vector2(100, 100))
        PlatformManager.initialize()

        self.load_content()

    def load_content(self):

        self.update()

    def update(self):
        while (True):
            Time.update(GameManager.clock)
            self.check_events()
            
            self.player.update()

            self.draw()
            GameManager.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    exit()

    def draw(self):
        Stage.stage.fill((0, 0, 0))

        PlatformManager.draw()
        self.player.draw()

        pygame.display.flip()
