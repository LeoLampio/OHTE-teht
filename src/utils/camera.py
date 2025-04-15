from pygame.math import lerp
from utils.stage import Stage
from utils.time import Time
from entities.entity import Entity

# Controls the movement of the screen

class Camera:
    def __init__(self, entity: Entity):
        self.entity = entity
        # linear interpolation speed (easing speed)
        self.lerp_speed = 10
        # if the player is above this y-value, the screen should move
        self.boundary = 300
        self.death_plane = 200
    
    def update(self):
        pos = self.entity.coll.pos + Stage.Offset
        if (pos.y > self.boundary):
            return
        
        d = self.boundary - pos.y
        Stage.Offset.y += lerp(d, 0, self.lerp_speed * Time.dt)

    def is_out_of_frustum(self) -> bool:
        return self.entity.coll.pos.y + Stage.Offset.y > Stage.HEIGHT + self.death_plane
