from enum import Enum


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