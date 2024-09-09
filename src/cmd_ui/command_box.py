import pygame as pg
import pygame_gui
import pygame_gui.core.interfaces

from src.core import pygame_window
from src.core.utils import const

class CommandBox:
    """
    Represents a command input box for user interactions within the
    application. This class initializes the command box UI element and manages
    its dimensions based on window size changes.
    """

    def __init__(self, manager: pygame_gui.core.interfaces.IUIManagerInterface):
        relative_rect = pg.Rect(0, 0, pygame_window.window_width - const.COMMAND_BOX_ANCHOR_OFFSET * 2, 50)
        relative_rect.bottomleft = (const.COMMAND_BOX_ANCHOR_OFFSET, -const.COMMAND_BOX_ANCHOR_OFFSET)

        self.UI = pygame_gui.elements.UITextEntryLine(
            relative_rect=relative_rect,
            manager=manager,
            anchors={
                "left": "left",
                "bottom": "bottom",
            },
            placeholder_text="Press '/' to start typing commands!",
            object_id=const.COMMAND_BOX_OBJECT_ID
        )

        self.UI.show()

    def on_window_size_changed(self):
        """
        Updates the dimensions of the command box when the window size changes. 
        """
    
        self.UI.set_dimensions((pygame_window.window_width - const.COMMAND_BOX_ANCHOR_OFFSET * 2, const.COMMAND_BOX_HEIGHT))
