from typing import Callable

from pygame.event import Event
from pygame_gui.core import UIElement


class EventDispatcher:

    def __init__(self):
        self.listeners: [Callable[[Event], bool]] = []

    def listen(self, listener: Callable[[Event], bool], element: UIElement = None, event_type: int | None = None):
        def filtered_listener(event: Event):
            no_element = element is None
            element_is_target = (hasattr(event, "target") and event.target == element) or \
                                (hasattr(event, "ui_element") and event.ui_element == element)
            no_event_type = event_type is None
            event_type_equals = event_type == event.type

            if (no_element or element_is_target) and (no_event_type or event_type_equals):
                listener(event)

        self.listeners.append(filtered_listener)

    def process_event(self, event: Event):
        for listener in self.listeners:
            if listener(event):
                return
