import copy
import math
from typing import Tuple, List, Iterable, Callable

import pygame
import pygame_gui
from pygame import Surface, Rect, KEYUP
from pygame.event import Event
from pygame.math import Vector2
from pygame_gui import UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UITextEntryLine, UILabel, UITextBox

from UICheckbox import get_checked_values, UICheckbox
from bezier import bezier_curve
from consts import WHITE, YELLOW, BodyPart, BodyFeature, SELECT_ELEMENT, CHECKBOX_CHANGED, NUM_CHARACTERS
from dnd_handler import DragAble
from event_dispatcher import EventDispatcher, on_change_checked_list, on_change_checked, on_change_float
from point import Point, PointSetting
from selection_handler import Selectable, Marks


def draw_bezier(surface: Surface, start_point: Point, point_a: Point, point_b: Point, end_point: Point, color):
    curve = bezier_curve([start_point.get_pos(), point_a.get_pos(), point_b.get_pos(), end_point.get_pos()])
    prev_point = None
    for curve_point in curve:
        if prev_point is not None:
            pygame.draw.line(surface, color, prev_point, curve_point)
        prev_point = curve_point


class Line(Selectable, DragAble):

    def __init__(self, point_a: Point, point_b: Point, settings: "LineSetting"):
        super().__init__()
        self.point_a: Point = point_a
        self.point_b: Point = point_b
        self.point_a_bezier: Point = Point(Vector2(point_a.pos), PointSetting())
        self.point_b_bezier: Point = Point(Vector2(point_b.pos), PointSetting())

        self.point_a_bezier.move(Vector2(0, 50), [])
        self.point_b_bezier.move(Vector2(0, 50), [])

        self.width = 2
        self.settings: LineSetting = settings

    def draw(self, screen: Surface):
        color = self.get_color()
        if self.settings.curve:
            draw_bezier(screen, self.point_a, self.point_a_bezier, self.point_b_bezier, self.point_b, color)
        else:
            pygame.draw.line(screen, color, self.point_a.get_pos(), self.point_b.get_pos(), int(self.width))
        if self.is_marked(Marks.SELECTED) and self.settings.curve:
            self.point_a_bezier.draw(screen)
            self.point_b_bezier.draw(screen)

    def render(self, screen: Surface):
        color = WHITE
        if self.settings.curve:
            draw_bezier(screen, self.point_a, self.point_a_bezier, self.point_b_bezier, self.point_b, color)
        else:
            pygame.draw.line(screen, color, self.point_a.get_pos(), self.point_b.get_pos(), int(self.width))

    def get_color(self):
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW
        return color

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()

    def get_pos(self) -> Tuple[float, float]:
        pa = self.point_a.get_pos()
        pb = self.point_b.get_pos()
        return (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2

    def move(self, direction: Vector2, already_moved: List[any]):
        if self.point_a not in already_moved:
            self.point_a.move(direction, already_moved)

        if self.point_b not in already_moved:
            self.point_b.move(direction, already_moved)

        if self.point_a_bezier not in already_moved:
            self.point_a_bezier.move(direction, already_moved)

        if self.point_b_bezier not in already_moved:
            self.point_b_bezier.move(direction, already_moved)

        already_moved.append(self)

    def is_selected(self, selection: Rect) -> bool:
        clipline = selection.clipline(self.point_a[0], self.point_a[1], self.point_b[0], self.point_b[1])
        return clipline != ()

    def distance(self, p: Point | Tuple[float, float]) -> float:
        if self.point_a is None or self.point_b is None:
            return math.inf
        x1, y1 = self.point_a
        x2, y2 = self.point_b
        x, y = p

        # check if point is within the X of the line / trust me I'm EnGiNeEr!
        if not (x1 <= p[0] <= x2 or x1 >= p[0] >= x2) and not (y1 <= p[1] <= y2 or y1 >= p[1] >= y2):
            return math.inf

        # For vertical lines
        if x2 - x1 == 0:
            return math.fabs(p[0] - x1)

        # calculate the slope and y-intercept of the line
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # calculate the coefficients A, B, C of the equation of the line
        A = -m
        B = 1
        C = -b

        # calculate the distance between the point and the line
        return abs((A * x + B * y + C) / math.sqrt(A ** 2 + B ** 2))

    def scale(self, factor: float):
        self.point_a_bezier.scale(factor)
        self.point_b_bezier.scale(factor)



class LineSetting:
    def __init__(self):
        self.width_variance_min: float = 1.0
        self.width_variance_max: float = 5.0
        self.body_parts: List[BodyPart] = []
        self.body_features: List[BodyFeature] = []
        self.curve: bool = False


class LineSettingView(UIContainer):
    def __init__(self, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect, anchor: dict[str, str]):
        super().__init__(relative_rect, pygame_gui.ui_manager.get_default_manager(), anchors=anchor)
        self.selection = []
        self.event_dispatcher: EventDispatcher = event_dispatcher
        y = 10
        self.title: UITextBox = UITextBox("Line Setting", Rect(10, y, 310, 30), container=self)
        y += 30
        self.title_pos_variance = UILabel(Rect(10, y, 310, 30), "Width", container=self)
        y += 30
        self.width_variance_min = UITextEntryLine(Rect(10, y, 150, 30), container=self, initial_text="1.0")
        self.width_variance_min.set_allowed_characters(NUM_CHARACTERS)
        self.width_variance_max = UITextEntryLine(Rect(160, y, 150, 30), container=self, initial_text="5.0")
        self.width_variance_max.set_allowed_characters(NUM_CHARACTERS)
        y += 30
        self.curve = UICheckbox(Rect(10, y, 300, 30), "Curve", "", container=self)
        y += 30
        self.body_parts: dict[BodyPart, UICheckbox] = self.generate_body_parts(Rect(10, y, 150, 30))
        self.body_features: dict[BodyFeature, UICheckbox] = self.generate_body_feature(Rect(160, y, 150, 30))

        event_dispatcher.listen(self.on_select, event_type=SELECT_ELEMENT)
        event_dispatcher.listen(on_change_float("width_variance_min", self.get_selected_settings),
                                element=self.width_variance_min,
                                event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(on_change_float("width_variance_max", self.get_selected_settings),
                                element=self.width_variance_max,
                                event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(on_change_checked("curve", self.get_selected_settings), element=self.curve,
                                event_type=CHECKBOX_CHANGED)
        event_dispatcher.listen(self.on_key_up, event_type=KEYUP)

    def get_selected_settings(self):
        return [line.settings for line in self.selection]

    def generate_body_parts(self, base_rect: Rect) -> dict[BodyPart, UICheckbox]:
        return self.generate_checkbox("body_parts", BodyPart, base_rect)

    def generate_body_feature(self, base_rect: Rect) -> dict[BodyFeature, UICheckbox]:
        return self.generate_checkbox("body_features", BodyFeature, base_rect)

    def generate_checkbox(self, attribute: str, values: Iterable, base_rect: Rect):
        features = dict()
        i = 0

        for value in values:
            rect = Rect(base_rect.x, base_rect.y + i * 30, base_rect.width, base_rect.height)
            ui_checkbox = UICheckbox(rect, value.name, value, container=self)
            event_handler = on_change_checked_list(attribute, self.get_selected_settings)
            self.event_dispatcher.listen(event_handler, element=ui_checkbox, event_type=CHECKBOX_CHANGED)
            features[value] = ui_checkbox
            i += 1

        return features

    def save_setting(self, setting: LineSetting):
        try:
            setting.body_features = get_checked_values(self.body_features)
            setting.body_parts = get_checked_values(self.body_parts)
            setting.width_variance_min = float(self.width_variance_min.text)
            setting.width_variance_max = float(self.width_variance_max.text)
            setting.curve = self.curve.is_checked()
        except ValueError:
            pass
        except TypeError:
            pass

    def load_setting(self, setting: LineSetting):
        for body_part, checkbox in self.body_parts.items():
            checkbox.set_checked(body_part in setting.body_parts)
        for body_feature, checkbox in self.body_features.items():
            checkbox.set_checked(body_feature in setting.body_features)
        self.width_variance_min.set_text(str(setting.width_variance_min))
        self.width_variance_max.set_text(str(setting.width_variance_max))
        self.curve.set_checked(setting.curve)

    def on_select(self, event: Event) -> bool:
        self.selection = [selection for selection in event.selection if isinstance(selection, Line)]
        self.update_view()
        return False

    def update_view(self):
        for element in self.selection:
            self.load_setting(element.settings)
            return

    def on_key_up(self, event: Event) -> bool:
        match event.key:
            case pygame.K_1:
                self.body_parts[BodyPart.LEG].toggle()
                return True
            case pygame.K_2:
                self.body_parts[BodyPart.ARM].toggle()
                return True
            case pygame.K_3:
                self.body_parts[BodyPart.HAND].toggle()
                return True
            case pygame.K_4:
                self.body_parts[BodyPart.BODY].toggle()
                return True
            case pygame.K_5:
                self.body_parts[BodyPart.TAIL].toggle()
                return True
            case pygame.K_6:
                self.body_parts[BodyPart.WING].toggle()
                return True
            case pygame.K_7:
                self.body_parts[BodyPart.HEAD].toggle()
                return True
            case pygame.K_c:
                self.curve.toggle()
        return False
