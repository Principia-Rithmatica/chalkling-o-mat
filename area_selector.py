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
    def __init__(self, event_dispatcher: EventDispatcher, target_surface: Surface,
                 on_target_selected: Callable[[Rect], None]):
        self.enabled = False
        self.target_surface = target_surface
        self.start_point: Vector2 = Vector2(0, 0)
        self.start_drag: bool = False
        self.target_rect: Rect = Rect(0, 0, 0, 0)
        self.on_target_selected: Callable[[Rect], None] = on_target_selected

        event_dispatcher.listen(self.on_select_start, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.on_select_preview, event_type=pygame.MOUSEMOTION)
        event_dispatcher.listen(self.on_select_end, event_type=pygame.MOUSEBUTTONUP)

    def draw(self, surface: Surface):
        if self.enabled:
            pygame.draw.rect(surface, YELLOW, self.target_rect)

    def on_select_start(self, event: Event) -> bool:
        if self.target_surface.get_rect().collidepoint(event.pos) and self.enabled:
            self.start_point = Vector2(event.pos)
            self.start_drag = True
        return False

    def on_select_preview(self, event: Event) -> bool:
        if self.target_surface.get_rect().collidepoint(event.pos) and self.enabled and self.start_drag:
            p1 = Vector2(min(event.pos[0], self.start_point.x), min(event.pos[1], self.start_point.y))
            p2 = Vector2(max(event.pos[0], self.start_point.x), max(event.pos[1], self.start_point.y))
            self.target_rect = Rect(p1, p2 - p1)
        return False

    def on_select_end(self, event: Event) -> bool:
        if self.target_surface.get_rect().collidepoint(event.pos) and self.enabled and self.start_drag:
            self.start_drag = False
            self.on_target_selected(self.target_rect)
            self.target_rect = Rect(0, 0, 0, 0)
        return False
