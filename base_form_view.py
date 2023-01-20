import pygame
import pygame_gui
from pygame.event import Event
from pygame.surface import Surface

from base_form import BaseForm
from consts import LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON, SELECT_ELEMENT
from dnd_handler import DragAndDropHandler
from event_dispatcher import EventDispatcher
from line import Line
from point import Point


class BaseFormView(DragAndDropHandler):
    def __init__(self, ui_manager, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)
        self.enable_edit = False
        self.current_base_form: BaseForm = BaseForm()
        self.selected: Point | Line | None = None
        self.edit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(-180, -120, 150, 30),
            text='Edit',
            manager=ui_manager,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'})

        event_dispatcher.listen(self.on_select, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.on_click, event_type=pygame.MOUSEBUTTONUP)
        event_dispatcher.listen(self.on_switch_edit, self.edit_button, event_type=pygame_gui.UI_BUTTON_PRESSED)

        self.form_surface = pygame.Surface((512, 512))

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def is_dnd_enabled(self) -> bool:
        return super().is_dnd_enabled() and self.enable_edit

    def on_switch_edit(self, event: Event) -> bool:
        print(f"switch edit {self.enable_edit} -> {not self.enable_edit}")
        self.enable_edit = not self.enable_edit
        if self.enable_edit:
            self.current_base_form.start_editing()
        else:
            self.current_base_form.stop_editing()
        return True

    def on_select(self, event: Event) -> bool:
        surf_rect = self.form_surface.get_rect()
        if surf_rect.collidepoint(event.pos):
            current_selected = self.selected
            self.selected = self.current_base_form.select(event.pos)
            self.dnd_selected = self.selected
            if current_selected != self.selected:
                select_event = pygame.event.Event(SELECT_ELEMENT, selected=self.selected)
                pygame.event.post(select_event)
        return False

    def on_click(self, event: Event) -> bool:
        surf_rect = self.form_surface.get_rect()
        if surf_rect.collidepoint(event.pos):
            pos = pygame.mouse.get_pos()
            if event.button == LEFT_MOUSE_BUTTON:
                self.left_click(pos)
                return True
            if event.button == RIGHT_MOUSE_BUTTON:
                self.right_click(pos)
                return True

        return False

    def left_click(self, pos: (int, int)):
        if self.enable_edit:
            self.add_point(pos)

    def right_click(self, pos: (int, int)):
        if self.enable_edit:
            self.remove_point(pos)

    def add_point(self, pos: (int, int)):
        if self.selected is None:
            self.current_base_form.add_point(pos)
            print("Add point")

    def remove_point(self, pos: (int, int)):
        self.current_base_form.remove_point(pos)
        print("Remove point")

    def show(self, form: BaseForm):
        print("Show new form")
        self.current_base_form = form if form is not None else BaseForm()
