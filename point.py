import math
import random
from typing import Tuple, List

import pygame
from pygame import Rect, Vector2
from pygame.surface import Surface

from consts import WHITE, YELLOW, POINT_SIZE, GREEN, GREY
from dnd_handler import DragAble
from point_setting import PointSetting
from selection_handler import Selectable, Marks


class Point(Selectable, DragAble):

    def __init__(self, pos: Vector2, settings: PointSetting):
        super().__init__()
        super(Selectable, self).__init__()
        self.settings: PointSetting = settings
        self.pos: Vector2 = pos
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

    def is_selected(self, selection: Rect) -> bool:
        collision_area = Rect(self.pos[0] - POINT_SIZE/2, self.pos[1] - POINT_SIZE/2, POINT_SIZE, POINT_SIZE)
        return selection.colliderect(collision_area)

    def get_pos(self) -> Tuple[float, float]:
        return self.pos.xy[0], self.pos.xy[1]

    def set_pos(self, pos: Tuple[float, float] | Vector2):
        self.pos.update(pos)
        self.settings.set_base(self.get_pos())

    def move(self, direction: Vector2, already_moved: List[any]):
        if self not in already_moved:
            self.set_pos(self.pos - direction)
            already_moved.append(self)

    def __getitem__(self, item):
        return self.pos[item]

    def scale(self, factor: float):
        self.set_pos(self.pos * factor)

    def set_bounds(self, bounds: Rect):
        self.set_pos(bounds.center)
        self.settings.set_bounds(bounds)

