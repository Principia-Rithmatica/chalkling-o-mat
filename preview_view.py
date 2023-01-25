import copy
from typing import List, Tuple

import pygame
from pygame import Rect, Surface, KEYUP
from pygame.event import Event
from pygame_gui import UI_TEXT_ENTRY_CHANGED

from base_form import BaseForm
from base_form_view import BaseFormView
from consts import REGENERATE, CHECKBOX_CHANGED, EDIT_FORM
from event_dispatcher import EventDispatcher


class PreviewView:
    def __init__(self, rect: Rect, event_dispatcher: EventDispatcher, base_form_view: BaseFormView, scale_factor: float):
        self.surface: Surface = Surface(rect.size)
        self.event_dispatcher = event_dispatcher
        self.base_form_view = base_form_view
        self.current_form: BaseForm | None = None
        self.rect = rect
        self.scale_factor = scale_factor

        event_dispatcher.listen(self.regenerate, event_type=REGENERATE)
        event_dispatcher.listen(self.regenerate, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(self.regenerate, event_type=CHECKBOX_CHANGED)
        event_dispatcher.listen(self.regenerate, event_type=EDIT_FORM)
        event_dispatcher.listen(self.on_key_up, event_type=KEYUP)

    def regenerate(self, event: Event) -> bool:
        self.current_form = copy.deepcopy(self.base_form_view.get_current_form())
        self.current_form.regenerate()
        self.current_form.scale(self.scale_factor)
        return False

    def draw(self, screen: Surface):
        self.surface.fill((5, 5, 5))
        if self.current_form is not None:
            self.current_form.render(self.surface)
        screen.blit(self.surface, self.rect.topleft)

    def on_key_up(self, event: Event) -> bool:
        match event.key:
            case pygame.K_r:
                pygame.event.post(Event(REGENERATE))
                return True
        return False
