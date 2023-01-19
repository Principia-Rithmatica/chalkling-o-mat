import pygame
import pygame_gui
from pygame.event import Event
from pygame.surface import Surface

from base_form import BaseForm
from event_dispatcher import EventDispatcher

LEFT_MOUSE_BUTTON = 1

RIGHT_MOUSE_BUTTON = 3


class BaseFormView:
    def __init__(self, ui_manager, event_dispatcher: EventDispatcher):
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

        event_dispatcher.listen(self.process_events)
        event_dispatcher.listen(self.switch_edit, self.edit_button)

        self.form_surface = pygame.Surface((512, 512))

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.current_base_form is not None:
            self.current_base_form.draw(self.form_surface)
        screen.blit(self.form_surface, (10, 10))

    def switch_edit(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print(f"switch edit {self.enable_edit} -> {not self.enable_edit}")
            self.enable_edit = not self.enable_edit
            return True

    def process_events(self, event: Event):
        if self.enable_edit and event.type == pygame.MOUSEBUTTONUP:
            surf_rect = self.form_surface.get_rect()
            if surf_rect.collidepoint(event.pos):
                if event.button == LEFT_MOUSE_BUTTON:
                    self.add_point()
                    return True
                if event.button == RIGHT_MOUSE_BUTTON:
                    self.delete_point()
                    return True
        return False

    def add_point(self):
        pos = pygame.mouse.get_pos()
        self.selected = self.current_base_form.select(pos)
        if self.selected is None:
            self.current_base_form.add_point(pos)
            print("Add point")
        else:
            print("select point")

    def delete_point(self):
        pos = pygame.mouse.get_pos()
        self.current_base_form.remove_point(pos)
        print("Remove point")

    def show(self, form: BaseForm):
        print("Show new form")
        self.current_base_form = form if form is not None else BaseForm()
