from typing import List

from pygame import Rect
from pygame.event import Event
from pygame_gui import UIManager
from pygame_gui.elements import UIWindow, UIButton, UILabel, UITextBox

from UICheckbox import UICheckbox
from consts import SELECT_ELEMENT, BodyPart
from event_dispatcher import EventDispatcher
from point import Point


class LineSettingView:
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher):
        self.ui_manager: UIManager = ui_manager
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.window: UIWindow = UIWindow(Rect(512, 290, 350, 340), ui_manager, "Line Setting", draggable=False)
        self.body_parts: List[UICheckbox] = self.generate_body_parts(Rect(10, 40, 150, 30))

        self.title_pos_variance = UILabel(Rect(10, 10, 310, 30), "Width", ui_manager, container=self.window)
        self.pos_variance_x_min = UITextBox("1", Rect(10, 40, 150, 30), ui_manager, container=self.window)
        self.pos_variance_x_max = UITextBox("15", Rect(160, 40, 150, 30), ui_manager, container=self.window)

    def generate_body_parts(self, base_rect: Rect) -> List[UICheckbox]:
        parts: List[UICheckbox] = []
        i = 0
        for part in BodyPart:
            i += 1
            rect = Rect(base_rect.x, base_rect.y + i * 30, base_rect.width, base_rect.height)
            ui_checkbox = UICheckbox(rect, part.name, part, container=self.window)
            parts.append(ui_checkbox)
        return parts

    def get_checked_body_parts(self) -> List[BodyPart]:
        parts = []
        for body_part in self.body_parts:
            if body_part.is_checked():
                parts.append(body_part.data)
        return parts


class PointSettingView:
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher):
        self.ui_manager: UIManager = ui_manager
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.selected_point: Point | None = None
        self.window: UIWindow = UIWindow(Rect(512, 0, 350, 300), ui_manager, "Point Setting", draggable=False)

        self.title_pos_variance = UILabel(Rect(10, 10, 310, 30), "Pos Variance X", ui_manager, container=self.window)
        self.pos_variance_x_min = UITextBox("-10", Rect(10, 40, 150, 30), ui_manager, container=self.window)
        self.pos_variance_x_max = UITextBox("10", Rect(160, 40, 150, 30), ui_manager, container=self.window)

        self.title_pos_variance = UILabel(Rect(10, 70, 310, 30), "Pos Variance Y", ui_manager, container=self.window)
        self.pos_variance_y_min = UITextBox("-10", Rect(10, 100, 150, 30), ui_manager, container=self.window)
        self.pos_variance_y_max = UITextBox("10", Rect(160, 100, 150, 30), ui_manager, container=self.window)

        self.title_angle = UILabel(Rect(10, 130, 310, 30), "Angle", ui_manager, container=self.window)
        self.angle_min = UITextBox("-10", Rect(10, 160, 150, 30), ui_manager, container=self.window)
        self.angle_max = UITextBox("10", Rect(160, 160, 150, 30), ui_manager, container=self.window)

    def set_point(self, point: Point):
        self.selected_point = point
        self.update_view()

    def update_view(self):
        # TODO implement update from selected point to the inputs
        pass


class SettingView:
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher):
        self.ui_manager: UIManager = ui_manager
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.line_setting_view = LineSettingView(ui_manager, event_dispatcher)
        self.point_setting_view = PointSettingView(ui_manager, event_dispatcher)
        self.event_dispatcher.listen(self.on_select, event_type=SELECT_ELEMENT)

    def on_select(self, event: Event) -> bool:
        print("select event")
        if event.selected is None or isinstance(event.selected, Point):
            self.point_setting_view.set_point(event.selected)
            # TODO Line handling
        return False
