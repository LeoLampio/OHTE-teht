import sys
import pygame
from pygame.math import Vector2
from utils.data.time import Time
from utils.gui.stage import Stage
from utils.gui.ui_manager import UIManager
from utils.environment.platform_manager import PlatformManager
from utils.data.statistics import StatHandler, DeathType
from utils.game_state import GameStateHandler, State
from utils.data.save_data import SaveManager
from entities.player import Player

# Manages the game session

class GameManager:
    # Initializes the game session variables etc
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Physics Based Platformer")
        Stage.initialize(pygame.display.set_mode((1200, 1000)))
        UIManager.initialize()

        self.clock = pygame.time.Clock()

        self.initialize()
        self.load_content()
        self.update()

    # Initializes individual game related variables
    def initialize(self):
        self.player = Player(Vector2(600, 600), 30)
        PlatformManager.begin()
        GameStateHandler.state = State.RUNNING

    # Loads external assets
    def load_content(self):
        StatHandler.initialize(SaveManager.decode())

    # Updates game state
    def update(self):
        while (True):
            self.check_events()
            Time.update(self.clock)

            if (GameStateHandler.state == State.RUNNING):
                self.gameplay_loop()

            self.update_screen()
            self.clock.tick(60)

    # Updates entities etc
    def gameplay_loop(self):
        self.player.update()
        PlatformManager.update()
        self.player.controller.collision_response()
        self.player.camera.update()
        StatHandler.update_score(self.player.coll.bounds.bottom)
    
    # Rendering phase of the update cycle
    def update_screen(self):
        if (GameStateHandler.state == State.ENDED):
            UIManager.gameover_view()
        else:
            Stage.draw_background()

            PlatformManager.draw()
            self.player.draw()

            if (GameStateHandler.state == State.PAUSED):
                UIManager.pause_view()
            else:
                UIManager.game_view()

        pygame.display.flip()
    
    # Checks events for gameover, quitting, resetting and pausing
    def check_events(self):
        if (GameStateHandler.state == State.RUNNING):
            if (self.player.camera.is_below_frustum()):
                GameStateHandler.on_gameover(DeathType.FALL)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                self.on_exit()
            
            if (event.type != pygame.KEYDOWN):
                continue
            
            if (GameStateHandler.state == State.ENDED):
                if (event.key == pygame.K_RETURN):
                    self.reset()
            if (event.key == pygame.K_ESCAPE):
                GameStateHandler.on_pause()

    # Restarts the game
    def reset(self):
        StatHandler.save()
        Stage.Offset = Vector2(0, 0)
        PlatformManager.reset()
        Player.instance = None
        self.initialize()

    # Handles quitting
    def on_exit(self):
        StatHandler.save()
        sys.exit()
