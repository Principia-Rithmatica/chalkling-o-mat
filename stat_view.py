import pygame
from pygame import Rect
from pygame.event import Event
from pygame_gui import UI_TEXT_ENTRY_CHANGED
from pygame_gui.core import UIContainer, IContainerLikeInterface
from pygame_gui.core.interfaces import IUIManagerInterface
from pygame_gui.elements import UITextEntryLine, UITextBox, UILabel

from base_form_view import BaseFormView
from consts import NUM_CHARACTERS, LOAD_FORM
from event_dispatcher import EventDispatcher


class StatView(UIContainer):
    def __init__(self, manager: IUIManagerInterface, event_dispatcher: EventDispatcher, relative_rect: pygame.Rect,
                 anchors: dict[str, str], base_from_view: BaseFormView):
        super().__init__(relative_rect, manager, anchors=anchors)
        self.base_from_view = base_from_view
        y = 10
        self.title = UITextBox("Stats", Rect(10, y, 150, 30), manager, container=self)
        y += 30
        self.attack_label = UILabel(Rect(0, y, 50, 30), "Atk:", container=self)
        self.attack = UITextEntryLine(Rect(50, y, 100, 30), manager, self, initial_text="0.5")
        self.attack.set_allowed_characters(NUM_CHARACTERS)
        y += 30
        self.defense_label = UILabel(Rect(0, y, 50, 30), "Def:", container=self)
        self.defense = UITextEntryLine(Rect(50, y, 100, 30), manager, self, initial_text="0.5")
        self.defense.set_allowed_characters(NUM_CHARACTERS)
        y += 30
        self.speed_label = UILabel(Rect(0, y, 50, 30), "Spd:", container=self)
        self.speed = UITextEntryLine(Rect(50, y, 100, 30), manager, self, initial_text="0.5")
        self.speed.set_allowed_characters(NUM_CHARACTERS)
        y += 30
        self.life_label = UILabel(Rect(0, y, 50, 30), "Life:", container=self)
        self.life = UITextEntryLine(Rect(50, y, 100, 30), manager, self, initial_text="0.5")
        self.life.set_allowed_characters(NUM_CHARACTERS)

        event_dispatcher.listen(self.on_update_stats, event_type=UI_TEXT_ENTRY_CHANGED)
        event_dispatcher.listen(self.on_load_form, event_type=LOAD_FORM)

    def on_update_stats(self, event: Event) -> bool:
        print("update stats")
        try:
            stats = self.base_from_view.get_current_form().stats
            stats.attack = float(self.attack.text)
            stats.defense = float(self.defense.text)
            stats.speed = float(self.speed.text)
            stats.life = float(self.life.text)
        except ValueError:
            pass
        except TypeError:
            pass
        return False

    def on_load_form(self, event: Event) -> bool:
        stats = event.form.stats
        self.attack.set_text(str(stats.attack))
        self.defense.set_text(str(stats.defense))
        self.speed.set_text(str(stats.speed))
        self.life.set_text(str(stats.life))
        return False
