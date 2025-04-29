from pygame.time import Clock, get_ticks

# Keeps time

class Time:
    # 'deltatime' or the time in between frames
    dt = 0
    # Total time since the game began
    time = 0

    @classmethod
    def update(cls, clock: Clock):
        cls.dt = clock.get_time() / 1000
        cls.time += get_ticks() / 1000
