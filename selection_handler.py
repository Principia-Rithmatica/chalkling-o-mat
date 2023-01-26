from abc import abstractmethod
from enum import Enum
from typing import List

from pygame import Rect


class Marks(Enum):
    UNMARKED = 0
    SELECTED = 1
    PREVIOUS = 2


class Selectable:

    def __init__(self):
        self.marking: [Marks] = []

    def mark(self, mark: Marks):
        self.marking.append(mark)

    def unmark(self, mark: Marks):
        if self.is_marked(mark):
            self.marking.remove(mark)

    def is_marked(self, mark: Marks):
        return mark in self.marking

    @abstractmethod
    def is_selected(self, selection: Rect) -> bool:
        """
        Checks if the item got selected with the given rect.
        :param selection: that should be checked
        :return: true if got selected
        """
        pass


class SelectionHandler:
    def __init__(self):
        # List of all possible selectables that can be selected with this handler
        self._selectables: List[Selectable] = []
        # Current selected selectables
        self.selection: List[Selectable] = []

    def add_selectables(self, selectables: List[Selectable]):
        """
        Add new selectables to this handler
        :param selectables: that are possible to select
        """
        self._selectables.extend(selectables)

    def remove_selectables(self, selectables: List[Selectable]):
        """
        Remove selectables from this handler.
        :param selectables: to remove
        """
        for selectable in selectables:
            self._selectables.remove(selectable)
            self.selection.remove(selectable)

    def get_selected(self, selection: Rect) -> List[Selectable]:
        """
        Get the selection of this handlers list that are inside the rect.
        :param selection: to get the selectables from
        :return: selection
        """
        selected_elements = []
        for selectable in self._selectables:
            if selectable.is_selected(selection):
                selected_elements.append(selectable)
        return selected_elements

    def select(self, selectables: List[Selectable]):
        """
        Mark the selectables as selected.
        :param selectables: to mark
        """
        for selectable in selectables:
            selectable.mark(Marks.SELECTED)
        self.selection.extend(selectables)

    def unselect(self, selectables: List[Selectable]):
        """
        Remove the mark from the selectables.
        :param selectables: to unmark
        """
        for selectable in selectables:
            selectable.unmark(Marks.SELECTED)
        for selectable in selectables:
            self.selection.remove(selectable)
