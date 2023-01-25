import random
from typing import Tuple

import pygame
from pygame import Rect, KEYUP
from pygame.event import Event
from pygame.math import Vector2
from pygame_gui import UIManager, UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UILabel, UITextEntryLine, UITextBox

from UICheckbox import UICheckbox
from consts import SELECT_ELEMENT, CHECKBOX_CHANGED, NUM_CHARACTERS
from event_dispatcher import EventDispatcher


class PointSetting:

    def __init__(self, pos_variance_x_min: float = 0, pos_variance_x_max: float = 0, pos_variance_y_min: float = 0,
                 pos_variance_y_max: float = 0, angle_min: float = 0, angle_max: float = 0):
        self.base_x: float = 0
        self.base_y: float = 0
        self.pos_variance_x_min: float = pos_variance_x_min
        self.pos_variance_x_max: float = pos_variance_x_max
        self.pos_variance_y_min: float = pos_variance_y_min
        self.pos_variance_y_max: float = pos_variance_y_max
        self.curve: bool = False

    def set_base(self, pos: Tuple[float, float] | Vector2):
        self.base_x, self.base_y = pos

    def get_new_position(self) -> Tuple[float, float]:
        new_x = self.base_x + random.uniform(self.pos_variance_x_min, self.pos_variance_x_max)
        new_y = self.base_y + random.uniform(self.pos_variance_y_min, self.pos_variance_y_max)
        return new_x, new_y

    def set_bounds(self, bounds: Rect):
        self.pos_variance_x_min = -bounds.width / 2
        self.pos_variance_x_max = bounds.width / 2
        self.pos_variance_y_min = -bounds.height / 2
        self.pos_variance_y_max = bounds.height / 2


class PointSettingView(UIContainer):
    def __init__(self, manager: UIManager, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect,
                 anchor: dict[str, str]):
        super().__init__(relative_rect, manager, anchors=anchor)
        self.selected_setting: PointSetting = PointSetting()

        y = 10
        self.title: UITextBox = UITextBox("Point Setting", Rect(10, y, 310, 30), container=self)
        y += 30

        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Pos Variance X", manager, container=self)
        y += 30
        self.pos_variance_x_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="-10")
        self.pos_variance_x_min.set_allowed_characters(NUM_CHARACTERS)
        self.pos_variance_x_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="10")
        self.pos_variance_x_max.set_allowed_characters(NUM_CHARACTERS)

        y += 30
        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Pos Variance Y", manager, container=self)
        y += 30
        self.pos_variance_y_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="-10")
        self.pos_variance_y_min.set_allowed_characters(NUM_CHARACTERS)
        self.pos_variance_y_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="10")
        self.pos_variance_y_max.set_allowed_characters(NUM_CHARACTERS)
        y += 30
        self.curve = UICheckbox(Rect(10, y, 310, 30), "Curve", None, container=self)

        event_dispatcher.listen(self.on_change_data, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(self.on_select, event_type=SELECT_ELEMENT)
        event_dispatcher.listen(self.on_key_up, event_type=KEYUP)
        event_dispatcher.listen(self.on_change_data, element=self.curve, event_type=CHECKBOX_CHANGED)

    def get_settings(self) -> PointSetting:
        setting = PointSetting()
        self.fill_setting(setting)
        return setting

    def fill_setting(self, setting: PointSetting):
        try:
            setting.pos_variance_x_min = float(self.pos_variance_x_min.text)
            setting.pos_variance_x_max = float(self.pos_variance_x_max.text)
            setting.pos_variance_y_min = float(self.pos_variance_y_min.text)
            setting.pos_variance_y_max = float(self.pos_variance_y_max.text)
            setting.curve = self.curve.is_checked()

        except ValueError:
            pass
        except TypeError:
            pass

    def set_setting(self, setting: PointSetting):
        if setting is None:
            # Copy the value to prevent overriding the previous selected point
            setting = PointSetting()
            self.fill_setting(setting)
        self.selected_setting = setting
        self.pos_variance_x_min.set_text(str(setting.pos_variance_x_min))
        self.pos_variance_x_max.set_text(str(setting.pos_variance_x_max))
        self.pos_variance_y_min.set_text(str(setting.pos_variance_y_min))
        self.pos_variance_y_max.set_text(str(setting.pos_variance_y_max))
        self.curve.set_checked(setting.curve)

    def on_change_data(self, event: Event) -> bool:
        print("update point data")
        self.fill_setting(self.selected_setting)
        return False

    def on_select(self, event: Event) -> bool:
        setting = event.selected_point.settings if hasattr(event, "selected_point") \
                                                   and event.selected_point is not None else None
        self.set_setting(setting)
        return False

    def on_key_up(self, event: Event) -> bool:
        match event.key:
            case pygame.K_c:
                self.curve.toggle()
                return True
        return False
