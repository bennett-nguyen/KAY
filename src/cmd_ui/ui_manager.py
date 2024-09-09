import pygame as pg
import pygame_gui

from src.core.utils import const
from src.core import pygame_window

class UIManager:
    """
    Manages the user interface elements of the application using pygame_gui. 
    This class handles the initialization, updating, event processing, and drawing 
    of UI components on the screen.
    """

    def __init__(self):
        self.manager = pygame_gui.UIManager(pygame_window.size, const.CMD_THEME_FILE)

    def update(self, dt_time: float):
        """
        Updates the UI manager with the elapsed time since the last frame. 
        This method ensures that all UI elements are refreshed and responsive to changes.

        Args:
            dt_time (float): The time in seconds since the last update call.
        """

        self.manager.update(dt_time)

    def process_event(self, event: pg.event.Event):
        """
        Processes input events for the UI manager. 
        This method allows the user interface to respond to various user interactions, 
        such as mouse clicks and keyboard inputs.
        """

        self.manager.process_events(event)

    def draw(self, screen: pg.Surface):
        """
        Draws the UI elements onto the specified surface. 
        This method renders all visible components of the user interface.
        """

        self.manager.draw_ui(screen)

    def on_window_size_changed(self):
        """
        Adjusts the UI manager's resolution when the window size changes. 
        This method ensures that all UI elements are correctly scaled and positioned 
        according to the new dimensions of the window.
        """

        self.manager.set_window_resolution(pygame_window.size)