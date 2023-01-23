import math
import random
from typing import Tuple, List

import pygame
from pygame import Surface
from pygame.math import Vector2

from bezier import bezier_curve
from consts import WHITE, YELLOW
from dnd_handler import DragAble
from line_setting import LineSetting
from point import Point
from selectable import Selectable, Marks


def draw_bezier(surface: Surface, start_point: Point, point: Point, end_point: Point, color):
    curve = bezier_curve([start_point.get_pos(), point.get_pos(), point.get_pos(), end_point.get_pos()])
    prev_point = None
    for curve_point in curve:
        if prev_point is not None:
            pygame.draw.line(surface, color, prev_point, curve_point)
        prev_point = curve_point


class Line(Selectable, DragAble):

    def __init__(self, point_a: Point, point_b: Point, settings: LineSetting):
        super().__init__()
        self.point_a: Point = point_a
        self.point_b: Point = point_b
        self.width = 1
        self.settings: LineSetting = settings

    def draw(self, screen: Surface):
        self.point_a.draw(screen)
        self.point_b.draw(screen)
        color = self.get_color()

        pygame.draw.line(screen, color, self.point_a.get_pos(), self.point_b.get_pos(), self.width)

    def get_color(self):
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW
        return color

    def draw_curves(self, screen: Surface, point: Point, connected_lines):
        point.draw(screen)
        if len(connected_lines) < 2:
            return []
        color = self.get_color()
        for start_line in connected_lines:
            start_point = start_line.point_b if start_line.point_a == point else start_line.point_a
            for end_line in connected_lines:
                if start_line == end_line:
                    continue
                end_point = end_line.point_b if end_line.point_a == point else end_line.point_a
                start_point.draw(screen)
                end_point.draw(screen)
                draw_bezier(screen, start_point, point, end_point, color)

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()
        self.width = float(random.uniform(self.settings.width_variance_min, self.settings.width_variance_max))

    def get_selected_point(self, pos: Tuple[float, float]) -> Point | None:
        if self.point_a.is_selected(pos):
            return self.point_a
        if self.point_b.is_selected(pos):
            return self.point_b
        return None

    def get_pos(self) -> Tuple[float, float]:
        pa = self.point_a.get_pos()
        pb = self.point_b.get_pos()
        return (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2

    def move(self, direction: Vector2):
        pos_a = self.point_a.pos - direction
        self.point_a.set_pos(pos_a)
        pos_b = self.point_b.pos - direction
        self.point_b.set_pos(pos_b)

    def distance(self, p: Point | Tuple[float, float]) -> float:
        if self.point_a is None or self.point_b is None:
            return math.inf
        x1, y1 = self.point_a
        x2, y2 = self.point_b
        x, y = p

        # check if point is within the X of the line / trust me I'm EnGiNeEr!
        if not(x1 <= p[0] <= x2 or x1 >= p[0] >= x2) and not(y1 <= p[1] <= y2 or y1 >= p[1] >= y2):
            return math.inf

        # For vertical lines
        if x2 - x1 == 0:
            return math.fabs(p[0] - x1)

        # calculate the slope and y-intercept of the line
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1

        # calculate the coefficients A, B, C of the equation of the line
        A = -m
        B = 1
        C = -b

        # calculate the distance between the point and the line
        return abs((A * x + B * y + C) / math.sqrt(A ** 2 + B ** 2))
