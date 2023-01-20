import random

import pygame
from pygame import Surface

from consts import WHITE, YELLOW
from point import Point
from selectable import Selectable, Marks


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
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW

        pygame.draw.line(screen, color, self.point_a.tuple(), self.point_b.tuple(), self.width)

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()
        self.width = int(random.uniform(self.width_min, self.width_max))

    def get_selected(self, pos: (int, int)):
        if self.point_a.is_selected(pos):
            return self.point_a
        if self.point_b.is_selected(pos):
            return self.point_b
        return None
