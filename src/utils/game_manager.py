import sys
import pygame
from pygame.math import Vector2
from utils.time import Time
from utils.stage import Stage
from utils.platform_manager import PlatformManager
from entities.player import Player

# Manages Game States & Updating

class GameManager:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Hello World!")
        Stage.initialize(pygame.display.set_mode((1200, 1000)))

        self.clock = pygame.time.Clock()

        self.player = Player(Vector2(600, 600), 30)
        PlatformManager.begin()

        self.load_content()

    # Load assets
    def load_content(self):
        # currently no assets
        self.update()

    # Update game state
    def update(self):
        while (True):
            Time.update(self.clock)
            self.check_events()
            
            self.player.update()
            PlatformManager.update()
            self.player.controller.collision_response()
            self.player.camera.update()
            PlatformManager.generate()

            self.update_screen()
            self.clock.tick(60)
    
    # Rendering phase of the update cycle
    def update_screen(self):
        Stage.draw_background()

        PlatformManager.render()
        self.player.draw()

        pygame.display.flip()

    # Press ESC to exit the game (or fall offscreen)
    def check_events(self):
        if (self.player.camera.is_out_of_frustum()):
            self.on_exit()

        for event in pygame.event.get():
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_ESCAPE):
                    self.on_exit()

    def on_exit(self):
        sys.exit()
