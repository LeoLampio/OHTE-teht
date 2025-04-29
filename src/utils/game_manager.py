import sys
import pygame
from pygame.math import Vector2
from utils.data.time import Time
from utils.gui.stage import Stage
from utils.gui.ui_manager import UIManager, FontAnchor, Anchor, FontSize
from utils.platform_manager import PlatformManager
from utils.data.statistics import StatHandler, DeathType
from entities.player import Player

# Manages Game States & Updating

class GameManager:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Physics Based Platformer")
        Stage.initialize(pygame.display.set_mode((1200, 1000)))
        UIManager.initialize()

        self.clock = pygame.time.Clock()

        self.initialize()
        self.load_content()
        self.update()

    def initialize(self):
        self.player = Player(Vector2(600, 600), 30)
        PlatformManager.begin()

        self.is_paused = False
        self.gameover = False

    # Load assets
    def load_content(self):
        # currently no assets

        # TODO Load data
        pass

    # Update game state
    def update(self):
        while (True):
            self.check_events()

            if (not self.gameover):
                Time.update(self.clock)

                if (not self.is_paused):
                    self.gameplay_loop()

            self.update_screen()
            self.clock.tick(60)

    # Update entities etc
    def gameplay_loop(self):
        self.player.update()
        PlatformManager.update()
        self.player.controller.collision_response()
        self.player.camera.update()
        StatHandler.update_score()
    
    # Rendering phase of the update cycle
    def update_screen(self):
        if (self.gameover):
            Stage.draw_custom_background((0, 0, 0))
            UIManager.gameover_view()
        else:
            Stage.draw_background()

            PlatformManager.draw()
            self.player.draw()

            UIManager.update_text(f"SCORE: {StatHandler.score:.0f}", (10, 10))

            if (self.is_paused):
                UIManager.pause_view()
                UIManager.update_text_anchored("press ESC to continue", FontAnchor(Anchor.LEFT, Anchor.RIGHT), (10, -10))
            else:
                UIManager.update_text_anchored("press ESC to pause", FontAnchor(Anchor.LEFT, Anchor.RIGHT), (10, -10), color=(160, 160, 160))

        pygame.display.flip()
    
    def check_events(self):
        if (not self.gameover and not self.is_paused):
            if (self.player.camera.is_out_of_frustum()):
                self.on_gameover(DeathType.Fall)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.on_exit()
            
            if (event.type != pygame.KEYDOWN):
                continue

            if (self.gameover):
                if (event.key == pygame.K_RETURN):
                    self.reset()
            else:
                if (event.key == pygame.K_ESCAPE):
                    self.is_paused = not self.is_paused

    def reset(self):
        Stage.Offset = Vector2(0, 0)
        PlatformManager.reset()
        Player.instance = None
        StatHandler.reset()
        self.initialize()

    def on_gameover(self, death_type: DeathType):
        self.gameover = True
        StatHandler.initiate_death(death_type)

    def on_exit(self):
        # TODO Save data
        sys.exit()
