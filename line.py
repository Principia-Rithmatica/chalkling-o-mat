import random
from typing import List

import pygame
from pygame import Surface

from consts import WHITE, YELLOW, BodyPart, BodyFeature
from dnd_handler import DragAble
from point import Point
from selectable import Selectable, Marks


class Line(Selectable, DragAble):

    def __init__(self, point_a: Point, point_b: Point):
        super().__init__()
        self.point_a: Point = point_a
        self.point_b: Point = point_b
        self.width_min = 1
        self.width_max = 5
        self.width = 1
        self.bodyPart: List[BodyPart] = [BodyPart.BODY]
        self.bodyFeature: List[BodyFeature] = []

    def draw(self, screen: Surface):
        self.point_a.draw(screen)
        self.point_b.draw(screen)
        color = WHITE
        if self.is_marked(Marks.SELECTED):
            color = YELLOW

        pygame.draw.line(screen, color, self.point_a.get_pos(), self.point_b.get_pos(), self.width)

    def regenerate(self):
        self.point_a.regenerate()
        self.point_b.regenerate()
        self.width = int(random.uniform(self.width_min, self.width_max))

    def get_selected(self, pos: (float, float)):
        if self.point_a.is_selected(pos):
            return self.point_a
        if self.point_b.is_selected(pos):
            return self.point_b
        return None

    def get_pos(self) -> (float, float):
        pa = self.point_a.get_pos()
        pb = self.point_b.get_pos()
        return (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2

    def set_pos(self, pos: (float, float)):
        old_pos = self.get_pos()
        offset = (old_pos[0] - pos[0], old_pos[1] - pos[1])
        pos_a = (self.point_a[0] + offset[0], self.point_a[1] + offset[1])
        self.point_a.set_pos(pos_a)
        pos_b = (self.point_b[0] + offset[0], self.point_b[1] + offset[1])
        self.point_b.set_pos(pos_b)
