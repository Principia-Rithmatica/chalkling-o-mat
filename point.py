import math
import random

import pygame
from pygame import Rect, Vector2
from pygame.surface import Surface

from consts import WHITE, YELLOW, POINT_SIZE, GREEN, GREY
from dnd_handler import DragAble
from point_setting import PointSetting
from selectable import Marks, Selectable


class Point(Selectable, DragAble):

    def __init__(self, pos: Vector2, settings: PointSetting):
        super().__init__()
        super(Selectable, self).__init__()
        self.settings: PointSetting = settings
        self.pos = pos
        self.settings.set_base(self.pos)

    def regenerate(self):
        self.pos.update(self.settings.get_new_position())

    def draw(self, screen: Surface):
        color = WHITE
        if self.is_marked(Marks.PREVIOUS):
            color = GREEN
        elif self.is_marked(Marks.SELECTED):
            color = YELLOW

        pygame.draw.circle(screen, color, self.get_pos(), POINT_SIZE)
        if self.is_marked(Marks.SELECTED):
            self.draw_addition_info(screen)

    def draw_addition_info(self, screen: Surface):
        rect = Rect(self.settings.base_x + self.settings.pos_variance_x_min,
                    self.settings.base_y + self.settings.pos_variance_y_min,
                    -self.settings.pos_variance_x_min + self.settings.pos_variance_x_max,
                    -self.settings.pos_variance_y_min + self.settings.pos_variance_y_max)

        pygame.draw.rect(screen, GREY, rect, 2)

    def is_selected(self, pos: (float, float)):
        if math.dist(self.get_pos(), pos) < POINT_SIZE * 2:
            return True
        return False

    def get_pos(self) -> (float, float):
        return self.pos.xy

    def set_pos(self, pos: (float, float)):
        self.pos.update(pos)
        self.settings.set_base(self.pos)