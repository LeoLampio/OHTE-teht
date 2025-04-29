from enum import Enum
import random
from utils.gui.stage import Stage
from entities.player import Player

class DeathType(Enum):
    Fall = 0,
    Squish = 1

class StatHandler:
    score = 0
    highscore = 0

    fall_count = 0
    squish_count = 0

    death_msg = ""

    @classmethod
    def update_score(cls):
        cls.score = max(
            cls.score,
            (Stage.HEIGHT / 2 - Player.instance.coll.pos.y) // 50
        )

    @classmethod
    def is_highscore(cls) -> bool:
        return cls.score > cls.highscore
    
    @classmethod
    def initiate_death(cls, death_type: DeathType):
        if (cls.is_highscore()):
            cls.death_msg= DeathMessages.highscore_msg
            cls.highscore = cls.score
        elif (death_type == DeathType.Fall):
            cls.death_msg = random.choice(DeathMessages.fall_msgs)
        elif (death_type == DeathType.Squish):
            cls.death_msg = random.choice(DeathMessages.squish_msgs)

    @classmethod
    def reset(cls):
        cls.score = 0
        cls.death_msg = ""

    # TODO Save & Load functionality

class DeathMessages:

    fall_msgs = [
        "you're supposed to go up",
        f"you have fallen {StatHandler.fall_count} time{'s' if StatHandler.fall_count != 1 else ''}",
        "is it cozy down there?",
        "the abyss is glad to have you",
        "the underground is vast. You may even find a skeleton or two"
    ]
    squish_msgs = [

    ]
    highscore_msg = "you've reached new heights!"