from typing import Tuple

import pygame
import pygame_gui
from pygame.event import Event
from pygame.surface import Surface
from pygame_gui import UIManager
from pygame_gui.elements import UIButton

from base_form import BaseForm
from consts import LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON, SELECT_ELEMENT
from dnd_handler import DragAndDropHandler
from event_dispatcher import EventDispatcher
from line import Line
from line_setting import LineSettingView
from point import Point
from point_setting import PointSettingView


class BaseFormView(DragAndDropHandler):
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher, point_setting_view: PointSettingView,
                 line_setting_view: LineSettingView):
        super().__init__(event_dispatcher)
        self.form_surface = pygame.Surface((512, 512))
        self.point_setting_view: PointSettingView = point_setting_view
        self.line_setting_view: LineSettingView = line_setting_view
        self.current_base_form: BaseForm = BaseForm()
        self.selected_point: Point | None = None
        self.selected_line: Line | None = None
        self.editable: bool = True

        event_dispatcher.listen(self.on_select, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.on_join, event_type=pygame.KEYUP)

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def on_select(self, event: Event) -> bool:
        if not self.form_surface.get_rect().collidepoint(event.pos) or not self.editable:
            return False
        selected_line, selected_point = self.current_base_form.get_selected(event.pos)
        selected_element = selected_point if selected_point is not None else selected_line
        # Start DnD
        self.start_drag(selected_element)

        # Select Point / Line
        self.selected_line, self.selected_point = self.current_base_form.select(event.pos)
        pygame.event.post(Event(SELECT_ELEMENT, selected_point=self.selected_point, selected_line=self.selected_line))

        # Select Previous One
        if selected_point is not None:
            self.current_base_form.set_previous_point(selected_point)

        # Add Point
        if event.button == LEFT_MOUSE_BUTTON and self.selected_point is None and self.selected_line is None:
            self.add_point(event.pos)
            return True
        if event.button == RIGHT_MOUSE_BUTTON:
            self.remove_point(event.pos)
            return True

        return False

    def on_join(self, event: Event) -> bool:
        if event.key != pygame.K_j:
            return False

        pos = pygame.mouse.get_pos()
        line, point = self.current_base_form.get_selected(pos)
        if point is None:
            return False

        line_setting = self.line_setting_view.get_setting()
        previous_point = self.current_base_form.previous_point
        self.current_base_form.add_line(point, previous_point, line_setting)

    def add_point(self, pos: Tuple[float, float]):
        if self.selected_point is None:
            line_setting = self.line_setting_view.get_setting()
            point_setting = self.point_setting_view.get_settings()
            self.current_base_form.add_point(pos, point_setting, line_setting)
            print("Add point")

    def remove_point(self, pos: Tuple[float, float]):
        self.current_base_form.remove_point(pos)
        print("Remove point")

    def show(self, form: BaseForm):
        print("Show new form")
        self.current_base_form = form if form is not None else BaseForm()
