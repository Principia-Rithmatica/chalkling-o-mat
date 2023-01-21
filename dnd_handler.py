from abc import abstractmethod

import pygame
from pygame.event import Event

from event_dispatcher import EventDispatcher


class DragAble:
    @abstractmethod
    def get_pos(self) -> (float, float):
        pass

    @abstractmethod
    def set_pos(self, pos: (float, float)):
        pass


class DragAndDropHandler:
    def __init__(self, event_dispatcher: EventDispatcher):
        self._dragged_object: DragAble | None = None
        self._previous_position: (float, float) = (0, 0)
        self._has_moved: bool = False

        event_dispatcher.listen(self.move_drag, event_type=pygame.MOUSEMOTION)
        event_dispatcher.listen(self.stop_drag, event_type=pygame.MOUSEBUTTONUP)

    def is_dragging(self) -> bool:
        return self._dragged_object is not None

    def start_drag(self, drag_able: DragAble | None) -> bool:
        if self.is_dragging() or drag_able is None:
            return False
        self._dragged_object = drag_able
        self._previous_position = drag_able.get_pos()
        return True

    def move_drag(self, event: Event) -> bool:
        if not self.is_dragging():
            return False
        if event.pos != self._dragged_object.get_pos():
            self._has_moved = True
        self._dragged_object.set_pos(event.pos)
        return True

    def stop_drag(self, event: Event) -> bool:
        if self.is_dragging():
            self._dragged_object = None
            has_moved = self._has_moved
            self._has_moved = False
            return has_moved
        return False
