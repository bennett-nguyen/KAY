import json
import pygame as pg
import pygame_gui as pg_gui
import src.preload.system.constants as const
from typing import List, Dict
from src.preload.business_objects.theme import Theme
from src.preload.system.app_type import VisibilityField


# Override the UIWindow so it hides itself when the close button is pressed
class Window(pg_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()


class ThemeSelectionUI:
    def __init__(self, manager, theme_list: List[str], default_theme: str):
        self.manager = manager
        self.layout_rect = pg.Rect(0, 0, const.THEME_DROP_DOWN_WIDTH, const.THEME_DROP_DOWN_HEIGHT)
        self.layout_rect.bottomright = (
            const.WIDTH-const.THEME_DROP_DOWN_OFFSET-10,
            const.HEIGHT-const.THEME_DROP_DOWN_OFFSET
        )

        self.UI = pg_gui.elements.UIDropDownMenu(
            options_list=theme_list,
            starting_option=default_theme,
            manager=self.manager,
            relative_rect=self.layout_rect,
            object_id=const.THEME_DROP_DOWN_OBJ_ID,
            expansion_height_limit=205
        )


class VisibilityUI:
    def __init__(self, manager: pg_gui.UIManager, visibility_dict: Dict[VisibilityField, bool]):
        self.manager = manager
        self.container_layout_rect = pg.Rect((0, 0), (const.VISIBILITY_WINDOW_WIDTH, const.VISIBILITY_WINDOW_HEIGHT))
        self.container_layout_rect.bottomleft = (50, const.HEIGHT-50)

        self.UI_layout_rect = pg.Rect((0, 0), (const.VISIBILITY_DROP_DOWN_WIDTH, const.VISIBILITY_DROP_DOWN_HEIGHT))
        self.container = Window(
            rect=self.container_layout_rect,
            manager=self.manager,
            window_display_title="Visibility Panel",
            object_id=const.VISIBILITY_WINDOW_OBJ_ID,
            visible=0
        )

        self.UI = pg_gui.elements.UISelectionList(
            relative_rect=self.UI_layout_rect,
            item_list=list(visibility_dict.keys()),
            manager=self.manager,
            container=self.container,
            allow_multi_select=True,
            object_id=const.VISIBILITY_DROP_DOWN_OBJ_ID,
            default_selection=[field for field, selected in visibility_dict.items() if selected]
        )


class AppUI:
    def __init__(self):
        self.GUI_MANAGER = pg_gui.UIManager(const.RESOLUTION, theme_path=const.ACTIVE_UI_FILE)

    def init_theme_selection_ui(self, theme_list: List[str], current_theme: Theme):
        self.theme_selection_ui = ThemeSelectionUI(self.GUI_MANAGER, theme_list, current_theme.NAME)
        self.set_theme(current_theme)

    def init_visibility_ui(self, visibility_dict: Dict[VisibilityField, bool]):
        self.visibility_ui = VisibilityUI(self.GUI_MANAGER, visibility_dict)

    def set_theme(self, theme: Theme):
        app_ui_path = theme.APP_UI_PATH

        with open(app_ui_path, 'r') as theme_file:
            chosen_theme = json.load(theme_file)

        with open(const.ACTIVE_UI_FILE, "w") as active_file:
            json.dump(chosen_theme, active_file, indent=4)
