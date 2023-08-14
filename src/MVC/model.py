import os, json
import pygame as pg
import pygame_gui as pg_gui
import src.preload.system.constants as const
import src.preload.algorithm.reingold_tilford as RT
from src.preload.business_objects.theme import Theme
from src.preload.business_objects.app_ui import AppUI
from src.preload.system.app_type import VisibilityField
from src.preload.business_objects.segment_tree import SegmentTree

from typing import List, Dict, Any
from src.preload.system.app_type import ThemeField, ValidJSONColorFormats


class Model:
    def __init__(self, segment_tree: SegmentTree):
        self.segment_tree = segment_tree
        self.app_ui = AppUI()

        self.visibility_dict: Dict[VisibilityField, bool] = {
            const.VIEW_ARRAY_FIELD: True,
            const.VIEW_NODE_DATA_FIELD: True,
            const.VIEW_NODE_INFO_FIELD: True,
            const.DISPLAY_THEME_SELECTION_FIELD: True
        }

        self.current_theme: Theme
        self.themes: Dict[str, Theme] = {}
        self.available_themes: List[str] = []

        self.load_themes()
        self.set_theme("Midnight (Built-in)")

        self.app_ui.init_theme_selection_ui(self.available_themes, self.current_theme)
        self.app_ui.init_visibility_ui(self.visibility_dict)

        self.previous_mouse_pos = (0, 0)
        self.current_mouse_pos = (0, 0)

        RT.calculate_node_position(self.segment_tree.root)

        # center the root node by the width of the screen
        delta_x = const.HALF_WIDTH - self.segment_tree.root.x
        RT.move_node_by_delta_pos(self.segment_tree.root, delta_x, 0)

    def handle_input(self, events: List[pg.event.Event]):
        visibility_ui = self.app_ui.visibility_ui
        self.change_visibility_dict()

        for event in events:
            if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.ui_object_id == const.THEME_DROP_DOWN_OBJ_ID:
                    self.set_theme(event.text)
                    self.app_ui.set_theme(self.current_theme)

            if event.type == pg.KEYDOWN and event.key == pg.K_q:
                if visibility_ui.container.visible:
                    visibility_ui.container.hide()
                else:
                    visibility_ui.container.show()

            self.app_ui.gui_manager.process_events(event)

        if not visibility_ui.container.visible:
            self.pan()

    def update_ui(self, delta_time: float):
        self.app_ui.gui_manager.update(delta_time)

    def pan(self):
        mouse_pressed = pg.mouse.get_pressed()

        if not mouse_pressed[0]:
            self.previous_mouse_pos = (0, 0)
            return

        self.current_mouse_pos = pg.mouse.get_pos()

        if self.previous_mouse_pos == (0, 0):
            self.previous_mouse_pos = self.current_mouse_pos

        delta_x = self.current_mouse_pos[0] - self.previous_mouse_pos[0]
        delta_y = self.current_mouse_pos[1] - self.previous_mouse_pos[1]

        RT.move_node_by_delta_pos(self.segment_tree.root, delta_x, delta_y)
        self.previous_mouse_pos = self.current_mouse_pos

    def change_visibility_dict(self):
        chosen_field: List[str] = self.app_ui.visibility_ui.UI.get_multi_selection()

        for field, _ in self.visibility_dict.items():
            self.visibility_dict[field] = field in chosen_field

    def create_theme(self, json_obj: Dict[str, Any], app_ui_path) -> Theme:
        name: str = json_obj["Name"]
        palette_obj: Dict[ThemeField, ValidJSONColorFormats] = json_obj["Palette"]

        return Theme(
            NAME=name,
            APP_UI_PATH=app_ui_path,
            LINE_CLR=pg.Color(palette_obj["line"]),
            BACKGROUND_CLR=pg.Color(palette_obj["background"]),
            NODE_OUTLINE_CLR=pg.Color(palette_obj["node_outline"]),
            NODE_FILLINGS_CLR=pg.Color(palette_obj["node_fillings"]),
            NODE_DISPLAY_DATA_CLR=pg.Color(palette_obj["node_display_data"]),
            NODE_OUTLINE_HIGHLIGHT_CLR=pg.Color(palette_obj["node_outline_highlight"]),
            NODE_DISPLAY_DATA_HIGHLIGHT_CLR=pg.Color(palette_obj["node_display_data_highlight"]),
        )

    def load_themes(self):
        for entry in os.listdir("./theme"):
            if not entry.endswith(const.THEME_IDENTIFIER_SUFFIX):
                continue

            suffix_start_index = entry.find(const.THEME_IDENTIFIER_SUFFIX)
            file_name = entry[:suffix_start_index]
            ui_path = const.DEFAULT_UI_FILE

            with open(f"./theme/{entry}/{file_name}.json", "r") as f:
                json_obj = json.load(f)

                if not json_obj["use_default_app_ui"]:
                    ui_path = f"./theme/{entry}/{const.CUSTOM_UI_FILE}"

                self.themes[json_obj["Name"]] = self.create_theme(json_obj, ui_path)
                self.available_themes.append(json_obj["Name"])

    def set_theme(self, name: str):
        try:
            self.current_theme = self.themes[name]
        except KeyError:
            print(f"Error: Theme <{name}> not found.")
            pg.quit()
            exit(1)
