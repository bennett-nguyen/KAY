import pygame as pg
from dataclasses import dataclass

from src.preload.system.app_type import HexStrFormat


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


    # Message Box Content
    NORMAL_TEXT_CLR: HexStrFormat
    HORIZONTAL_LINE_CLR: HexStrFormat
    ERROR_TEXT_CLR: HexStrFormat
    OUTPUT_TEXT_CLR: HexStrFormat
    COMMAND_CLR: HexStrFormat
    OPTIONAL_NOTATION_CLR: HexStrFormat
    ARGUMENT_NAME_CLR: HexStrFormat
    COLON_CLR: HexStrFormat
    TYPE_CLR: HexStrFormat