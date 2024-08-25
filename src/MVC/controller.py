from typing import List, Optional

import pygame as pg

from src.MVC.view import View
from src.MVC.model import Model
from src.preload.tree.node import Node
from src.preload.tree.segment_tree import SegmentTree


class Controller:
    def __init__(self, segment_tree: SegmentTree):
        self.model = Model(segment_tree)
        self.view = View()

    def process(self, events: List[pg.event.Event], delta_time: float):
        self.model.update_ui(delta_time)
        self.model.handle_input(events)

    def update_view(self):
        self.view.request_theme(self.model.current_theme)
        self.view.request_visibility(self.model.visibility_dict)
        self.model.app_ui.message_box_ui.request_theme(self.model.current_theme)

        if self.model.segment_tree.array_length != 0:
            hovered_node: Optional[Node] = self.model.find_hovered_node(self.model.segment_tree.root)
            self.view.draw_tree(self.model.segment_tree.root, hovered_node)
            self.view.view_array(self.model.segment_tree.array, hovered_node)
            self.view.view_hovered_node_info(hovered_node)

        self.view.view_app_ui(self.model.app_ui)
