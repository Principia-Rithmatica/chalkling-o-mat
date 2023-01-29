import copy
import math
import random
from typing import Tuple, List

import pygame
from pygame import Surface, Rect
from pygame.math import Vector2

from bezier import bezier_curve
from consts import WHITE, YELLOW
from dnd_handler import DragAble
from line_setting import LineSetting
from point import Point
from selection_handler import Selectable, Marks


def draw_bezier(surface: Surface, start_point: Point, point_a: Point, point_b: Point, end_point: Point, color):
    curve = bezier_curve([start_point.get_pos(), point_a.get_pos(), point_b.get_pos(), end_point.get_pos()])
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
        self.point_a_bezier: Point = copy.deepcopy(point_a)
        self.point_b_bezier: Point = copy.deepcopy(point_b)

        self.point_a_bezier.move(Vector2(0, 50))
        self.point_b_bezier.move(Vector2(0, 50))

        self.width = 2
        self.settings: LineSetting = settings

    def draw(self, screen: Surface):
        color = self.get_color()
        if self.settings.curve:
            draw_bezier(screen, self.point_a, self.point_a_bezier, self.point_b_bezier, self.point_b, color)
        else:
            pygame.draw.line(screen, color, self.point_a.get_pos(), self.point_b.get_pos(), int(self.width))
        if self.is_marked(Marks.SELECTED) and self.settings.curve:
            self.point_a_bezier.draw(screen)
            self.point_b_bezier.draw(screen)

    def get_color(self):
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW
        return color

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()

    def get_pos(self) -> Tuple[float, float]:
        pa = self.point_a.get_pos()
        pb = self.point_b.get_pos()
        return (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2

    def move(self, direction: Vector2):
        pos_a = self.point_a.pos - direction
        self.point_a.set_pos(pos_a)
        pos_b = self.point_b.pos - direction
        self.point_b.set_pos(pos_b)

        pos_a = self.point_a_bezier.pos - direction
        self.point_a_bezier.set_pos(pos_a)
        pos_b = self.point_b_bezier.pos - direction
        self.point_b_bezier.set_pos(pos_b)
        return [self.point_a, self.point_b, self.point_a_bezier, self.point_b_bezier]

    def is_selected(self, selection: Rect) -> bool:
        clipline = selection.clipline(self.point_a[0], self.point_a[1], self.point_b[0], self.point_b[1])
        return clipline != ()

    def distance(self, p: Point | Tuple[float, float]) -> float:
        if self.point_a is None or self.point_b is None:
            return math.inf
        x1, y1 = self.point_a
        x2, y2 = self.point_b
        x, y = p

        # check if point is within the X of the line / trust me I'm EnGiNeEr!
        if not (x1 <= p[0] <= x2 or x1 >= p[0] >= x2) and not (y1 <= p[1] <= y2 or y1 >= p[1] >= y2):
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
