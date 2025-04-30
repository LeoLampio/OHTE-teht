from enum import Enum
from utils.data.statistics import DeathType, StatHandler

class State(Enum):
    Running = 0,
    Paused = 1,
    Ended = 2

# Manages game states
class GameStateHandler:
    state : State = None

    @classmethod
    def on_pause(cls):
        if (cls.state == State.Ended):
            return
        if (cls.state == State.Running):
            cls.state = State.Paused
        else:
            cls.state = State.Running

    @classmethod
    def on_gameover(cls, death_type: DeathType):
        StatHandler.initiate_death(death_type)
        cls.state = State.Ended
