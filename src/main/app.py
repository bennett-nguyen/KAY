from typing import Optional

import pygame as pg

from src.window import pygame_window
from src.utils import const
from src.segment_tree import Node

from src.app_state.app_state import AppState
from src.main.command_manager import CommandManager

class App:
    """Main application class that manages the overall functionality.

    This class initializes the application state, processes user input,
    updates the view, and handles window resizing and zooming. It serves
    as the central hub for managing interactions between various components
    of the application.
    """

    def __init__(self):
        self.previous_mouse_pos = (0, 0)
        self.current_mouse_pos = (0, 0)

        self.app_state = AppState()
        tree_manager = self.app_state.tree_manager
        theme_manager = self.app_state.theme_manager
        cmdline_interface = self.app_state.cmdline_interface

        tree_manager.generate_node_position()
        tree_manager.center_tree()
        theme_manager.load_themes()
        theme_manager.set_theme("Seria Dark")
        cmdline_interface.set_theme(theme_manager.current_theme)

        self.command_manager = CommandManager()

    def process_input(self, events: list[pg.event.Event]):
        """Processes user input events for the application.

        This method handles various types of input events, including mouse
        wheel scrolling for zooming, window resizing, and command input from the command
        line interface. It updates the application state based on user interactions
        and manages panning when the command box is not focused.

        Args:
            events (list[pg.event.Event]): A list of events to process.
        """

        cmdline_interface = self.app_state.cmdline_interface

        for event in events:
            if event.type == pg.MOUSEWHEEL and not cmdline_interface.command_box.UI.is_focused:
                self.zoom(event.y)

            if event.type == pg.VIDEORESIZE:
                self.on_window_size_changed()

            input_text = cmdline_interface.process_event(event)

            if input_text is not None:
                self.command_manager.parse_inputs(input_text, self.app_state)

        if not cmdline_interface.command_box.UI.is_focused:
            self.pan()

    def update_view(self, dt_time: float):
        """Updates the application view based on the elapsed time.

        This method refreshes the user interface by updating the command
        line interface, requesting the current theme for rendering, and
        drawing the segment tree along with its associated data. It also
        handles the display of any hovered node information and ensures
        the UI is drawn correctly on the screen.

        Args:
            dt_time (float): The elapsed time since the last update,
            used for animations and updates.
        """

        cmdline_interface = self.app_state.cmdline_interface
        tree_manager = self.app_state.tree_manager
        theme_manager = self.app_state.theme_manager
        rendering = self.app_state.rendering

        cmdline_interface.update(dt_time)
        rendering.request_theme(theme_manager.current_theme)

        pygame_window.fill_background(theme_manager.current_theme.BACKGROUND_CLR)

        if tree_manager.segment_tree.array_length != 0:
            hovered_node: Optional[Node] = rendering.draw_tree(tree_manager.segment_tree.root)
            rendering.view_array(tree_manager.segment_tree.array, hovered_node)
            rendering.view_hovered_node_info(hovered_node)

        cmdline_interface.draw_ui(pygame_window.screen)

    def on_window_size_changed(self):
        """Handles the event when the window size changes.

        This method updates the command line interface to adjust its
        layout and components according to the new window size. It
        ensures that the user interface remains functional and visually
        appealing after a resize event.
        """

        self.app_state.cmdline_interface.on_window_size_changed()

    def zoom(self, y: int):
        """Adjusts the zoom level of the tree based on mouse wheel input.

        This method increases or decreases the zoom level of the tree
        visualization depending on the direction of the mouse wheel scroll.
        It ensures that the zoom level remains within predefined minimum
        and maximum limits and updates the transformed coordinates accordingly.

        Args:
            y (int): The amount of scroll input from the mouse wheel, where
            positive values indicate zooming in and negative values indicate zooming out.
        """

        tree_manager = self.app_state.tree_manager

        if (y > 0):
            tree_manager.zoom_level = min(tree_manager.zoom_level+const.ZOOM_INTENSITY, const.MAX_ZOOM_LEVEL)
        else:
            tree_manager.zoom_level = max(tree_manager.zoom_level-const.ZOOM_INTENSITY, const.MIN_ZOOM_LEVEL)

        tree_manager.compute_transformed_coordinates()

    def pan(self):
        """Handles panning of the tree visualization based on mouse movement.

        This method allows the user to move the tree view by clicking and dragging
        the mouse. It calculates the change in mouse position and updates the tree's
        position accordingly, ensuring that the view remains responsive to user input.
        """

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
