from pygame.time import Clock, get_ticks

class Time:
    dt = 0
    time = 0

    @classmethod
    def update(cls, clock: Clock):
        cls.dt = clock.get_time() / 1000
        cls.time += get_ticks() / 1000