from typing import Optional

import pygame as pg

from src.core import pygame_window
from src.core.tree_utils import Node
from src.mvc.view import View
from src.mvc.model import Model


class Controller:
    """
    Handles the interaction between the model and the view in the application. This class processes
    user input, updates the model state, and refreshes the view based on the current state of the model.
    """

    def __init__(self):
        self.model = Model()
        self.view = View()

    def process_input(self, events: list[pg.event.Event]):
        """
        Processes a list of input events to update the model's state based on user interactions. It specifically handles mouse wheel events for zooming and delegates other events to the command line interface.

        This function checks each event in the provided list, applying zoom functionality when the mouse wheel is scrolled and the command box is not focused. Additionally, it processes each event through the command line interface and initiates panning if the command box remains unfocused.

        Args:
            events (list[pg.event.Event]): A list of Pygame event objects to be processed.
        """
        cmdline_interface = self.model.cmdline_interface

        for event in events:
            if event.type == pg.MOUSEWHEEL and not cmdline_interface.command_box.command_box.is_focused:
                self.model.zoom(event.y)
            elif event.type == pg.VIDEORESIZE:
                self.model.on_window_size_changed()

            cmdline_interface.process_event(event)

        if not cmdline_interface.command_box.command_box.is_focused:
            self.model.pan()


    def update_view(self, dt_time: float):
        """
        Updates the view based on the elapsed time and the current state of the model. It refreshes the command line interface, theme, visibility, and draws the segment tree if available.

        This function processes the time delta to update the command line interface and requests the current theme and visibility settings from the model. If the segment tree contains nodes, it draws the tree, displays the array, and shows information about the hovered node, while also rendering the user interface.

        Args:
            dt_time (float): The time elapsed since the last update, used for animations and updates.
        """

        cmdline_interface = self.model.cmdline_interface
        tree_manager = self.model.tree_manager
        theme_manager = self.model.theme_manager

        cmdline_interface.update(dt_time)
        self.view.request_theme(theme_manager.current_theme)
        self.view.request_visibility(self.model.visibility_dict)

        pygame_window.fill_background(theme_manager.current_theme.BACKGROUND_CLR)

        if tree_manager.segment_tree.array_length != 0:
            hovered_node: Optional[Node] = self.view.draw_tree(tree_manager.segment_tree.root)
            self.view.view_array(tree_manager.segment_tree.array, hovered_node)
            self.view.view_hovered_node_info(hovered_node)

        cmdline_interface.draw_ui(pygame_window.screen)