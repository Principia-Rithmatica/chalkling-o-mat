from enum import Enum
from typing import Tuple, List

import pygame
from pygame.event import Event
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface

from area_selector import AreaSelector
from base_form import BaseForm
from consts import LEFT_MOUSE_BUTTON, RIGHT_MOUSE_BUTTON, EDIT_FORM, POINT_SIZE
from dnd_handler import DragAndDropHandler, DragAble
from event_dispatcher import EventDispatcher
from line_setting import LineSetting
from point import Point
from point_setting import PointSetting


class Modes(Enum):
    DISABLED = 0
    FROM_EDIT = 1
    BOUND_EDIT = 2


class BaseFormView(DragAndDropHandler):
    def __init__(self, event_dispatcher: EventDispatcher):
        super().__init__(event_dispatcher)
        self.form_surface = pygame.Surface((512, 512))
        self.form: BaseForm = BaseForm()
        self.mode: Modes = Modes.FROM_EDIT
        self.editable: bool = True
        self.area_selector: AreaSelector = AreaSelector(event_dispatcher, self.form_surface)

        event_dispatcher.listen(self.on_button_down, event_type=pygame.MOUSEBUTTONDOWN)
        event_dispatcher.listen(self.on_button_up, event_type=pygame.MOUSEBUTTONUP)
        event_dispatcher.listen(self.on_keyup, event_type=pygame.KEYUP)

    def draw(self, screen: Surface):
        self.form_surface.fill((30, 30, 30))
        if self.form is not None:
            self.form.draw(self.form_surface)
        self.area_selector.draw(self.form_surface)
        screen.blit(self.form_surface, (0, 0))

    def disable(self):
        self.mode = Modes.DISABLED
        self.area_selector.stop_select()
        self.area_selector.enabled = False
        self.stop_drag()

    def enable(self):
        self.mode = Modes.FROM_EDIT

    def on_button_down(self, event: Event) -> bool:
        if not self.form_surface.get_rect().collidepoint(event.pos) or self.mode == Modes.DISABLED:
            return False

        if event.button == LEFT_MOUSE_BUTTON:
            if self.mode == Modes.FROM_EDIT:
                self.click_form_edit(event)
            elif self.mode == Modes.BOUND_EDIT:
                self.click_bound_edit(event)

        # Unselect all elements
        if event.button == RIGHT_MOUSE_BUTTON:
            self.form.unselect(self.form.selection)
            return True
        return False

    def on_button_up(self, event: Event) -> bool:
        if event.button == RIGHT_MOUSE_BUTTON:
            return False

        if self.stop_drag():
            pygame.event.post(Event(EDIT_FORM))
            return True

        # Selection was done
        selected_rect = self.area_selector.stop_select()
        if selected_rect.width > 0:
            if self.mode == Modes.BOUND_EDIT:
                points = self.get_selected_points()
                points[0].set_bounds(selected_rect)
                pygame.event.post(Event(EDIT_FORM))
                return True
            elif self.mode == Modes.FROM_EDIT:
                selection = self.form.get_selected(selected_rect)
                print(f"{len(selection)} was selected")
                self.form.select(selection)
                return True
        return False

    def click_bound_edit(self, event: Event):
        self.area_selector.start_select(Vector2(event.pos))

    def click_form_edit(self, event: Event):
        touched_elements = self.get_selected_from_pos(event.pos)

        self.form.unselect(self.form.selection)

        # Start selection
        print(f"Touched Elements: {len(touched_elements)}")
        if len(touched_elements) == 0:
            self.area_selector.start_select(Vector2(event.pos))
        else:
            self.form.select(touched_elements)

        # Start DnD
        for element in touched_elements:
            if element in self.form.selection:
                drag_ables = [x for x in self.form.selection if isinstance(x, DragAble)]
                self.start_drag(drag_ables)
                break

        # Select first point as previous one
        for element in touched_elements:
            if isinstance(element, Point):
                print("Select previous point")
                self.form.set_previous_point(element)
                break

    def get_selected_from_pos(self, pos: Tuple[int, int]):
        return self.form.get_selected(
            Rect(pos[0] - POINT_SIZE, pos[1] - POINT_SIZE, POINT_SIZE*2, POINT_SIZE*2))

    def get_selected_points(self) -> List[Point]:
        return [x for x in self.form.selection if isinstance(x, Point)]

    def on_keyup(self, event: Event) -> bool:
        if self.mode == Modes.DISABLED:
            return False

        match event.key:
            case pygame.K_n:
                self.form = BaseForm()
                pygame.event.post(Event(EDIT_FORM))
                return True
            case pygame.K_p:
                selected_points = self.get_selected_points()
                if len(selected_points) == 1:
                    self.mode = Modes.BOUND_EDIT
                return True
            case pygame.K_DELETE:
                if self.form_surface.get_rect().collidepoint(pygame.mouse.get_pos()):
                    self.form.remove(self.form.selection)
                return True
            case pygame.K_a:
                self.add_point(Vector2(pygame.mouse.get_pos()))
                return True
        return False

    def join_line(self):
        pos = pygame.mouse.get_pos()
        selection = self.get_selected_from_pos(pos)
        points = [x for x in selection if isinstance(x, Point)]
        previous_point = self.form.previous_point

        # TODO Also join 2 selected points
        if len(points) == 0 or previous_point is None:
            return

        self.form.add_line(points[0], previous_point, LineSetting())  # TODO Swap line setting with real one

    def add_point(self, pos: Vector2):
        self.form.add_point(pos, PointSetting(), LineSetting())  # TODO Swap line setting with real one
        print("Add point")

    def set_current_form(self, form: BaseForm):
        print("Show new form")
        self.form = form if form is not None else BaseForm()

    def get_current_form(self) -> BaseForm:
        return self.form
