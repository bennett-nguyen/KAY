import pygame as pg
import pygame_gui
import pygame_gui.core.interfaces

from src.core import pygame_window
from src.core.utils import const

class CommandBox:
    def __init__(self, manager: pygame_gui.core.interfaces.IUIManagerInterface):
        self.relative_rect = pg.Rect(0, 0, pygame_window.window_width - const.COMMAND_BOX_ANCHOR_OFFSET * 2, 50)
        self.relative_rect.bottomleft = (const.COMMAND_BOX_ANCHOR_OFFSET, -const.COMMAND_BOX_ANCHOR_OFFSET)

        self.command_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=self.relative_rect,
            manager=manager,
            anchors={
                "left": "left",
                "bottom": "bottom",
            },
            placeholder_text="Press '/' to start typing commands!",
            object_id=const.COMMAND_BOX_OBJECT_ID
        )

        self.command_box.show()

    def on_window_size_changed(self):
        self.command_box.set_dimensions((pygame_window.window_width - const.COMMAND_BOX_ANCHOR_OFFSET * 2, 50))
