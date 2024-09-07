from collections import deque
from typing import Optional

import pygame as pg

import src.preload.system.constants as const
from src.preload.tree.segment_tree import Node
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

        self.tree_manager.generate_node_position()

        # center the root node by the width of the screen
        delta_x = const.HALF_WIDTH - self.tree_manager.segment_tree.root.x
        self.tree_manager.move_tree_by_delta_pos(delta_x, 0)

    def find_hovered_node(self) -> Optional[Node]:
        mouse_pos = pg.mouse.get_pos()
        hit_box = pg.Rect((0, 0), (const.NODE_CIRCLE_RADIUS+25, const.NODE_CIRCLE_RADIUS+25))

        queue: deque[Node] = deque([self.tree_manager.segment_tree.root])

        while queue:
            node = queue.popleft()
            hit_box.center = node.coordinates

            if hit_box.collidepoint(mouse_pos):
                return node

            if node.is_leaf():
                continue;

            for child in node.children:
                queue.append(child)

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
