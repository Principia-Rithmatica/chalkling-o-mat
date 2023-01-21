import random

from pygame import Rect
from pygame.event import Event
from pygame_gui import UIManager, UI_TEXT_ENTRY_FINISHED, UI_TEXT_ENTRY_CHANGED
from pygame_gui.elements import UIWindow, UILabel, UITextEntryLine

from event_dispatcher import EventDispatcher


class PointSetting:

    def __init__(self, pos_variance_x_min: float = 0, pos_variance_x_max: float = 0, pos_variance_y_min: float = 0,
                 pos_variance_y_max: float = 0, angle_min: float = 0, angle_max: float = 0):
        self.base_x: float = 0
        self.base_y: float = 0
        self.pos_variance_x_min: float = pos_variance_x_min
        self.pos_variance_x_max: float = pos_variance_x_max
        self.pos_variance_y_min: float = pos_variance_y_min
        self.pos_variance_y_max: float = pos_variance_y_max
        self.angle_min: float = angle_min
        self.angle_max: float = angle_max

    def set_base(self, pos: (float, float)):
        self.base_x, self.base_y = pos

    def get_new_position(self) -> (float, float):
        new_x = self.base_x + random.uniform(self.pos_variance_x_min, self.pos_variance_x_max)
        new_y = self.base_y + random.uniform(self.pos_variance_y_min, self.pos_variance_y_max)
        # TODO Implement angle
        return new_x, new_y


class PointSettingView:
    def __init__(self, ui_manager: UIManager, event_dispatcher: EventDispatcher):
        self.ui_manager: UIManager = ui_manager
        self.event_dispatcher: EventDispatcher = event_dispatcher
        self.selected_setting: PointSetting | None = None
        self.window: UIWindow = UIWindow(Rect(512, 0, 350, 300), ui_manager, "Pofloat Setting", draggable=False)

        allowed_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '-']
        self.title_pos_variance = UILabel(Rect(10, 10, 310, 30), "Pos Variance X", ui_manager, container=self.window)
        self.pos_variance_x_min = UITextEntryLine(relative_rect=Rect(10, 40, 150, 30), manager=ui_manager,
                                                  container=self.window, initial_text="-10")
        self.pos_variance_x_min.set_allowed_characters(allowed_characters)
        self.pos_variance_x_max = UITextEntryLine(relative_rect=Rect(160, 40, 150, 30), manager=ui_manager,
                                                  container=self.window, initial_text="10")
        self.pos_variance_x_max.set_allowed_characters(allowed_characters)

        self.title_pos_variance = UILabel(Rect(10, 70, 310, 30), "Pos Variance Y", ui_manager, container=self.window)
        self.pos_variance_y_min = UITextEntryLine(relative_rect=Rect(10, 100, 150, 30), manager=ui_manager,
                                                  container=self.window, initial_text="-10")
        self.pos_variance_y_min.set_allowed_characters(allowed_characters)
        self.pos_variance_y_max = UITextEntryLine(relative_rect=Rect(160, 100, 150, 30), manager=ui_manager,
                                                  container=self.window, initial_text="10")
        self.pos_variance_y_max.set_allowed_characters(allowed_characters)

        self.title_angle = UILabel(Rect(10, 130, 310, 30), "Angle", ui_manager, container=self.window)
        self.angle_min = UITextEntryLine(relative_rect=Rect(10, 160, 150, 30), manager=ui_manager,
                                         container=self.window, initial_text="0")
        self.angle_min.set_allowed_characters(allowed_characters)
        self.angle_max = UITextEntryLine(relative_rect=Rect(160, 160, 150, 30), manager=ui_manager,
                                         container=self.window, initial_text="0")
        self.angle_max.set_allowed_characters(allowed_characters)

        event_dispatcher.listen(self.on_change_data, event_type=UI_TEXT_ENTRY_CHANGED)

    def get_point_settings(self) -> PointSetting:
        setting = PointSetting()
        self.fill_setting(setting)
        return setting

    def fill_setting(self, setting: PointSetting):
        try:
            setting.pos_variance_x_min = float(self.pos_variance_x_min.text)
            setting.pos_variance_x_max = float(self.pos_variance_x_max.text)
            setting.pos_variance_y_min = float(self.pos_variance_y_min.text)
            setting.pos_variance_y_max = float(self.pos_variance_y_max.text)
            setting.angle_min = float(self.angle_min.text)
            setting.angle_max = float(self.angle_max.text)

        except ValueError:
            pass
        except TypeError:
            pass

    def set_setting(self, setting: PointSetting):
        if setting is None:
            # Copy the value to prevent overriding the previous selected point
            setting = PointSetting()
            self.fill_setting(setting)
        self.selected_setting = setting
        self.pos_variance_x_min.set_text(str(setting.pos_variance_x_min))
        self.pos_variance_x_max.set_text(str(setting.pos_variance_x_max))
        self.pos_variance_y_min.set_text(str(setting.pos_variance_y_min))
        self.pos_variance_y_max.set_text(str(setting.pos_variance_y_max))
        self.angle_min.set_text(str(setting.angle_min))
        self.angle_max.set_text(str(setting.angle_max))

    def on_change_data(self, event: Event) -> bool:
        print("fill data")
        self.fill_setting(self.selected_setting)
        return True
