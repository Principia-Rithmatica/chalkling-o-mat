from typing import Callable

import pygame
import pygame_gui
from pygame import MOUSEBUTTONDOWN
from pygame_gui.windows import UIFileDialog

from event_dispatcher import EventDispatcher


class FilePicker:
    def __init__(self, ui_manager, event_dispatcher: EventDispatcher):
        self.on_pick_file: Callable[[str], None] | None = None
        self.on_close: Callable[[], None] | None = None
        self.file_dialog: UIFileDialog | None = None
        self.ui_manager = ui_manager
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.listen(self.process_events)

    def open(self, window_title: str, folder: str, on_pick_file: Callable[[str], None], on_close: Callable[[], None]):
        self.on_pick_file = on_pick_file
        self.on_close = on_close
        self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                        self.ui_manager,
                                        window_title=window_title,
                                        initial_file_path=folder,
                                        allow_picking_directories=False,
                                        allow_existing_files_only=False,
                                        allowed_suffixes={".pickle"})

    def process_events(self, event):
        if hasattr(event, "ui_element") and event.ui_element != self.file_dialog:
            return False

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            self.on_pick_file(event.text)
            pygame.event.set_allowed(MOUSEBUTTONDOWN)
            return True
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            self.file_dialog = None
            self.on_close()
            return True
        return False
