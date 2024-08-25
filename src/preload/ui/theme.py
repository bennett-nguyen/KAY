import pygame as pg
from dataclasses import dataclass

from src.preload.system.app_type import HexStrColorFormat


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
    NORMAL_TEXT_CLR: HexStrColorFormat
    HORIZONTAL_LINE_CLR: HexStrColorFormat
    ERROR_TEXT_CLR: HexStrColorFormat
    OUTPUT_TEXT_CLR: HexStrColorFormat
    COMMAND_CLR: HexStrColorFormat
    OPTIONAL_NOTATION_CLR: HexStrColorFormat
    ARGUMENT_NAME_CLR: HexStrColorFormat
    COLON_CLR: HexStrColorFormat
    TYPE_CLR: HexStrColorFormat