import math
from typing import List, Tuple

import pygame
from pygame import Surface, Vector2
from pygame.event import Event

from consts import POINT_SIZE, EDIT_FORM
from line import Line
from line_setting import LineSetting
from point import Point
from point_setting import PointSetting
from selectable import Marks


class Stats:
    def __init__(self):
        self.attack: float = 0.5
        self.defense: float = 0.5
        self.speed: float = 0.5
        self.life: float = 0.5
        self.aesthetic: float = 0.5


class BaseForm:
    def __init__(self, lines=None):
        super().__init__()
        if lines is None:
            lines = []
        self.lines: List[Line] = lines
        self.point_line_map: dict[Point, List[Line]] = dict()
        self.previous_point: Point | None = None
        self.selected_line: Line | None = None
        self.selected_point: Point | None = None
        self.stats = Stats()

    def draw(self, screen: Surface):
        for line in self.lines:
            if line.point_a.settings.curve:
                connected_lines = self.point_line_map[line.point_a]
                line.draw_curves(screen, line.point_a, connected_lines)
            elif line.point_b.settings.curve:
                connected_lines = self.point_line_map[line.point_b]
                line.draw_curves(screen, line.point_b, connected_lines)
            else:
                line.draw(screen)

    def render(self, screen: Surface):
        for line in self.lines:
            if line.point_a.settings.curve:
                connected_lines = self.point_line_map[line.point_a]
                line.draw_curves(screen, line.point_a, connected_lines, draw_points=False)
            elif line.point_b.settings.curve:
                connected_lines = self.point_line_map[line.point_b]
                line.draw_curves(screen, line.point_b, connected_lines, draw_points=False)
            else:
                line.draw(screen, draw_points=False)

    def get_selected(self, pos: Tuple[float, float]) -> Tuple[Line | None, Point | None]:
        for line in self.lines:
            selected_line = None

            if line.distance(pos) < POINT_SIZE:
                selected_line = line

            selected_point = line.get_selected_point(pos)

            if selected_point is not None or selected_line is not None:
                return selected_line, selected_point
        return None, None

    def select(self, line: (Line | None), point: (Point | None)):
        self.set_selected_line(line)
        self.set_selected_point(point)

    def add_point(self, pos: Tuple[float, float], point_setting: PointSetting, line_setting: LineSetting)\
            -> (Point, Line | None):
        point = Point(Vector2(pos), point_setting)
        line = None
        if self.previous_point is not None:
            line = self.add_line(self.previous_point, point, line_setting)

        self.set_previous_point(point)
        pygame.event.post(Event(EDIT_FORM))
        return point, line

    def add_line(self, point_a: Point, point_b: Point, line_setting: LineSetting) -> Line:
        line = Line(point_a, point_b, line_setting)
        self.lines.append(line)

        self.point_line_map.setdefault(point_a, [])
        self.point_line_map.setdefault(point_b, [])
        self.point_line_map[point_a].append(line)
        self.point_line_map[point_b].append(line)
        pygame.event.post(Event(EDIT_FORM))
        return line

    def remove_point(self, pos):
        to_remove = []
        for line in self.lines:
            if math.dist(line.point_a.get_pos(), pos) < POINT_SIZE * 2 or \
                    math.dist(line.point_b.get_pos(), pos) < POINT_SIZE * 2:
                to_remove.append(line)

        for line in to_remove:
            self.lines.remove(line)
            self.point_line_map[line.point_a].remove(line)
            self.point_line_map[line.point_b].remove(line)
        pygame.event.post(Event(EDIT_FORM))

    def regenerate(self):
        for line in self.lines:
            line.regenerate()

    def scale(self, factor: float):
        for point in self.point_line_map.keys():
            point.scale(factor)

    def set_selected_line(self, line: Line | None):
        if self.selected_line is not None:
            self.selected_line.unmark(Marks.SELECTED)

        self.selected_line = line

        if line is not None:
            line.mark(Marks.SELECTED)

    def set_selected_point(self, point: Point | None):
        if self.selected_point is not None:
            self.selected_point.unmark(Marks.SELECTED)

        self.selected_point = point

        if point is not None:
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

    def __setstate__(self, state):
        self.__dict__.update(state)
        # Handle old not migrated data
        if 'state' not in state:
            self.stats = Stats()

