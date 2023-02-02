from typing import Callable, Iterable, List

from pygame.event import Event
from pygame_gui.core import UIElement


class EventDispatcher:

    def __init__(self):
        self._listeners: [Callable[[Event], bool]] = []

    def listen(self, listener: Callable[[Event], bool], element: UIElement = None, event_type: int | None = None):
        def filtered_listener(event: Event):
            no_element = element is None
            element_is_target = (hasattr(event, "target") and event.target == element) or \
                                (hasattr(event, "ui_element") and event.ui_element == element)
            no_event_type = event_type is None
            event_type_equals = event_type == event.type

            if (no_element or element_is_target) and (no_event_type or event_type_equals):
                return listener(event)

        self._listeners.append(filtered_listener)

    def process_event(self, event: Event):
        for listener in self._listeners:
            if listener(event):
                return


def on_change(converter: Callable[[any, Event], None], get_elements: Callable[[], Iterable])\
        -> Callable[[Event], bool]:
    """
    Creates a general event handler that needs a converter to update the value of all elements in get_selections.
    :param converter: to set change data in the selected
    :param get_elements: getter to receive the current elements that should be changed
    :return: event handler
    """
    def handle(event: Event) -> bool:
        for element in get_elements():
            try:
                converter(element, event)
            except ValueError:
                pass
            except TypeError:
                pass
        return True
    return handle


def on_change_float(attribute: str, get_elements: Callable[[], Iterable]) -> Callable[[Event], bool]:
    """
    Generates an event handler that updates the attribute of all elements in get_selections.
    :param attribute: to update (has to be a float)
    :param get_elements: all elements that should be updated
    :return: event handler
    """
    def converter(element, event: Event):
        setattr(element, attribute, float(event.text))
    return on_change(converter, get_elements)


def on_change_checked(attribute: str, get_elements: Callable[[], Iterable]) -> Callable[[Event], bool]:
    """
    Generates an event handler that update the attribute of all elements in get_selections.
    :param attribute: to update (has to be a bool)
    :param get_elements: all elements that should be updated
    :return: event handler
    """
    def converter(element, event: Event):
        setattr(element, attribute, event.checked)
    return on_change(converter, get_elements)


def on_change_checked_list(attribute: str, get_elements: Callable[[], Iterable]) -> Callable[[Event], bool]:
    """
    Generates an event handler that update the attribute of all elements in get_selections.
    :param attribute: to update (has to be a List)
    :param get_elements: all elements that should be updated
    :return: event handler
    """
    def converter(element, event: Event):
        values: List = getattr(element, attribute)
        values.append(event.ui_element.data)
        setattr(element, attribute, values)
    return on_change(converter, get_elements)
