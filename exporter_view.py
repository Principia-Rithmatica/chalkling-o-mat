import copy
import os

import numpy as np
import pyexiv2
import pygame
import pygame_gui
from pyexiv2 import Image
from pygame import Surface
from pygame.event import Event
from pygame.rect import Rect
from pygame_gui import UI_BUTTON_PRESSED
from pygame_gui.core import UIContainer
from pygame_gui.elements import UIButton, UITextEntryLine

from base_form import BaseForm, Stats
from base_form_storage import BaseFormStorageView
from base_form_view import BaseFormView
from consts import REGENERATE
from event_dispatcher import EventDispatcher
from preview_view import PreviewView


def get_latest_file(folder):
    files = os.listdir(folder)
    highest_number = 0
    for file in files:
        name, extension = os.path.splitext(file)
        try:
            number = int(name)
            if number > highest_number:
                highest_number = number
        except ValueError:
            pass
    return highest_number


def save_meta(file_path: str, stats: Stats):
    xmp_stats = {'Xmp.dc.' + key: value for key, value in vars(stats).items()}

    image = Image(file_path)
    image.modify_xmp(xmp_stats)
    image.close()


class ExporterView(UIContainer):
    def __init__(self, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect, anchor: dict[str, str],
                 base_form_view: BaseFormView, storage_view: BaseFormStorageView):
        super().__init__(relative_rect, pygame_gui.ui_manager.get_default_manager(), anchors=anchor)
        self.export_button = UIButton(Rect(10, 10, 160, 30), "Export", container=self)
        self.copies = UITextEntryLine(Rect(10, 40, 160, 30), initial_text="10", container=self)
        self.copies.set_allowed_characters(list("0123456798"))

        export_size = Rect(0, 0, 128, 128)
        self.export_surface = Surface(export_size.size)
        self.render: PreviewView = PreviewView(export_size, event_dispatcher, base_form_view)
        self.storage_view = storage_view
        self.base_form_view = base_form_view

        event_dispatcher.listen(self.on_export, element=self.export_button, event_type=UI_BUTTON_PRESSED)

    def on_export(self, event: Event) -> bool:
        try:
            print("export started..")
            folder = self.storage_view.get_name()
            save_folder = os.path.join("data", folder)
            if not os.path.exists(save_folder):
                os.mkdir(save_folder)
            starts_with = get_latest_file(save_folder)

            copies = int(self.copies.text)

            for copy_index in range(copies):
                self.render.regenerate(Event(REGENERATE))
                self.render.draw(self.export_surface)
                stats = self.calculate_similarity(self.base_form_view.form, self.render.current_form)
                file_path = os.path.join("data", folder, f"{starts_with + copy_index}.png")
                pygame.image.save(self.export_surface, file_path)
                save_meta(file_path, stats)
            print(f"{copies} copies exported")
        except TypeError:
            pass
        except ValueError:
            pass
        print("..export done")
        return True

    def calculate_similarity(self, original: BaseForm, variant: BaseForm) -> Stats:
        original_points = original.to_numpy()
        variant_points = variant.to_numpy()
        deviation = np.mean(1 - cosine_similarity(original_points, variant_points))
        stats = copy.deepcopy(original.stats)
        stats.scale(deviation)
        stats.aesthetic = deviation
        return stats


def cosine_similarity(a, b) -> float:
    return np.dot(a, b.T)/(np.linalg.norm(a)*np.linalg.norm(b))
