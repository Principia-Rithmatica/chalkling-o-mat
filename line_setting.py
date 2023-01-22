from typing import List, Iterable

import pygame
from pygame import Rect
from pygame.event import Event
from pygame_gui import UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UILabel, UITextBox, UITextEntryLine

from UICheckbox import UICheckbox, get_checked_values
from consts import BodyPart, BodyFeature, SELECT_ELEMENT, CHECKBOX_CHANGED
from event_dispatcher import EventDispatcher


class LineSetting:
    def __init__(self):
        self.width_variance_min: float = 1.0
        self.width_variance_max: float = 15.0
        self.body_parts: List[BodyPart] = []
        self.body_features: List[BodyFeature] = []


class LineSettingView(UIContainer):
    def __init__(self, manager: IUIManagerInterface, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect,
                 anchor: dict[str, str]):
        super().__init__(relative_rect, manager, anchors=anchor)
        self.selected_setting: LineSetting = LineSetting()

        y = 10
        self.title: UITextBox = UITextBox("Line Setting", Rect(10, y, 310, 30), container=self)
        y += 30
        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Width", container=self)
        y += 30
        self.width_variance_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="1")
        self.width_variance_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="15")
        y += 30
        self.body_parts: dict[BodyPart, UICheckbox] = self.generate_body_parts(Rect(10, y, 150, 30))
        self.body_features: dict[BodyFeature, UICheckbox] = self.generate_body_feature(Rect(160, y, 150, 30))

        event_dispatcher.listen(self.on_change_data, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(self.on_change_data, event_type=CHECKBOX_CHANGED)
        event_dispatcher.listen(self.on_select, event_type=SELECT_ELEMENT)

    def generate_body_parts(self, base_rect: Rect) -> dict[BodyPart, UICheckbox]:
        return self.generate_checkbox(BodyPart, base_rect)

    def generate_body_feature(self, base_rect: Rect) -> dict[BodyFeature, UICheckbox]:
        return self.generate_checkbox(BodyFeature, base_rect)

    def generate_checkbox(self, values: Iterable, base_rect: Rect):
        features = dict()
        i = 0
        for value in values:
            rect = Rect(base_rect.x, base_rect.y + i * 30, base_rect.width, base_rect.height)
            ui_checkbox = UICheckbox(rect, value.name, value, container=self)
            features[value] = ui_checkbox
            i += 1

        return features

    def get_setting(self) -> LineSetting:
        setting = LineSetting()
        self.fill_setting(setting)
        return setting

    def fill_setting(self, setting: LineSetting):
        try:
            setting.body_features = get_checked_values(self.body_features)
            setting.body_parts = get_checked_values(self.body_parts)
            setting.width_variance_min = float(self.width_variance_min.text)
            setting.width_variance_max = float(self.width_variance_max.text)
        except ValueError:
            pass
        except TypeError:
            pass

    def set_setting(self, setting: LineSetting):
        if setting is None:
            # Copy the value to prevent overriding the previous selected line
            setting = LineSetting()
            self.fill_setting(setting)
        self.selected_setting = setting
        for body_part, checkbox in self.body_parts.items():
            checkbox.set_checked(body_part in setting.body_parts)
        for body_feature, checkbox in self.body_features.items():
            checkbox.set_checked(body_feature in setting.body_features)
        self.width_variance_min.set_text(str(setting.width_variance_min))
        self.width_variance_max.set_text(str(setting.width_variance_max))

    def on_change_data(self, event: Event) -> bool:
        print("update line data")
        self.fill_setting(self.selected_setting)
        return False

    def on_select(self, event: Event) -> bool:
        print("Select line for settings")
        setting = None if event.selected_line is None else event.selected_line.settings
        self.set_setting(setting)
        return False