from enum import Enum

from pygame import USEREVENT

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
GREY = (60,60,60)

# Inputs
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

# Defaults
POINT_SIZE = 5
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800

# Events
MY_EVENTS = USEREVENT+100
SELECT_ELEMENT = MY_EVENTS + 1


# Classifications
class BodyPart(Enum):
    LEG = 1
    ARM = 2
    HAND = 4
    BODY = 8
    TAIL = 16
    WING = 32


class BodyFeature(Enum):
    ARMORED = 1
    WEAPONIZED = 2
    SPIKEY = 4
    HEALTHY = 8