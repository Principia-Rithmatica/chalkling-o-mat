from abc import abstractmethod
from typing import Tuple, List, Type

import pygame
from pygame.event import Event
from pygame.math import Vector2

from event_dispatcher import EventDispatcher


class DragAble:
    @abstractmethod
    def move(self, direction: Vector2, already_moved: List[any]):
        """
        Moves the drag able for the given amount in the direction.
        :param already_moved: elements that got moved already to prevent to move parts of a whole twice
        :param direction: to move it
        :return: a list of drag ables that got moved in case of groups and lines that things don't get moved twice.
        """
        pass


class DragAndDropHandler:
    def __init__(self, event_dispatcher: EventDispatcher):
        self._dragged_objects: List[DragAble] = []
        self._previous_position: Vector2 = Vector2(0, 0)
        self._start_pos: Vector2 = Vector2(0, 0)
        self._has_moved: bool = False

        event_dispatcher.listen(self.on_move_drag, event_type=pygame.MOUSEMOTION)

    def is_dragging(self) -> bool:
        return len(self._dragged_objects) != 0

    def start_drag(self, drag_ables: List[DragAble]) -> bool:
        """
        Starts dragging if possible.
        :param drag_ables: to drag around
        :return: true if starting worked false when already dragging stuff
        """
        if self.is_dragging() or len(drag_ables) == 0:
            return False
        print(f"+ start dragging with {len(drag_ables)} objects")
        self._previous_position = pygame.mouse.get_pos()
        self._start_pos = pygame.mouse.get_pos()
        self._dragged_objects = drag_ables
        return True

    def on_move_drag(self, event: Event) -> bool:
        """
        Moves all dragged objects to the difference of the last mouse position.
        :param event: with current info
        :return: true if the event was handled / false otherwise
        """
        if not self.is_dragging():
            return False
        if event.pos != self._start_pos:
            self._has_moved = True

        direction = self._previous_position - Vector2(event.pos)
        already_moved_objects = []
        for dragged_object in self._dragged_objects:
            if dragged_object not in already_moved_objects:
                dragged_object.move(direction, already_moved_objects)
        self._previous_position = event.pos
        return True

    def stop_drag(self) -> bool:
        """
        Stop dragging process.
        :return: if the drag has moved
        """
        self._start_pos = Vector2(0, 0)
        self._previous_position = Vector2(0, 0)
        dragged_object_count = len(self._dragged_objects)
        self._dragged_objects = []
        if self._has_moved:
            self._has_moved = False
            print(f"+ stop dragging release {dragged_object_count} objects")
            return True
        return False
