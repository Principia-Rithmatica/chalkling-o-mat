from typing import Callable

import pygame
import pygame_gui
from pygame_gui.elements import UIButton
from pygame_gui.windows import UIFileDialog


class FileLoader:
    def __init__(self, ui_manager, on_pick_file: Callable[[str], None]):
        self.load_button = UIButton(
            relative_rect=pygame.Rect(-180, -60, 150, 30),
            text='Load Form',
            manager=ui_manager,
            anchors={'left': 'right',
                     'right': 'right',
                     'top': 'bottom',
                     'bottom': 'bottom'})
        self.on_pick_file = on_pick_file
        self.file_dialog = None
        self.ui_manager = ui_manager

    def process_events(self, event):
        if (event.type == pygame_gui.UI_BUTTON_PRESSED and
                event.ui_element == self.load_button):
            self.file_dialog = UIFileDialog(pygame.Rect(160, 50, 440, 500),
                                            self.ui_manager,
                                            window_title='Load Base Form...',
                                            initial_file_path='base_forms/',
                                            allow_picking_directories=False,
                                            allow_existing_files_only=True,
                                            allowed_suffixes={".pickle"})
            self.load_button.disable()

        if hasattr(event, "ui_element") and event.ui_element != self.file_dialog:
            return

        if event.type == pygame_gui.UI_FILE_DIALOG_PATH_PICKED:
            self.on_pick_file(event.text)
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            self.file_dialog = None
            self.load_button.enable()
