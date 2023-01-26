import os

import dill
import pygame
import pygame_gui
from pygame import KEYUP
from pygame.event import Event
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.core import UIContainer, IContainerLikeInterface
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UIButton, UITextEntryLine

from base_form_view import BaseFormView
from consts import LOAD_FORM, FILE_SUFFIX
from event_dispatcher import EventDispatcher
from file_picker import FilePicker


class BaseFormStorageView(UIContainer):
    def __init__(self, event_dispatcher: EventDispatcher, base_form_view: BaseFormView,
                 relative_rect: pygame.Rect, anchors: dict[str, str]):
        super().__init__(relative_rect, pygame_gui.ui_manager.get_default_manager(), anchors=anchors)
        self.path = "base_forms"
        self.load_button = UIButton(pygame.Rect(10, 10, 150, 30), 'Load', container=self)
        self.save_button = UIButton(pygame.Rect(10, 40, 150, 30), 'Save', container=self)
        self.file_name = UITextEntryLine(pygame.Rect(10, 70, 150, 30), container=self,
                                         initial_text=self.get_free_name())
        self.base_form_view = base_form_view
        self.file_picker = FilePicker(event_dispatcher)

        event_dispatcher.listen(self.on_load, self.load_button, UI_BUTTON_PRESSED)
        event_dispatcher.listen(self.on_save, self.save_button, UI_BUTTON_PRESSED)
        event_dispatcher.listen(self.on_key_up, event_type=KEYUP)

    def on_load(self, event: Event):
        print("Show loading window")
        self.base_form_view.disable()
        self.file_picker.open("Load Base Form...", self.path, self.load, self.enable_input)
        return True

    def load(self, file):
        try:
            with open(file, "rb") as f:
                self.set_filename(file)
                current_base_form = dill.load(f)
                self.base_form_view.set_current_form(current_base_form)
                pygame.event.post(Event(LOAD_FORM, form=current_base_form))
        except Exception as ex:
            print("Error during unpickling object (Possibly unsupported):", ex)
        self.enable_input()

    def set_filename(self, filepath):
        self.path = os.path.dirname(filepath)
        self.file_name.set_text(os.path.basename(filepath))

    def on_save(self, event: Event):
        self.save()
        return True

    def save(self):
        try:
            with open(os.path.join(self.path, self.file_name.get_text()), "wb") as f:
                dill.dump(self.base_form_view.get_current_form(), f)
        except Exception as ex:
            print("Error during pickling object (Possibly unsupported):", ex)
        self.enable_input()

    def enable_input(self):
        self.base_form_view.enable()

    def on_key_up(self, event: Event) -> bool:
        match event.key:
            case pygame.K_s:
                self.save()
                return True
        return False

    # def list_forms(self, path):
    #     files = os.listdir(path)
    #     result = []
    #     for file in files:
    #         if file.endswith(FILE_FORMAT):
    #             form = self.load(os.path.join(path, file))
    #             result.append(form)
    #     return result
    def get_free_name(self) -> str:
        files = os.listdir(self.path)
        i = 0
        def_name = "unnamed"
        current_filename = def_name + FILE_SUFFIX
        unused = False
        while not unused:
            if current_filename in files:
                i += 1
                current_filename = f'{def_name}_{i}{FILE_SUFFIX}'
            else:
                unused = True
        return current_filename
