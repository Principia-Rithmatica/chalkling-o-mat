import math
from typing import List, Tuple

import numpy as np
import pygame
from pygame import Surface, Vector2
from pygame.event import Event

from consts import EDIT_FORM
from line import Line, LineSetting
from point import Point, PointSetting
from selection_handler import SelectionHandler, Selectable, Marks


class Stats:
    def __init__(self):
        self.attack: float = 0.5
        self.defense: float = 0.5
        self.speed: float = 0.5
        self.life: float = 0.5
        self.aesthetic: float = 0.5

    def scale(self, factor):
        self.attack *= factor
        self.defense *= factor
        self.speed *= factor
        self.life *= factor
        self.aesthetic *= factor


class BaseForm(SelectionHandler):
    def __init__(self, lines=None):
        super().__init__()
        self.lines: List[Line] = lines if lines is not None else []
        self.points: List[Point] = []
        self.previous_point: Point | None = None
        self.stats = Stats()

    def draw(self, screen: Surface):
        for line in self.lines:
            line.draw(screen)
        for point in self.points:
            point.draw(screen)

    def render(self, screen: Surface):
        for line in self.lines:
            line.render(screen)

    def add_point(self, pos: Vector2, point_setting: PointSetting, line_setting: LineSetting) -> (Point, Line | None):
        point = Point(pos, point_setting)
        line = None
        if self.previous_point is not None:
            line = self.add_line(self.previous_point, point, line_setting)

        self.set_previous_point(point)
        self.points.append(point)
        self.add_selectables([point])
        pygame.event.post(Event(EDIT_FORM))
        return point, line

    def add_line(self, point_a: Point, point_b: Point, line_setting: LineSetting) -> Line:
        line = Line(point_a, point_b, line_setting)
        self.lines.append(line)
        self.add_selectables([line, line.point_a_bezier, line.point_b_bezier])
        pygame.event.post(Event(EDIT_FORM))
        return line

    def remove(self, selectables: List[Selectable]):
        selectables = [selectable for selectable in selectables if not selectable.is_marked(Marks.BEZIER)]
        for selectable in selectables:
            if isinstance(selectable, Point):
                self.points.remove(selectable)
            if isinstance(selectable, Line):
                self.lines.remove(selectable)
                self.remove_selectables([selectable.point_a_bezier, selectable.point_b_bezier])
        self.remove_selectables(selectables)
        pygame.event.post(Event(EDIT_FORM))

    def regenerate(self):
        for line in self.lines:
            line.regenerate()

    def scale(self, factor: float):
        for point in self.points:
            point.scale(factor)
        for line in self.lines:
            line.scale(factor)

    def set_previous_point(self, point: Point | None):
        if point.is_marked(Marks.BEZIER):
            return

        if self.previous_point is not None:
            self.previous_point.unmark(Marks.PREVIOUS)
        if self.previous_point == point:
            self.previous_point = None
        else:
            self.previous_point = point
            if point is not None:
                point.mark(Marks.PREVIOUS)

    def to_numpy(self):
        return np.array([p.get_pos() for p in self.points])
