from enum import Enum
from utils.data.statistics import DeathType, StatHandler

class State(Enum):
    RUNNING = 0,
    PAUSED = 1,
    ENDED = 2

# Manages game states
class GameStateHandler:
    state : State = None

    @classmethod
    def on_pause(cls):
        if (cls.state == State.ENDED):
            return
        if (cls.state == State.RUNNING):
            cls.state = State.PAUSED
        else:
            cls.state = State.RUNNING

    @classmethod
    def on_gameover(cls, death_type: DeathType):
        StatHandler.initiate_death(death_type)
        cls.state = State.ENDED
