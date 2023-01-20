import math
import random

import pygame

from consts import WHITE, YELLOW, POINT_SIZE, GREEN
from dnd_handler import DragAble
from selectable import Marks, Selectable


class Point(Selectable, DragAble):

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
        if self.is_marked(Marks.PREVIOUS):
            color = GREEN
        elif self.is_marked(Marks.SELECTED):
            color = YELLOW

        pygame.draw.circle(screen, color, self.tuple(), POINT_SIZE)

    def is_selected(self, pos: (int, int)):
        if math.dist(self.tuple(), pos) < POINT_SIZE * 2:
            return True
        return False

    def get_pos(self) -> (int, int):
        return self.current_pos

    def set_pos(self, pos: (int, int)):
        self.base_pos = pos
        self.current_pos = pos
