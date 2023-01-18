import pygame
import pygame_gui

from base_form import BaseForm
from base_form_view import BaseFormView
from file_loader import FileLoader
from base_form_storage import load_form, save_form


class Runner:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Chalkling-o-mat")
        self.window_surface = pygame.display.set_mode((800, 600))

        self.ui_manager = pygame_gui.UIManager((800, 600), 'theme/theme1.json')
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface((800, 600))
        self.background.fill((0, 0, 0))

        self.file_loader = FileLoader(self.ui_manager, self.load_file)
        self.base_form_view = BaseFormView()

        self.event_listeners = [self.file_loader]
        self.drawables = [self.base_form_view]

    def run(self):
        while self.is_running:
            time_delta = self.clock.tick(60)/1000.0
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
            for event_listener in self.event_listeners:
                event_listener.process_events(event)
            self.ui_manager.process_events(event)

    def load_file(self, file: str):
        form = load_form(file)
        if form is None:
            return
        self.base_form_view.show(form)


if __name__ == "__main__":
    app = Runner()
    app.run()
    pygame.quit()
