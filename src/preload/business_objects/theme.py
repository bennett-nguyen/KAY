import pygame as pg
from typing import Dict, Any
from src.preload.system.app_type import ThemeField, ValidJSONColorFormats


class Theme:
    __slots__ = (
        "NAME",
        "APP_UI_PATH",
        "BACKGROUND_CLR",
        "NODE_FILLINGS_CLR",
        "NODE_OUTLINE_CLR",
        "NODE_DISPLAY_DATA_CLR",
        "LINE_CLR",
        "NODE_DISPLAY_DATA_HIGHLIGHT_CLR",
        "NODE_OUTLINE_HIGHLIGHT_CLR"
    )

    def __init__(self, json_obj: Dict[str, Any], app_ui_path: str):
        name: str = json_obj["Name"]
        palette_obj: Dict[ThemeField, ValidJSONColorFormats] = json_obj["Palette"]

        self.NAME: str = name

        # Background
        self.BACKGROUND_CLR: pg.Color = pg.Color(palette_obj["background"])

        # Node
        self.NODE_FILLINGS_CLR: pg.Color = pg.Color(palette_obj["node_fillings"])
        self.NODE_OUTLINE_CLR: pg.Color = pg.Color(palette_obj["node_outline"])
        self.NODE_DISPLAY_DATA_CLR: pg.Color = pg.Color(palette_obj["node_display_data"])

        self.NODE_OUTLINE_HIGHLIGHT_CLR: pg.Color = pg.Color(palette_obj["node_outline_highlight"])
        self.NODE_DISPLAY_DATA_HIGHLIGHT_CLR: pg.Color = pg.Color(palette_obj["node_display_data_highlight"])

        # Line
        self.LINE_CLR: pg.Color = pg.Color(palette_obj["line"])

        # App UI
        self.APP_UI_PATH: str = app_ui_path
