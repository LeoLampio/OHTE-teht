import random
from enum import Enum
from utils.gui.stage import Stage
from utils.data.save_data import SaveManager

# How the game ended
class DeathType(Enum):
    FALL = 0,
    SQUISH = 1

# Handles data
class StatHandler:
    """Handles player session variables."""
    score = 0
    highscore = 0

    fall_count = 0
    squish_count = 0

    death_msg = ""

    @classmethod
    def update_score(cls, player_height: int):
        cls.score = max(
            cls.score,
            (Stage.HEIGHT / 2 - player_height) // 50
        )

    @classmethod
    def is_highscore(cls) -> bool:
        return cls.score > cls.highscore
    
    # Update stats after a death occured
    # Set a randomized death message based on the type of death
    @classmethod
    def initiate_death(cls, death_type: DeathType):
        if (death_type == DeathType.FALL):
            cls.fall_count += 1
        elif (death_type == DeathType.SQUISH):
            cls.squish_count += 1
        
        if (cls.is_highscore()):
            cls.death_msg = DeathMessages.highscore_msg
            cls.highscore = cls.score
        elif (death_type == DeathType.FALL):
            cls.death_msg = DeathMessages.get_fall_msg()
        elif (death_type == DeathType.SQUISH):
            cls.death_msg = DeathMessages.get_squish_msg()

    # Save data to file
    @classmethod
    def save(cls):
        cls.score = 0
        data = {
            'highscore': int(cls.highscore),
            'fall_count': cls.fall_count,
            'squish_count': cls.squish_count
        }
        SaveManager.encode(data)

    # Load data from a file, if it exists
    @classmethod
    def initialize(cls, data: dict):
        if (data is None):
            return
        cls.highscore = int(data['highscore'])
        cls.fall_count = data['fall_count']
        cls.squish_count = data['squish_count']

# Manages death messages
class DeathMessages:

    @classmethod
    def get_fall_msg(cls) -> str:
        if (random.random() < 1 / 3):
            return f"you have fallen {StatHandler.fall_count} time{'s' if StatHandler.fall_count != 1 else ''}"
        
        msg = random.choice(cls.__fall_msgs)
        while (msg == StatHandler.death_msg):
            msg = random.choice(cls.__fall_msgs)
        return msg
    
    @classmethod
    def get_squish_msg(cls) -> str:
        if (random.random() < 1 / 3):
            return f"current scoreboard is 0 - {StatHandler.squish_count}, in favor of the platforms"
        msg = random.choice(cls.__squish_msgs)
        while (msg == StatHandler.death_msg):
            msg = random.choice(cls.__squish_msgs)
        return msg

    __fall_msgs = [
        "you're supposed to go up",
        "is it cozy down there?",
        "the abyss is glad to have you",
        "the underground is vast. You may even find a skeleton or two"
    ]
    __squish_msgs = [
        "please be more vigilant next time",
        "well that was gruesome",
        "the platforms won't wait for you"
    ]
    highscore_msg = "you've reached new heights!"
