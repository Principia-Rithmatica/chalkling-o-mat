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
from point import Point
from point_setting import PointSettingView


class BaseFormView(DragAndDropHandler):
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher, point_setting_view: PointSettingView):
        super().__init__(event_dispatcher)
        self.form_surface = pygame.Surface((512, 512))
        self.point_setting_view: PointSettingView = point_setting_view
        self.current_base_form: BaseForm = BaseForm()
        self.selected: Point | Line | None = None
        self.editable: bool = True
        event_dispatcher.listen(self.on_select, event_type=pygame.MOUSEBUTTONDOWN)

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def on_select(self, event: Event) -> bool:
        if not self.form_surface.get_rect().collidepoint(event.pos) or not self.editable:
            return False
        print(f'{event}')
        selected_line, selected_point = self.current_base_form.get_selected(event.pos)
        selected_element = selected_point if selected_point is not None else selected_line
        # Start DnD
        self.start_drag(selected_element)

        # Select Point / Line
        # Select Previous One
        current_selected = self.selected
        self.selected = self.current_base_form.select(event.pos)

        if current_selected != self.selected:
            select_event = pygame.event.Event(SELECT_ELEMENT, selected=self.selected)
            pygame.event.post(select_event)

        # Add Point
        if event.button == LEFT_MOUSE_BUTTON and self.selected is None:
            self.add_point(event.pos)
            return True
        if event.button == RIGHT_MOUSE_BUTTON:
            self.remove_point(event.pos)
            return True

        return False

    def add_point(self, pos: (float, float)):
        if self.selected is None:
            settings = self.point_setting_view.get_point_settings()
            self.current_base_form.add_point(pos, settings)
            print("Add point")

    def remove_point(self, pos: (float, float)):
        self.current_base_form.remove_point(pos)
        print("Remove point")

    def show(self, form: BaseForm):
        print("Show new form")
        self.current_base_form = form if form is not None else BaseForm()
