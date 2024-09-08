import pygame as pg
import pygame_gui
import pygame_gui.core.interfaces

from src.core.utils import const

class CommandBox:
    def __init__(self, manager: pygame_gui.core.interfaces.IUIManagerInterface):
        self.relative_rect = pg.Rect(0, 0, const.WIDTH - 20 * 2, 50)
        self.relative_rect.bottomleft = (20, -20)
        self.command_box = pygame_gui.elements.UITextEntryLine(
            relative_rect=self.relative_rect,
            manager=manager,
            anchors={
                "left": "left",
                "bottom": "bottom"
            },
            placeholder_text="real",
            object_id="#command-box"
        )

        self.command_box.show()