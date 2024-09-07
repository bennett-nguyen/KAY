from typing import Any
import json, os

import pygame as pg

from src.preload.ui.theme import Theme
from src.preload.system.app_type import ThemeField, ValidJSONColorFormats
import src.preload.system.constants as const

class ThemeManager:
    def __init__(self):
        self.current_theme: Theme
        self.themes: dict[str, Theme] = {}
        self.available_themes: list[str] = []

    def load_themes(self):
        for entry in os.listdir("./theme"):
            if not entry.endswith(const.THEME_IDENTIFIER_SUFFIX):
                continue

            suffix_start_index = entry.find(const.THEME_IDENTIFIER_SUFFIX)
            file_name = entry[:suffix_start_index]

            with open(f"./theme/{entry}/{file_name}.json", "r") as f:
                json_obj = json.load(f)

                self.themes[json_obj["Name"]] = self.create_theme(json_obj)
                self.available_themes.append(json_obj["Name"])
    
    def create_theme(self, json_obj: dict[str, Any]) -> Theme:
        name: str = json_obj["Name"]
        palette_obj: dict[ThemeField, ValidJSONColorFormats] = json_obj["Palette"]

        return Theme(
            NAME=name,

            LINE_CLR=pg.Color(palette_obj["line"]),
            BACKGROUND_CLR=pg.Color(palette_obj["background"]),
            NODE_OUTLINE_CLR=pg.Color(palette_obj["node_outline"]),
            NODE_FILLINGS_CLR=pg.Color(palette_obj["node_fillings"]),
            NODE_DISPLAY_DATA_CLR=pg.Color(palette_obj["node_display_data"]),
            NODE_OUTLINE_HIGHLIGHT_CLR=pg.Color(palette_obj["node_outline_highlight"]),
            NODE_DISPLAY_DATA_HIGHLIGHT_CLR=pg.Color(palette_obj["node_display_data_highlight"]),
        )

    def set_theme(self, name: str):
        try:
            self.current_theme = self.themes[name]
        except KeyError:
            print(f"Error: Theme <{name}> not found.")
            pg.quit()
            exit(1)