from abc import abstractmethod
from typing import Tuple

import pygame
from pygame.event import Event
from pygame.math import Vector2

from event_dispatcher import EventDispatcher


class DragAble:
    @abstractmethod
    def get_pos(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def move(self, direction: Vector2):
        pass


class DragAndDropHandler:
    def __init__(self, event_dispatcher: EventDispatcher):
        self._dragged_object: DragAble | None = None
        self._previous_position: Vector2 = Vector2(0, 0)
        self._has_moved: bool = False

        event_dispatcher.listen(self.move_drag, event_type=pygame.MOUSEMOTION)

    def is_dragging(self) -> bool:
        return self._dragged_object is not None

    def start_drag(self, drag_able: DragAble | None) -> bool:
        if self.is_dragging() or drag_able is None:
            return False
        self._dragged_object = drag_able
        return True

    def move_drag(self, event: Event) -> bool:
        if not self.is_dragging():
            return False
        if event.pos != self._dragged_object.get_pos():
            self._has_moved = True

        if self._previous_position != Vector2(0, 0):
            direction = self._previous_position - Vector2(event.pos)
            self._dragged_object.move(direction)
        self._previous_position = event.pos
        return True

    def stop_drag(self) -> bool:
        """
        Stop dragging process.
        :return: if the drag has moved
        """
        self._previous_position = Vector2(0, 0)
        self._dragged_object = None
        if self._has_moved:
            self._has_moved = False
            return True
        return False
