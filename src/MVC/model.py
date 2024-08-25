import os
import json
import webbrowser
from collections import deque
from typing import List, Dict, Any, Optional

import pygame as pg
import pygame_gui as pg_gui

import src.preload.system.constants as const
import src.preload.algorithm.reingold_tilford as RT
from src.preload.ui.theme import Theme
from src.preload.ui.app_ui import AppUI
from src.preload.command.command import CommandManager
from src.preload.tree.segment_tree import SegmentTree, Node
from src.preload.system.app_type import VisibilityField, ThemeField, ValidJSONColorFormats, HexStrColorFormat


class Model:
    def __init__(self, segment_tree: SegmentTree):
        self.segment_tree = segment_tree
        # self.commands = commands
        self.app_ui = AppUI()
        self.command_manager = CommandManager()

        self.visibility_dict: Dict[VisibilityField, bool] = {
            const.VIEW_ARRAY_FIELD: True,
            const.VIEW_NODE_DATA_FIELD: True,
            const.VIEW_NODE_INFO_FIELD: True,
            const.DISPLAY_BOTTOM_BAR: True
        }

        self.current_theme: Theme
        self.themes: Dict[str, Theme] = {}
        self.available_themes: List[str] = []

        self.load_themes()
        self.set_theme("Midnight (Built-in)")

        self.app_ui.init_theme_selection_ui(self.available_themes, self.current_theme)
        self.app_ui.init_visibility_ui(self.visibility_dict)
        self.app_ui.init_command_text_box_and_message_text_box(self.current_theme)

        self.command_manager.init_commands(self.app_ui.message_box_ui)

        self.previous_mouse_pos = (0, 0)
        self.current_mouse_pos = (0, 0)

        RT.calculate_node_position(self.segment_tree.root)

        # center the root node by the width of the screen
        delta_x = const.HALF_WIDTH - self.segment_tree.root.x
        RT.move_node_by_delta_pos(self.segment_tree.root, delta_x, 0)

        self._focus_textbox = False

    def handle_input(self, events: List[pg.event.Event]):
        visibility_ui = self.app_ui.visibility_ui
        cmd_textbox = self.app_ui.cmd_textbox_ui

        if self._focus_textbox:
            cmd_textbox.UI.focus()
            self._focus_textbox = False

        self.change_visibility_dict()

        for event in events:
            if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED \
                and event.ui_object_id == const.THEME_DROP_DOWN_OBJ_ID:
                self.set_theme(event.text)
                self.app_ui.set_theme(self.current_theme)

            if event.type == pg.KEYDOWN:
                self._keydown_event_processor(event)

            if event.type == pg_gui.UI_TEXT_ENTRY_FINISHED \
                and event.ui_object_id == const.COMMAND_TEXTBOX_OBJ_ID and event.text:
                    self.parse_command(event.text)
                    cmd_textbox.UI.clear()
                    cmd_textbox.UI.focus()
            
            if event.type == pg_gui.UI_TEXT_BOX_LINK_CLICKED \
                and event.ui_object_id == const.MESSAGE_TEXTBOX_OBJ_ID:
                    webbrowser.open(event.link_target, new=2)

            self.app_ui.gui_manager.process_events(event)

        if not any([
            visibility_ui.container.visible,
            cmd_textbox.UI.is_focused
        ]):
            self.pan()
    
    def find_hovered_node(self, root_node: Node) -> Optional[Node]:
        mouse_pos = pg.mouse.get_pos()
        hit_box = pg.Rect((0, 0), (const.NODE_CIRCLE_RADIUS+25, const.NODE_CIRCLE_RADIUS+25))

        queue: deque[Node] = deque([root_node])

        while queue:
            node = queue.popleft()
            hit_box.center = node.coordinates

            if hit_box.collidepoint(mouse_pos):
                return node

            if node.is_leaf():
                continue;

            for child in node.children:
                queue.append(child)

    
    def _keydown_event_processor(self, event: pg.event.Event):
        cmd_textbox = self.app_ui.cmd_textbox_ui
        message_box = self.app_ui.message_box_ui

        if event.key == pg.K_q and not cmd_textbox.UI.is_focused:
            visibility_ui = self.app_ui.visibility_ui
            if visibility_ui.container.visible:
                visibility_ui.container.hide()
            else:
                visibility_ui.container.show()

        if event.key == pg.K_SLASH:
            self._focus_textbox = True

        if event.key == pg.K_ESCAPE:
            cmd_textbox.UI.unfocus()

        if event.key == pg.K_e and not cmd_textbox.UI.is_focused:
            if message_box.UI.visible:
                message_box.UI.hide()
            else:
                message_box.UI.show()

    def update_ui(self, delta_time: float):
        self.app_ui.gui_manager.update(delta_time)

    def parse_command(self, text: str):
        text = text.strip().split()
        cmd, args = text[0].lower(), text[1:]
        commands = self.command_manager.commands
        message_box_ui = self.app_ui.message_box_ui

        if cmd not in commands:
            message_box_ui.create_error("Model.parse_command()", f"command <i>{message_box_ui.generate_text(cmd, message_box_ui.current_theme.COMMAND_CLR, const.H3)}</i> was not found.")
            return

        match cmd:
            case "insert":
                commands["insert"].execute(*args, segment_tree=self.segment_tree)
            case "remove":
                commands["remove"].execute(*args, segment_tree=self.segment_tree)
            case "query":
                commands["query"].execute(*args, segment_tree=self.segment_tree)
            case "update":
                commands["update"].execute(*args, segment_tree=self.segment_tree)
            case "home":
                commands["home"].execute(*args, segment_tree=self.segment_tree)
            case "help":
                commands["help"].execute(*args, available_commands=commands)
            case "about":
                commands["about"].execute(*args)

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
        
        with open(app_ui_path, "r") as f:
            message_box_palette_obj: Dict[ThemeField, HexStrColorFormat] = json.load(f)["Message Box Content Palette"]

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

            NORMAL_TEXT_CLR=message_box_palette_obj["normal_text"],
            HORIZONTAL_LINE_CLR=message_box_palette_obj["horizontal_line"],
            ERROR_TEXT_CLR=message_box_palette_obj["error_text"],
            OUTPUT_TEXT_CLR=message_box_palette_obj["output_text"],
            COMMAND_CLR=message_box_palette_obj["command"],
            ARGUMENT_NAME_CLR=message_box_palette_obj["argument_name"],
            OPTIONAL_NOTATION_CLR=message_box_palette_obj["optional_notation"],
            COLON_CLR=message_box_palette_obj["colon"],
            TYPE_CLR=message_box_palette_obj["type"]
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
