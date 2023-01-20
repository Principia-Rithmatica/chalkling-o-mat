from abc import abstractmethod

import pygame
from pygame.event import Event

from event_dispatcher import EventDispatcher


class DragAble:
    @abstractmethod
    def get_pos(self) -> (int, int):
        pass

    @abstractmethod
    def set_pos(self, pos: (int, int)):
        pass


class DragAndDropHandler:
    def __init__(self, event_dispatcher: EventDispatcher):
        self.dnd_selected: DragAble | None = None
        self.dnd_dragged: DragAble | None = None
        self.previous_position: (int, int) = (0, 0)

        event_dispatcher.listen(self.move_drag, event_type=pygame.MOUSEMOTION)
        event_dispatcher.listen(self.start_drag, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.stop_drag, event_type=pygame.MOUSEBUTTONUP)

    def is_dnd_enabled(self) -> bool:
        return self.dnd_selected is not None or self.is_dnd()

    def is_dnd(self) -> bool:
        return self.dnd_dragged is not None

    def start_drag(self, event: Event):
        if not self.is_dnd_enabled():
            return
        print("start dnd")
        self.dnd_dragged = self.dnd_selected
        self.previous_position = self.dnd_selected.get_pos()
        return True

    def move_drag(self, event: Event):
        if not self.is_dnd_enabled():
            return

        self.dnd_selected.set_pos(event.pos)
        return True

    def stop_drag(self, event: Event):
        if not self.is_dnd_enabled():
            return
        print("stop dnd")
        self.dnd_dragged = None
        self.dnd_selected = None
        return True
