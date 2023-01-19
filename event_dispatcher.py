from typing import Callable

from pygame.event import Event
from pygame_gui.core import UIElement


class EventDispatcher:

    def __init__(self):
        self.listeners: [Callable[[Event], bool]] = []

    def listen(self, listener: Callable[[Event], bool], element: UIElement = None):
        if element is not None:
            def filtered_listener(event):
                if (hasattr(event, "target") and event.target == element) or \
                   (hasattr(event, "ui_element") and event.ui_element == element):
                    listener(event)

            self.listeners.append(filtered_listener)
        else:
            self.listeners.append(listener)

    def process_event(self, event: Event):
        for listener in self.listeners:
            if listener(event):
                return
