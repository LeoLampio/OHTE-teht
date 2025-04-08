from pygame.time import Clock

class Time:
    dt = 0
    time = 0

    @classmethod
    def update(cls, clock: Clock):
        cls.dt = clock.get_time() / 1000
        cls.time += Clock.get_ticks() / 1000
