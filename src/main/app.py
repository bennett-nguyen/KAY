from typing import Optional

import pygame as pg

from src.window import pygame_window
from src.utils import const
from src.segment_tree import Node

from src.app_state.app_state import AppState
from src.main.rendering import Rendering
from src.main.command_manager import CommandManager

class App:
    """
    Handles the interaction between the model and the view in the application. This class processes
    user input, updates the model state, and refreshes the view based on the current state of the model.
    """

    def __init__(self):
        self.previous_mouse_pos = (0, 0)
        self.current_mouse_pos = (0, 0)

        self.app_state = AppState()
        self._init_app_state()

        self.rendering = Rendering()
        self.command_manager = CommandManager()

    def process_input(self, events: list[pg.event.Event]):
        """
        Processes a list of input events to update the model's state based on user interactions. It specifically handles mouse wheel events for zooming and delegates other events to the command line interface.

        This function checks each event in the provided list, applying zoom functionality when the mouse wheel is scrolled and the command box is not focused. Additionally, it processes each event through the command line interface and initiates panning if the command box remains unfocused.

        Args:
            events (list[pg.event.Event]): A list of Pygame event objects to be processed.
        """

        cmdline_interface = self.app_state.cmdline_interface

        for event in events:
            if event.type == pg.MOUSEWHEEL and not cmdline_interface.command_box.UI.is_focused:
                self.zoom(event.y)

            if event.type == pg.VIDEORESIZE:
                self.on_window_size_changed()

            input_text = cmdline_interface.process_event(event)

            if input_text is not None:
                self.command_manager.read_inputs(input_text, self.app_state)

        if not cmdline_interface.command_box.UI.is_focused:
            self.pan()

    def update_view(self, dt_time: float):
        """
        Updates the view based on the elapsed time and the current state of the model. It refreshes the command line interface, theme, visibility, and draws the segment tree if available.

        This function processes the time delta to update the command line interface and requests the current theme and visibility settings from the model. If the segment tree contains nodes, it draws the tree, displays the array, and shows information about the hovered node, while also rendering the user interface.

        Args:
            dt_time (float): The time elapsed since the last update, used for animations and updates.
        """

        cmdline_interface = self.app_state.cmdline_interface
        tree_manager = self.app_state.tree_manager
        theme_manager = self.app_state.theme_manager

        cmdline_interface.update(dt_time)
        self.rendering.request_theme(theme_manager.current_theme)
        self.rendering.request_visibility(self.app_state.visibility_dict)

        pygame_window.fill_background(theme_manager.current_theme.BACKGROUND_CLR)

        if tree_manager.segment_tree.array_length != 0:
            hovered_node: Optional[Node] = self.rendering.draw_tree(tree_manager.segment_tree.root)
            self.rendering.view_array(tree_manager.segment_tree.array, hovered_node)
            self.rendering.view_hovered_node_info(hovered_node)

        cmdline_interface.draw_ui(pygame_window.screen)
    
    def on_window_size_changed(self):
        self.app_state.cmdline_interface.on_window_size_changed()

    def zoom(self, y: int):
        tree_manager = self.app_state.tree_manager

        if (y > 0):
            tree_manager.zoom_level = min(tree_manager.zoom_level+0.1, const.MAX_ZOOM_LEVEL)
        else:
            tree_manager.zoom_level = max(tree_manager.zoom_level-0.1, const.MIN_ZOOM_LEVEL)

        tree_manager.compute_transformed_coordinates()

    def pan(self):
        tree_manager = self.app_state.tree_manager
        mouse_pressed = pg.mouse.get_pressed()

        if not mouse_pressed[0]:
            self.previous_mouse_pos = (0, 0)
            return

        self.current_mouse_pos = pg.mouse.get_pos()

        if self.previous_mouse_pos == (0, 0):
            self.previous_mouse_pos = self.current_mouse_pos

        delta_x = self.current_mouse_pos[0] - self.previous_mouse_pos[0]
        delta_y = self.current_mouse_pos[1] - self.previous_mouse_pos[1]

        tree_manager.move_tree_by_delta_pos(delta_x, delta_y)
        self.previous_mouse_pos = self.current_mouse_pos
        tree_manager.compute_transformed_coordinates()

    def _init_app_state(self):
        cmdline_interface = self.app_state.cmdline_interface
        tree_manager = self.app_state.tree_manager
        theme_manager = self.app_state.theme_manager

        self.app_state.tree_manager.generate_node_position()
        self.app_state.theme_manager.load_themes()
        self.app_state.theme_manager.set_theme("Seria Dark")
        self.app_state.cmdline_interface.set_theme(theme_manager.current_theme)

        tree_manager.center_tree()