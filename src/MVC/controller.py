from typing import Optional

import pygame as pg

from src.MVC.view import View
from src.MVC.model import Model
from src.preload.tree.node import Node


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
    
    def process_input(self, events: list[pg.event.Event], dt_time: float):
        self.model.pan()

    def update_view(self):
        tree_manager = self.model.tree_manager
        theme_manager = self.model.theme_manager
        self.view.request_theme(theme_manager.current_theme)
        self.view.request_visibility(self.model.visibility_dict)

        if tree_manager.segment_tree.array_length != 0:
            hovered_node: Optional[Node] = self.view.draw_tree(tree_manager.segment_tree.root)
            self.view.view_array(tree_manager.segment_tree.array, hovered_node)
            self.view.view_hovered_node_info(hovered_node)
