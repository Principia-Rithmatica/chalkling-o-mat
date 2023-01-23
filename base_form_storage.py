import os
import pickle

import dill
import pygame
import pygame_gui
from pygame.event import Event
from pygame_gui.elements import UIButton

from base_form import BaseForm
from base_form_view import BaseFormView
from consts import LOAD_FORM
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
            self.base_form_view.editable = False
            self.file_picker.open("Load Base Form...", "base_forms", self.load, self.enable_edit)
            return True
        return False

    def load(self, file):
        try:
            with open(file, "rb") as f:
                current_base_form = dill.load(f)
                self.base_form_view.set_current_form(current_base_form)
                pygame.event.post(Event(LOAD_FORM, form=current_base_form))
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)
        self.enable_edit()

    def process_save(self, event: Event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            print("Show saving window")
            self.base_form_view.editable = False
            self.file_picker.open("Save Base Form...", "base_forms", self.save, self.enable_edit)
            return True
        return False

    def save(self, file):
        try:
            with open(file, "wb") as f:
                dill.dump(self.base_form_view.get_current_form(), f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)
        self.enable_edit()

    def enable_edit(self):
        self.base_form_view.editable = True

    # def list_forms(self, path):
    #     files = os.listdir(path)
    #     result = []
    #     for file in files:
    #         if file.endswith(FILE_FORMAT):
    #             form = self.load(os.path.join(path, file))
    #             result.append(form)
    #     return result
