import pygame as pg

import src.preload.system.constants as const
from src.MVC.model_helpers.theme_manager import ThemeManager
from src.MVC.model_helpers.tree_manager import TreeManager
from src.preload.system.app_enum import Visibility

class Model:
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.tree_manager = TreeManager([1, 3, -2, 8, -7])

        self.visibility_dict: dict[Visibility, bool] = {
            Visibility.ARRAY_FIELD: True,
            Visibility.NODE_DATA_FIELD: True,
            Visibility.NODE_INFO_FIELD: True,
        }

        self.theme_manager.load_themes()
        self.theme_manager.set_theme("Dark (built-in)")

        self.previous_mouse_pos = (0, 0)
        self.current_mouse_pos = (0, 0)

        self.zoom_level: float = 1.0

        self.tree_manager.generate_node_position(self.zoom_level)

        # center the root node by the width of the screen
        delta_x = const.HALF_WIDTH - self.tree_manager.segment_tree.root.x
        self.tree_manager.move_tree_by_delta_pos(delta_x, 0)
        self.tree_manager.compute_transformed_coordinates(self.zoom_level)

    def zoom(self, y: int):
        if (y > 0):
            self.zoom_level = min(self.zoom_level+0.1, const.MAX_ZOOM_LEVEL)
        else:
            self.zoom_level = max(self.zoom_level-0.1, const.MIN_ZOOM_LEVEL)

        self.tree_manager.compute_transformed_coordinates(self.zoom_level)

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

        self.tree_manager.move_tree_by_delta_pos(delta_x, delta_y)
        self.previous_mouse_pos = self.current_mouse_pos
        self.tree_manager.compute_transformed_coordinates(self.zoom_level)