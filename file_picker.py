from typing import Callable

import pygame
import pygame_gui
from pygame import MOUSEBUTTONDOWN
from pygame.event import Event
from pygame_gui import UI_FILE_DIALOG_PATH_PICKED, UI_WINDOW_CLOSE
from pygame_gui.windows import UIFileDialog

from consts import FILE_SUFFIX
from event_dispatcher import EventDispatcher


class FilePicker:
    def __init__(self, event_dispatcher: EventDispatcher):
        self.on_pick_file: Callable[[str], None] | None = None
        self.on_close: Callable[[], None] | None = None
        self.file_dialog: UIFileDialog | None = None
        self.event_dispatcher = event_dispatcher
        self.event_dispatcher.listen(self.on_file_picked, event_type=UI_FILE_DIALOG_PATH_PICKED)
        self.event_dispatcher.listen(self.on_close_window, event_type=UI_WINDOW_CLOSE)

    def open(self, window_title: str, folder: str, on_pick_file: Callable[[str], None], on_close: Callable[[], None]):
        self.on_pick_file = on_pick_file
        self.on_close = on_close
        self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                        pygame_gui.ui_manager.get_default_manager(),
                                        window_title=window_title,
                                        initial_file_path=folder,
                                        allow_picking_directories=False,
                                        allow_existing_files_only=False,
                                        allowed_suffixes={FILE_SUFFIX})

    def on_close_window(self, event: Event) -> bool:
        if hasattr(event, "ui_element") and event.ui_element != self.file_dialog:
            return False
        self.file_dialog = None
        self.on_close()
        return True

    def on_file_picked(self, event: Event) -> bool:
        if hasattr(event, "ui_element") and event.ui_element != self.file_dialog:
            return False
        self.on_pick_file(event.text)
        pygame.event.set_allowed(MOUSEBUTTONDOWN)
        return True
