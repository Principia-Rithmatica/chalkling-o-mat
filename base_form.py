import json

import pygame
WHITE = (255, 255, 255)


class Line:
    def __init__(self, point_a: (int, int), point_b: (int, int)):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.point_a, 5)
        pygame.draw.circle(screen, WHITE, self.point_b, 5)
        pygame.draw.line(screen, WHITE, self.point_a, self.point_b, 2)


class BaseForm:
    def __init__(self, lines: [Line] = []):
        self.lines: [Line] = lines
        self.previous_point = (0, 0)

    def add_point(self, point: (int, int)):
        if self.previous_point != (0, 0):
            self.lines.append(Line(self.previous_point, point))
        self.previous_point = point

    def draw(self, screen):
        for line in self.lines:
            line.draw(screen)