import json, os
from typing import Any

import pygame as pg

from src.core.utils import const
from src.core.dataclasses import Theme
from src.core.utils import JSONThemeFieldsEnum

class ThemeManager:
    """
    Manages the themes used in the application, including loading themes from files
    and setting the current theme. This class provides functionality to create 
    themes from JSON data and handle theme-related operations.
    """

    def __init__(self):
        self.current_theme: Theme
        self.themes: dict[str, Theme] = {}
        self.available_themes: list[str] = []

    def load_themes(self):
        """
        Loads themes from the specified theme directory and stores them in the manager. It reads
        theme configuration files and creates theme objects based on the loaded data.

        This function iterates through the entries in the "theme/" directory, filtering for file
        that match the theme identifier suffix. For each valid entry, it reads the corresponding 
        JSON file, creates a theme object, and adds it to the themes collection while also keeping
        track of available themes.
        """

        for entry in os.listdir("theme/"):
            if not entry.endswith(const.THEME_IDENTIFIER_SUFFIX):
                continue

            suffix_start_index = entry.find(const.THEME_IDENTIFIER_SUFFIX)
            file_name = entry[:suffix_start_index]

            with open(f"theme/{entry}/{file_name}.json", "r") as f:
                json_obj = json.load(f)

                self.themes[json_obj[JSONThemeFieldsEnum.NAME.value]] = self.create_theme(json_obj, f"theme/{entry}/{file_name}")
                self.available_themes.append(json_obj[JSONThemeFieldsEnum.NAME.value])
    
    def create_theme(self, json_obj: dict[str, Any], file_name: str) -> Theme:
        """
        Creates a new theme based on the provided JSON object. This function 
        extracts the theme name and color palette from the JSON object and 
        constructs a Theme instance with the specified colors.

        Args:
            json_obj (dict[str, Any]): A dictionary containing the theme name and color palette.

        Returns:
            Theme: An instance of the Theme class initialized with the specified colors.

        Raises:
            KeyError: If the required keys are not present in the JSON object.
        """

        palette_obj = json_obj[JSONThemeFieldsEnum.PALETTE.value]

        cmd_ui_file_path = None

        if not json_obj[JSONThemeFieldsEnum.USE_DEFAULT_CMD_UI.value]:
            cmd_ui_file_path = f"{file_name}-cmd.json"

        return Theme(
            CMD_UI_FILE_PATH=cmd_ui_file_path,
            NAME=json_obj[JSONThemeFieldsEnum.NAME.value],

            LINE_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.LINE.value]),
            BACKGROUND_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.BACKGROUND.value]),
            NODE_OUTLINE_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.NODE_OUTLINE.value]),
            NODE_FILLINGS_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.NODE_FILLINGS.value]),
            NODE_DISPLAY_DATA_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.NODE_DISPLAY_DATA.value]),
            NODE_OUTLINE_HIGHLIGHT_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.NODE_OUTLINE_HIGHLIGHT.value]),
            NODE_DISPLAY_DATA_HIGHLIGHT_CLR=pg.Color(palette_obj[JSONThemeFieldsEnum.NODE_DISPLAY_DATA_HIGHLIGHT.value]),
        )

    def set_theme(self, name: str):
        """
        Sets the current theme to the specified theme by name. If the theme does 
        not exist, an error message is printed, and the program is terminated.

        Args:
            name (str): The name of the theme to set as the current theme.

        Raises:
            KeyError: If the specified theme name does not exist in the themes dictionary.
        """

        try:
            self.current_theme = self.themes[name]
        except KeyError:
            print(f"Error: Theme <{name}> not found.")
            pg.quit()
            exit(1)