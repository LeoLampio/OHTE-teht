from pygame.math import lerp
from utils.gui.stage import Stage
from utils.data.time import Time
from entities.entity import Entity

# Controls the movement of the screen

class Camera:
    def __init__(self, entity: Entity):
        # parent
        self.entity = entity
        # linear interpolation speed (easing speed)
        self.lerp_speed = 10
        # if the player's distance from the camera's top is this
        # the screen should move
        self.boundary = 300

    def update(self):
        if (not self.should_move()):
            return
        
        delta = self.entity.coll.bounds.bottom - Camera.top() - self.boundary
        Stage.Offset.y += lerp(delta, 0, self.lerp_speed * Time.dt)

    def should_move(self) -> bool:
        return self.entity.coll.bounds.bottom < Camera.top() + self.boundary

    def is_below_frustum(self) -> bool:
        return self.entity.coll.bounds.top > Camera.bottom()

# Bounds

    @classmethod
    def left(cls) -> int:
        return int(Stage.Offset.x)
    
    @classmethod
    def right(cls) -> int:
        return int(Stage.WIDTH + Stage.Offset.x)
    
    @classmethod
    def top(cls) -> int:
        return int(Stage.Offset.y)
    
    @classmethod
    def bottom(cls) -> int:
        return int(Stage.HEIGHT + Stage.Offset.y)
    
# Center Coordinates

    @classmethod
    def horizontal_center(cls) -> int:
        return (cls.left() + cls.right()) // 2
    
    @classmethod
    def vertical_center(cls) -> int:
        return (cls.top() + cls.bottom()) // 2
