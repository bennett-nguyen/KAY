import json

import pygame as pg
import pygame_gui

from src.core.utils import const 
from src.core.dataclasses import Theme
from src.cmd_ui import CommandBox, UIManager

class CMDLineInterface:
    def __init__(self):
        self.ui_manager = UIManager()
        self.command_box = CommandBox(self.ui_manager.manager)
        self._focused_textbox = False

    def process_event(self, event: pg.event.Event):
        self.ui_manager.process_event(event)

        if self._focused_textbox:
            self.command_box.command_box.focus()
            self._focused_textbox = False

        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_SLASH:
                self._focused_textbox = True

            elif event.key == pg.K_ESCAPE:
                self.command_box.command_box.unfocus()

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
            and event.ui_object_id == const.COMMAND_BOX_OBJECT_ID and event.text:
                self.command_box.command_box.clear()
                self.command_box.command_box.focus()

    def update(self, dt_time: float):
        self.ui_manager.update(dt_time)
    
    def draw_ui(self, screen: pg.Surface):
        self.ui_manager.draw(screen)

    def set_theme(self, theme: Theme):
        if theme.CMD_UI_FILE_PATH is None:
            json_obj = json.loads(const.DEFAULT_CMD_THEME)
        else:
            with open(theme.CMD_UI_FILE_PATH, "r") as ui_theme_file:
                json_obj = json.load(ui_theme_file)

        with open(const.CMD_THEME_FILE, "w") as cmd_ui_file:
            json.dump(json_obj, indent=4, fp=cmd_ui_file)
    
    def on_window_size_changed(self):
        self.ui_manager.on_window_size_changed()
        self.command_box.on_window_size_changed()
