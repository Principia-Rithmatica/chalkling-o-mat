import json
import math

import pygame
from pygame import Surface

WHITE = (255, 255, 255)
POINT_SIZE = 5


class Line:
    def __init__(self, point_a: (int, int), point_b: (int, int)):
        self.point_a: (int, int) = point_a
        self.point_b: (int, int) = point_b

    def draw(self, screen: Surface):
        pygame.draw.circle(screen, WHITE, self.point_a, POINT_SIZE)
        pygame.draw.circle(screen, WHITE, self.point_b, POINT_SIZE)
        pygame.draw.line(screen, WHITE, self.point_a, self.point_b, 2)


class BaseForm:
    def __init__(self, lines: [Line] = []):
        self.lines: [Line] = lines
        self.previous_point = (0, 0)

    def draw(self, screen: Surface):
        for line in self.lines:
            line.draw(screen)

    def select(self, pos: (int, int)):
        for line in self.lines:
            if math.dist(line.point_a, pos) < POINT_SIZE*2:
                self.previous_point = line.point_a
                return line
            if math.dist(line.point_b, pos) < POINT_SIZE*2:
                self.previous_point = line.point_b
                return line
        return None

    def add_point(self, point: (int, int)):
        if self.previous_point != (0, 0):
            self.lines.append(Line(self.previous_point, point))
        self.previous_point = point

    def remove_point(self, pos):
        for line in self.lines:
            if math.dist(line.point_a, pos) < POINT_SIZE*2 or math.dist(line.point_b, pos) < POINT_SIZE*2:
                self.lines.remove(line)
