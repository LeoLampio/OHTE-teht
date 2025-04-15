from pygame.math import lerp
from utils.stage import Stage
from utils.time import Time
from entities.player import PlayerController
from entities.platforms import PlatformManager

# Controls the movement of the screen

class Camera:
    def __init__(self):
        # linear interpolation speed (easing speed)
        self.lerp_speed = 10
        # if the player is above this y-value, the screen should move
        self.boundary = 300
    
    def update(self):
        pos = PlayerController.instance.coll.pos + Stage.Offset
        if (pos.y > self.boundary):
            return
        
        d = self.boundary - pos.y
        Stage.Offset.y += lerp(d, 0, self.lerp_speed * Time.dt)

        PlatformManager.generate()
        PlatformManager.destroy()

    def is_out_of_frustum(self) -> bool:
        return PlayerController.instance.coll.pos.y + Stage.Offset.y > Stage.HEIGHT + PlayerController.instance.coll.radius + 20
