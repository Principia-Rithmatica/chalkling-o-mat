import os
import pickle

import pygame
import pygame_gui
from pygame.event import Event
from pygame_gui.elements import UIButton

from base_form import BaseForm
from base_form_view import BaseFormView
from event_dispatcher import EventDispatcher
from file_picker import FilePicker

FILE_FORMAT = ".pickle"
BOTTOM_RIGHT = {'left': 'right',
                'right': 'right',
                'top': 'bottom',
                'bottom': 'bottom'}


class BaseFormStorageView:
    def __init__(self, ui_manager, event_dispatcher: EventDispatcher, base_form_view: BaseFormView):
        self.load_button = UIButton(
            relative_rect=pygame.Rect(-180, -60, 150, 30),
            text='Load',
            manager=ui_manager,
            anchors=BOTTOM_RIGHT)
        self.save_button = UIButton(
            relative_rect=pygame.Rect(-180, -90, 150, 30),
            text='Save',
            manager=ui_manager,
            anchors=BOTTOM_RIGHT)
        self.base_form_view = base_form_view
        self.file_picker = FilePicker(ui_manager, event_dispatcher)
        event_dispatcher.listen(self.process_load, self.load_button)
        event_dispatcher.listen(self.process_save, self.save_button)

    def process_load(self, event: Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("Show loading window")
            self.file_picker.open("Load Base Form...", "base_forms",
                                  lambda file: self.base_form_view.show(load_form(file)))
            return True
        return False

    def process_save(self, event: Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("Show saving window")
            self.file_picker.open("Save Base Form...", "base_forms",
                                  lambda file: save_form(self.base_form_view.current_base_form, file))
            return True
        return False

def save_form(form: BaseForm, file: str):
    try:
        with open(file, "wb") as f:
            pickle.dump(form, f)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)


def load_form(file: str):
    try:
        with open(file, "rb") as f:
            return pickle.load(f)
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)


def list_forms(path):
    files = os.listdir(path)
    result = []
    for file in files:
        if file.endswith(FILE_FORMAT):
            form = load_form(os.path.join(path, file))
            result.append(form)
    return result
