import random
from typing import Tuple, List, Callable

import pygame
import pygame_gui
from pygame import Rect, Vector2
from pygame.event import Event
from pygame.surface import Surface
from pygame_gui import UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UITextBox, UILabel, UITextEntryLine

from consts import WHITE, YELLOW, POINT_SIZE, GREEN, GREY, NUM_CHARACTERS, SELECT_ELEMENT
from dnd_handler import DragAble
from event_dispatcher import EventDispatcher, on_change_float
from selection_handler import Selectable, Marks


class Point(Selectable, DragAble):

    def __init__(self, pos: Vector2, settings: "PointSetting"):
        super().__init__()
        super(Selectable, self).__init__()
        self.settings: PointSetting = settings
        self.pos: Vector2 = pos
        self.settings.set_base(self.pos)
        self.selectable = True

    def regenerate(self):
        self.pos.update(self.settings.get_new_position())

    def draw(self, screen: Surface):
        color = WHITE
        if self.is_marked(Marks.PREVIOUS):
            color = GREEN
        elif self.is_marked(Marks.SELECTED):
            color = YELLOW

        pygame.draw.circle(screen, color, self.get_pos(), POINT_SIZE)
        if self.is_marked(Marks.SELECTED):
            self.draw_addition_info(screen)

    def draw_addition_info(self, screen: Surface):
        rect = Rect(self.settings.base_x + self.settings.pos_variance_x_min,
                    self.settings.base_y + self.settings.pos_variance_y_min,
                    -self.settings.pos_variance_x_min + self.settings.pos_variance_x_max,
                    -self.settings.pos_variance_y_min + self.settings.pos_variance_y_max)

        pygame.draw.rect(screen, GREY, rect, 2)

    def is_selected(self, selection: Rect) -> bool:
        if not self.selectable:
            return False

        collision_area = Rect(self.pos[0] - POINT_SIZE / 2, self.pos[1] - POINT_SIZE / 2, POINT_SIZE, POINT_SIZE)
        return selection.colliderect(collision_area)

    def get_pos(self) -> Tuple[float, float]:
        return self.pos.xy[0], self.pos.xy[1]

    def set_pos(self, pos: Tuple[float, float] | Vector2):
        self.pos.update(pos)
        self.settings.set_base(self.get_pos())

    def move(self, direction: Vector2, already_moved: List[any]):
        if self not in already_moved:
            self.set_pos(self.pos - direction)
            already_moved.append(self)

    def __getitem__(self, item):
        return self.pos[item]

    def scale(self, factor: float):
        self.set_pos(self.pos * factor)

    def set_bounds(self, bounds: Rect):
        self.set_pos(bounds.center)
        self.settings.set_bounds(bounds)


class PointSetting:

    def __init__(self,
                 pos_variance_x_min: float = -10,
                 pos_variance_x_max: float = 10,
                 pos_variance_y_min: float = -10,
                 pos_variance_y_max: float = 10):
        self.base_x: float = 0
        self.base_y: float = 0
        self.pos_variance_x_min: float = pos_variance_x_min
        self.pos_variance_x_max: float = pos_variance_x_max
        self.pos_variance_y_min: float = pos_variance_y_min
        self.pos_variance_y_max: float = pos_variance_y_max

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
    def __init__(self, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect,
                 anchor: dict[str, str]):
        super().__init__(relative_rect, pygame_gui.ui_manager.get_default_manager(), anchors=anchor)
        self.selection = []

        y = 10
        self.title: UITextBox = UITextBox("Point Setting", Rect(10, y, 310, 30), container=self)
        y += 30

        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Pos Variance X", container=self)
        y += 30
        self.pos_variance_x_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="-10")
        self.pos_variance_x_min.set_allowed_characters(NUM_CHARACTERS)
        self.pos_variance_x_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="10")
        self.pos_variance_x_max.set_allowed_characters(NUM_CHARACTERS)

        y += 30
        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Pos Variance Y", container=self)
        y += 30
        self.pos_variance_y_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="-10")
        self.pos_variance_y_min.set_allowed_characters(NUM_CHARACTERS)
        self.pos_variance_y_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="10")
        self.pos_variance_y_max.set_allowed_characters(NUM_CHARACTERS)

        event_dispatcher.listen(self.on_select, event_type=SELECT_ELEMENT)
        event_dispatcher.listen(on_change_float("pos_variance_x_min", self.get_selected_settings),
                                element=self.pos_variance_x_min, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(on_change_float("pos_variance_x_max", self.get_selected_settings),
                                element=self.pos_variance_x_max, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(on_change_float("pos_variance_y_min", self.get_selected_settings),
                                element=self.pos_variance_y_min, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(on_change_float("pos_variance_y_max", self.get_selected_settings),
                                element=self.pos_variance_y_max, event_type=UI_TEXT_ENTRY_CHANGED)

    def get_selected_settings(self):
        return [point.settings for point in self.selection]

    def save_setting(self, setting: PointSetting):
        """
        Saves the UI Elements back to the given setting object.
        :param setting: to put the data into
        """
        try:
            setting.pos_variance_x_min = float(self.pos_variance_x_min.text)
            setting.pos_variance_x_max = float(self.pos_variance_x_max.text)
            setting.pos_variance_y_min = float(self.pos_variance_y_min.text)
            setting.pos_variance_y_max = float(self.pos_variance_y_max.text)
        except ValueError:
            pass
        except TypeError:
            pass

    def load_setting(self, setting: PointSetting):
        """
        Loads the given setting into text fields.
        :param setting: to load
        """
        self.pos_variance_x_min.set_text(str(setting.pos_variance_x_min))
        self.pos_variance_x_max.set_text(str(setting.pos_variance_x_max))
        self.pos_variance_y_min.set_text(str(setting.pos_variance_y_min))
        self.pos_variance_y_max.set_text(str(setting.pos_variance_y_max))

    def on_select(self, event: Event) -> bool:
        self.selection = [x for x in event.selection if isinstance(x, Point)]
        self.update_view()
        return False

    def update_view(self):
        for element in self.selection:
            self.load_setting(element.settings)
            return

    def current(self):
        setting = PointSetting()
        self.save_setting(setting)
        return setting
