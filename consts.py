# Colors
from enum import Enum

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Inputs
LEFT_MOUSE_BUTTON = 1
RIGHT_MOUSE_BUTTON = 3

# Defaults
POINT_SIZE = 5


# Classifications
class BodyParts(Enum):
    LEG = 1
    ARM = 2
    HAND = 4
    BODY = 8
    TAIL = 16
    WING = 32


class BodyFeatures(Enum):
    ARMORED = 1
    WEAPONIZED = 2
    SPIKEY = 4
    HEALTHY = 8
