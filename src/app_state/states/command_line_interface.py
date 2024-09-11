import json
from typing import Optional

import pygame as pg
import pygame_gui

from src.utils import const 
from src.dataclass import Theme
from src.cmd_ui import CommandBox, UIManager

class CMDLineInterface:
    """
    Manages the command line interface for user input within the application. 
    This class handles event processing, UI updates, and theme management, 
    acting as a front-end for command inputs.
    """

    def __init__(self):
        self.ui_manager = UIManager()
        self.command_box = CommandBox(self.ui_manager.manager)
        self._focused_textbox = False

    def process_event(self, event: pg.event.Event) -> Optional[str]:
        """
        Processes input events for the command line interface. 
        This method handles keyboard events to manage the focus state of the command box 
        and processes text entry completion, allowing for user interaction with the interface.

        Args:
            event (pg.event.Event): The event to be processed, which may include keyboard 
            inputs and UI interactions.
        """

        returned_text = None

        self.ui_manager.process_event(event)

        if self._focused_textbox:
            self.command_box.UI.focus()
            self._focused_textbox = False

        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_SLASH:
                self._focused_textbox = True

            elif event.key == pg.K_ESCAPE:
                self.command_box.UI.unfocus()

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
            and event.ui_object_id == const.COMMAND_BOX_OBJECT_ID and event.text:
                returned_text = event.text
                self.command_box.UI.clear()
                self.command_box.UI.focus()
        
        return returned_text

    def update(self, dt_time: float):
        """
        Updates the user interface manager with the elapsed time since the last frame. 
        This method ensures that all UI elements are refreshed and remain responsive to user interactions.

        Args:
            dt_time (float): The time in seconds since the last update call.
        """

        self.ui_manager.update(dt_time)
    
    def draw_ui(self, screen: pg.Surface):
        """
        Draws the user interface elements onto the main application screen. 
        This method utilizes the UI manager to render all of its visible components.
        """

        self.ui_manager.draw(screen)

    def set_theme(self, theme: Theme):
        """
        Sets the theme for the command line interface based on the provided theme object. 
        This method loads the theme configuration from a specified file or defaults to a 
        predefined theme if no file path is provided, and then saves the theme settings.
        The UI manager will read the theme settings and change the theme of the command
        line interface.
        """

        if theme.CMD_UI_FILE_PATH is None:
            json_obj = json.loads(const.DEFAULT_CMD_THEME)
        else:
            with open(theme.CMD_UI_FILE_PATH, "r") as ui_theme_file:
                json_obj = json.load(ui_theme_file)

        with open(const.CMD_THEME_FILE, "w") as cmd_ui_file:
            json.dump(json_obj, indent=4, fp=cmd_ui_file)
    
    def on_window_size_changed(self):
        """
        Adjusts the user interface elements when the window size changes. 
        This method ensures that both the UI manager and the command box are updated 
        to reflect the new dimensions of the window.
        """

        self.ui_manager.on_window_size_changed()
        self.command_box.on_window_size_changed()
