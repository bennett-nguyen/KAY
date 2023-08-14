import pygame as pg
from src.MVC.view import View
from src.MVC.model import Model
from src.preload.business_objects.node import Node
from src.preload.business_objects.segment_tree import SegmentTree

from typing import List, Tuple


class Controller:
    def __init__(self, segment_tree: SegmentTree):
        self.model = Model(segment_tree)
        self.view = View()

    def process(self, events: List[pg.event.Event], delta_time: float):
        self.model.update_ui(delta_time)
        self.model.handle_input(events)

    def update_view(self):
        # hovered_node[0]: is the mouse hovering on the queried node
        # hovered_node[1]: return the queried node if mouse is hovering on that node
        hovered_node: Tuple[bool, Node] = self.view.mouse_hover_node(self.model.segment_tree.root)

        self.view.request_theme(self.model.current_theme)
        self.view.request_visibility(self.model.visibility_dict)

        self.view.draw_tree(self.model.segment_tree.root, hovered_node)
        self.view.view_array(self.model.segment_tree.arr, hovered_node)
        self.view.view_hovered_node_info(hovered_node)
        self.view.view_app_ui(self.model.app_ui)
