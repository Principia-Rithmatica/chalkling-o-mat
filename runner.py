import pygame
import pygame_gui
from pygame.event import Event
from pygame.rect import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIButton

from base_form_storage import BaseFormStorageView
from base_form_view import BaseFormView
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, TOP_RIGHT, BOTTOM_LEFT, BOTTOM_RIGHT, REGENERATE
from event_dispatcher import EventDispatcher
from line_setting import LineSettingView
from point_setting import PointSettingView
from preview_view import PreviewView
from stat_view import StatView


class Runner:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chalkling-o-mat")
        self.window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.ui_manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), 'theme/theme1.json')
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.background.fill((0, 0, 0))

        self.global_buttons = UIContainer(Rect(-180, -30 * 5, 170, 30 * 5), self.ui_manager, anchors=BOTTOM_RIGHT)
        self.event_dispatcher = EventDispatcher()
        self.point_setting_view = PointSettingView(
            self.ui_manager, self.event_dispatcher, Rect(-350, 10, 350, 340), TOP_RIGHT)
        self.line_setting_view = LineSettingView(
            self.ui_manager, self.event_dispatcher, Rect(-350, 340, 350, 340), TOP_RIGHT)
        self.base_form_view = BaseFormView(self.ui_manager, self.event_dispatcher, self.point_setting_view,
                                           self.line_setting_view)
        self.stats_view = StatView(self.ui_manager, self.event_dispatcher, Rect(10, -200, 200, 200), BOTTOM_LEFT,
                                   self.base_form_view)
        self.storage_view = BaseFormStorageView(self.ui_manager, self.event_dispatcher, self.base_form_view,
                                                self.global_buttons)
        self.drawables = [self.base_form_view]

        preview_width = 128
        preview_height = 128
        self.add_regenerate_button()
        for i in range(4):
            x = i % 2 * preview_width
            y = int(i / 2) * preview_height
            view_rect = Rect(220 + x, 522 + y, preview_width, preview_height)
            preview_view = PreviewView(view_rect, self.event_dispatcher, self.base_form_view, preview_width / 512)
            self.drawables.append(preview_view)

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.draw()
            self.ui_manager.update(time_delta)
            pygame.display.update()

    def draw(self):
        for drawable in self.drawables:
            drawable.draw(self.background)
        self.window_surface.blit(self.background, (0, 0))
        self.ui_manager.draw_ui(self.window_surface)

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.is_running = False
            self.event_dispatcher.process_event(event)
            self.ui_manager.process_events(event)

    def add_regenerate_button(self):
        regenerate = UIButton(Rect(10, 70, 150, 30), "Reload", self.ui_manager, self.global_buttons)

        def send_regenerate(event: Event) -> bool:
            pygame.event.post(Event(REGENERATE))
            return True
        self.event_dispatcher.listen(send_regenerate, regenerate, UI_BUTTON_PRESSED)


if __name__ == "__main__":
    app = Runner()
    app.run()
    pygame.quit()
