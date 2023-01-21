import math
from typing import List

from pygame import Surface, Vector2

from consts import POINT_SIZE
from line import Line
from point import Point
from point_setting import PointSetting
from selectable import Marks


class BaseForm:
    def __init__(self, lines=None):
        super().__init__()
        if lines is None:
            lines = []
        self.lines: List[Line] = lines
        self.previous_point: Point | None = None
        self.selected_line: Line | None = None
        self.selected_point: Point | None = None

    def draw(self, screen: Surface):
        for line in self.lines:
            line.draw(screen)

    def get_selected(self, pos: (float, float)):
        for line in self.lines:
            # TODO Select Line
            point = line.get_selected(pos)
            if point is None:
                continue
            return line, point
        return None, None

    def select(self, pos: (float, float)) -> Point | None:
        line, point = self.get_selected(pos)
        if point is None:
            return None

        self.set_selected_line(line)
        self.set_selected_point(point)
        self.set_previous_point(point)
        return point

    def add_point(self, pos: (float, float), settings: PointSetting):
        point = Point(Vector2(pos), settings)
        if self.previous_point is not None:
            self.lines.append(Line(self.previous_point, point))
        self.set_previous_point(point)

    def remove_point(self, pos):
        to_remove = []
        for line in self.lines:
            if math.dist(line.point_a.get_pos(), pos) < POINT_SIZE * 2 or \
               math.dist(line.point_b.get_pos(), pos) < POINT_SIZE * 2:
                to_remove.append(line)

        for line in to_remove:
            self.lines.remove(line)

    def regenerate(self):
        for line in self.lines:
            line.regenerate()

    def set_selected_line(self, line: Line):
        if self.selected_line is not None:
            self.selected_line.unmark(Marks.SELECTED)
        self.selected_line = line
        line.mark(Marks.SELECTED)

    def set_selected_point(self, point: Point):
        if self.selected_point is not None:
            self.selected_point.unmark(Marks.SELECTED)
        self.selected_point = point
        point.mark(Marks.SELECTED)

    def set_previous_point(self, point: Point | None):
        if self.previous_point is not None:
            self.previous_point.unmark(Marks.PREVIOUS)
        if self.previous_point == point:
            self.previous_point = None
        else:
            self.previous_point = point
            if point is not None:
                point.mark(Marks.PREVIOUS)
