from pygame.math import lerp
from utils.stage import Stage
from utils.time import Time
from entities.player import PlayerController

class Camera:
    def __init__(self):
        self.lerp_speed = 10
        self.boundary = 300
    
    def update(self):
        pos = PlayerController.instance.coll.pos + Stage.Offset
        if (pos.y > self.boundary):
            return
        
        d = self.boundary - pos.y
        Stage.Offset.y += lerp(0, d, self.lerp_speed * Time.dt)

    def is_out_of_frustum(self) -> bool:
        return PlayerController.instance.coll.pos.y + Stage.Offset.y > Stage.HEIGHT + 100
