import math
import random
from enum import Enum

import pygame
from pygame import Surface

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
POINT_SIZE = 5


class BodyParts(Enum):
    LEG = 1
    ARM = 2
    HAND = 4
    BODY = 8
    TAIL = 16
    WING = 32


class BodyFeatures(Enum):
    ARMORED = 1
    WEAPONIZED = 2
    SPIKEY = 4
    HEALTHY = 8


class Marks(Enum):
    UNMARKED = 0
    SELECTED = 1


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


class Point(Selectable):
    def __init__(self, pos: (int, int)):
        super().__init__()
        self.current_pos: (int, int) = pos
        self.base_pos: (int, int) = pos
        self.x_bounds: (int, int) = (0, 0)
        self.y_bounds: (int, int) = (0, 0)

    def regenerate(self):
        new_x = int(self.base_pos[0] + random.uniform(self.x_bounds[0], self.x_bounds[1]))
        new_y = int(self.base_pos[1] + random.uniform(self.y_bounds[0], self.y_bounds[1]))
        self.current_pos = (new_x, new_y)

    def __getitem__(self, idx):
        return self.current_pos[idx]

    def tuple(self):
        return self.current_pos

    def draw(self, screen):
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW
        pygame.draw.circle(screen, color, self.tuple(), POINT_SIZE)

    def is_selected(self, pos: (int, int)):
        if math.dist(self.tuple(), pos) < POINT_SIZE * 2:
            return True
        return False


class Line(Selectable):
    def __init__(self, point_a: Point, point_b: Point):
        super().__init__()
        self.point_a: Point = point_a
        self.point_b: Point = point_b
        self.width_min = 1
        self.width_max = 5
        self.width = 1
        self.regenerate()

    def draw(self, screen: Surface):
        self.point_a.draw(screen)
        self.point_b.draw(screen)
        pygame.draw.line(screen, WHITE, self.point_a.tuple(), self.point_b.tuple(), self.width)

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()
        self.width = int(random.uniform(self.width_min, self.width_max))

    def select(self, pos: (int, int)):
        if self.point_a.is_selected(pos):
            return self.point_a
        if self.point_b.is_selected(pos):
            return self.point_b
        return None


class BaseForm:
    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.lines: [Line] = lines
        self.previous_point: Point = Point((0, 0))

    def draw(self, screen: Surface):
        for line in self.lines:
            line.draw(screen)

    def select(self, pos: (int, int)):
        for line in self.lines:
            point = line.select(pos)
            if point is None:
                continue
            self.set_previous_point(point)
            return point
        return None

    def add_point(self, pos: (int, int)):
        point = Point(pos)
        if self.previous_point.tuple() != (0, 0):
            self.lines.append(Line(self.previous_point, point))
        self.set_previous_point(point)

    def set_previous_point(self, point: Point):
        self.previous_point.unmark(Marks.SELECTED)
        self.previous_point = point
        point.mark(Marks.SELECTED)

    def remove_point(self, pos):
        to_remove = []
        for line in self.lines:
            if math.dist(line.point_a.tuple(), pos) < POINT_SIZE * 2 or math.dist(line.point_b.tuple(), pos) < POINT_SIZE * 2:
                to_remove.append(line)

        for line in to_remove:
            self.lines.remove(line)

    def regenerate(self):
        for line in self.lines:
            line.regenerate()
