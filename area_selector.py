from typing import Callable

import pygame
from pygame import math
from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from consts import YELLOW
from event_dispatcher import EventDispatcher


class AreaSelector:
    def __init__(self, event_dispatcher: EventDispatcher, target_surface: Surface):
        self.target_surface = target_surface
        self.start_point: Vector2 = Vector2(0, 0)
        self.start_drag: bool = False
        self.target_rect: Rect = Rect(0, 0, 0, 0)
        self._has_moved = False

        event_dispatcher.listen(self.on_select_preview, event_type=pygame.MOUSEMOTION)

    def draw(self, surface: Surface):
        if self.start_drag:
            selection_surface = pygame.Surface(self.target_rect.size)
            selection_surface.fill(YELLOW)
            selection_surface.set_alpha(64)
            surface.blit(selection_surface, self.target_rect.topleft)

    def start_select(self, pos: Vector2):
        if self.target_surface.get_rect().collidepoint(pos.x, pos.y):
            self.start_point = pos
            self.start_drag = True
            print("Start selection")

    def on_select_preview(self, event: Event) -> bool:
        if self.target_surface.get_rect().collidepoint(event.pos) and self.start_drag:
            p1 = Vector2(min(event.pos[0], self.start_point.x), min(event.pos[1], self.start_point.y))
            p2 = Vector2(max(event.pos[0], self.start_point.x), max(event.pos[1], self.start_point.y))
            self.target_rect = Rect(p1, p2 - p1)
        return False

    def stop_select(self) -> Rect:
        target_rect = self.target_rect
        self.start_drag = False
        self.target_rect = Rect(0, 0, 0, 0)
        print("Stop selection")
        return target_rect
