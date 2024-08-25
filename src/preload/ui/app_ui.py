import json
import pygame as pg
from typing import List, Dict
from itertools import product

import pygame_gui as pg_gui

import src.preload.system.constants as const
from src.preload.ui.theme import Theme
from src.preload.system.app_type import VisibilityField, HexStrColorFormat


# Override the UIWindow so it hides itself when the close button is pressed
class Window(pg_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()


class ThemeSelectionUI:
    __slots__ = "manager", "UI", "_layout_rect"

    def __init__(self, manager, theme_list: List[str], default_theme: str):
        self.manager = manager
        self._layout_rect = pg.Rect(0, 0, const.THEME_DROP_DOWN_WIDTH, const.THEME_DROP_DOWN_HEIGHT)
        self._layout_rect.bottomright = (
            const.WIDTH-const.THEME_DROP_DOWN_OFFSET-10,
            const.HEIGHT-const.THEME_DROP_DOWN_OFFSET
        )
        
        self._layout_rect.right = const.WIDTH - const.COMMAND_TEXTBOX_MARGIN
        self._layout_rect.bottom = const.HEIGHT - const.COMMAND_TEXTBOX_MARGIN

        self.UI = pg_gui.elements.UIDropDownMenu(
            options_list=theme_list,
            starting_option=default_theme,
            manager=self.manager,
            relative_rect=self._layout_rect,
            object_id=const.THEME_DROP_DOWN_OBJ_ID,
            expansion_height_limit=205
        )


class VisibilityUI:
    __slots__ = "manager", "container", "UI", "_container_layout_rect", "_UI_layout_rect"

    def __init__(self, manager: pg_gui.UIManager, visibility_dict: Dict[VisibilityField, bool]):
        self.manager = manager
        self._container_layout_rect = pg.Rect((0, 0), (const.VISIBILITY_WINDOW_WIDTH, const.VISIBILITY_WINDOW_HEIGHT))
        self._container_layout_rect.bottomleft = (50, const.HEIGHT-50)

        self._UI_layout_rect = pg.Rect((0, 0), (const.VISIBILITY_DROP_DOWN_WIDTH, const.VISIBILITY_DROP_DOWN_HEIGHT))
        self.container = Window(
            rect=self._container_layout_rect,
            manager=self.manager,
            window_display_title="Visibility Panel",
            object_id=const.VISIBILITY_WINDOW_OBJ_ID,
            visible=0
        )

        self.UI = pg_gui.elements.UISelectionList(
            relative_rect=self._UI_layout_rect,
            item_list=list(visibility_dict.keys()),
            manager=self.manager,
            container=self.container,
            allow_multi_select=True,
            object_id=const.VISIBILITY_DROP_DOWN_OBJ_ID,
            default_selection=[field for field, selected in visibility_dict.items() if selected]
        )

class MessageTextBoxUI:
    __slots__ = "manager", "_layout_rect", "UI", "current_theme", "should_display"
    def __init__(self, manager: pg_gui.UIManager, theme: Theme):
        self.manager = manager
        self.current_theme = theme
        self.should_display: bool = False

        self._layout_rect = pg.Rect((0, 0), (const.COMMAND_TEXTBOX_WIDTH, 200))
        self._layout_rect.left = const.COMMAND_TEXTBOX_MARGIN
        self._layout_rect.bottom = const.HEIGHT - const.COMMAND_TEXTBOX_HEIGHT - const.COMMAND_TEXTBOX_MARGIN*2
        
        self.UI = pg_gui.elements.UITextBox(
            html_text="",
            relative_rect=self._layout_rect,
            manager=self.manager,
            object_id=const.MESSAGE_TEXTBOX_OBJ_ID,
            visible=0
        )

        self.create_about()

    def request_theme(self, theme: Theme):
        self.current_theme = theme

    def create_error(self, command_name: str, html_content: str):
        self.should_display = True
        self.UI.show()
        self.UI.clear()

        current_theme = self.current_theme
        self.UI.set_text(f"<b>{self.generate_text('ERROR', current_theme.ERROR_TEXT_CLR, const.H1)}</b><br>")
        self.UI.append_html_text(f"{self.generate_text('raised from: ', current_theme.NORMAL_TEXT_CLR, const.H3)}<i>{self.generate_text(command_name, current_theme.COMMAND_CLR, const.H3)}</i><br>")
        self.UI.append_html_text(f"{self.generate_horizontal_rule()}<br><br>")
        self.UI.append_html_text(self.generate_text(text=f'message: {html_content}', color=current_theme.NORMAL_TEXT_CLR, pixel_size=const.H3))

    def create_output(self, command_name: str, html_content: str):
        self.should_display = True
        self.UI.show()
        self.UI.clear()
        
        current_theme = self.current_theme
        self.UI.set_text(f"<b>{self.generate_text('OUTPUT', current_theme.OUTPUT_TEXT_CLR, const.H1)}</b><br>")
        self.UI.append_html_text(f"{self.generate_text('returned from: ', current_theme.NORMAL_TEXT_CLR, const.H3)}<i>{self.generate_text(command_name, current_theme.COMMAND_CLR, const.H3)}</i><br>")
        self.UI.append_html_text(f"{self.generate_horizontal_rule()}<br><br>")
        self.UI.append_html_text(self.generate_text(html_content, color=current_theme.NORMAL_TEXT_CLR, pixel_size=const.H3))

    def create_about(self):
        current_theme = self.current_theme

        self.UI.set_text(f"<b>{self.generate_text('KAY - Segment Tree Visualizer', current_theme.NORMAL_TEXT_CLR, const.H1)}</b><br>")
        self.UI.append_html_text(f"{self.generate_text('Copyright © 2023 Nguyen Vinh Phu', current_theme.NORMAL_TEXT_CLR, const.H3)}<br>")
        self.UI.append_html_text(f"{self.generate_text(f'Version: v{const.VERSION}', current_theme.NORMAL_TEXT_CLR, const.H3)}<br><br>")
        self.UI.append_html_text(f"&bullet; <a href='{const.GITHUB_LINK}'>Github</a><br>&bullet; <a href='{const.LICENSE_LINK}'>License</a>")

    def generate_text(self, text: str, color: HexStrColorFormat, pixel_size: int, face: str = "CascadiaCode") -> str:
        return f"<font face='{face}' color='{color}' pixel_size='{pixel_size}'>{text}</font>"

    def generate_horizontal_rule(self) -> str:
        current_theme = self.current_theme
        return self.generate_text("&#8213;"*245, color=current_theme.HORIZONTAL_LINE_CLR, pixel_size=7)

class CommandTextBoxUI:
    __slots__ = "manager", "_layout_rect", "UI"
    def __init__(self, manager: pg_gui.UIManager):
        self.manager = manager
        self._layout_rect = pg.Rect((0, 0), (const.COMMAND_TEXTBOX_WIDTH, const.COMMAND_TEXTBOX_HEIGHT))
        self._layout_rect.left = const.COMMAND_TEXTBOX_MARGIN
        self._layout_rect.bottom = const.HEIGHT - const.COMMAND_TEXTBOX_MARGIN

        self.UI = pg_gui.elements.UITextEntryLine(
            relative_rect=self._layout_rect,
            manager=self.manager,
            placeholder_text="Press '/' to enter a command.",
            object_id=const.COMMAND_TEXTBOX_OBJ_ID
        )


class AppUI:
    __slots__ = "gui_manager", "theme_selection_ui", "visibility_ui", "cmd_textbox_ui", "message_box_ui"

    def __init__(self):
        self.gui_manager = pg_gui.UIManager(const.RESOLUTION, theme_path=const.ACTIVE_UI_FILE)
        self.gui_manager.add_font_paths(
            font_name="CascadiaCode",
            regular_path="./fonts/CascadiaCode/CascadiaCode-Regular.ttf",
            bold_path="./fonts/CascadiaCode/CascadiaCode-Bold.ttf",
            italic_path="./fonts/CascadiaCode/CascadiaCode-Italic.ttf",
            bold_italic_path="./fonts/CascadiaCode/CascadiaCode-BoldItalic.ttf"
        )

        font_to_be_preload = ("CascadiaCode",)
        font_size = (const.H1, const.H2, const.H3, const.H4, const.H5, const.H6)
        font_style = ('regular', 'italic', 'bold', 'bold_italic')

        font_list = [
            {'name': font, 'point_size': size, 'style': style}
            for font, size, style in product(
                font_to_be_preload, font_size, font_style
            )
        ]
        
        # for the horizontal rule
        font_list.append({'name': "CascadiaCode", 'point_size': 7, 'style': 'regular'})
        self.gui_manager.preload_fonts(font_list)

    def init_theme_selection_ui(self, theme_list: List[str], current_theme: Theme):
        self.theme_selection_ui = ThemeSelectionUI(self.gui_manager, theme_list, current_theme.NAME)
        self.set_theme(current_theme)

    def init_visibility_ui(self, visibility_dict: Dict[VisibilityField, bool]):
        self.visibility_ui = VisibilityUI(self.gui_manager, visibility_dict)

    def init_command_text_box_and_message_text_box(self, theme: Theme):
        self.cmd_textbox_ui = CommandTextBoxUI(self.gui_manager)
        self.message_box_ui = MessageTextBoxUI(self.gui_manager, theme)

    def set_theme(self, theme: Theme):
        app_ui_path = theme.APP_UI_PATH

        with open(app_ui_path, 'r') as theme_file:
            chosen_theme = json.load(theme_file)

        with open(const.ACTIVE_UI_FILE, "w") as active_file:
            json.dump(chosen_theme, active_file, indent=4)
