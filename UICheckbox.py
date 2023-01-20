import pygame
from pygame_gui.elements import UIButton


class UICheckbox(UIButton):
    def __init__(self, relative_rect: pygame.Rect, text: str, data: any, **attr):
        self.checked: bool = False
        self.original_text = text
        self.data: any = data
        super().__init__(relative_rect, text, **attr)
        self.set_checked(self.checked)

    def set_checked(self, checked: bool):
        self.checked = checked
        new_text = f' [x] {self.original_text}' if self.checked else f' [ ] {self.original_text}'
        self.set_text(new_text)

    def update(self, time_delta: float):
        super().update(time_delta)
        if self.check_pressed():
            self.set_checked(not self.checked)

    def is_checked(self) -> bool:
        return self.checked


