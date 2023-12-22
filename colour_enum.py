import enum


class Colour(enum.Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    DARK_RED = (200, 0, 0)
    DARK_GREEN = (0, 200, 0)
    DARK_BLUE = (0, 0, 200)
    DARK_YELLOW = (200, 200, 0)
    PINK = (255, 0, 200)
    LIGHT_BLUE = (0, 200, 255)
    PURPLE = (128, 0, 128)
    GREY = (128, 128, 128)
    SELECTED_COLOR = (200, 100, 200)
