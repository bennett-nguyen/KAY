import pygame as pg

from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Theme:
    """
    Represents a theme configuration for the user interface. 
    This class encapsulates various color settings used throughout the application, 
    allowing for consistent styling and easy theme management.
    """

    CMD_UI_FILE_PATH: Optional[str]

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
