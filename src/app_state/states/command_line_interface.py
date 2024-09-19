import json, re, os
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
        self.idx = -1

        if os.path.isfile("history.txt"):
            return

        with open("history.txt", "w") as f:
            pass

    def process_event(self, event: pg.event.Event) -> Optional[str]:
        """Processes a user event for the command line interface.

        This function handles keyboard events and updates the user
        interface accordingly. It focuses or unfocuses the command
        box based on user input and returns any processed text from
        the command box.

        Args:
            event (pg.event.Event): The event to process.

        Returns:
            Optional[str]: The processed command text if available, otherwise None.
        """

        returned_text: Optional[str] = None

        self.ui_manager.process_event(event)

        if self._focused_textbox:
            self.command_box.UI.focus()
            self._focused_textbox = False

        if not self.command_box.UI.is_focused:
            self.idx = -1

        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_SLASH:
                self._focused_textbox = True

            elif event.key == pg.K_ESCAPE:
                self.command_box.UI.unfocus()
            
            elif event.key == pg.K_UP and self.command_box.UI.is_focused:
                self.query_history()

        elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED \
            and event.ui_object_id == const.COMMAND_BOX_OBJECT_ID and event.text:
                returned_text = re.sub(" +", " ", event.text.strip())
                self.command_box.UI.clear()
                self.command_box.UI.focus()
                self.write_to_history(event.text)
                self.idx = -1

        return returned_text

    def is_history_empty(self):
        return os.stat('history.txt').st_size == 0

    def history_size(self):
        with open("history.txt") as f:
            return sum(1 for _ in f)

    def clear_history(self):
        if self.history_size() >= const.HISTORY_SIZE_LIMIT:
            with open('history.txt', 'w'):
                pass

    def write_to_history(self, text):
        self.clear_history()

        with open("history.txt", "a+") as f:
            if self.is_history_empty():
                f.write(text)
                return

            f.write('\n')
            f.write(text)

    def read_history(self) -> list[str]:
        with open("history.txt") as f:
            return list(filter(lambda entry: entry.strip(), f.read().splitlines()))

    def query_history(self):
        history = self.read_history()

        if self.idx <= 0:
            self.idx = len(history) - 1
        else:
            self.idx -= 1

        self.command_box.UI.set_text(history[self.idx])
        self._focused_textbox = True

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
