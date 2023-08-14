import pygame as pg
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Theme:
    NAME: str

    # Background
    BACKGROUND_CLR: pg.Color

    # Node
    NODE_FILLINGS_CLR: pg.Color
    NODE_OUTLINE_CLR: pg.Color
    NODE_DISPLAY_DATA_CLR: pg.Color

    NODE_OUTLINE_HIGHLIGHT_CLR: pg.Color
    NODE_DISPLAY_DATA_HIGHLIGHT_CLR: pg.Color

    # Line
    LINE_CLR: pg.Color

    # App UI
    APP_UI_PATH: str
