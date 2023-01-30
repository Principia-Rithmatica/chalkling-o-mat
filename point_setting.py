import random
from typing import Tuple

import pygame
import pygame_gui
from pygame import Rect, KEYUP
from pygame.event import Event
from pygame.math import Vector2
from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UILabel, UITextEntryLine, UITextBox

from UICheckbox import UICheckbox
from consts import SELECT_ELEMENT, CHECKBOX_CHANGED, NUM_CHARACTERS
from event_dispatcher import EventDispatcher
from point import Point


