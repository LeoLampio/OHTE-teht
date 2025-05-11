from enum import Enum
from pygame import font
from utils.gui.stage import Stage, Surface
from utils.data.statistics import StatHandler

# Moves the anchor or origin of a UI element
class Anchor(Enum):
    LEFT = 0,
    CENTER = 1,
    RIGHT = 2

# X: LEFT = 0, RIGHT = screen width, CENTER = screen width / 2
# Y: LEFT = 0, RIGHT = screen height, CENTER = screen height / 2
class FontAnchor:
    def __init__(self, x_anchor: Anchor, y_anchor: Anchor):
        self.x = x_anchor
        self.y = y_anchor

class FontSize(Enum):
    SMALL = 0,
    MEDIUM = 1,
    LARGE = 2

# Manages fonts
class Fonts:
    small : font.Font = None
    medium : font.Font = None
    large : font.Font = None

    @classmethod
    def get_font(cls, size: FontSize) -> font.Font:
        if (size == FontSize.SMALL):
            return cls.small
        if (size == FontSize.MEDIUM):
            return cls.medium
        if (size == FontSize.LARGE):
            return cls.large
        return None

# Manages UI elements

class UIManager:
    """Used to create UI elements."""
    @classmethod
    def initialize(cls):
        Fonts.small = font.SysFont('Arial', 20)
        Fonts.medium = font.SysFont('Arial', 30)
        Fonts.large = font.SysFont('Arial', 40)

    # Renders text in normal screen space
    @classmethod
    def render_text(cls, text: str, pos: tuple, size: FontSize = FontSize.SMALL, color: tuple = (255, 255, 255)):
        Stage.draw_ui_element(Fonts.get_font(size).render(text, True, color), pos)

    # Renders text using the given anchor
    @classmethod
    def render_text_anchored(cls, text: str, anchor: FontAnchor, offset: tuple, 
                             size: FontSize = FontSize.SMALL, color: tuple = (255, 255, 255)):
        surf = Fonts.get_font(size).render(text, True, color)
        x = offset[0]
        y = offset[1]

        if (anchor.x == Anchor.CENTER):
            x += (Stage.WIDTH - surf.get_width()) / 2
        elif (anchor.x == Anchor.RIGHT):
            x += Stage.WIDTH - surf.get_width()
        
        if (anchor.y == Anchor.CENTER):
            y += (Stage.HEIGHT - surf.get_height()) / 2
        elif (anchor.y == Anchor.RIGHT):
            y += Stage.HEIGHT - surf.get_height()
            
        Stage.draw_ui_element(surf, (x, y))

    # Render the UI during gameplay
    @classmethod
    def game_view(cls):
        cls.render_text(f"SCORE: {StatHandler.score:.0f}", (10, 10))
        cls.render_text_anchored("press ESC to pause", FontAnchor(Anchor.LEFT, Anchor.RIGHT), (10, -10), color=(160, 160, 160))

    # Render the pause screen UI
    @classmethod
    def pause_view(cls):
        cls.render_text(f"SCORE: {StatHandler.score:.0f}", (10, 10))
        darken = Surface((Stage.WIDTH, Stage.HEIGHT))
        darken.set_alpha(160)
        Stage.draw_ui_element(darken, (0, 0))
        cls.render_text_anchored("PAUSED", FontAnchor(Anchor.CENTER, Anchor.CENTER), (0, -100), FontSize.LARGE)
        cls.render_text_anchored("press ESC to continue", FontAnchor(Anchor.LEFT, Anchor.RIGHT), (10, -10))

    # Render the gameover screen
    @classmethod
    def gameover_view(cls):
        Stage.draw_custom_background((0, 0, 0))
        cls.render_text_anchored(
            "GAMEOVER", FontAnchor(Anchor.CENTER, Anchor.CENTER), (0, -100), FontSize.LARGE, (255, 128, 128))
        cls.render_text_anchored(
            StatHandler.death_msg, FontAnchor(Anchor.CENTER, Anchor.CENTER), (0, -50), FontSize.SMALL, (160, 160, 160))
        cls.render_text_anchored(
            f"Final Score: {StatHandler.score:.0f}", FontAnchor(Anchor.CENTER, Anchor.CENTER), 
            (0, 0), FontSize.MEDIUM, (128, 255, 128))
        cls.render_text_anchored(
            "press ENTER to play again", FontAnchor(Anchor.CENTER, Anchor.CENTER), (0, 50), FontSize.SMALL, (128, 128, 128))
