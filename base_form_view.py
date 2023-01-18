from types import NoneType

from pygame.event import Event
from pygame.surface import Surface

from base_form import BaseForm


class BaseFormView:
    def __init__(self):
        self.current_base_form: BaseForm | NoneType = None

    def draw(self, screen: Surface):
        self.current_base_form.draw(screen)

    def process_events(self, event: Event):
        # TODO implement
        pass

    def show(self, form: BaseForm):
        self.current_base_form = form
