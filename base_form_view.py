from typing import Tuple

import pygame
from pygame.event import Event
from pygame.rect import Rect
from pygame.surface import Surface
from pygame_gui import UIManager

from area_selector import AreaSelector
from base_form import BaseForm
from consts import LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON, SELECT_ELEMENT, EDIT_FORM
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
        self.area_selector: AreaSelector = AreaSelector(event_dispatcher, self.form_surface, self.on_selection_done)

        event_dispatcher.listen(self.on_select, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.on_keyup, event_type=pygame.KEYUP)

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        self.area_selector.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def on_select(self, event: Event) -> bool:
        if not self.form_surface.get_rect().collidepoint(event.pos) or not self.editable:
            return False
        selected_line, selected_point = self.current_base_form.get_selected(event.pos)

        # Start DnD
        selected_element = selected_point if selected_point is not None else selected_line
        self.start_drag(selected_element)

        # Select -> Deselect
        unselect = False
        if selected_line is not None and selected_line == self.selected_line:
            selected_line = None
            unselect = True
        if selected_point is not None and selected_point == self.selected_point:
            selected_point = None
            unselect = True

        # Select Point / Line
        self.select_element(selected_line, selected_point)

        # Select Previous One
        if selected_point is not None:
            self.current_base_form.set_previous_point(selected_point)

        # Add Point
        if event.button == LEFT_MOUSE_BUTTON \
                and self.selected_point is None \
                and self.selected_line is None \
                and not unselect:
            self.add_point(event.pos)
            return True
        if event.button == RIGHT_MOUSE_BUTTON:
            self.remove_point(event.pos)
            return True

        return False

    def on_selection_done(self, selected: Rect):
        if self.area_selector.enabled and self.selected_point is not None:
            self.selected_point.set_bounds(selected)
            pygame.event.post(Event(SELECT_ELEMENT, selected_point=self.selected_point))
            self.area_selector.enabled = False
            self.editable = True

    def on_keyup(self, event: Event) -> bool:
        match event.key:
            case pygame.K_j:
                self.join_line()
            case pygame.K_n:
                self.current_base_form = BaseForm()
                pygame.event.post(Event(EDIT_FORM))
            case pygame.K_p:
                if self.selected_point is not None:
                    self.editable = False
                    self.area_selector.enabled = True
                    print("Start selection")

        return False

    def stop_drag(self, event: Event) -> bool:
        was_dragged = super().stop_drag(event)
        if was_dragged:
            pygame.event.post(Event(EDIT_FORM))
            print("Stop DND")
        return was_dragged

    def join_line(self):
        pos = pygame.mouse.get_pos()
        line, point = self.current_base_form.get_selected(pos)
        previous_point = self.current_base_form.previous_point

        if point is None or previous_point is None:
            return
        line_setting = self.line_setting_view.get_setting()
        self.current_base_form.add_line(point, previous_point, line_setting)

    def add_point(self, pos: Tuple[float, float]):
        if self.selected_point is None:
            line_setting = self.line_setting_view.get_setting()
            point_setting = self.point_setting_view.get_settings()
            point, line = self.current_base_form.add_point(pos, point_setting, line_setting)
            self.select_element(line, point)
            print("Add point")

    def select_element(self, line: Line | None = None, point: Point | None = None):
        self.current_base_form.select(line, point)
        self.selected_line = line
        self.selected_point = point
        pygame.event.post(Event(SELECT_ELEMENT, selected_point=self.selected_point, selected_line=self.selected_line))

    def remove_point(self, pos: Tuple[float, float]):
        self.current_base_form.remove_point(pos)
        print("Remove point")

    def set_current_form(self, form: BaseForm):
        print("Show new form")
        self.current_base_form = form if form is not None else BaseForm()

    def get_current_form(self) -> BaseForm:
        return self.current_base_form

    def disable_input(self):
        self.editable = False
        self.area_selector.enabled = False

    def enable_input(self):
        self.editable = True
        self.area_selector.enabled = False
