import pygame
import pygame_gui
from pygame.event import Event
from pygame.surface import Surface

from base_form import BaseForm
from consts import LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON
from dnd_handler import DragAndDropHandler
from event_dispatcher import EventDispatcher


class BaseFormView(DragAndDropHandler):
    def __init__(self, ui_manager, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)
        self.enable_edit = False
        self.current_base_form: BaseForm = BaseForm()
        self.selected: dict | None = None
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
        event_dispatcher.listen(self.on_switch_edit, self.edit_button)

        self.form_surface = pygame.Surface((512, 512))

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def on_switch_edit(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(f"switch edit {self.enable_edit} -> {not self.enable_edit}")
            self.enable_edit = not self.enable_edit
            if self.enable_edit:
                self.current_base_form.start_editing()
            else:
                self.current_base_form.stop_editing()
            return True

    def on_select(self, event: Event):
        pos = pygame.mouse.get_pos()
        self.selected = self.current_base_form.select(pos)
        self.dnd_selected = self.selected
        return False

    def on_click(self, event: Event):
        surf_rect = self.form_surface.get_rect()
        if surf_rect.collidepoint(event.pos):
            pos = pygame.mouse.get_pos()
            if event.button == LEFT_MOUSE_BUTTON:
                self.on_left_click(pos)
                return True
            if event.button == RIGHT_MOUSE_BUTTON:
                self.on_right_click(pos)
                return True

        return False

    def on_left_click(self, pos: (int, int)):
        if self.enable_edit:
            self.add_point(pos)

    def on_right_click(self, pos: (int, int)):
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
